import psutil
import datetime


def get_cpu_ussage():
    return psutil.cpu_percent(interval=1)

def get_memory_info():
    return psutil.virtual_memory()

def get_disk_info(path="C:\\"):
    return psutil.disk_usage(path)

def get_battery_info():
    return psutil.sensors_battery()

def get_uptime():
    boot_timestamp = psutil.boot_time()
    boot_time = datetime.datetime.fromtimestamp(boot_timestamp)

    now = datetime.datetime().now
    uptime = now - boot_time

    return uptime, boot_time

def get_top_processes(limit=10):
    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "memory_info"]
    ):
        try:
            info = process.info
            memory = info["memory_info"]

            if memory is None:
                continue
            
            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "memory": memory.rss
            })
        
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

        processes.sort(
            key=lambda process: process["memory"],
            reverse=True
        )

        return processes[:limit]