# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import ssl
    import socket
    from datetime import datetime
except Exception as e:
    MissingModule(e)

Title("Network Ssl Checker")
Connection()

try:
    domain = input(f"{INPUT} Domain {red}->{reset} ").strip()
    if not domain:
        ErrorInput()

    domain = domain.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]

    print(f"{LOADING} Checking Ssl Certificate..", reset)

    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
    conn.settimeout(10)
    conn.connect((domain, 443))
    cert = conn.getpeercert()
    cipher = conn.cipher()
    version = conn.version()
    conn.close()

    subject = dict(x[0] for x in cert.get('subject', []))
    issuer = dict(x[0] for x in cert.get('issuer', []))

    not_before = cert.get('notBefore', 'N/A')
    not_after = cert.get('notAfter', 'N/A')

    try:
        expire_date = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
        days_left = (expire_date - datetime.now()).days
        if days_left > 30:
            expiry_status = f"{days_left} days remaining"
        elif days_left > 0:
            expiry_status = f"{days_left} days remaining (expiring soon)"
        else:
            expiry_status = f"EXPIRED ({abs(days_left)} days ago)"
    except:
        days_left = "N/A"
        expiry_status = "Could not calculate"

    san_list = []
    for san_type, san_value in cert.get('subjectAltName', []):
        san_list.append(san_value)

    serial = cert.get('serialNumber', 'N/A')

    Scroll(f"""
 {INFO} Domain                   :{red} {domain}
 {INFO} Common Name              :{red} {subject.get('commonName', 'N/A')}
 {INFO} Organization             :{red} {subject.get('organizationName', 'N/A')}
 {INFO} Issuer                   :{red} {issuer.get('organizationName', 'N/A')}
 {INFO} Issuer CN                :{red} {issuer.get('commonName', 'N/A')}
 {INFO} Serial Number            :{red} {serial}
 {INFO} Valid From               :{red} {not_before}
 {INFO} Valid Until              :{red} {not_after}
 {INFO} Expiry Status            :{red} {expiry_status}
 {INFO} Tls Version              :{red} {version}
 {INFO} Cipher Suite             :{red} {cipher[0] if cipher else 'N/A'}
 {INFO} Cipher Bits              :{red} {cipher[2] if cipher else 'N/A'}
 {INFO} Subject Alt Names        :{red} {', '.join(san_list[:10]) if san_list else 'N/A'}
""")

    if len(san_list) > 10:
        print(f" {INFO} ... and {len(san_list) - 10} more Sans", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)
