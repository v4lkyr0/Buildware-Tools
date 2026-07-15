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
    import tkinter as tk
    from tkintermapview import TkinterMapView
except Exception as e:
    MissingModule(e)


def ShowMapWindow(lat, lon, ip):
    window = tk.Tk()
    window.title(f"{name_tool} v{version_tool} - [Map]")
    window.geometry("900x650")
    window.configure(bg="#000000")

    try:
        window.iconbitmap(os.path.join(tool_path, 'Programs', 'Images', 'BuildwareIcon.ico'))
    except Exception:
        pass

    map_widget = TkinterMapView(window, width=900, height=650, corner_radius=0)
    map_widget.pack(fill="both", expand=True)

    map_widget.set_tile_server(
        "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
        max_zoom=22
    )

    map_widget.set_position(lat, lon)
    map_widget.set_zoom(13)
    map_widget.set_marker(lat, lon, text=ip)

    window.mainloop()


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

            Scroll(f"""
 {SUCCESS} Ip          :{red} {data.get('query',      'None')}{white}
 {SUCCESS} Country     :{red} {data.get('country',    'None')} ({data.get('countryCode', 'None')}){white}
 {SUCCESS} Region      :{red} {data.get('regionName', 'None')}{white}
 {SUCCESS} City        :{red} {data.get('city',       'None')}{white}
 {SUCCESS} Zip         :{red} {data.get('zip',        'None')}{white}
 {SUCCESS} Latitude    :{red} {lat}{white}
 {SUCCESS} Longitude   :{red} {lon}{white}
 {SUCCESS} Timezone    :{red} {data.get('timezone',   'None')}{white}
 {SUCCESS} Isp         :{red} {data.get('isp',        'None')}{white}
 {SUCCESS} Org         :{red} {data.get('org',        'None')}{white}
 {SUCCESS} As          :{red} {data.get('as',         'None')}{white}
 {SUCCESS} As Name     :{red} {data.get('asname',     'None')}{white}
 {SUCCESS} Reverse Dns :{red} {data.get('reverse',    'None')}{white}
 {SUCCESS} Type        :{red} {proxy_str}{white}
""")

            if lat != "None" and lon != "None":
                try:
                    print(f"{LOADING} Opening map..", reset)
                    ShowMapWindow(float(lat), float(lon), data.get('query', resolved))
                except Exception as e:
                    print(f"{ERROR} Could not open map:{red} {e}", reset)

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