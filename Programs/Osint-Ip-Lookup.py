# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
except Exception as e:
    MissingModule(e)

Title("Osint Ip Lookup")
Connection()

try:
    ip = input(f"{INPUT} Ip Address {red}->{reset} ").strip()
    if not ip:
        ErrorInput()

    print(f"{LOADING} Looking Up Ip Address..", reset)

    response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,continent,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,hosting,query", timeout=10)
    data = response.json()

    if data.get("status") != "success":
        print(f"{ERROR} Lookup failed!", reset)
        Continue()
        Reset()

    Scroll(f"""
 {INFO} Ip Address               :{red} {data.get('query', 'N/A')}
 {INFO} Continent                :{red} {data.get('continent', 'N/A')}
 {INFO} Country                  :{red} {data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')})
 {INFO} Region                   :{red} {data.get('regionName', 'N/A')}
 {INFO} City                     :{red} {data.get('city', 'N/A')}
 {INFO} Zip Code                 :{red} {data.get('zip', 'N/A')}
 {INFO} Latitude                 :{red} {data.get('lat', 'N/A')}
 {INFO} Longitude                :{red} {data.get('lon', 'N/A')}
 {INFO} Timezone                 :{red} {data.get('timezone', 'N/A')}
 {INFO} Isp                      :{red} {data.get('isp', 'N/A')}
 {INFO} Organization             :{red} {data.get('org', 'N/A')}
 {INFO} As Number                :{red} {data.get('as', 'N/A')}
 {INFO} As Name                  :{red} {data.get('asname', 'N/A')}
 {INFO} Reverse Dns              :{red} {data.get('reverse', 'N/A')}
 {INFO} Mobile Connection        :{red} {data.get('mobile', 'N/A')}
 {INFO} Proxy / Vpn              :{red} {data.get('proxy', 'N/A')}
 {INFO} Hosting / Datacenter     :{red} {data.get('hosting', 'N/A')}
""")

    Continue()
    Reset()

except Exception as e:
    Error(e)
