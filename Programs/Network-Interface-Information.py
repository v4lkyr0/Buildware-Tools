# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import socket
    import psutil
except Exception as e:
    MissingModule(e)

Title("Network Interface Information")
Connection()

try:
    print(f"{LOADING} Gathering Network Information..", reset)

    hostname = socket.gethostname()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "Could not determine"

    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    output = ""
    output += f"\n {INFO} Hostname                 :{red} {hostname}{reset}\n"
    output += f" {INFO} Local Ip Address         :{red} {local_ip}{reset}\n\n"

    for iface_name, addrs in interfaces.items():
        iface_stat = stats.get(iface_name)
        status = "Up" if iface_stat and iface_stat.isup else "Down"
        speed = f"{iface_stat.speed} Mbps" if iface_stat and iface_stat.speed > 0 else "N/A"

        output += f" {INFO} Interface:{red} {iface_name} {white}| Status:{red} {status} {white}| Speed:{red} {speed}{reset}\n"

        for addr in addrs:
            family_name = {
                socket.AF_INET: "IPv4",
                socket.AF_INET6: "IPv6",
            }.get(addr.family, "MAC" if addr.family == psutil.AF_LINK else "Other")

            if family_name == "IPv4":
                output += f" {SUCCESS} IPv4     :{red} {addr.address}{white} / {addr.netmask or 'N/A'}{reset}\n"
            elif family_name == "IPv6":
                output += f" {SUCCESS} IPv6     :{red} {addr.address}{reset}\n"
            elif family_name == "MAC":
                output += f" {SUCCESS} MAC      :{red} {addr.address}{reset}\n"

        output += "\n"

    io = psutil.net_io_counters()
    output += f" {INFO} Network I/O\n"
    output += f" {SUCCESS} Bytes Sent               :{red} {io.bytes_sent / (1024**2):.1f} MB{reset}\n"
    output += f" {SUCCESS} Bytes Received           :{red} {io.bytes_recv / (1024**2):.1f} MB{reset}\n"
    output += f" {SUCCESS} Packets Sent             :{red} {io.packets_sent:,}{reset}\n"
    output += f" {SUCCESS} Packets Received         :{red} {io.packets_recv:,}{reset}\n"

    Scroll(output)

    Continue()
    Reset()

except Exception as e:
    Error(e)
