from flask import Flask, render_template
import json
import psutil
import os
from datetime import datetime
import platform
import time
import sys
import socket

app = Flask(__name__)

def get_primary_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

def get_files(dir):
    all_files = []
    for root, dirs, files in os.walk(dir):
        for f in files:
            file_path = os.path.join(root, f)
            all_files.append(file_path)


@app.route("/")
def home():
    processes = []
    py_files = 0
    text_files = 0
    pdf_files = 0
    img_files = 0
    files_ext = []
    all_files = []

    home_dir = os.path.expanduser("~")

    for root, dirs, files in os.walk(home_dir):
        for f in files:
            file_path = os.path.join(root, f)
            all_files.append(file_path)

            name, ext = os.path.splitext(f)
            ext = ext.lower()
            if f.lower().endswith(".py"):
                py_files += 1
            elif f.lower().endswith(".pdf"):
                pdf_files += 1
            elif f.lower().endswith(".jpg"):
                img_files += 1
            elif f.lower().endswith(".txt"):
                text_files += 1
            else:
                if not ext in files_ext:
                    files_ext.append(ext)

    for p in psutil.process_iter(attrs=["pid", "name"]):
        processes.append({
            "pid": p.info["pid"],
            "name": p.info["name"],
            "cpu": round(p.cpu_percent(None), 1),
            "ram": round(p.memory_percent(), 1) 
    })

    app.logger.warning(files)

    def sort_by_cpu(proc):
        return proc["cpu"]
    
    def sort_by_ram(proc):
        return proc["ram"]

    processes.sort(key=sort_by_cpu, reverse=True)
    processes.sort(key=sort_by_ram, reverse=True)
    top_cpu = processes[:3]
    top_ram = processes[:3]

    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    try:
        cpu_speed = round(psutil.cpu_freq().current, 2)
    except:
        cpu_speed = "unknown"

    log = {
        "time": datetime.now().isoformat(),
        "CPU.physical_core_count": psutil.cpu_count(logical=False),
        "CPU.logical_core_count": psutil.cpu_count(logical=True),
        "CPU.speed_current": cpu_speed,
        "CPU.percentage": psutil.cpu_percent(interval=0.2),

        "RAM.used": round(psutil.virtual_memory().used / (1024 ** 3), 2),
        "RAM.total": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "RAM.percentage": psutil.virtual_memory().percent,

        "SYS.hostname": os.uname().nodename,
        "SYS.operating_system_ver":platform.version(),
        "SYS.system_wake_up": str(datetime.fromtimestamp(psutil.boot_time())),
        "SYS.wake_uptime": (time.time() - psutil.boot_time()),
        "SYS.connected_users_count": len(psutil.users()),
        "SYS.main_IP": get_primary_ip(),
    }

    return render_template("index.html",
                           GEN_TIME = datetime.now().isoformat(),
                           SYS_HOSTNAME = log["SYS.hostname"],
                           SYS_OS_NAME = log["SYS.operating_system_ver"],
                           SYS_UPTIME = log["SYS.wake_uptime"],
                           SYS_CONNECTED_USERS = log["SYS.connected_users_count"],
                           CPU_PERCENTAGE=log["CPU.percentage"],
                           CPU_CORE_COUNT=log["CPU.logical_core_count"],
                           CPU_CURRENT_FREQ=log["CPU.speed_current"],
                           MEMORY_TOTAL_GB=log["RAM.total"],
                           MEMORY_USED_GB=log["RAM.used"],
                           MEMORY_USAGE_PERCENT=log["RAM.percentage"],
                           NETWORK_IP=log["SYS.main_IP"],
                           TOP_CPU_PROCESSES = top_cpu,
                           TOP_MEMORY_PROCESSES = top_ram,
                           ALL_PROCESSES = processes,
                           FILES_DIR = home_dir,
                           FILES_TOTAL_COUNT = len(all_files),
                           IMAGE_FILES_COUNT = img_files,
                           TEXT_FILES_COUNT = text_files,
                           PDF_FILES_COUNT = pdf_files,
                           PYTHON_FILES_COUNT = py_files,
                           CPU_PER_CORE = psutil.cpu_percent(interval=None, percpu=True),

                           )

if __name__ == "__main__":
    app.run(debug=True)
