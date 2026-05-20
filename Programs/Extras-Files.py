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
    import os
    import subprocess
except Exception as e:
    MissingModule(e)

Title("Extras Files")

Scroll(GradientBanner(extras_banner))

try:
    extras_path = os.path.join(tool_path, "Programs", "Extras")

    Scroll(f"""
 {PREFIX}01{SUFFIX} Data File
 {PREFIX}02{SUFFIX} Extras Folder
""")

    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    if choice == "1":
        file_path = os.path.join(extras_path, "Config.json")
        file_name = "Config.json"
        print(f"{INFO} Contains webhooks, tokens, bots and settings.", reset)
    elif choice == "2":
        file_path = extras_path
        file_name = "Extras Folder"
    else:
        ErrorChoice()

    if not os.path.exists(file_path):
        print(f"{ERROR} {file_name} not found!", reset)
        Continue()
        Reset()

    print(f"{LOADING} Opening..", reset)

    try:
        if platform_pc == "Windows":
            os.startfile(file_path)
        else:
            subprocess.Popen(["xdg-open", file_path])
        print(f"{SUCCESS} {file_name} opened!", reset)
    except Exception:
        print(f"{ERROR} Could not open {file_name}!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)