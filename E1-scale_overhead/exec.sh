# exec.sh method op value
# @method: vitio_mem, balloon
# op: set, get
# value: {int}

# doc func
function doc() {
      echo "Usage: $0 method op value"
      echo " - method: virtio_mem, balloon"
      echo " - op: set, get"
      echo " - value: {int} && op must is set"
}

# check param, #$ must is 2 or 3, if is 2,op must is get, if is 3, op must is set
# method must is virtio_mem or balloon
# value must is int
function param_check() {
    if [ $# -lt 2 -o $# -gt 3 ]; then
    doc
    exit 1
    fi

    if [ $1 != "virtio_mem" -a $1 != "balloon" ]; then
        doc
        exit 1
    fi

    if [ $# -eq 2 ]; then
        if [ $2 != "get" ]; then
            doc
            exit 1
        fi
    fi

    if [ $# -eq 3 ]; then
        if [ $2 != "set" ]; then
            doc
            exit 1
        fi
        if [ $3 -lt 0 ]; then
            doc
            exit 1
        fi
    fi
}

param_check $@

method=$1
op=$2
value=$3
qemu_pid=$(ps -ef | grep qemu-system-x86_64 | grep -v grep | awk '{print $2}')


if [ $op == "get" ]; then
  url="127.0.0.1:8081/current_${method}_size"
  curl "$url"

else
  url="127.0.0.1:8081/change_${method}_to?value=${value}"
  # get pgfault from /sys/fs/cgroup/qemu/memory.stat
  echo -n "$(cat /sys/fs/cgroup/qemu/memory.stat | grep pgfault | awk '{print $2}')"
  # get qemu-system-x86_64 rss from /proc/$qemu_pid/statm, pages to MBs(%.2f)
  echo " $(cat /proc/$qemu_pid/statm | awk '{print $2/1024*4}')"
  curl "$url"
  echo -n "$(cat /sys/fs/cgroup/qemu/memory.stat | grep pgfault | awk '{print $2}')"
  echo " $(cat /proc/$qemu_pid/statm | awk '{print $2/1024*4}')"
fi