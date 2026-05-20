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
    import whois
except Exception as e:
    MissingModule(e)

Title("Whois Lookup")

Scroll(GradientBanner(osint_banner))

try:
    target = input(f"{INPUT} Domain {red}->{reset} ").strip()

    if not target:
        ErrorInput()

    target = target.removeprefix("https://").removeprefix("http://").rstrip("/")

    print(f"{LOADING} Looking up..", reset)

    def Clean(value):
        if not value:
            return "None"
        if isinstance(value, list):
            unique = list(dict.fromkeys([str(v).strip() for v in value if v]))
            return ", ".join(unique[:3]) + (" ..." if len(unique) > 3 else "")
        return str(value).strip() or "None"

    try:
        data = whois.whois(target)

        if not data or not data.domain_name:
            print(f"{ERROR} Could not fetch Whois information!", reset)
            Continue()
            Reset()

        name_servers = data.name_servers
        if isinstance(name_servers, (list, set)):
            name_servers = ", ".join(sorted(set(str(n).lower() for n in name_servers if n)))
        else:
            name_servers = str(name_servers) if name_servers else "None"

        Scroll(f"""
 {SUCCESS} Domain       :{red} {Clean(data.domain_name)}{white}
 {SUCCESS} Registrar    :{red} {Clean(data.registrar)}{white}
 {SUCCESS} Created      :{red} {Clean(data.creation_date)}{white}
 {SUCCESS} Expires      :{red} {Clean(data.expiration_date)}{white}
 {SUCCESS} Updated      :{red} {Clean(data.updated_date)}{white}
 {SUCCESS} Status       :{red} {Clean(data.status)}{white}
 {SUCCESS} Name Servers :{red} {name_servers}{white}
 {SUCCESS} Emails       :{red} {Clean(data.emails)}{white}
 {SUCCESS} Country      :{red} {Clean(data.country)}{white}
 {SUCCESS} State        :{red} {Clean(data.state)}{white}
 {SUCCESS} City         :{red} {Clean(data.city)}{white}
 {SUCCESS} Org          :{red} {Clean(data.org)}{white}
 {SUCCESS} Address      :{red} {Clean(data.address)}{white}
 {SUCCESS} Zipcode      :{red} {Clean(data.zipcode)}{white}
 {SUCCESS} Dnssec       :{red} {Clean(data.dnssec)}{white}
 {SUCCESS} Whois Server :{red} {Clean(data.whois_server)}{white}
""")

    except whois.parser.PywhoisError as e:
        print(f"{ERROR} Whois error:{red} {e}", reset)
    except ConnectionResetError:
        print(f"{ERROR} Connection reset by Whois server!", reset)
    except Exception:
        print(f"{ERROR} Could not fetch Whois information!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)