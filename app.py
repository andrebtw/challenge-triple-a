from flask import Flask, render_template
import json
import psutil
import os
from datetime import datetime
import platform
import time
import socket

app = Flask(__name__)

def get_primary_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

@app.route("/")
def home():
    processes = []

    for p in psutil.process_iter(attrs=["pid", "name"]):
        processes.append({
            "pid": p.info["pid"],
            "name": p.info["name"],
            "cpu": p.cpu_percent(None),
            "ram": p.memory_percent()
    })

    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    try:
        cpu_speed = psutil.cpu_freq().current
    except:
        cpu_speed = "unknown"

    log = {
        "time": datetime.now().isoformat(),
        "CPU.physical_core_count": psutil.cpu_count(logical=False),
        "CPU.logical_core_count": psutil.cpu_count(logical=True),
        "CPU.speed_current": cpu_speed,
        "CPU.percentage": psutil.cpu_percent(interval=0.2),

        "RAM.used": round(psutil.virtual_memory().used / (1024 ** 3), 3),
        "RAM.total": round(psutil.virtual_memory().total / (1024 ** 3), 3),
        "RAM.percentage": psutil.virtual_memory().percent,

        "SYS.hostname": os.uname().nodename,
        "SYS.operating_system_ver":platform.version(),
        "SYS.system_wake_up": str(datetime.fromtimestamp(psutil.boot_time())),
        "SYS.wake_uptime": time.time() - psutil.boot_time(),
        "SYS.connected_users_count": len(psutil.users()),
        "SYS.main_IP": get_primary_ip(),
        "PROCESSES": processes,
    }

    return render_template("index.html",
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

                           )

if __name__ == "__main__":
    app.run(debug=True)
