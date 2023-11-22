#!/bin/bash

# 设置循环次数
max_iterations=100

# 创建cgroup
mkdir /sys/fs/cgroup/memory/test
for size in 512M 1024M 2048M 3072M;do
    echo "size: $size"
    # 设置迭代计数
    iteration=0
    while [ $iteration -lt $max_iterations ]; do
        # enable memory faascale
        echo $size > /sys/fs/cgroup/memory/test/memory.faascale.size
        # free memory faascale
        while [ $(cat /sys/fs/cgroup/memory/test/memory.faascale.size) != "0" ]; do
            echo 1 > /sys/fs/cgroup/memory/test/memory.faascale.free
        done
        # 增加迭代计数
        ((iteration++))
    done
done
# 删除cgroup
rmdir /sys/fs/cgroup/memory/test

echo "Script finished."
