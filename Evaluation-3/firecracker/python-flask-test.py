import os
import subprocess
import requests
import time


def wait_flask():
    while True:
        try:
            # 发送 HTTP 请求检查是否能够连接到 flask
            response = requests.get("http://172.16.0.2:8080")
            if response.status_code == 200 and response.text == "Hello, World!":
                break
        except requests.ConnectionError:
            pass


def start_flask_with_timing():
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
    wait_flask()
    print(f"Flask started in {(time.time() - start_time) * 1000:.2f} ms.")

    subprocess.Popen("pkill firecracker", shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE).wait()


def restore_flask_with_timing():
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

    wait_flask()

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
    wait_flask()
    print(f"Flask restore in {(time.time() - start_time) * 1000:.2f} ms.")

    subprocess.Popen("pkill firecracker", shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE).wait()


if __name__ == "__main__":
    start_flask_with_timing()
    time.sleep(1)
    restore_flask_with_timing()
