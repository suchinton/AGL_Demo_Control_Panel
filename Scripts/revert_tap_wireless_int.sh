#!/bin/bash

BRIDGE=br0
NETWORK=10.10.10.0
NETMASK=255.255.255.0
GATEWAY=10.10.10.1
DHCPRANGE=10.10.10.100,10.10.10.254

# Delete the bridge interface
ip link delete dev $BRIDGE type bridge

# Disable IP forwarding
sysctl -w net.ipv4.ip_forward=0 > /dev/null 2>&1

# Flush existing iptables rules and set default policies to ACCEPT
iptables --flush
iptables -t nat -F
iptables -X
iptables -Z
iptables -P OUTPUT ACCEPT
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT

# Allow DHCP and DNS traffic on the network interface
iptables -A INPUT -i $BRIDGE -p tcp -m tcp --dport 67 -j ACCEPT
iptables -A INPUT -i $BRIDGE -p udp -m udp --dport 67 -j ACCEPT
iptables -A INPUT -i $BRIDGE -p tcp -m tcp --dport 53 -j ACCEPT
iptables -A INPUT -i $BRIDGE -p udp -m udp --dport 53 -j ACCEPT

# Allow forwarding of packets between the network and the bridge
iptables -A FORWARD -s $NETWORK/$NETMASK -i $BRIDGE -j ACCEPT
iptables -A FORWARD -d $NETWORK/$NETMASK -o $BRIDGE -m state --state RELATED,ESTABLISHED -j ACCEPT

# Delete the network address translation (NAT) rules
iptables -t nat -D POSTROUTING -s $NETWORK/$NETMASK -d $NETWORK/$NETMASK -j ACCEPT
iptables -t nat -D POSTROUTING -s $NETWORK/$NETMASK -j MASQUERADE

# Delete the dnsmasq process
pid_file="/var/run/qemu-dnsmasq-$BRIDGE.pid"
if [ -f "$pid_file" ]; then
    kill $(cat "$pid_file")
    rm "$pid_file"
fi

# Remove the wireless interface from the forwarding rules
iptables -D FORWARD -i $BRIDGE -o $WIRELESS -j ACCEPT
iptables -t nat -D POSTROUTING -o $WIRELESS -j MASQUERADE

# Allow known traffic from the wireless interface to return to the network interface
iptables -D FORWARD -i $WIRELESS -o $BRIDGE -m state --state RELATED,ESTABLISHED -j ACCEPT

echo "Reverted back to default configuration."

