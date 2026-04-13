# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import re
except Exception as e:
    MissingModule(e)

Title("Utility Hash Identifier")

hash_patterns = [
    (r'^[a-fA-F0-9]{32}$', ["MD5", "NTLM", "MD4"]),
    (r'^[a-fA-F0-9]{40}$', ["SHA-1", "RIPEMD-160"]),
    (r'^[a-fA-F0-9]{56}$', ["SHA-224", "SHA3-224"]),
    (r'^[a-fA-F0-9]{64}$', ["SHA-256", "SHA3-256", "BLAKE2s"]),
    (r'^[a-fA-F0-9]{96}$', ["SHA-384", "SHA3-384"]),
    (r'^[a-fA-F0-9]{128}$', ["SHA-512", "SHA3-512", "BLAKE2b", "Whirlpool"]),
    (r'^\$2[aby]?\$\d{1,2}\$.{53}$', ["bcrypt"]),
    (r'^\$6\$.*\$[./a-zA-Z0-9]{86}$', ["SHA-512 Crypt (Unix)"]),
    (r'^\$5\$.*\$[./a-zA-Z0-9]{43}$', ["SHA-256 Crypt (Unix)"]),
    (r'^\$1\$.*\$[./a-zA-Z0-9]{22}$', ["MD5 Crypt (Unix)"]),
    (r'^[a-fA-F0-9]{16}$', ["MySQL (old)", "Half MD5", "DES"]),
    (r'^\*[a-fA-F0-9]{40}$', ["MySQL 4.1+"]),
    (r'^[a-fA-F0-9]{8}$', ["CRC-32", "Adler-32"]),
    (r'^pbkdf2', ["PBKDF2"]),
    (r'^scrypt:', ["scrypt"]),
    (r'^\$argon2', ["Argon2"]),
]

try:
    hash_input = input(f"{INPUT} Hash {red}->{reset} ").strip()
    if not hash_input:
        ErrorInput()

    output = ""
    output += f"\n {INFO} Hash   :{red} {hash_input}{reset}\n"
    output += f" {INFO} Length :{red} {len(hash_input)} characters{reset}\n"

    matches = []
    for pattern, algorithms in hash_patterns:
        if re.match(pattern, hash_input):
            matches.extend(algorithms)

    if matches:
        pad = len(str(len(matches)))
        output += f" {INFO} Possible hash type(s):\n"
        for i, algo in enumerate(matches, 1):
            output += f" {PREFIX}{str(i).zfill(pad)}{SUFFIX} {red}{algo}{reset}\n"
    else:
        output += f" {ERROR} Could not identify hash type!{reset}\n"
        output += f" {INFO} The hash may be custom, encoded, or truncated.{reset}\n"

    is_hex = all(c in '0123456789abcdefABCDEF' for c in hash_input.replace('$', '').replace('.', '').replace('/', '').replace('*', ''))
    has_upper = any(c.isupper() for c in hash_input)
    has_lower = any(c.islower() for c in hash_input)
    has_special = any(c in '$./!*' for c in hash_input)

    output += f"\n {INFO} Analysis:\n"
    output += f" {INFO} Hex Characters Only :{red} {is_hex}{reset}\n"
    output += f" {INFO} Contains Uppercase  :{red} {has_upper}{reset}\n"
    output += f" {INFO} Contains Lowercase  :{red} {has_lower}{reset}\n"
    output += f" {INFO} Contains Special    :{red} {has_special}{reset}\n"

    Scroll(output)

    Continue()
    Reset()

except Exception as e:
    Error(e)
