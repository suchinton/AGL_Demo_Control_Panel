#!/bin/bash

if [[ $EUID > 0 ]]; then
  echo "Run this script as root"
  exit
fi

BRIDGE="br0"
TAP="tap0"

echo "Removing bridge $BRIDGE"
ip link delete $BRIDGE type bridge

echo "Removing tap $TAP"
ip link delete $TAP type tap

echo "Setting $INTERFACE up"
ip link set up dev $INTERFACE

echo "Starting NetworkManager"
systemctl start NetworkManager

