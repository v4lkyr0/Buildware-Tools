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
except Exception as e:
    MissingModule(e)

Title("Email Breach Checker")

Scroll(GradientBanner(osint_banner))

try:
    email = input(f"{INPUT} Email {red}->{reset} ").strip()

    if not email or "@" not in email or "." not in email:
        print(f"{ERROR} Invalid email!", reset)
        Continue()
        Reset()

    print(f"{LOADING} Checking..", reset)

    found   = False
    sources = []

    try:
        response = requests.get(
            f"https://leakcheck.io/api/public?check={email}",
            headers = {"User-Agent": RandomUserAgents()},
            timeout = 10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("found", 0) > 0:
                found = True
                sources.append({
                    "source" : "LeakCheck.io",
                    "found"  : data.get("found", 0),
                    "fields" : ", ".join(data.get("fields",  [])) or "None",
                    "sources": ", ".join(data.get("sources", [])) or "None",
                })
        elif response.status_code == 429:
            print(f"{ERROR} LeakCheck.io rate limited!", reset)
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.ConnectionError:
        pass
    except Exception:
        pass

    try:
        response = requests.get(
            f"https://intelx.io/phonebook/search?term={email}&k=&maxresults=1&media=0&terminate=[]&timeout=20",
            headers = {"User-Agent": RandomUserAgents()},
            timeout = 10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("selectors") and len(data["selectors"]) > 0:
                found = True
                sources.append({
                    "source" : "IntelX",
                    "found"  : len(data["selectors"]),
                    "fields" : "Email",
                    "sources": "IntelX Database",
                })
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.ConnectionError:
        pass
    except Exception:
        pass

    try:
        response = requests.get(
            f"https://breachdirectory.org/api?func=auto&term={email}",
            headers = {"User-Agent": RandomUserAgents()},
            timeout = 10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("result"):
                found = True
                sources.append({
                    "source" : "BreachDirectory",
                    "found"  : len(data["result"]),
                    "fields" : "Password Hash",
                    "sources": "BreachDirectory Database",
                })
        elif response.status_code == 429:
            print(f"{ERROR} BreachDirectory rate limited!", reset)
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.ConnectionError:
        pass
    except Exception:
        pass

    if found:
        total = sum(s["found"] for s in sources)
        print(f"{ERROR} Found in {total} breaches across {len(sources)} sources!\n", reset)
        for s in sources:
            Scroll(f"""
 {SUCCESS} Source  :{red} {s['source']}{white}
 {SUCCESS} Found   :{red} {s['found']}{white}
 {SUCCESS} Fields  :{red} {s['fields']}{white}
 {SUCCESS} Sources :{red} {s['sources']}{white}
""")
    else:
        print(f"{SUCCESS} No breaches found!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)