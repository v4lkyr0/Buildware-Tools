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
 {INFO}      Sorry for the wait on the fixes and this update — I've been pretty busy and my mind was
 {INFO}      a bit elsewhere lately, but I'm back. I've fixed all the bugs you reported on my Discord
 {INFO}      (make sure to join if you haven't yet!). Now, I need your help: give me your best ideas
 {INFO}      for new features, and let me know if there's any current feature you think I should remove.
 {INFO}      Thanks for your patience, looking forward to your feedback!
 
 {INFO} New Features
 {INFO}    - Nothing :(
 
 {INFO} Improvements
 {INFO}    - Added interactive map windows to Osint-Ip-Lookup.py
 
 {INFO} Bug Fixes
 {INFO}    - Fixed incomplete pattern matching in Stealer-Builder.py
 {INFO}    - Fixed star check failing on fine-grained tokens
 
 {INFO} Renamed/Changed
 {INFO}    - Nothing :(
 
 {INFO} Removed 
 {INFO}    - Nothing :(

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────"""

    Scroll(Gradient(changelog))

    Continue()
    Reset()

except Exception as e:
    Error(e)