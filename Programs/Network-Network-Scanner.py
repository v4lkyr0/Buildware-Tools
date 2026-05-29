# Copyright (c) 2025-2026 v4lkyr0 — Buildware-Tools
# See the file 'LICENSE' for copying permission.
# --------------------------------------------------------
# EN: Non-commercial use only. Do not sell, remove credits
#     or redistribute without prior written permission.
# FR: Usage non-commercial uniquement. Ne pas vendre, supprimer
#     les crédits ou redistribuer sans autorisation écrite.

from Core.Utils import *
from Core.Config import *

try:
    from icmplib import ping
    import socket
    import threading
except Exception as e:
    MissingModule(e)

Title("Network Scanner")

Scroll(GradientBanner(network_banner))

try:
    target = input(f"{INPUT} Host {red}->{reset} ").strip()

    if not target:
        ErrorInput()

    target = target.removeprefix("https://").removeprefix("http://").rstrip("/")

    try:
        resolved = socket.gethostbyname(target)
        base     = ".".join(resolved.split(".")[:3])
    except Exception:
        print(f"{ERROR} Could not resolve host!", reset)
        Continue()
        Reset()

    print(f"{INFO} Subnet:{red} {base}.0/24", reset)
    print(f"{LOADING} Scanning..", reset)

    hosts     = []
    lock      = threading.Lock()
    semaphore = threading.Semaphore(50)

    def GetOpenPort(ip):
        for port in [80, 443, 22, 445]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.3)
                if sock.connect_ex((ip, port)) == 0:
                    sock.close()
                    return str(port)
                sock.close()
            except Exception:
                pass
        return "None"

    def ScanHost(ip):
        with semaphore:
            try:
                result = ping(ip, count=1, timeout=1, privileged=False)
                if result.is_alive:
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                    except Exception:
                        hostname = "None"
                    open_port = GetOpenPort(ip)
                    with lock:
                        hosts.append(ip)
                        print(f"{SUCCESS} Host:{red} {ip:<16}{white} | Rtt:{red} {round(result.avg_rtt, 2)}ms{white} | Port:{red} {open_port:<5}{white} | Hostname:{red} {hostname}", reset)
            except Exception:
                pass

    threads = [threading.Thread(target=ScanHost, args=(f"{base}.{i}",), daemon=True) for i in range(1, 255)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"\n{SUCCESS} Found:{red} {len(hosts)} host(s)", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)