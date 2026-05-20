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
except Exception as e:
    MissingModule(e)

Title("Ip Lookup")

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

    print(f"{LOADING} Looking up..", reset)

    try:
        response = requests.get(
            f"http://ip-api.com/json/{resolved}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,hosting,query",
            timeout = 10
        )

        if response.status_code == 429:
            print(f"{ERROR} Rate limited!", reset)
            Continue()
            Reset()

        data = response.json()

        if data.get("status") == "success":
            proxy_type = []
            if data.get("proxy"):
                proxy_type.append("Proxy")
            if data.get("hosting"):
                proxy_type.append("Hosting/VPN")
            if data.get("mobile"):
                proxy_type.append("Mobile")
            proxy_str = ", ".join(proxy_type) if proxy_type else "None"

            lat = data.get("lat", "None")
            lon = data.get("lon", "None")
            maps_url = f"https://www.google.com/maps?q={lat},{lon}" if lat != "None" and lon != "None" else "None"

            Scroll(f"""
 {SUCCESS} Ip          :{red} {data.get('query',      'None')}{white}
 {SUCCESS} Country     :{red} {data.get('country',    'None')} ({data.get('countryCode', 'None')}){white}
 {SUCCESS} Region      :{red} {data.get('regionName', 'None')}{white}
 {SUCCESS} City        :{red} {data.get('city',       'None')}{white}
 {SUCCESS} Zip         :{red} {data.get('zip',        'None')}{white}
 {SUCCESS} Latitude    :{red} {lat}{white}
 {SUCCESS} Longitude   :{red} {lon}{white}
 {SUCCESS} Google Maps :{red} {maps_url}{white}
 {SUCCESS} Timezone    :{red} {data.get('timezone',   'None')}{white}
 {SUCCESS} Isp         :{red} {data.get('isp',        'None')}{white}
 {SUCCESS} Org         :{red} {data.get('org',        'None')}{white}
 {SUCCESS} As          :{red} {data.get('as',         'None')}{white}
 {SUCCESS} As Name     :{red} {data.get('asname',     'None')}{white}
 {SUCCESS} Reverse Dns :{red} {data.get('reverse',    'None')}{white}
 {SUCCESS} Type        :{red} {proxy_str}{white}
""")
        else:
            msg = data.get("message", "None")
            print(f"{ERROR} Ip not found:{red} {msg}", reset)

    except requests.exceptions.Timeout:
        print(f"{ERROR} Request timed out!", reset)
    except requests.exceptions.ConnectionError:
        print(f"{ERROR} Could not connect to api!", reset)
    except Exception:
        print(f"{ERROR} Could not fetch Ip information!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)