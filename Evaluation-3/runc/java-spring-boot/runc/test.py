import subprocess
import requests
import time


def runc_java_sping_boot(command):
    # checkpoint runc 命令
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()


def start_java_sping_boot_with_timing(command, restore=False):
    # 启动 runc 命令
    start_time = time.time()
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 等待 java_sping_boot 启动
    while True:
        try:
            # 发送 HTTP 请求检查是否能够连接到 java_sping_boot
            response = requests.get("http://127.0.0.1:8080")
            if response.status_code == 200 and response.text == "Hello World!":
                break
        except requests.ConnectionError:
            pass

    # 计算启动时间
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    if restore:
        print(f"Java-SpringBoot restored in {elapsed_time:.2f} ms.")
    else:
        print(f"Java-SpringBoot started in {elapsed_time:.2f} ms.")


if __name__ == "__main__":
    start_runc_java_sping_boot_command = "runc run java_sping_boot"
    start_java_sping_boot_with_timing(start_runc_java_sping_boot_command)

    # rm -rf ./checkpoint
    subprocess.Popen("rm -rf ./checkpoint", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    checkpoint_runc_java_sping_boot_command = "runc checkpoint --tcp-established java_sping_boot"
    runc_java_sping_boot(checkpoint_runc_java_sping_boot_command)

    restore_runc_java_sping_boot_command = "runc restore  --tcp-established java_sping_boot"
    start_java_sping_boot_with_timing(restore_runc_java_sping_boot_command, restore=True)

    kill_runc_java_sping_boot_command = "runc kill java_sping_boot"
    runc_java_sping_boot(kill_runc_java_sping_boot_command)
