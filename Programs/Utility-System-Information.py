# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import platform
    import socket
    import psutil
    from datetime import datetime, timedelta
except Exception as e:
    MissingModule(e)

Title("Utility System Information")

def get_cpu_name():
    if platform_pc == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
            winreg.CloseKey(key)
            return name.strip()
        except:
            pass
    elif platform_pc == "Linux":
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        except:
            pass
    return platform.processor() or "N/A"

def get_gpu_names():
    gpus = []
    if platform_pc == "Windows":
        try:
            import winreg
            key_path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    try:
                        desc, _ = winreg.QueryValueEx(subkey, "DriverDesc")
                        if desc and desc not in gpus:
                            gpus.append(desc)
                    except FileNotFoundError:
                        pass
                    winreg.CloseKey(subkey)
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(key)
        except:
            pass
    elif platform_pc == "Linux":
        try:
            with open("/proc/driver/nvidia/gpus/0/information", "r") as f:
                for line in f:
                    if "Model:" in line:
                        gpus.append(line.split(":")[1].strip())
        except:
            pass
    return gpus if gpus else ["N/A"]

try:
    print(f"{LOADING} Gathering System Information..", reset)

    output = ""

    output += f"\n {INFO} System Information\n"
    output += f" {SUCCESS} OS                       :{red} {platform.system()} {platform.release()}{reset}\n"
    output += f" {SUCCESS} OS Version               :{red} {platform.version()}{reset}\n"
    output += f" {SUCCESS} Architecture             :{red} {platform.machine()}{reset}\n"
    output += f" {SUCCESS} Platform                 :{red} {platform.platform()}{reset}\n"
    output += f" {SUCCESS} Hostname                 :{red} {socket.gethostname()}{reset}\n"
    output += f" {SUCCESS} Username                 :{red} {username_pc}{reset}\n"
    output += f" {SUCCESS} Python Version           :{red} {platform.python_version()}{reset}\n"
    output += f" {SUCCESS} Python Compiler          :{red} {platform.python_compiler()}{reset}\n"
    output += f" {SUCCESS} Python Build             :{red} {' '.join(platform.python_build())}{reset}\n"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        output += f" {SUCCESS} Local Ip                 :{red} {local_ip}{reset}\n"
    except:
        pass

    output += f"\n {INFO} Hardware Details\n"

    cpu_name = get_cpu_name()
    output += f" {SUCCESS} CPU                      :{red} {cpu_name}{reset}\n"

    cpu_physical = psutil.cpu_count(logical=False) or "N/A"
    cpu_logical = psutil.cpu_count(logical=True) or "N/A"
    output += f" {SUCCESS} CPU Cores                :{red} {cpu_physical} physical, {cpu_logical} logical{reset}\n"

    try:
        freq = psutil.cpu_freq()
        if freq:
            output += f" {SUCCESS} CPU Frequency            :{red} {freq.current:.0f} MHz (max {freq.max:.0f} MHz){reset}\n"
    except:
        pass

    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        output += f" {SUCCESS} CPU Usage                :{red} {cpu_usage}%{reset}\n"
    except:
        pass

    vm = psutil.virtual_memory()
    total_ram = vm.total / (1024 ** 3)
    used_ram = vm.used / (1024 ** 3)
    available_ram = vm.available / (1024 ** 3)
    output += f" {SUCCESS} Total RAM                :{red} {total_ram:.1f} GB{reset}\n"
    output += f" {SUCCESS} Used RAM                 :{red} {used_ram:.1f} GB ({vm.percent}%){reset}\n"
    output += f" {SUCCESS} Available RAM            :{red} {available_ram:.1f} GB{reset}\n"

    for gpu in get_gpu_names():
        output += f" {SUCCESS} GPU                      :{red} {gpu}{reset}\n"

    output += f"\n {INFO} Disk Information\n"

    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total = usage.total / (1024 ** 3)
            free = usage.free / (1024 ** 3)
            used = usage.used / (1024 ** 3)
            output += f" {SUCCESS} Disk {partition.device:12s}        :{red} {free:.1f} GB free / {total:.1f} GB total ({usage.percent}%){reset}\n"
        except:
            pass

    output += f"\n {INFO} Uptime\n"

    try:
        boot = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        output += f" {SUCCESS} Boot Time                :{red} {boot.strftime('%Y-%m-%d %H:%M:%S')}{reset}\n"
        output += f" {SUCCESS} Uptime                   :{red} {days}d {hours}h {minutes}m{reset}\n"
    except:
        pass

    Scroll(f"\n{output}")

    Continue()
    Reset()

except Exception as e:
    Error(e)
