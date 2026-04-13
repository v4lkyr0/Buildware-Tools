# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import re
    import socket
    import requests
except Exception as e:
    MissingModule(e)

Title("Osint Email Checker")
Connection()

disposable_domains = [
    "tempmail.com", "guerrillamail.com", "mailinator.com", "throwaway.email",
    "yopmail.com", "sharklasers.com", "guerrillamailblock.com", "grr.la",
    "dispostable.com", "trashmail.com", "10minutemail.com", "tempail.com",
    "fakeinbox.com", "mailnesia.com", "maildrop.cc", "discard.email",
    "temp-mail.org", "mohmal.com", "emailondeck.com", "crazymailing.com",
    "1secmail.com", "1secmail.org", "1secmail.net", "getnada.com"
]

try:
    email = input(f"{INPUT} Email Address {red}->{reset} ").strip()
    if not email:
        ErrorInput()

    print(f"{LOADING} Checking Email Address..", reset)

    email_regex = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    valid_format = bool(re.match(email_regex, email))

    local_part, domain = email.rsplit('@', 1) if '@' in email else (email, "")

    mx_record = "Not Found"
    has_mx = False
    if domain:
        try:
            mx_hosts = socket.getaddrinfo(domain, 25, socket.AF_INET, socket.SOCK_STREAM)
            if mx_hosts:
                mx_record = mx_hosts[0][4][0]
                has_mx = True
        except:
            pass

        if not has_mx:
            try:
                socket.gethostbyname(domain)
                mx_record = "Domain resolves (no MX port 25)"
                has_mx = True
            except:
                mx_record = "Domain does not resolve"

    is_disposable = domain.lower() in disposable_domains

    if valid_format and has_mx and not is_disposable:
        status = "Likely Valid"
    elif valid_format and has_mx and is_disposable:
        status = "Disposable Email"
    elif valid_format and not has_mx:
        status = "Domain Not Found"
    else:
        status = "Invalid Format"

    Scroll(f"""
 {INFO} Email Address            :{red} {email}
 {INFO} Valid Format             :{red} {valid_format}
 {INFO} Local Part               :{red} {local_part}
 {INFO} Domain                   :{red} {domain}
 {INFO} MX Record                :{red} {mx_record}
 {INFO} Disposable Email         :{red} {is_disposable}
 {INFO} Status                   :{red} {status}
""")

    Continue()
    Reset()

except Exception as e:
    Error(e)
