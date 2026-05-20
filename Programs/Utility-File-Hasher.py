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
    import hashlib
    import os
except Exception as e:
    MissingModule(e)

Title("File Hasher")

Scroll(GradientBanner(utilities_banner))

try:
    file_path = BrowseFile("Select File")

    if not file_path:
        ErrorInput()

    if not os.path.exists(file_path):
        print(f"{ERROR} File not found!", reset)
        Continue()
        Reset()

    print(f"{LOADING} Hashing..", reset)

    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except Exception:
        print(f"{ERROR} Could not read file!", reset)
        Continue()
        Reset()

    md5    = hashlib.md5(data).hexdigest()
    sha1   = hashlib.sha1(data).hexdigest()
    sha256 = hashlib.sha256(data).hexdigest()
    sha512 = hashlib.sha512(data).hexdigest()

    size   = os.path.getsize(file_path)
    size_str = f"{round(size / 1024 / 1024, 2)} MB" if size >= 1024 * 1024 else f"{round(size / 1024, 2)} KB"

    Scroll(f"""
 {SUCCESS} File   :{red} {os.path.basename(file_path)}{white}
 {SUCCESS} Size   :{red} {size_str}{white}
 {SUCCESS} Md5    :{red} {md5}{white}
 {SUCCESS} Sha1   :{red} {sha1}{white}
 {SUCCESS} Sha256 :{red} {sha256}{white}
 {SUCCESS} Sha512 :{red} {sha512}{white}
""")

    Continue()
    Reset()

except Exception as e:
    Error(e)