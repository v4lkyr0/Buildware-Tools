# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    from icmplib import traceroute as icmp_traceroute
    import socket
except Exception as e:
    MissingModule(e)

Title("Network Traceroute")
Connection()

try:
    target = input(f"{INPUT} Target {red}->{reset} ").strip()
    if not target:
        ErrorInput()

    target = target.replace("http://", "").replace("https://", "").split("/")[0]

    print(f"{LOADING} Tracing Route to {red}{target}{white}..", reset)

    output = ""

    try:
        hops = icmp_traceroute(target, max_hops=30, timeout=2)

        last_distance = 0
        for hop in hops:
            if hop.distance != last_distance:
                if hop.address:
                    try:
                        hostname = socket.gethostbyaddr(hop.address)[0]
                        display = f"{hop.address} ({hostname})"
                    except:
                        display = hop.address
                    output += f" {PREFIX}{hop.distance:02d}{SUFFIX} {red}{display}{white} - {red}{hop.avg_rtt:.2f} ms{reset}\n"
                else:
                    output += f" {PREFIX}{hop.distance:02d}{SUFFIX} {red}* * *{reset}\n"
                last_distance = hop.distance

        output += f"\n{SUCCESS} Traceroute completed!{reset}\n"

    except PermissionError:
        output += f"{ERROR} Administrator privileges required for traceroute!{reset}\n"
    except Exception as e:
        output += f"{ERROR} Traceroute failed:{red} {e}{reset}\n"

    Scroll(f"\n{output}")

    Continue()
    Reset()

except Exception as e:
    Error(e)
