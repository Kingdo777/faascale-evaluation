#!/bin/bash

current_dir=$(dirname "$0")

sudo setfacl -m u:${USER}:rw /dev/kvm
sudo rm -f /tmp/firecracker.socket
sudo $current_dir/network-ifup tap0
$current_dir/../bin/release-v1.1.3-x86_64/firecracker-v1.1.3-x86_64 --api-sock /tmp/firecracker.socket
sudo $current_dir/network-ifdown tap0
