from flask import Flask, render_template
from monitor import *

app = Flask(__name__)

@app.route("/")
def home():
    processes = get_processes_info()
    files = get_files_info()

    return render_template("index.html",
                           GEN_TIME=get_time_now(),
                           SYS_HOSTNAME=get_hostname(),
                           SYS_OS_NAME=get_platform(),
                           SYS_UPTIME=get_uptime(),
                           SYS_CONNECTED_USERS=get_connected_users_count(),
                           
                           CPU_PERCENTAGE=get_cpu_percentage(),
                           CPU_CORE_COUNT=get_cpu_physical_core_count(),
                           CPU_THREADS_COUNT=get_cpu_core_count(),
                           CPU_CURRENT_FREQ=get_cpu_speed(),
                           CPU_PHYSICAL_CORE_COUNT=get_cpu_physical_core_count(),
                           CPU_PER_CORE=get_cpu_per_core(),
                           
                           MEMORY_TOTAL_GB=get_memory_total_gb(),
                           MEMORY_USED_GB=get_memory_used_gb(),
                           MEMORY_USAGE_PERCENT=get_memory_percentage(),
                           
                           NETWORK_IP=get_primary_ip(),

                           TOP_CPU_PROCESSES=processes["top_cpu"],
                           TOP_MEMORY_PROCESSES=processes["top_ram"],
                           ALL_PROCESSES=processes["all"],

                           FILES_DIR=files["home_dir"],
                           FILES_TOTAL_COUNT=len(files["all_files"]),
                           IMAGE_FILES_COUNT=files["img_files_count"],
                           TEXT_FILES_COUNT=files["text_files_count"],
                           PDF_FILES_COUNT=files["pdf_files_count"],
                           PYTHON_FILES_COUNT=files["py_files_count"],
                           )

if __name__ == "__main__":
    app.run(debug=True)
