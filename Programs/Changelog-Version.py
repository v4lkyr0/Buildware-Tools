# Copyright (c) 2025-2026 v4lkyr0 — Buildware-Tools
# See the file 'LICENSE' for copying permission.
# --------------------------------------------------------
# EN: Non-commercial use only. Do not sell, remove credits
#     or redistribute without prior written permission.
# FR: Usage non-commercial uniquement. Ne pas vendre, supprimer
#     les crédits ou redistribuer sans autorisation écrite.

from Core.Utils import *
from Core.Config import *

Title(f"{version_tool} Changelog")

Scroll(GradientBanner(utilities_banner)) 

try:
    changelog = f"""
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 
 {INFO} Creator Message
 {INFO}    - Hi {username_pc}! In this version, I haven't added many new features because I don't know what else to add.
 {INFO}      Please join our Discord server at {red}{discord_url}{white} and suggest features or report bugs.
 
 {INFO} New Features
 {INFO}    - Website Vulnerability Scanner
 
 {INFO} Improvements
 {INFO}    - I've added a Discord server, join it!
 
 {INFO} Bug Fixes
 {INFO}    - No bugs found
 
 {INFO} Renamed/Changed
 {INFO}    - Google Dork Builder {red}->{white} Dorking Query Engine
 {INFO}    - Exif Data Extractor {red}->{white} File Metadata Scanner
 
 {INFO} Removed
 {INFO}    - HTTP Headers
 
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────"""

    Scroll(Gradient(changelog))

    Continue()
    Reset()

except Exception as e:
    Error(e)