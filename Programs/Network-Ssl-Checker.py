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
    import ssl
    import socket
    from datetime import datetime, timezone
except Exception as e:
    MissingModule(e)

Title("Ssl Checker")

Scroll(GradientBanner(network_banner))

try:
    target = input(f"{INPUT} Domain {red}->{reset} ").strip()

    if not target:
        ErrorInput()

    target = target.removeprefix("https://").removeprefix("http://").rstrip("/")

    try:
        resolved = socket.gethostbyname(target)
    except Exception:
        print(f"{ERROR} Could not resolve domain!", reset)
        Continue()
        Reset()

    print(f"{LOADING} Checking..", reset)

    try:
        context = ssl.create_default_context()
        conn    = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=target)
        conn.settimeout(10)
        conn.connect((resolved, 443))
        cert        = conn.getpeercert()
        cipher      = conn.cipher()
        tls_version = conn.version()

        try:
            conn.close()
        except Exception:
            pass

        subject    = dict(x[0] for x in cert["subject"])
        issuer     = dict(x[0] for x in cert["issuer"])
        valid_from = cert["notBefore"]
        valid_to   = cert["notAfter"]
        version    = cert["version"]
        serial     = cert.get("serialNumber", "None")
        san        = cert.get("subjectAltName", [])
        san_list   = ", ".join([v for _, v in san]) if san else "None"

        try:
            valid_to_dt = datetime.strptime(valid_to, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
            days_left   = (valid_to_dt - datetime.now(timezone.utc)).days
            expiry_str  = f"{valid_to} ({days_left} days left)"
        except Exception:
            expiry_str = valid_to

        Scroll(f"""
 {SUCCESS} Common Name  :{red} {subject.get('commonName',       'None')}{white}
 {SUCCESS} Organization :{red} {subject.get('organizationName', 'None')}{white}
 {SUCCESS} Issuer       :{red} {issuer.get('organizationName',  'None')}{white}
 {SUCCESS} Issuer CN    :{red} {issuer.get('commonName',        'None')}{white}
 {SUCCESS} Valid From   :{red} {valid_from}{white}
 {SUCCESS} Valid To     :{red} {expiry_str}{white}
 {SUCCESS} Version      :{red} {version}{white}
 {SUCCESS} Serial       :{red} {serial}{white}
 {SUCCESS} Tls Version  :{red} {tls_version}{white}
 {SUCCESS} Cipher       :{red} {cipher[0] if cipher else 'None'}{white}
 {SUCCESS} San          :{red} {san_list[:150]}{white}
""")

    except ssl.SSLCertVerificationError as e:
        print(f"{ERROR} Certificate verification failed:{red} {e}", reset)
    except ssl.SSLError as e:
        print(f"{ERROR} Ssl error:{red} {e}", reset)
    except ConnectionRefusedError:
        print(f"{ERROR} Port 443 is closed!", reset)
    except socket.timeout:
        print(f"{ERROR} Connection timed out!", reset)
    except Exception:
        print(f"{ERROR} Could not retrieve Ssl certificate!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)