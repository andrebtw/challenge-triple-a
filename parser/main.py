import json
import psutil
from datetime import datetime

if __name__ == "__main__":
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
        "RAM.percentage": psutil.virtual_memory().percent
    }

    
    data.setdefault("logs", [])
    data["logs"].append(log)

    print(data)
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
