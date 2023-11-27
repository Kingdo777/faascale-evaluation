import subprocess
import requests
import time


def runc_nginx(command):
    # checkpoint runc 命令
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()


def start_nginx_with_timing(command, restore=False):
    # 启动 runc 命令
    start_time = time.time()
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 等待 nginx 启动
    while True:
        try:
            # 发送 HTTP 请求检查是否能够连接到 nginx
            response = requests.get("http://127.0.0.1:80")
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            pass

    # 计算启动时间
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    if restore:
        print(f"Nginx restored in {elapsed_time:.2f} ms.")
    else:
        print(f"Nginx started in {elapsed_time:.2f} ms.")


if __name__ == "__main__":
    start_runc_nginx_command = "runc run nginx"
    start_nginx_with_timing(start_runc_nginx_command)

    # rm -rf ./checkpoint
    subprocess.Popen("rm -rf ./checkpoint", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    checkpoint_runc_nginx_command = "runc checkpoint nginx"
    runc_nginx(checkpoint_runc_nginx_command)

    restore_runc_nginx_command = "runc restore nginx"
    start_nginx_with_timing(restore_runc_nginx_command, restore=True)

    kill_runc_nginx_command = "runc kill nginx"
    runc_nginx(kill_runc_nginx_command)
