# Copyright (c) 2025-2026 v4lkyr0 — Buildware-Tools
# See the file 'LICENSE' for copying permission.
# --------------------------------------------------------
# EN: Non-commercial use only. Do not sell, remove credits
#     or redistribute without prior written permission.
# FR: Usage non-commercial uniquement. Ne pas vendre, supprimer
#     les crédits ou redistribuer sans autorisation écrite.

import os, secrets
os.environ["bkey"] = secrets.token_hex(32)

from Programs.Core.Utils import *
from Programs.Core.Config import *

try:
    import re
    import json as _json
    import time
except Exception as e:
    MissingModule(e)

def Configuration():
    data = LoadData()
    if data.get("configured"):
        return
    
    Title("Configuration")
    Clear()
    question_1 = input(f"{INPUT} Do you want auto updates? {YESORNO} {red}->{reset} ").strip().lower()
    question_2 = input(f"{INPUT} Skip startup animaton? {YESORNO} {red}->{reset} ")
    data["configured"]     = True
    data["auto_update"]    = question_1 in ["y", "yes"]
    data["skip_animation"] = question_2 in ["y", "yes"]
    SaveData(data)

def Connection():
    try:
        requests.get("https://www.google.com", timeout=5)
    except Exception:
        print(f"{ERROR} An internet connection is required to use {name_tool}!", reset)
        Continue()
        sys.exit()

def SavePage(page):
    try:
        data = LoadData()
        data["page"] = page
        SaveData(data)
    except Exception:
        pass

def LoadPage():
    try:
        data = LoadData()
        return int(data.get("page", 1))
    except Exception:
        return 1

def SaveLaunched():
    try:
        data = LoadData()
        data["launched"] = True
        SaveData(data)
    except Exception:
        pass

def HasLaunched():
    try:
        data = LoadData()
        return data.get("launched", False)
    except Exception:
        return False

Configuration()

def GetVisiblePlugins():
    try:
        data        = LoadData()
        visible     = data.get("plugins_visible", [])
        plugins_dir = os.path.join(tool_path, "Programs", "Plugins")
 
        if not os.path.exists(plugins_dir):
            return []
 
        result = []
        for folder in sorted(os.listdir(plugins_dir)):
            if folder == "__pycache__":
                continue
            if folder not in visible:
                continue
            json_path = os.path.join(plugins_dir, folder, "plugin.json")
            if not os.path.exists(json_path):
                continue
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    pdata = _json.load(f)
                result.append((folder, pdata))
            except Exception:
                continue
 
        return result[:10]
    except Exception:
        return []
 
def BuildPluginLines():
    plugins = GetVisiblePlugins()
    lines   = []
 
    for i, (folder, pdata) in enumerate(plugins):
        num     = str(41 + i).zfill(2)
        is_last = (i == len(plugins) - 1)
        prefix  = "└─" if is_last else "├─"
        name    = pdata.get("name", folder)
        if VisibleLen(name) > 30:
            name = name[:29] + ".."
        lines.append(f" {prefix} {PREFIX1}{num}{SUFFIX1} {name}")
 
    return lines
 
def VisibleLen(s):
    return len(re.sub(r'\033\[[0-9;]*m', '', s))
 
def PadLine(s, width):
    return s + " " * (width - VisibleLen(s))
 
def BuildPage2():
    stealer_lines = [
        f" └─ {PREFIX1}31{SUFFIX1} {StarRequired('Stealer Builder')}",
        f"      ├─ {white}System Information{reset}",
        f"      ├─ {white}Wallets Sessions Files{reset}",
        f"      ├─ {white}Games/Telegram Sessions Files{reset}",
        f"      ├─ {white}Discord Tokens{reset}",
        f"      ├─ {white}Discord Injection{reset}",
        f"      ├─ {white}Browsers Data{reset}",
        f"      ├─ {white}Interesting Files{reset}",
        f"      ├─ {white}Camera Capture{reset}",
        f"      └─ {white}Screenshots{reset}",
    ]
 
    plugin_lines = BuildPluginLines()
 
    roblox_lines = [
        f" ├─ {PREFIX1}51{SUFFIX1} {StarRequired('Cookie Login')}",
        f" ├─ {PREFIX1}52{SUFFIX1} Cookie Information",
        f" ├─ {PREFIX1}53{SUFFIX1} Id Information",
        f" ├─ {PREFIX1}54{SUFFIX1} Username Information",
        f" ├─ {PREFIX1}55{SUFFIX1} {StarRequired('Group Information')}",
        f" └─ {PREFIX1}56{SUFFIX1} Game Information",
    ]
 
    max_lines = max(len(stealer_lines), len(plugin_lines), len(roblox_lines))
    rows      = []
 
    for i in range(max_lines):
        c1 = stealer_lines[i] if i < len(stealer_lines) else ""
        c2 = plugin_lines[i]  if i < len(plugin_lines)  else ""
        c3 = roblox_lines[i]  if i < len(roblox_lines)  else ""
        rows.append(f"{PadLine(c1, 40)}{PadLine(c2, 40)}{c3}")
 
    return "\n".join(rows)

def Menu(page=1):
    update = Update()
    Title(f"Page {page}")

    if page == 1:
        content = f"""
{red}> {PREFIX}?{SUFFIX} {version_tool} Changelog            ░                       ░                                            {white}Plugin Manager {PREFIX}P{SUFFIX}{red} <
{red}> {PREFIX}!{SUFFIX} Tool Information                                                                                Extras Files {PREFIX}E{SUFFIX}{red} <
                                                                                                         Next Page {PREFIX}N{SUFFIX}{red} <

╓──────────────────────────────────────╖╓──────────────────────────────────────╖╓──────────────────────────────────────╖
                Network                                  Osint                                 Utilities               
╙┬─────────────────────────────────────╜╙┬─────────────────────────────────────╜╙┬─────────────────────────────────────╜
 ├─ {PREFIX1}01{SUFFIX1} Ip Port Scanner                 ├─ {PREFIX1}11{SUFFIX1} Ip Lookup                       ├─ {PREFIX1}21{SUFFIX1} Password Generator
 ├─ {PREFIX1}02{SUFFIX1} Ip Pinger                       ├─ {PREFIX1}12{SUFFIX1} Whois Lookup                    ├─ {PREFIX1}22{SUFFIX1} Hash Identifier
 ├─ {PREFIX1}03{SUFFIX1} Traceroute                      ├─ {PREFIX1}13{SUFFIX1} Ip Reputation Checker           ├─ {PREFIX1}23{SUFFIX1} {StarRequired("Hash Cracker")}
 ├─ {PREFIX1}04{SUFFIX1} Dns Lookup                      ├─ {PREFIX1}14{SUFFIX1} {StarRequired("Subdomain Finder")}                ├─ {PREFIX1}24{SUFFIX1} {StarRequired("Zip Cracker")}
 ├─ {PREFIX1}05{SUFFIX1} Mac Lookup                      ├─ {PREFIX1}15{SUFFIX1} {StarRequired("Username Tracker")}                ├─ {PREFIX1}25{SUFFIX1} File Hasher
 ├─ {PREFIX1}06{SUFFIX1} Ssl Checker                     ├─ {PREFIX1}16{SUFFIX1} {StarRequired("Email Breach Checker")}            ├─ {PREFIX1}26{SUFFIX1} Text Encoder/Decoder
 ├─ {PREFIX1}07{SUFFIX1} Proxy Checker                   ├─ {PREFIX1}17{SUFFIX1} {StarRequired("Phone Number Lookup")}             ├─ {PREFIX1}27{SUFFIX1} {StarRequired("Jwt Decoder")}
 ├─ {PREFIX1}08{SUFFIX1} Network Scanner                 ├─ {PREFIX1}18{SUFFIX1} {StarRequired("File Metadata Scanner")}           ├─ {PREFIX1}28{SUFFIX1} Qr Code Generator
 ├─ {PREFIX1}09{SUFFIX1} {StarRequired("Proxy Scraper")}                   ├─ {PREFIX1}19{SUFFIX1} {StarRequired("Dorking Query Engine")}            ├─ {PREFIX1}29{SUFFIX1} Temporary Mail
 └─ {PREFIX1}10{SUFFIX1} {StarRequired("Website Vulnerability Scanner")}   └─ {PREFIX1}20{SUFFIX1} {StarRequired("Dox Creator")}                     └─ {PREFIX1}30{SUFFIX1} {StarRequired("Advanced Python Obfuscator")}"""

    elif page == 2:
        page2_rows = BuildPage2()
        content    = f"""
{red}> {PREFIX}?{SUFFIX} {version_tool} Changelog            ░                       ░                                            {white}Plugin Manager {PREFIX}P{SUFFIX}{red} <
{red}> {PREFIX}!{SUFFIX} Tool Information                                                                                Extras Files {PREFIX}E{SUFFIX}{red} <
{red}> {PREFIX}B{SUFFIX} Back Page                                                                                          Next Page {PREFIX}N{SUFFIX}{red} <
 
╓──────────────────────────────────────╖╓──────────────────────────────────────╖╓──────────────────────────────────────╖
            Stealer Builder                             Plugins                                  Roblox                
╙┬─────────────────────────────────────╜╙┬─────────────────────────────────────╜╙┬─────────────────────────────────────╜
{page2_rows}"""

    elif page == 3:
        content = f"""
{red}> {PREFIX}?{SUFFIX} {version_tool} Changelog            ░                       ░                                            {white}Plugin Manager {PREFIX}P{SUFFIX}{red} <
{red}> {PREFIX}!{SUFFIX} Tool Information                                                                                Extras Files {PREFIX}E{SUFFIX}{red} <
{red}> {PREFIX}B{SUFFIX} Back Page

╓──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╖
                                                         Discord                                                        
╙┬───────────────────────────────────────┬───────────────────────────────────────┬─────────────────────────────────────╜
 ├─ {PREFIX1}61{SUFFIX1} Server Information              ├─ {PREFIX1}71{SUFFIX1} Token Information               ├─ {PREFIX1}81{SUFFIX1} Token Image Changer
 ├─ {PREFIX1}62{SUFFIX1} {StarRequired("Server Scraper")}                  ├─ {PREFIX1}72{SUFFIX1} Token Login                     ├─ {PREFIX1}82{SUFFIX1} Token Bio Changer
 ├─ {PREFIX1}63{SUFFIX1} {StarRequired("Server Cloner")}                   ├─ {PREFIX1}73{SUFFIX1} Token Joiner                    ├─ {PREFIX1}83{SUFFIX1} Token Status Changer
 ├─ {PREFIX1}64{SUFFIX1} {StarRequired("Server Editor")}                   ├─ {PREFIX1}74{SUFFIX1} Token Leaver                    ├─ {PREFIX1}84{SUFFIX1} Token Generator
 ├─ {PREFIX1}65{SUFFIX1} {StarRequired("Server Ban All")}                  ├─ {PREFIX1}75{SUFFIX1} Token Onliner                   ├─ {PREFIX1}85{SUFFIX1} {StarRequired("Token Nuker")}
 ├─ {PREFIX1}66{SUFFIX1} {StarRequired("Server Kick All")}                 ├─ {PREFIX1}76{SUFFIX1} {StarRequired("Token Mass Dm")}                   ├─ {PREFIX1}86{SUFFIX1} {StarRequired("Token Disabler")}
 ├─ {PREFIX1}67{SUFFIX1} Server Unban All                ├─ {PREFIX1}77{SUFFIX1} {StarRequired("Token Spammer")}                   ├─ {PREFIX1}87{SUFFIX1} {StarRequired("Token Ghost Pinger")}
 ├─ {PREFIX1}68{SUFFIX1} Server Mute All                 ├─ {PREFIX1}78{SUFFIX1} {StarRequired("Webhook Spammer")}                 ├─ {PREFIX1}88{SUFFIX1} Webhook Information
 ├─ {PREFIX1}69{SUFFIX1} {StarRequired("Bot Nuker")}                       ├─ {PREFIX1}79{SUFFIX1} {StarRequired("Vanity Url Sniper")}               ├─ {PREFIX1}89{SUFFIX1} Embed Creator
 └─ {PREFIX1}70{SUFFIX1} {StarRequired("Bot Raider")}                      └─ {PREFIX1}80{SUFFIX1} Injection Cleaner               └─ {PREFIX1}90{SUFFIX1} {StarRequired("Nitro Generator")}"""

    return f"""{update}{buildware_banner}{content}"""

options = {
    "01": "Network-Ip-Port-Scanner",               "11": "Osint-Ip-Lookup",                          "21": "Utility-Password-Generator",
    "02": "Network-Ip-Pinger",                     "12": "Osint-Whois-Lookup",                       "22": "Utility-Hash-Identifier",
    "03": "Network-Traceroute",                    "13": "Osint-Ip-Reputation-Checker",              "23": "Utility-Hash-Cracker",
    "04": "Network-Dns-Lookup",                    "14": "Osint-Subdomain-Finder",                   "24": "Utility-Zip-Cracker",
    "05": "Network-Mac-Lookup",                    "15": "Osint-Username-Tracker",                   "25": "Utility-File-Hasher",
    "06": "Network-Ssl-Checker",                   "16": "Osint-Email-Breach-Checker",               "26": "Utility-Text-Encoder-Decoder",
    "07": "Network-Proxy-Checker",                 "17": "Osint-Phone-Number-Lookup",                "27": "Utility-Jwt-Decoder",
    "08": "Network-Network-Scanner",               "18": "Osint-File-Metadata-Scanner",              "28": "Utility-Qr-Code-Generator",
    "09": "Network-Proxy-Scraper",                 "19": "Osint-Dorking-Query-Engine",               "29": "Utility-Temporary-Mail",
    "10": "Network-Website-Vulnerability-Scanner", "20": "Osint-Dox-Creator",                        "30": "Utility-Advanced-Python-Obfuscator",

    "31": "Stealer-Builder",                                                                         "51": "Roblox-Cookie-Login",
                                                                                                     "52": "Roblox-Cookie-Information",
                                                                                                     "53": "Roblox-Id-Information",
                                                                                                     "54": "Roblox-Username-Information",
                                                                                                     "55": "Roblox-Group-Information",
                                                                                                     "56": "Roblox-Game-Information",

    "61": "Discord-Server-Information",            "71": "Discord-Token-Information",                "81": "Discord-Token-Image-Changer",
    "62": "Discord-Server-Scraper",                "72": "Discord-Token-Login",                      "82": "Discord-Token-Bio-Changer",
    "63": "Discord-Server-Cloner",                 "73": "Discord-Token-Joiner",                     "83": "Discord-Token-Status-Changer",
    "64": "Discord-Server-Editor",                 "74": "Discord-Token-Leaver",                     "84": "Discord-Token-Generator",
    "65": "Discord-Server-Ban-All",                "75": "Discord-Token-Onliner",                    "85": "Discord-Token-Nuker",
    "66": "Discord-Server-Kick-All",               "76": "Discord-Token-Mass-Dm",                    "86": "Discord-Token-Disabler",
    "67": "Discord-Server-Unban-All",              "77": "Discord-Token-Spammer",                    "87": "Discord-Token-Ghost-Pinger",
    "68": "Discord-Server-Mute-All",               "78": "Discord-Webhook-Spammer",                  "88": "Discord-Webhook-Information",
    "69": "Discord-Bot-Nuker",                     "79": "Discord-Vanity-Url-Sniper",                "89": "Discord-Embed-Creator",
    "70": "Discord-Bot-Raider",                    "80": "Discord-Injection-Cleaner",                "90": "Discord-Nitro-Generator",
}

def LoadPluginOptions():
    plugins = GetVisiblePlugins()
    result  = {}
    for i, (folder, pdata) in enumerate(plugins):
        num         = str(41 + i).zfill(2)
        result[num] = os.path.join("Plugins", folder, "main.py")
    return result

star_required       = {"09", "10", "14", "15", "16", "17", "18", "19", "20", "23", "24", "27", "30", "31", "51", "55", "62", "63", "64", "65", "66", "69", "70", "76", "77", "78", "79", "85", "86", "87", "90"}
connection_required = {"01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "20", "23", "24", "29", "31", "51", "52", "53", "54", "55", "56", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90"}


page = LoadPage()

data = LoadData()
if '--no-anim' not in sys.argv and not data.get("skip_animation", False):
    Title("B̵̼͕̑ḽ̶́̔o̶̫͕̓o̸̦̗̓̐d̷̘̔̈́")
    BloodAnimation()

while True:
    try:
        Clear()
        Scroll(Gradient(Menu(page)))

        plugin_options = LoadPluginOptions()
        all_options    = {**options, **plugin_options}

        choice = input(f"{PREFIX}{username_pc}@Buildware{SUFFIX} {red}->{reset} ").strip().lower()

        if choice in ['p', 'plugin']:
            StartProgram('Plugin-Manager.py')
        elif choice in ['f', 'feedback']:
            StartProgram('Feedback.py')
        elif choice in ['n', 'next']:
            page = 1 if page == 3 else page + 1
            SavePage(page)
        elif choice in ['b', 'back']:
            page = 3 if page == 1 else page - 1
            SavePage(page)
        elif choice in ['?', 'changelog']:
            StartProgram('Changelog-Version.py')
        elif choice in ['!', 'tool', 'info']:
            StartProgram('Tool-Information.py')
        elif choice in ['e', 'extras']:
            StartProgram('Extras-Files.py')
        elif choice in all_options:
            padded = choice.zfill(2)
            if padded in star_required and not CheckGithubStar():
                continue
            if padded in connection_required:
                Connection()
            target = all_options[padded]
            if target.startswith("Plugins"):
                StartProgram(target)
            else:
                StartProgram(target + '.py')
        elif choice.zfill(2) in all_options:
            padded = choice.zfill(2)
            if padded in star_required and not CheckGithubStar():
                continue
            if padded in connection_required:
                Connection()
            target = all_options[padded]
            if target.startswith("Plugins"):
                StartProgram(target)
            else:
                StartProgram(target + '.py')
        else:
            ErrorFeature()

        SavePage(page)

    except Exception as e:
        Error(e)