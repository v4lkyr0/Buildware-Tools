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
    import re
except Exception as e:
    MissingModule(e)

Title("Mac Lookup")

Scroll(GradientBanner(network_banner))

try:
    mac = input(f"{INPUT} Mac Address {red}->{reset} ").strip()

    if not mac:
        ErrorInput()

    mac_clean = re.sub(r"[^0-9a-fA-F]", "", mac)
    if len(mac_clean) < 6:
        print(f"{ERROR} Invalid Mac Address!", reset)
        Continue()
        Reset()

    print(f"{LOADING} Looking up..", reset)

    try:
        response = requests.get(
            f"https://api.macvendors.com/{mac}",
            headers = {"User-Agent": RandomUserAgents()},
            timeout = 10
        )

        if response.status_code == 200:
            Scroll(f"""
 {SUCCESS} Mac Address :{red} {mac}{white}
 {SUCCESS} Vendor      :{red} {response.text.strip()}{white}
""")
        elif response.status_code == 404:
            print(f"{ERROR} Mac Address not found!", reset)
        elif response.status_code == 429:
            print(f"{ERROR} Rate limited!", reset)
        elif response.status_code == 422:
            print(f"{ERROR} Invalid Mac Address format!", reset)
        else:
            print(f"{ERROR} Could not look up Mac Address! {red}({white}status: {response.status_code}{red})", reset)

    except requests.exceptions.Timeout:
        print(f"{ERROR} Request timed out!", reset)
    except requests.exceptions.ConnectionError:
        print(f"{ERROR} Could not connect to api!", reset)
    except Exception:
        print(f"{ERROR} Could not look up Mac Address!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)