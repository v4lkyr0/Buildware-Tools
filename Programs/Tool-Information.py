# Copyright (c) 2025-2026 v4lkyr0 — Buildware-Tools
# See the file 'LICENSE' for copying permission.
# --------------------------------------------------------
# EN: Non-commercial use only. Do not sell, remove credits
#     or redistribute without prior written permission.
# FR: Usage non-commercial uniquement. Ne pas vendre, supprimer
#     les crédits ou redistribuer sans autorisation écrite.

from Core.Utils import *
from Core.Config import *

Title("Tool Information")

Scroll(GradientBanner(information_banner))

try:
    Scroll(f"""
 {INFO} Tool Name :{red} {name_tool}{white}
 {INFO} Version   :{red} {version_tool}{white}
 {INFO} Author    :{red} {author_tool}{white}
 {INFO} Type      :{red} {type_tool}{white}
 {INFO} License   :{red} {license} ({license_url}){white}
 {INFO} GitHub    :{red} {github_url}{white}
 {INFO} Discord   :{red} {discord_url}{white}
 {INFO} Guns.lol  :{red} {gunslol_url}{white}
""")

    Continue()
    Reset()

except Exception as e:
    Error(e)