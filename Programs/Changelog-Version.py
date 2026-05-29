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
 {INFO}    - Hey {username_pc},
 {INFO}      Sorry for the wait on this update — school's been keeping me pretty busy lately. No major additions
 {INFO}      this time around, but I've focused on squashing bugs and sneaked in a cool new feature I think you'll enjoy.
 {INFO}      Thanks for your patience, more coming soon!
 
 {INFO} New Features
 {INFO}    - Added Auto Config Backup : The configuration is automatically saved and restored after updates.
 
 {INFO} Improvements
 {INFO}    - Nothing
 
 {INFO} Bug Fixes
 {INFO}    - Fixed configuration not saving correctly between sessions.
 {INFO}    - Server Cloner: Fixed an issue related to channel order and icon
 
 {INFO} Renamed/Changed
 {INFO}    - Nothing
 
 {INFO} Removed
 {INFO}    - Nothing

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────"""

    Scroll(Gradient(changelog))

    Continue()
    Reset()

except Exception as e:
    Error(e)