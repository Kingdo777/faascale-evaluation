kernel_path=/home/kingdo/firecracker/vmlinux-5.10.198
rootfs_path=/home/kingdo/firecracker/ubuntu-22.04-4G.ext4
kernel_args="console=ttyS0 noapic reboot=k panic=1 pci=off"


# set the guest kernel
curl --unix-socket /tmp/firecracker.socket -i \
      -X PUT 'http://localhost/boot-source'   \
      -H 'Accept: application/json'           \
      -H 'Content-Type: application/json'     \
      -d "{
            \"kernel_image_path\": \"${kernel_path}\",
            \"boot_args\": \"${kernel_args}\"
       }"

# set the guest rootfs
curl --unix-socket /tmp/firecracker.socket -i \
  -X PUT 'http://localhost/drives/rootfs' \
  -H 'Accept: application/json'           \
  -H 'Content-Type: application/json'     \
  -d "{
        \"drive_id\": \"rootfs\",
        \"path_on_host\": \"${rootfs_path}\",
        \"is_root_device\": true,
        \"is_read_only\": false
   }"

# Configure resource
curl --unix-socket /tmp/firecracker.socket -i  \
  -X PUT 'http://localhost/machine-config' \
  -H 'Accept: application/json'            \
  -H 'Content-Type: application/json'      \
  -d '{
      "vcpu_count": 1,
      "mem_size_mib": 512
  }'

curl -X PUT \
  --unix-socket /tmp/firecracker.socket \
  http://localhost/network-interfaces/eth0 \
  -H accept:application/json \
  -H content-type:application/json \
  -d '{
    "iface_id": "eth0",
    "guest_mac": "06:00:AC:10:00:02",
    "host_dev_name": "tap0"
}'

# start the guest machine
curl --unix-socket /tmp/firecracker.socket -i \
  -X PUT 'http://localhost/actions'       \
  -H  'Accept: application/json'          \
  -H  'Content-Type: application/json'    \
  -d '{
      "action_type": "InstanceStart"
   }'


