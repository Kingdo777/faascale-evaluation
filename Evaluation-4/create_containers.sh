#!/bin/bash

# https://github.com/opencontainers/runc
# 1. Install runc in firecracker-vm
# 2. Run this script in firecracker-vm


# 检查输入参数
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <number_of_containers> <container_prefix>"
    exit 1
fi

# 从命令行参数获取容器数量和前缀
num_containers=$1
container_prefix=$2

# 创建N个容器
for ((i=1; i<=$num_containers; i++)); do
    container_id="${container_prefix}${i}"
    echo "Creating container: $container_id"
    runc run -d $container_id
done

echo "Containers created successfully."