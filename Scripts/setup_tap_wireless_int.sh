#!/bin/bash

# Find the wireless interface
WIRELESS=$(iwconfig 2>/dev/null | awk '/IEEE 802.11/ {print $1; exit}')

BRIDGE=br0
NETWORK=10.10.10.0
NETMASK=255.255.255.0
GATEWAY=10.10.10.1
DHCPRANGE=10.10.10.100,10.10.10.254

# Create the bridge interface
ip link add $BRIDGE type bridge
ip link set dev $BRIDGE up

# Assign an IP address to the bridge interface
ip addr add dev $BRIDGE $GATEWAY/$NETMASK

# Enable IP forwarding
sysctl -w net.ipv4.ip_forward=1 > /dev/null 2>&1

# Flush existing iptables rules and set default policies to ACCEPT
iptables --flush
iptables -t nat -F
iptables -X
iptables -Z
iptables -P OUTPUT ACCEPT
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT

# Allow DHCP and DNS traffic on the bridge interface
iptables -A INPUT -i $BRIDGE -p tcp -m tcp --dport 67 -j ACCEPT
iptables -A INPUT -i $BRIDGE -p udp -m udp --dport 67 -j ACCEPT
iptables -A INPUT -i $BRIDGE -p tcp -m tcp --dport 53 -j ACCEPT
iptables -A INPUT -i $BRIDGE -p udp -m udp --dport 53 -j ACCEPT

# Allow forwarding of packets between the bridge and the network
iptables -A FORWARD -i $BRIDGE -o $BRIDGE -j ACCEPT
iptables -A FORWARD -s $NETWORK/$NETMASK -i $BRIDGE -j ACCEPT
iptables -A FORWARD -d $NETWORK/$NETMASK -o $BRIDGE -m state --state RELATED,ESTABLISHED -j ACCEPT

# Accept packets from the bridge interface with source and destination within the network
# to prevent masquerading of bridged frames/packets
iptables -t nat -A POSTROUTING -s $NETWORK/$NETMASK -d $NETWORK/$NETMASK -j ACCEPT

# Perform network address translation (NAT) for packets from the network
iptables -t nat -A POSTROUTING -s $NETWORK/$NETMASK -j MASQUERADE

# Configure dnsmasq as the DHCP and DNS server for the bridge interface
dns_cmd=(
    dnsmasq
    --strict-order
    --except-interface=lo
    --interface=$BRIDGE
    --listen-address=$GATEWAY
    --bind-interfaces
    --dhcp-range=$DHCPRANGE
    --conf-file=""
    --pid-file=/var/run/qemu-dnsmasq-$BRIDGE.pid
    --dhcp-leasefile=/var/run/qemu-dnsmasq-$BRIDGE.leases
    --dhcp-no-override
)

# Execute the dnsmasq command
echo ${dns_cmd[@]} | bash

# Allow traffic from the bridge interface to the wireless interface
iptables -A FORWARD -i $BRIDGE -o $WIRELESS -j ACCEPT

# Perform masquerading for outgoing packets on the wireless interface
iptables -t nat -A POSTROUTING -o $WIRELESS -j MASQUERADE

# Allow known traffic from the wireless interface to return to the bridge interface
iptables -A FORWARD -i $WIRELESS -o $BRIDGE -m state --state RELATED,ESTABLISHED -j ACCEPT

