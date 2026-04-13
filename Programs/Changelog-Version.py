# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

Title(f"{version_tool} Changelog")

try:
    changelog = f"""
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

 {INFO} Creator Message:
 {INFO}    - Hey {username_pc}! This is v{version_tool} of {name_tool}. A major feature will be coming in
 {INFO}      the next update. Get ready!
 
 {INFO} New Features:
 {INFO}    - Added Feedback System
 {INFO}    - Added Osint Ip Lookup
 {INFO}    - Added Osint Dns Lookup
 {INFO}    - Added Osint Whois Lookup
 {INFO}    - Added Osint Subdomain Finder
 {INFO}    - Added Osint Header Analyzer
 {INFO}    - Added Osint Website Detector
 {INFO}    - Added Osint Username Lookup
 {INFO}    - Added Osint Email Checker
 {INFO}    - Added Osint Email Breach Checker
 {INFO}    - Added Osint Phone Lookup
 {INFO}    - Added Network Port Scanner
 {INFO}    - Added Network Ip Pinger
 {INFO}    - Added Network Traceroute
 {INFO}    - Added Network Reverse Dns
 {INFO}    - Added Network Mac Lookup
 {INFO}    - Added Network Interface Information
 {INFO}    - Added Network Website Status
 {INFO}    - Added Network Ssl Checker
 {INFO}    - Added Network Proxy Checker
 {INFO}    - Added Network Wifi Passwords
 {INFO}    - Added Utilities Password Generator
 {INFO}    - Added Utilities Temp Mail
 {INFO}    - Added Utilities System Information
 {INFO}    - Added Utilities Hash Generator
 {INFO}    - Added Utilities Hash Identifier
 {INFO}    - Added Utilities File Hasher
 {INFO}    - Added Utilities Base64 Converter
 {INFO}    - Added Utilities Caesar Cipher
 {INFO}    - Added Utilities Text Converter
 {INFO}    - Added Utilities Url Analyzer
 {INFO}    - Added Roblox Cookie Login
 {INFO}    - Added Roblox Cookie Information
 {INFO}    - Added Roblox Id Information
 {INFO}    - Added Roblox Username Information
 {INFO}    - Added Roblox Group Information
 {INFO}    - Added Roblox Game Information

 {INFO} Improvements:
 {INFO}    - New Categories: OSINT, NETWORK, UTILITIES & ROBLOX
 {INFO}    - Improved error handling across all programs

 {INFO} Bug Fixes:
 {INFO}    - All known bugs have been fixed

 {INFO} Renamed Features:
 {INFO}    - Discord Token Pfp Changer {red}->{white} Discord Token Image Changer

 {INFO} Removed Features:
 {INFO}    - Removed Discord Bot Id To Invite
 {INFO}    - Removed Discord Bot Information
 {INFO}    - Removed Discord Id To Token
 {INFO}    - Removed Discord Injection Builder
 {INFO}    - Removed Discord Invite Generator
 {INFO}    - Removed Discord Invite Tracker
 {INFO}    - Removed Discord Token Banner Changer
 {INFO}    - Removed Discord Token Block Friends
 {INFO}    - Removed Discord Token Delete Dm
 {INFO}    - Removed Discord Token Delete Friends
 {INFO}    - Removed Discord Token Grabber Builder
 {INFO}    - Removed Discord Token House Changer
 {INFO}    - Removed Discord Token Language Changer
 {INFO}    - Removed Discord Token Pronoun Changer
 {INFO}    - Removed Discord Token Theme Changer
 {INFO}    - Removed Discord Token Unblock Users
 {INFO}    - Removed Discord Webhook Deleter
 {INFO}    - Removed Discord Webhook Generator
 {INFO}    - Removed Exit Buildware

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────"""
    Scroll(Gradient(changelog))

    Continue()
    Reset()

except Exception as e:
    Error(e)