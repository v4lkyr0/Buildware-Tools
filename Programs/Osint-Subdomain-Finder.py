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

Title("Subdomain Finder")

Scroll(GradientBanner(osint_banner))

fallback_wordlist = [
    "www", "mail", "ftp", "smtp", "pop", "imap", "webmail", "admin", "portal",
    "api", "dev", "staging", "test", "beta", "app", "mobile", "m", "cdn",
    "static", "media", "img", "images", "assets", "shop", "store", "blog",
    "forum", "wiki", "docs", "support", "help", "kb", "status", "monitor",
    "vpn", "remote", "gateway", "proxy", "ns", "ns1", "ns2", "dns", "mx",
    "cloud", "server", "host", "web", "secure", "ssl", "auth", "login",
    "account", "dashboard", "panel", "cpanel", "whm", "phpmyadmin", "db",
    "database", "sql", "mysql", "git", "gitlab", "github", "jenkins", "ci",
    "jira", "confluence", "intranet", "internal", "extranet", "ldap", "sso",
]

try:
    target = input(f"{INPUT} Domain {red}->{reset} ").strip()

    if not target:
        ErrorInput()

    target = target.removeprefix("https://").removeprefix("http://").rstrip("/")

    try:
        socket.gethostbyname(target)
    except socket.gaierror:
        print(f"{ERROR} Could not resolve host!", reset)
        Continue()
        Reset()

    print(f"{LOADING} Fetching wordlist..", reset)

    wordlist = None

    try:
        response = requests.get(
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt",
            timeout=10
        )
        if response.status_code == 200:
            wordlist = [w for w in response.text.splitlines() if w.strip()]
            print(f"{SUCCESS} Wordlist:{red} {len(wordlist)} entries", reset)
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.ConnectionError:
        pass
    except Exception:
        pass

    if not wordlist:
        print(f"{LOADING} Using fallback wordlist {red}({white}{len(fallback_wordlist)} entries{red}){white}..", reset)
        wordlist = fallback_wordlist

    print(f"{LOADING} Scanning..", reset)

    found     = []
    lock      = threading.Lock()
    semaphore = threading.Semaphore(50)

    def ScanSubdomain(sub):
        with semaphore:
            try:
                subdomain = f"{sub}.{target}"
                resolved  = socket.gethostbyname(subdomain)
                with lock:
                    found.append((subdomain, resolved))
                    print(f"{SUCCESS} Subdomain:{red} {subdomain:<45}{white} | Ip:{red} {resolved}", reset)
            except socket.gaierror:
                pass
            except Exception:
                pass

    threads = [threading.Thread(target=ScanSubdomain, args=(sub,), daemon=True) for sub in wordlist]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    if not found:
        print(f"{ERROR} No subdomains found!", reset)
    else:
        print(f"\n{SUCCESS} Found:{red} {len(found)} subdomain(s)", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)