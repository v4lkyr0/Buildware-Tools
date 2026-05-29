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
    import urllib.parse
    import html
except Exception as e:
    MissingModule(e)

Title("Text Encoder/Decoder")

Scroll(GradientBanner(utilities_banner))

try:
    Scroll(f"""
 {PREFIX}01{SUFFIX} Base64
 {PREFIX}02{SUFFIX} Url
 {PREFIX}03{SUFFIX} Html
 {PREFIX}04{SUFFIX} Hex
 {PREFIX}05{SUFFIX} Binary
 {PREFIX}06{SUFFIX} Rot13
""")

    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    if choice not in ["1", "2", "3", "4", "5", "6"]:
        ErrorChoice()

    Scroll(f"""
 {PREFIX}01{SUFFIX} Encode
 {PREFIX}02{SUFFIX} Decode
""")

    mode = input(f"{INPUT} Mode {red}->{reset} ").strip().lstrip("0")

    if mode not in ["1", "2"]:
        ErrorMode()

    text = input(f"{INPUT} Text {red}->{reset} ").strip()

    if not text:
        ErrorInput()

    print(f"{LOADING} Processing..", reset)

    result = None

    if choice == "1":
        if mode == "1":
            result = base64.b64encode(text.encode()).decode()
        else:
            try:
                result = base64.b64decode(text.encode()).decode()
            except Exception:
                print(f"{ERROR} Invalid Base64!", reset)
                Continue()
                Reset()

    elif choice == "2":
        if mode == "1":
            result = urllib.parse.quote(text)
        else:
            result = urllib.parse.unquote(text)

    elif choice == "3":
        if mode == "1":
            result = html.escape(text)
        else:
            result = html.unescape(text)

    elif choice == "4":
        if mode == "1":
            result = text.encode().hex()
        else:
            try:
                result = bytes.fromhex(text).decode()
            except Exception:
                print(f"{ERROR} Invalid Hex!", reset)
                Continue()
                Reset()

    elif choice == "5":
        if mode == "1":
            result = " ".join(format(ord(c), "08b") for c in text)
        else:
            try:
                result = "".join(chr(int(b, 2)) for b in text.split())
            except Exception:
                print(f"{ERROR} Invalid Binary!", reset)
                Continue()
                Reset()

    elif choice == "6":
        import codecs
        result = codecs.encode(text, "rot_13")

    if result is not None:
        print(f"{SUCCESS} Result:{red} {result}", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)