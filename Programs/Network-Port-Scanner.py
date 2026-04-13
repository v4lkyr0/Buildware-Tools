# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import socket
    import time
except Exception as e:
    MissingModule(e)

Title("Network Port Scanner")
Connection()

common_ports = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 111: "RPCBind", 135: "MSRPC",
    139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    993: "IMAPS", 995: "POP3S", 1433: "MSSQL", 1521: "Oracle",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
    6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB",
}

try:
    target = input(f"{INPUT} Target {red}->{reset} ").strip()
    if not target:
        ErrorInput()

    target = target.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]

    Scroll(f"""
 {PREFIX}01{SUFFIX} Common Ports
 {PREFIX}02{SUFFIX} Custom Range
 {PREFIX}03{SUFFIX} Top 1000 Ports
""")
    mode = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    if mode == "1":
        ports = list(common_ports.keys())
    elif mode == "2":
        try:
            start = int(input(f"{INPUT} Start Port {red}->{reset} ").strip())
            end = int(input(f"{INPUT} End Port {red}->{reset} ").strip())
        except ValueError:
            ErrorNumber()
        if start < 1 or end > 65535 or start > end:
            ErrorNumber()
        ports = list(range(start, end + 1))
    elif mode == "3":
        ports = list(range(1, 1001))
    else:
        ErrorChoice()

    try:
        ip = socket.gethostbyname(target)
    except:
        print(f"{ERROR} Could not resolve Target!", reset)
        Continue()
        Reset()

    print(f"{LOADING} Scanning Ports..", reset)

    open_ports = []
    closed = 0
    output = ""
    start_time = time.time()

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                service = common_ports.get(port, "Unknown")
                output += f" {SUCCESS} Port:{red} {port:5d}  {white}| Service:{red} {service}{reset}\n"
                open_ports.append((port, service))
            else:
                closed += 1
            sock.close()
        except:
            closed += 1

    elapsed = time.time() - start_time

    output += f"\n{INFO} Scan Completed in{red} {elapsed:.2f}s{reset}\n"
    output += f"{INFO} Open:{red} {len(open_ports)}{white} | Closed:{red} {closed}{reset}\n"

    Scroll(f"\n{output}")

    Continue()
    Reset()

except Exception as e:
    Error(e)
