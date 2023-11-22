# socket_location=/tmp/firecracker.socket
#
# curl --unix-socket $socket_location -i \
#                     -X GET 'http://localhost/balloon/statistics' \
#                            -H 'Accept: application/json'
import shlex
import subprocess
import time

# get result:
# {"target_pages":0,"actual_pages":0,"target_mib":0,"actual_mib":0,"swap_in":0,"swap_out":0,"major_faults":1020,"minor_faults":61745,"free_memory":8114397184,"total_memory":8348553216,"available_memory":8052191232,"disk_caches":145842176,"hugetlb_allocations":0,"hugetlb_failures":0}


# curl --unix-socket $socket_location -i \
#      -X PATCH 'http://localhost/balloon' \
#      -H 'Accept: application/json' \
#      -H 'Content-Type: application/json' \
#       -d "{
#           \"amount_mib\": $amount_mib \
#     }"

import requests_unixsocket

import json


def run_curl(url):
    try:
        # 使用subprocess运行curl命令
        result = subprocess.run(['curl', url], capture_output=True, text=True, check=True)

        # 检查curl命令的返回代码
        if result.returncode == 0:
            # 如果成功，返回curl的输出内容
            return result.stdout.strip()
        else:
            print(f"Error: {result.returncode}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None


socket_location = '/tmp/firecracker.socket'


def get_balloon():
    try:
        curl = r"""curl --unix-socket /tmp/firecracker.socket -X GET 'http://localhost/balloon/statistics' -H 'Accept: application/json'"""
        # 使用subprocess运行curl命令
        lcmd = shlex.split(curl)  # Splits cURL into an array

        p = subprocess.Popen(lcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out, err = p.communicate()  # Get the output and the err message

        data = json.loads(out.decode('utf-8'))  # Decode the JSON from the output

        return int(data['target_pages'] / 256), int(data['actual_pages'] / 256)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None


def set_balloon(amount_mib):
    try:
        curl = f"""curl --unix-socket /tmp/firecracker.socket -X PATCH 'http://localhost/balloon' -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{{\"amount_mib\": {amount_mib} }}'"""
        # 使用subprocess运行curl命令
        lcmd = shlex.split(curl)  # Splits cURL into an array

        p = subprocess.Popen(lcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out, err = p.communicate()  # Get the output and the err message

        data = out.decode('utf-8')  # Decode the JSON from the output

        return data
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None


def wait_balloon_ok(amount_mib):
    while True:
        target, actual = get_balloon()
        if target == amount_mib and actual == amount_mib:
            return True
        else:
            time.sleep(0.01)


expand = []
shrink = []

sizes = [128, 512, 1024, 2048, 3096]

loop = 10

if __name__ == '__main__':
    for size in sizes:
        expand_tmp = []
        shrink_tmp = []
        set_balloon(0)
        wait_balloon_ok(0)

        for i in range(loop):
            start_time = time.time()
            set_balloon(size)
            wait_balloon_ok(size)
            shrink_tmp.append((time.time() - start_time) * 1000)

            start_time = time.time()
            set_balloon(0)
            wait_balloon_ok(0)
            expand_tmp.append((time.time() - start_time) * 1000)

        expand.append(expand_tmp)
        shrink.append(shrink_tmp)

    print(expand)
    print(shrink)
