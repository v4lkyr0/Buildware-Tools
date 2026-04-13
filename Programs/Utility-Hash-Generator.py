# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import hashlib
except Exception as e:
    MissingModule(e)

Title("Utility Hash Generator")

try:
    text = input(f"{INPUT} Text to Hash {red}->{reset} ").strip()
    if not text:
        ErrorInput()

    text_bytes = text.encode('utf-8')

    hashes = {
        "MD5":       hashlib.md5(text_bytes).hexdigest(),
        "SHA-1":     hashlib.sha1(text_bytes).hexdigest(),
        "SHA-224":   hashlib.sha224(text_bytes).hexdigest(),
        "SHA-256":   hashlib.sha256(text_bytes).hexdigest(),
        "SHA-384":   hashlib.sha384(text_bytes).hexdigest(),
        "SHA-512":   hashlib.sha512(text_bytes).hexdigest(),
    }

    try:
        hashes["SHA3-256"] = hashlib.sha3_256(text_bytes).hexdigest()
        hashes["SHA3-512"] = hashlib.sha3_512(text_bytes).hexdigest()
    except:
        pass

    try:
        hashes["BLAKE2b"] = hashlib.blake2b(text_bytes).hexdigest()
        hashes["BLAKE2s"] = hashlib.blake2s(text_bytes).hexdigest()
    except:
        pass

    output = f"\n {INFO} Input :{red} {text}{reset}\n"

    for name, value in hashes.items():
        output += f" {SUCCESS} {name:12s}:{red} {value}{reset}\n"

    Scroll(output)

    Continue()
    Reset()

except Exception as e:
    Error(e)
