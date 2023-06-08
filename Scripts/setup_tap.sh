#!/bin/bash

if [[ $EUID > 0 ]]; then
  echo "Run this script as root"
  exit
fi

BRIDGE="br0"
TAP="tap0"

echo "Available network interfaces:"
interfaces=$(ip link | awk -F ': ' '{print $2}')
index=0

# Array to store interface names
declare -a interface_names

# Array to store interface types
declare -a interface_types

# Loop through each interface and display its type
for interface in $interfaces; do
  type=$(ip link show $interface | grep -o 'type .*' | awk '{print $2}')
  echo "$index: $interface - $type"
  
  # Store interface name and type in arrays
  interface_names[$index]=$interface
  interface_types[$index]=$type
  
  ((index++))
done

# Prompt the user to select an interface
read -p "Enter the number of the interface you want to use: " selection

# Validate the user's input
if [[ ! $selection =~ ^[0-9]+$ || $selection -lt 0 || $selection -ge $index ]]; then
  echo "Invalid selection. Exiting."
  exit
fi

INTERFACE=${interface_names[$selection]}
INTERFACE_TYPE=${interface_types[$selection]}

echo "Selected interface: $INTERFACE - $INTERFACE_TYPE"

echo "Adding bridge $BRIDGE"
ip link add name $BRIDGE type bridge

echo "Flushing interface $INTERFACE"
ip addr flush dev $INTERFACE

echo "Setting $BRIDGE as master of $INTERFACE"
ip link set $INTERFACE master $BRIDGE

echo "Adding tap $TAP"
ip tuntap add $TAP mode tap

echo "Setting $BRIDGE as master of $TAP"
ip link set $TAP master $BRIDGE

echo "Setting $INTERFACE, $BRIDGE, and $TAP up"
ip link set up dev $INTERFACE
ip link set up dev $TAP
ip link set up dev $BRIDGE

echo "Stopping NetworkManager"
systemctl stop NetworkManager

echo "Requesting IP for $BRIDGE"
dhclient -1 -v $BRIDGE

if [ $? -eq 0 ]; then
    echo "Requesting IP for $INTERFACE"
    dhclient $INTERFACE
    echo "Killing dhclient and starting NetworkManager"
    pkill -9 dhclient
    systemctl start NetworkManager
fi

# run qemu with the below arguments
#
# qemu-system-x86_64 -netdev tap,id=net0,ifname=tap0,script=no,downscript=no -device virtio-net-pci,netdev=net0

