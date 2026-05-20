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
    from icmplib import traceroute
    import socket
except Exception as e:
    MissingModule(e)

Title("Traceroute")

Scroll(GradientBanner(network_banner))

try:
    target = input(f"{INPUT} Host {red}->{reset} ").strip()

    if not target:
        ErrorInput()

    target = target.removeprefix("https://").removeprefix("http://").rstrip("/")

    try:
        resolved = socket.gethostbyname(target)
    except Exception:
        print(f"{ERROR} Could not resolve host!", reset)
        Continue()
        Reset()

    print(f"{INFO} Resolved:{red} {resolved}", reset)
    print(f"{LOADING} Tracerouting..", reset)

    try:
        hops = traceroute(resolved, max_hops=30, timeout=2, privileged=False)

        if not hops:
            print(f"{ERROR} No hops found!", reset)
            Continue()
            Reset()

        last_distance = 0
        total_hops    = 0
        reached       = False

        for hop in hops:
            for missing in range(last_distance + 1, hop.distance):
                print(f"{ERROR} Hop:{red} {missing:<3}{white} | * * * No response.", reset)

            if hop.is_alive:
                try:
                    hostname = socket.gethostbyaddr(hop.address)[0]
                except Exception:
                    hostname = "None"
                print(f"{SUCCESS} Hop:{red} {hop.distance:<3}{white} | Ip:{red} {hop.address:<16}{white} | Time:{red} {round(hop.avg_rtt, 2)}ms{white} | Host:{red} {hostname}", reset)
                total_hops += 1
                if hop.address == resolved:
                    reached = True
            else:
                print(f"{ERROR} Hop:{red} {hop.distance:<3}{white} | * * * Request timed out.", reset)

            last_distance = hop.distance

        print(f"\n{SUCCESS} Hops:{red} {total_hops}{white} | Reached:{red} {'Yes' if reached else 'No'}", reset)

    except PermissionError:
        print(f"{ERROR} Traceroute requires elevated privileges!", reset)
    except Exception:
        print(f"{ERROR} Traceroute failed!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)