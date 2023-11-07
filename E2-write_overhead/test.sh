#!/bin/bash

# 设置循环次数
max_iterations=100

# 设置输出文件
out_file="out.txt"

if [ -f $out_file ]; then
    rm $out_file
    touch $out_file
fi

# 创建cgroup
mkdir /sys/fs/cgroup/memory/test
for size in 512 1 2 3;do
    echo "size: $size" >> $out_file
    echo "size: $size"
    # 设置迭代计数
    iteration=0
    while [ $iteration -lt $max_iterations ]; do
        # enable memory faascale
        echo 4G > /sys/fs/cgroup/memory/test/memory.faascale.size
        # execute the program, out the result to out_file
        ./a.out $size >> $out_file
        # free memory faascale
        while [ $(cat /sys/fs/cgroup/memory/test/memory.faascale.size) != "0" ]; do
            sleep 1
            echo 1 > /sys/fs/cgroup/memory/test/memory.faascale.free
        done
        # 增加迭代计数
        ((iteration++))
        sleep 1
    done
done
# 删除cgroup
rmdir /sys/fs/cgroup/memory/test

echo "Script finished."
