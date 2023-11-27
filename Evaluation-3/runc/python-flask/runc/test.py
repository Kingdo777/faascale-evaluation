import subprocess
import requests
import time


def runc_python_flask(command):
    # checkpoint runc 命令
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()


def start_python_flask_with_timing(command, restore=False):
    # 启动 runc 命令
    start_time = time.time()
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 等待 python_flask 启动
    while True:
        try:
            # 发送 HTTP 请求检查是否能够连接到 python_flask
            response = requests.get("http://127.0.0.1:8080")
            if response.status_code == 200 and response.text == "Hello, World!":
                break
        except requests.ConnectionError:
            pass

    # 计算启动时间
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    if restore:
        print(f"Python-Flask restored in {elapsed_time:.2f} ms.")
    else:
        print(f"Python-Flask started in {elapsed_time:.2f} ms.")


if __name__ == "__main__":
    start_runc_python_flask_command = "runc run python_flask"
    start_python_flask_with_timing(start_runc_python_flask_command)

    # rm -rf ./checkpoint
    subprocess.Popen("rm -rf ./checkpoint", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    checkpoint_runc_python_flask_command = "runc checkpoint python_flask"
    runc_python_flask(checkpoint_runc_python_flask_command)

    restore_runc_python_flask_command = "runc restore python_flask"
    start_python_flask_with_timing(restore_runc_python_flask_command, restore=True)

    kill_runc_python_flask_command = "runc kill python_flask"
    runc_python_flask(kill_runc_python_flask_command)
