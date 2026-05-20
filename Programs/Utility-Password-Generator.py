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
    import random
    import string
    import secrets
except Exception as e:
    MissingModule(e)

Title("Password Generator")

Scroll(GradientBanner(utilities_banner))

try:
    try:
        length = int(input(f"{INPUT} Length {red}->{reset} ").strip())
        if length < 1:
            ErrorNumber()
        if length > 2048:
            length = 2048
    except ValueError:
        ErrorNumber()

    Scroll(f"""
 {PREFIX}01{SUFFIX} Letters Only
 {PREFIX}02{SUFFIX} Letters & Numbers
 {PREFIX}03{SUFFIX} Letters, Numbers & Symbols
""")

    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    if choice == "1":
        chars = string.ascii_letters
    elif choice == "2":
        chars = string.ascii_letters + string.digits
    elif choice == "3":
        chars = string.ascii_letters + string.digits + string.punctuation
    else:
        ErrorChoice()

    password = "".join(secrets.choice(chars) for _ in range(length))

    print(f"{SUCCESS} Password:{red} {password}", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)