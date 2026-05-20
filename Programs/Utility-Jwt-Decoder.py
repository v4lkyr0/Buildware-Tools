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
    import base64
    import json
    from datetime import datetime, timezone
except Exception as e:
    MissingModule(e)

Title("Jwt Decoder")

Scroll(GradientBanner(utilities_banner))

def DecodeSegment(segment):
    padding = 4 - len(segment) % 4
    if padding != 4:
        segment += "=" * padding
    return json.loads(base64.urlsafe_b64decode(segment).decode())

def FormatValue(key, value):
    if key in ("exp", "iat", "nbf") and isinstance(value, int):
        try:
            dt = datetime.fromtimestamp(value, tz=timezone.utc)
            return f"{value} ({dt.strftime('%Y-%m-%d %H:%M:%S UTC')})"
        except Exception:
            pass
    return value

try:
    token = input(f"{INPUT} Token {red}->{reset} ").strip()

    if not token:
        ErrorInput()

    print(f"{LOADING} Decoding..", reset)

    parts = token.split(".")

    if len(parts) != 3:
        print(f"{ERROR} Invalid Jwt token!", reset)
        Continue()
        Reset()

    try:
        header  = DecodeSegment(parts[0])
        payload = DecodeSegment(parts[1])

        print(f"\n{SUCCESS} Header:", reset)
        for key, value in header.items():
            print(f"   {SUCCESS} {key:<16}{red} {FormatValue(key, value)}", reset)

        print(f"\n{SUCCESS} Payload:", reset)
        for key, value in payload.items():
            print(f"   {SUCCESS} {key:<16}{red} {FormatValue(key, value)}", reset)

        print(f"\n{SUCCESS} Signature:{red} {parts[2]}", reset)

    except Exception:
        print(f"{ERROR} Could not decode Jwt token!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)