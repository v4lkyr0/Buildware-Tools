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
    import re
except Exception as e:
    MissingModule(e)

Title("Hash Identifier")

Scroll(GradientBanner(utilities_banner))

try:
    hash_input = input(f"{INPUT} Hash {red}->{reset} ").strip()

    if not hash_input:
        ErrorInput()

    print(f"{LOADING} Identifying..", reset)

    def IdentifyHash(h):
        length     = len(h)
        results    = []
        only_hex   = bool(re.fullmatch(r"[0-9a-fA-F]+", h))
        only_b64   = bool(re.fullmatch(r"[A-Za-z0-9+/=]+", h))
        has_dollar = h.startswith("$")
        has_colon  = ":" in h

        if has_dollar:
            if h.startswith("$2a$") or h.startswith("$2b$") or h.startswith("$2y$"):
                results.append(("Bcrypt",       "High"))
            if h.startswith("$1$"):
                results.append(("Md5 Crypt",    "Medium"))
            if h.startswith("$5$"):
                results.append(("Sha256 Crypt", "Medium"))
            if h.startswith("$6$"):
                results.append(("Sha512 Crypt", "High"))
            if h.startswith("$apr1$"):
                results.append(("Apr1 Md5",     "Medium"))
            if h.startswith("$argon2"):
                results.append(("Argon2",       "High"))
            if h.startswith("$pbkdf2"):
                results.append(("Pbkdf2",       "High"))
            if results:
                return results

        if has_colon and only_hex:
            results.append(("Ntlm (with username)", "Medium"))

        if only_hex:
            if length == 8:
                results.append(("Crc32",            "Low"))
            elif length == 13:
                results.append(("Des",              "Low"))
            elif length == 16:
                results.append(("Md5 (half)",       "Low"))
            elif length == 32:
                results.append(("Md5",              "Low"))
                results.append(("Ntlm",             "Low"))
                results.append(("Md4",              "Low"))
                results.append(("Ripemd128",        "Low"))
            elif length == 40:
                results.append(("Sha1",             "Low"))
                results.append(("Sha0",             "Low"))
                results.append(("Ripemd160",        "Low"))
                results.append(("Haval160",         "Low"))
            elif length == 48:
                results.append(("Tiger192",         "Medium"))
                results.append(("Haval192",         "Medium"))
            elif length == 56:
                results.append(("Sha224",           "Medium"))
                results.append(("Haval224",         "Medium"))
            elif length == 64:
                results.append(("Sha256",           "Medium"))
                results.append(("Ripemd256",        "Medium"))
                results.append(("Haval256",         "Medium"))
                results.append(("Blake2s",          "Medium"))
                results.append(("Sha3-256",         "Medium"))
            elif length == 96:
                results.append(("Sha384",           "High"))
                results.append(("Haval384",         "High"))
                results.append(("Sha3-384",         "High"))
            elif length == 128:
                results.append(("Sha512",           "High"))
                results.append(("Whirlpool",        "High"))
                results.append(("Blake2b",          "High"))
                results.append(("Sha3-512",         "High"))
                results.append(("Ripemd512",        "High"))

        if only_b64 and not only_hex:
            if length == 44:
                results.append(("Sha256 (base64)",  "Medium"))
            elif length == 88:
                results.append(("Sha512 (base64)",  "High"))
            elif length == 24:
                results.append(("Md5 (base64)",     "Low"))

        return results

    matches = IdentifyHash(hash_input)
    length  = len(hash_input)

    if matches:
        print()
        for name, confidence in matches:
            print(f"{SUCCESS} Type:{red} {name:<22}{white} | Confidence:{red} {confidence:<8}{white} | Length:{red} {length}", reset)
    else:
        print(f"{INFO} Type:{red} {'Unknown':<22}{white} | Length:{red} {length}", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)