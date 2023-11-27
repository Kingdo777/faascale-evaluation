import os
import subprocess
import requests
import time


def wait_nginx():
    while True:
        try:
            # 发送 HTTP 请求检查是否能够连接到 nginx
            response = requests.get("http://172.16.0.2")
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            pass


def start_nginx_with_timing():
    # 启动 firecracker
    subprocess.Popen("./scripts/start-firecracker.sh", shell=False,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)

    time.sleep(1)

    # 启动 VM
    subprocess.Popen("./scripts/start-vm.sh", shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE).wait()

    start_time = time.time()
    wait_nginx()
    print(f"Nginx started in {(time.time() - start_time) * 1000:.2f} ms.")

    subprocess.Popen("pkill firecracker", shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE).wait()


def restore_nginx_with_timing():
    # 启动 firecracker
    subprocess.Popen("./scripts/start-firecracker.sh", shell=False,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    print("start-firecracker")
    time.sleep(1)

    # 启动 VM
    subprocess.Popen("./scripts/start-vm.sh", shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE).wait()
    print("start-vm")

    wait_nginx()

    subprocess.Popen("./scripts/checkpoint.sh", shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE).wait()
    print("checkpoint")
    time.sleep(1)

    # 启动 firecracker
    subprocess.Popen("./scripts/start-firecracker.sh", shell=False,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    print("re-start-firecracker")
    time.sleep(1)

    subprocess.Popen("./scripts/restore.sh", shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)

    start_time = time.time()
    wait_nginx()
    print(f"Nginx restore in {(time.time() - start_time) * 1000:.2f} ms.")

    subprocess.Popen("pkill firecracker", shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE).wait()


if __name__ == "__main__":
    start_nginx_with_timing()
    time.sleep(1)
    restore_nginx_with_timing()
