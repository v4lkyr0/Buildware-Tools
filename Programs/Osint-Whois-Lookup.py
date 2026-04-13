# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    from datetime import datetime
except Exception as e:
    MissingModule(e)

Title("Osint Whois Lookup")
Connection()

try:
    domain = input(f"{INPUT} Domain {red}->{reset} ").strip().lower()
    if not domain:
        ErrorInput()

    domain = domain.replace("http://", "").replace("https://", "").split("/")[0]

    print(f"{LOADING} Looking Up Whois Data..", reset)

    response = requests.get(f"https://rdap.org/domain/{domain}", timeout=15)

    if response.status_code != 200:
        print(f"{ERROR} Could not retrieve WHOIS data for this domain!", reset)
        Continue()
        Reset()

    data = response.json()

    name = data.get("ldhName", data.get("name", "N/A"))
    handle = data.get("handle", "N/A")
    status = ", ".join(data.get("status", [])) or "N/A"

    registrar = "N/A"
    for entity in data.get("entities", []):
        roles = entity.get("roles", [])
        if "registrar" in roles:
            vcard = entity.get("vcardArray", [None, []])
            if len(vcard) > 1:
                for field in vcard[1]:
                    if field[0] == "fn":
                        registrar = field[3]
                        break

    nameservers = []
    for ns in data.get("nameservers", []):
        ns_name = ns.get("ldhName", "")
        if ns_name:
            nameservers.append(ns_name)

    events_info = {}
    for event in data.get("events", []):
        action = event.get("eventAction", "")
        date = event.get("eventDate", "")
        if date:
            try:
                dt = datetime.fromisoformat(date.replace("Z", "+00:00"))
                date = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
            except:
                pass
        events_info[action] = date

    Scroll(f"""
 {INFO} Domain Name              :{red} {name}
 {INFO} Handle                   :{red} {handle}
 {INFO} Status                   :{red} {status}
 {INFO} Registrar                :{red} {registrar}
 {INFO} Registration Date        :{red} {events_info.get('registration', 'N/A')}
 {INFO} Last Updated             :{red} {events_info.get('last changed', events_info.get('last update of RDAP database', 'N/A'))}
 {INFO} Expiration Date          :{red} {events_info.get('expiration', 'N/A')}
 {INFO} Nameservers              :{red} {', '.join(nameservers) if nameservers else 'N/A'}
""")

    Continue()
    Reset()

except Exception as e:
    Error(e)
