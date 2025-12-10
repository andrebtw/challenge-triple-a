import psutil
import os
from datetime import datetime
import platform
import time
from datetime import timedelta
import socket

def get_time_now():
    return datetime.now().isoformat()

def get_hostname():
    os.uname().nodename

def get_platform():
    if platform.system() == "Linux":
        try:
            info = platform.freedesktop_os_release()
            return info.get("PRETTY_NAME", "Linux")
        except Exception:
            return "Linux"
    else:
        return f"{platform.system()} {platform.release()}"

def get_uptime():
    seconds = time.time() - psutil.boot_time()
    return str(timedelta(seconds=seconds))

def get_connected_users_count():
    return len(psutil.users())


def get_primary_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()


def get_cpu_percentage():
    return psutil.cpu_percent(interval=0.2)


def get_cpu_core_count():
    return psutil.cpu_count(logical=True)


def get_cpu_physical_core_count():
    return psutil.cpu_count(logical=False)


def get_cpu_speed():
    try:
        return round(psutil.cpu_freq().current, 2)
    except Exception:
        return "unknown"


def get_cpu_per_core():
    return psutil.cpu_percent(interval=None, percpu=True)


def get_memory_total_gb():
    return round(psutil.virtual_memory().total / (1024 ** 3), 2)


def get_memory_used_gb():
    return round(psutil.virtual_memory().used / (1024 ** 3), 2)


def get_memory_percentage():
    return psutil.virtual_memory().percent

def get_files_info():
    home_dir = os.path.expanduser("~")
    py_files = 0
    text_files = 0
    pdf_files = 0
    img_files = 0
    all_files = []

    for root, dirs, files in os.walk(home_dir):
        for f in files:
            file_path = os.path.join(root, f)
            all_files.append(file_path)

            lower = f.lower()
            if lower.endswith(".py"):
                py_files += 1
            elif lower.endswith(".pdf"):
                pdf_files += 1
            elif lower.endswith((".jpg", ".jpeg", ".png")):
                img_files += 1
            elif lower.endswith(".txt"):
                text_files += 1

    return {
        "home_dir": home_dir,
        "all_files": all_files,
        "py_files_count": py_files,
        "text_files_count": text_files,
        "pdf_files_count": pdf_files,
        "img_files_count": img_files
        }

def get_processes_info():
    processes = []
    for p in psutil.process_iter(attrs=["pid", "name"]):
        try:
            processes.append({
                "pid": p.info["pid"],
                "name": p.info["name"],
                "cpu": round(p.cpu_percent(None), 1),
                "ram": round(p.memory_percent(), 1),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes_by_cpu = sorted(processes, key=lambda proc: proc["cpu"], reverse=True)
    processes_by_ram = sorted(processes, key=lambda proc: proc["ram"], reverse=True)

    top_cpu = processes_by_cpu[:3]
    top_ram = processes_by_ram[:3]

    return {
        "all": processes,
        "top_cpu": top_cpu,
        "top_ram": top_ram
    }