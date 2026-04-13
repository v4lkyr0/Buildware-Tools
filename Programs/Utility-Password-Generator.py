# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import string
    import random
except Exception as e:
    MissingModule(e)

Title("Utility Password Generator")

try:
    length = input(f"{INPUT} Password Length {red}->{reset} ").strip()
    length = int(length) if length.isdigit() else 16

    if length < 4 or length > 256:
        print(f"{ERROR} Length must be between 4 and 256!", reset)
        Continue()
        Reset()

    count = input(f"{INPUT} Number of Passwords {red}->{reset} ").strip()
    count = int(count) if count.isdigit() else 1

    if count < 1 or count > 100:
        ErrorNumber()

    Scroll(f"""
 {PREFIX}01{SUFFIX} All Characters (letters + digits + symbols)
 {PREFIX}02{SUFFIX} Letters + Digits
 {PREFIX}03{SUFFIX} Letters Only
 {PREFIX}04{SUFFIX} Digits Only
 {PREFIX}05{SUFFIX} Hex (0-9, a-f)
""")
    mode = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    if mode == "1":
        charset = string.ascii_letters + string.digits + string.punctuation
    elif mode == "2":
        charset = string.ascii_letters + string.digits
    elif mode == "3":
        charset = string.ascii_letters
    elif mode == "4":
        charset = string.digits
    elif mode == "5":
        charset = string.hexdigits[:16]
    else:
        ErrorChoice()

    output = f"\n {INFO} Generated Password(s):\n"

    pad = len(str(count))
    passwords = []
    for i in range(count):
        password = ''.join(random.SystemRandom().choice(charset) for _ in range(length))
        passwords.append(password)
        output += f" {PREFIX}{str(i+1).zfill(pad)}{SUFFIX} {red}{password}{reset}\n"

    pwd = passwords[0]
    has_upper = any(c.isupper() for c in pwd)
    has_lower = any(c.islower() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_special = any(c in string.punctuation for c in pwd)
    complexity = sum([has_upper, has_lower, has_digit, has_special])

    if length >= 16 and complexity >= 3:
        strength = "Very Strong"
    elif length >= 12 and complexity >= 3:
        strength = "Strong"
    elif length >= 8 and complexity >= 2:
        strength = "Moderate"
    else:
        strength = "Weak"

    output += f"\n {INFO} Strength Analysis:\n"
    output += f" {INFO} Length:{red} {length} {white}| Uppercase:{red} {has_upper} {white}| Lowercase:{red} {has_lower} {white}| Digits:{red} {has_digit} {white}| Symbols:{red} {has_special}{reset}\n"
    output += f" {INFO} Strength:{red} {strength}{reset}\n"

    Scroll(output)

    Continue()
    Reset()

except Exception as e:
    Error(e)
