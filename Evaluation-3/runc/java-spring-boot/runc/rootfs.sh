#!/bin/bash

image="kingdo/java-spring-boot:latest"

# Create the rootfs directory
sudo rm -rf rootfs && mkdir rootfs

# Create the list of files to be included in the rootfs
sudo docker export $(docker create "${image}") | tar -C rootfs -xvf -
