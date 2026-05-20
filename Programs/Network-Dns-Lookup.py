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
    import dns.resolver
    import socket
except Exception as e:
    MissingModule(e)

Title("Dns Lookup")

Scroll(GradientBanner(network_banner))

try:
    target = input(f"{INPUT} Domain {red}->{reset} ").strip()

    if not target:
        ErrorInput()

    target = target.removeprefix("https://").removeprefix("http://").rstrip("/")

    try:
        resolved = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"{ERROR} Could not resolve domain!", reset)
        Continue()
        Reset()

    print(f"{INFO} Resolved:{red} {resolved}", reset)
    print(f"{LOADING} Looking up..", reset)

    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "PTR", "SRV", "CAA", "DMARC", "SPF"]

    found      = False
    found_by   = {}

    for record_type in record_types:
        try:
            query   = f"_dmarc.{target}" if record_type == "DMARC" else target
            rtype   = "TXT" if record_type in ("DMARC", "SPF") else record_type
            answers = dns.resolver.resolve(query, rtype, lifetime=5)
            for answer in answers:
                text = answer.to_text()
                if record_type == "SPF" and "v=spf" not in text.lower():
                    continue
                print(f"{SUCCESS} {record_type:<8}{red}|{white} {text}", reset)
                found_by[record_type] = found_by.get(record_type, 0) + 1
                found = True
        except dns.resolver.NXDOMAIN:
            pass
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.Timeout:
            pass
        except Exception:
            pass

    if not found:
        print(f"{ERROR} No records found!", reset)
    else:
        total = sum(found_by.values())
        print(f"\n{SUCCESS} Found:{red} {total} record(s) across {len(found_by)} types", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)