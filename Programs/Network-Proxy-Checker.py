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
    import time
except Exception as e:
    MissingModule(e)

Title("Proxy Checker")

Scroll(GradientBanner(network_banner))

try:
    proxy = input(f"{INPUT} Proxy {red}->{reset} ").strip()

    if not proxy:
        ErrorInput()

    if "://" in proxy:
        proxy = proxy.split("://", 1)[1]

    Scroll(f"""
 {PREFIX}01{SUFFIX} Http
 {PREFIX}02{SUFFIX} Https
 {PREFIX}03{SUFFIX} Socks4
 {PREFIX}04{SUFFIX} Socks5
""")

    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    protocols = {
        "1": "http",
        "2": "https",
        "3": "socks4",
        "4": "socks5",
    }

    if choice not in protocols:
        ErrorChoice()

    protocol = protocols[choice]

    print(f"{LOADING} Checking..", reset)

    try:
        proxies  = {protocol: f"{protocol}://{proxy}"}
        start    = time.time()
        response = requests.get(
            "https://api.ipify.org?format=json",
            proxies = proxies,
            timeout = 10
        )
        latency = round((time.time() - start) * 1000)

        if response.status_code == 200:
            ip  = response.json().get("ip", "None")
            geo = {}

            try:
                geo_response = requests.get(
                    f"http://ip-api.com/json/{ip}",
                    timeout = 5
                )
                if geo_response.status_code == 200:
                    geo = geo_response.json()
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.ConnectionError:
                pass
            except Exception:
                pass

            Scroll(f"""
 {SUCCESS} Status   :{red} Valid{white}
 {SUCCESS} Protocol :{red} {protocol.capitalize()}{white}
 {SUCCESS} Proxy    :{red} {proxy}{white}
 {SUCCESS} Ip       :{red} {ip}{white}
 {SUCCESS} Latency  :{red} {latency} ms{white}
 {SUCCESS} Country  :{red} {geo.get('country', 'None')}{white}
 {SUCCESS} City     :{red} {geo.get('city',    'None')}{white}
 {SUCCESS} Isp      :{red} {geo.get('isp',     'None')}{white}
""")
        else:
            print(f"{ERROR} Proxy invalid! {red}({white}status: {response.status_code}{red})", reset)

    except requests.exceptions.Timeout:
        print(f"{ERROR} Proxy timed out!", reset)
    except requests.exceptions.ProxyError:
        print(f"{ERROR} Proxy connection failed!", reset)
    except requests.exceptions.ConnectionError:
        print(f"{ERROR} Proxy connection refused!", reset)
    except Exception:
        print(f"{ERROR} Proxy invalid!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)