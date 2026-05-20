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
    import requests
    import socket
    import threading
except Exception as e:
    MissingModule(e)

Title("Ip Reputation Checker")

Scroll(GradientBanner(osint_banner))

try:
    target = input(f"{INPUT} Host {red}->{reset} ").strip()

    if not target:
        ErrorInput()

    target = target.removeprefix("https://").removeprefix("http://").rstrip("/")

    try:
        resolved = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"{ERROR} Could not resolve host!", reset)
        Continue()
        Reset()

    print(f"{INFO} Resolved:{red} {resolved}", reset)
    print(f"{LOADING} Checking..", reset)

    reversed_ip = ".".join(resolved.split(".")[::-1])

    blacklists = {
        "Spamhaus SBL"  : f"{reversed_ip}.sbl.spamhaus.org",
        "Spamhaus XBL"  : f"{reversed_ip}.xbl.spamhaus.org",
        "Spamhaus PBL"  : f"{reversed_ip}.pbl.spamhaus.org",
        "Spamhaus DBL"  : f"{reversed_ip}.dbl.spamhaus.org",
        "Barracuda"     : f"{reversed_ip}.b.barracudacentral.org",
        "Blocklist.de"  : f"{reversed_ip}.bl.blocklist.de",
        "Sorbs SPAM"    : f"{reversed_ip}.spam.sorbs.net",
        "Sorbs HTTP"    : f"{reversed_ip}.http.sorbs.net",
        "Sorbs Socks"   : f"{reversed_ip}.socks.sorbs.net",
        "Abuse.ch"      : f"{reversed_ip}.abuse.ch",
        "SpamCop"       : f"{reversed_ip}.bl.spamcop.net",
        "RATS Spam"     : f"{reversed_ip}.spam.rats-telekom.de",
        "Uceprotect L1" : f"{reversed_ip}.dnsbl-1.uceprotect.net",
        "Uceprotect L2" : f"{reversed_ip}.dnsbl-2.uceprotect.net",
        "Drone BL"      : f"{reversed_ip}.drone.abuse.ch",
        "Nix Spam"      : f"{reversed_ip}.ix.dnsbl.manitu.net",
    }

    results = {}
    lock    = threading.Lock()

    def CheckBlacklist(name, host):
        try:
            socket.gethostbyname(host)
            with lock:
                results[name] = True
        except socket.gaierror:
            with lock:
                results[name] = False
        except Exception:
            with lock:
                results[name] = False

    threads = [threading.Thread(target=CheckBlacklist, args=(n, h), daemon=True) for n, h in blacklists.items()]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    blacklisted_count = sum(1 for v in results.values() if v)
    total             = len(results)

    abuseipdb = "None"
    try:
        r = requests.get(
            f"https://api.abuseipdb.com/api/v2/check?ipAddress={resolved}",
            headers = {"Key": "none", "Accept": "application/json"},
            timeout = 5
        )
        if r.status_code == 200:
            data      = r.json().get("data", {})
            abuseipdb = f"{data.get('abuseConfidenceScore', 0)}% confidence"
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.ConnectionError:
        pass
    except Exception:
        pass

    print()
    for name, is_blacklisted in sorted(results.items()):
        if is_blacklisted:
            print(f"{ERROR} {name:<20} :{red} Blacklisted", reset)
        else:
            print(f"{SUCCESS} {name:<20} :{red} Clean", reset)

    Scroll(f"""
 {INFO} Host       :{red} {target}{white}
 {INFO} Ip         :{red} {resolved}{white}
 {INFO} Blacklists :{red} {blacklisted_count}/{total}{white}
 {INFO} AbuseIPDB  :{red} {abuseipdb}{white}
""")

    Continue()
    Reset()

except Exception as e:
    Error(e)