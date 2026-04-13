# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Programs.Plugins.Utils import *
from Programs.Plugins.Config import *

try:
    import os
    import sys
    import time
except Exception as e:
    MissingModule(e)

def Connection():
    try:
        requests.get("https://www.google.com", timeout=5)
    except:
        print(f"{ERROR} An internet connection is required to use {name_tool}!", reset)
        Continue()
        sys.exit()

def SavePage(page):
    try:
        data = load_data()
        data["page"] = page
        save_data(data)
    except:
        pass

def LoadPage():
    try:
        data = load_data()
        return int(data.get("page", 1))
    except:
        return 1

Banner = """
                          ▄▄▄▄    █    ██  ██▓ ██▓    ▓█████▄  █     █░ ▄▄▄       ██▀███  ▓█████  
                         ▓█████▄  ██  ▓██▒▓██▒▓██▒    ▒██▀ ██▌▓█░ █ ░█░▒████▄    ▓██ ▒ ██▒▓█   ▀  
                         ▒██▒ ▄██▓██  ▒██░▒██▒▒██░    ░██   █▌▒█░ █ ░█ ▒██  ▀█▄  ▓██ ░▄█ ▒▒███   
                         ▒██░█▀  ▓▓█  ░██░░██░▒██░    ░▓█▄   ▌░█░ █ ░█ ░██▄▄▄▄██ ▒██▀▀█▄  ▒▓█  ▄  
                         ░▓█  ▀█▓▒▒█████▓ ░██░░██████▒░▒████▓ ░░██▒██▓  ▓█   ▓██▒░██▓ ▒██▒░▒████▒ 
                         ░▒▓███▀▒░▒▓▒ ▒ ▒ ░▓  ░ ▒░▓  ░ ▒▒▓  ▒ ░ ▓░▒ ▒   ▒▒   ▓▒█░░ ▒▓ ░▒▓░░░ ▒░ ░ 
                         ▒░▒   ░ ░░▒░ ░ ░  ▒ ░░ ░ ▒  ░ ░ ▒  ▒   ▒ ░ ░    ▒   ▒▒ ░  ░▒ ░ ▒░ ░ ░  ░ 
                          ░    ░  ░░░ ░ ░  ▒ ░  ░ ░    ░ ░  ░   ░   ░    ░   ▒     ░░   ░    ░    
                          ░         ░      ░      ░  ░   ░        ░          ░  ░   ░        ░  ░ """

def Menu(page=1):
    update = Update()
    Title(f"Page {page}")

    if page == 1:
        nav = f"{red}> {PREFIX}?{SUFFIX} {version_tool} Changelog            ░                       ░                                                  {white}Feedback {PREFIX}F{SUFFIX} {red}<\n{red}> {PREFIX}!{SUFFIX} Tool Information                                                                                Extras Files {PREFIX}E{SUFFIX} {red}<\n                                                                                                         Next Page {PREFIX}N{SUFFIX} {red}<"
        content = f"""
╓──────────────────────────────────────╖╓──────────────────────────────────────╖╓──────────────────────────────────────╖
                 OSINT                                  NETWORK                                UTILITIES               
╙┬─────────────────────────────────────╜╙┬─────────────────────────────────────╜╙┬─────────────────────────────────────╜
 ├─ {PREFIX1}01{SUFFIX1} Osint Ip Lookup                 ├─ {PREFIX1}11{SUFFIXP} Network Port Scanner            ├─ {PREFIX1}21{SUFFIX1} Utility Password Generator
 ├─ {PREFIX1}02{SUFFIX1} Osint Dns Lookup                ├─ {PREFIX1}12{SUFFIX1} Network Ip Pinger               ├─ {PREFIX1}22{SUFFIXP} Utility Temp Mail
 ├─ {PREFIX1}03{SUFFIX1} Osint Whois Lookup              ├─ {PREFIX1}13{SUFFIX1} Network Traceroute              ├─ {PREFIX1}23{SUFFIX1} Utility System Information
 ├─ {PREFIX1}04{SUFFIXP} Osint Subdomain Finder          ├─ {PREFIX1}14{SUFFIX1} Network Reverse Dns             ├─ {PREFIX1}24{SUFFIX1} Utility Hash Generator
 ├─ {PREFIX1}05{SUFFIX1} Osint Header Analyzer           ├─ {PREFIX1}15{SUFFIX1} Network Mac Lookup              ├─ {PREFIX1}25{SUFFIX1} Utility Hash Identifier
 ├─ {PREFIX1}06{SUFFIX1} Osint Website Detector          ├─ {PREFIX1}16{SUFFIX1} Network Interface Information   ├─ {PREFIX1}26{SUFFIX1} Utility File Hasher
 ├─ {PREFIX1}07{SUFFIXP} Osint Username Lookup           ├─ {PREFIX1}17{SUFFIX1} Network Website Status          ├─ {PREFIX1}27{SUFFIX1} Utility Base64 Converter
 ├─ {PREFIX1}08{SUFFIX1} Osint Email Checker             ├─ {PREFIX1}18{SUFFIX1} Network Ssl Checker             ├─ {PREFIX1}28{SUFFIX1} Utility Caesar Cipher
 ├─ {PREFIX1}09{SUFFIXP} Osint Email Breach Checker      ├─ {PREFIX1}19{SUFFIX1} Network Proxy Checker           ├─ {PREFIX1}29{SUFFIX1} Utility Text Converter
 └─ {PREFIX1}10{SUFFIX1} Osint Phone Lookup              └─ {PREFIX1}20{SUFFIXP} Network Wifi Passwords          └─ {PREFIX1}30{SUFFIX1} Utility Url Analyzer"""

    elif page == 2:
        nav = f"{red}> {PREFIX}?{SUFFIX} {version_tool} Changelog            ░                       ░                                                  {white}Feedback {PREFIX}F{SUFFIX} {red}<\n{red}> {PREFIX}!{SUFFIX} Tool Information                                                                                Extras Files {PREFIX}E{SUFFIX} {red}<\n{red}> {PREFIX}B{SUFFIX} Back Page                                                                                          Next Page {PREFIX}N{SUFFIX} {red}<"
        content = f"""
╓──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╖
                                                         DISCORD                                                        
╙┬───────────────────────────────────────┬───────────────────────────────────────┬─────────────────────────────────────╜
 ├─ {PREFIX1}31{SUFFIX1} Discord Server Information      ├─ {PREFIX1}41{SUFFIX1} Discord Token Information       ├─ {PREFIX1}51{SUFFIX1} Discord Token Image Changer
 ├─ {PREFIX1}32{SUFFIX1} Discord Server Editor           ├─ {PREFIX1}42{SUFFIX1} Discord Token Login             ├─ {PREFIX1}52{SUFFIX1} Discord Token Bio Changer
 ├─ {PREFIX1}33{SUFFIXP} Discord Server Scraper          ├─ {PREFIX1}43{SUFFIX1} Discord Token Joiner            ├─ {PREFIX1}53{SUFFIX1} Discord Token Status Changer
 ├─ {PREFIX1}34{SUFFIXP} Discord Server Cloner           ├─ {PREFIX1}44{SUFFIX1} Discord Token Leaver            ├─ {PREFIX1}54{SUFFIX1} Discord Token Generator
 ├─ {PREFIX1}35{SUFFIXP} Discord Server Ban All          ├─ {PREFIX1}45{SUFFIXP} Discord Token Mass Dm           ├─ {PREFIX1}55{SUFFIX1} Discord Embed Creator
 ├─ {PREFIX1}36{SUFFIX1} Discord Server Kick All         ├─ {PREFIX1}46{SUFFIX1} Discord Token Spammer           ├─ {PREFIX1}56{SUFFIX1} Discord Injection Cleaner
 ├─ {PREFIX1}37{SUFFIX1} Discord Server Unban All        ├─ {PREFIX1}47{SUFFIX1} Discord Token Ghost Pinger      ├─ {PREFIX1}57{SUFFIX1} Discord Webhook Spammer
 ├─ {PREFIX1}38{SUFFIX1} Discord Server Mute All         ├─ {PREFIX1}48{SUFFIXP} Discord Token Nuker             ├─ {PREFIX1}58{SUFFIX1} Discord Webhook Information
 ├─ {PREFIX1}39{SUFFIXP} Discord Bot Nuker               ├─ {PREFIX1}49{SUFFIX1} Discord Token Disabler          ├─ {PREFIX1}59{SUFFIX1} Discord Vanity Url Sniper
 └─ {PREFIX1}40{SUFFIX1} Discord Bot Raider              └─ {PREFIX1}50{SUFFIX1} Discord Token Onliner           └─ {PREFIX1}60{SUFFIX1} Discord Snowflake Decoder"""

    elif page == 3:
        nav = f"{red}> {PREFIX}?{SUFFIX} {version_tool} Changelog            ░                       ░                                                  {white}Feedback {PREFIX}F{SUFFIX} {red}<\n{red}> {PREFIX}!{SUFFIX} Tool Information                                                                                Extras Files {PREFIX}E{SUFFIX} {red}<\n{red}> {PREFIX}B{SUFFIX} Back Page"
        content = f"""
╓──────────────────────────────────────╖╓──────────────────────────────────────╖╓──────────────────────────────────────╖
                 ROBLOX                
╙┬─────────────────────────────────────╜╙┬─────────────────────────────────────╜╙┬─────────────────────────────────────╜
 ├─ {PREFIX1}61{SUFFIXP} Roblox Cookie Login             ├─ {PREFIX1}71{SUFFIX1}                                 ├─ {PREFIX1}81{SUFFIX1}
 ├─ {PREFIX1}62{SUFFIXP} Roblox Cookie Information       ├─ {PREFIX1}72{SUFFIX1}                                 ├─ {PREFIX1}82{SUFFIX1}
 ├─ {PREFIX1}63{SUFFIX1} Roblox Id Information           ├─ {PREFIX1}73{SUFFIX1}                                 ├─ {PREFIX1}83{SUFFIX1}
 ├─ {PREFIX1}64{SUFFIX1} Roblox Username Information     ├─ {PREFIX1}74{SUFFIX1}                                 ├─ {PREFIX1}84{SUFFIX1}
 ├─ {PREFIX1}65{SUFFIX1} Roblox Group Information        ├─ {PREFIX1}75{SUFFIX1}                                 ├─ {PREFIX1}85{SUFFIX1}
 ├─ {PREFIX1}66{SUFFIX1} Roblox Game Information         ├─ {PREFIX1}76{SUFFIX1}                                 ├─ {PREFIX1}86{SUFFIX1}
 ├─ {PREFIX1}67{SUFFIX1}                                 ├─ {PREFIX1}77{SUFFIX1}                                 ├─ {PREFIX1}87{SUFFIX1}
 ├─ {PREFIX1}68{SUFFIX1}                                 ├─ {PREFIX1}78{SUFFIX1}                                 ├─ {PREFIX1}88{SUFFIX1}
 ├─ {PREFIX1}69{SUFFIX1}                                 ├─ {PREFIX1}79{SUFFIX1}                                 ├─ {PREFIX1}89{SUFFIX1}
 └─ {PREFIX1}70{SUFFIX1}                                 └─ {PREFIX1}80{SUFFIX1}                                 └─ {PREFIX1}90{SUFFIX1}"""

    return f"""{update}{Banner}
{nav}
{content}"""

options = {
    "01": "Osint-Ip-Lookup",                 "21": "Utility-Password-Generator",     "41": "Discord-Token-Information",
    "02": "Osint-Dns-Lookup",                "22": "Utility-Temp-Mail",              "42": "Discord-Token-Login",
    "03": "Osint-Whois-Lookup",              "23": "Utility-System-Information",     "43": "Discord-Token-Joiner",
    "04": "Osint-Subdomain-Finder",          "24": "Utility-Hash-Generator",         "44": "Discord-Token-Leaver",
    "05": "Osint-Header-Analyzer",           "25": "Utility-Hash-Identifier",        "45": "Discord-Token-Mass-Dm",
    "06": "Osint-Website-Detector",          "26": "Utility-File-Hasher",            "46": "Discord-Token-Spammer",
    "07": "Osint-Username-Lookup",           "27": "Utility-Base64-Converter",       "47": "Discord-Token-Ghost-Pinger",
    "08": "Osint-Email-Checker",             "28": "Utility-Caesar-Cipher",          "48": "Discord-Token-Nuker",
    "09": "Osint-Email-Breach-Checker",      "29": "Utility-Text-Converter",         "49": "Discord-Token-Disabler",
    "10": "Osint-Phone-Lookup",              "30": "Utility-Url-Analyzer",           "50": "Discord-Token-Onliner",
    "11": "Network-Port-Scanner",            "31": "Discord-Server-Information",     "51": "Discord-Token-Image-Changer",
    "12": "Network-Ip-Pinger",               "32": "Discord-Server-Editor",          "52": "Discord-Token-Bio-Changer",
    "13": "Network-Traceroute",              "33": "Discord-Server-Scraper",         "53": "Discord-Token-Status-Changer",
    "14": "Network-Reverse-Dns",             "34": "Discord-Server-Cloner",          "54": "Discord-Token-Generator",
    "15": "Network-Mac-Lookup",              "35": "Discord-Server-Ban-All",         "55": "Discord-Embed-Creator",
    "16": "Network-Interface-Information",   "36": "Discord-Server-Kick-All",        "56": "Discord-Injection-Cleaner",
    "17": "Network-Website-Status",          "37": "Discord-Server-Unban-All",       "57": "Discord-Webhook-Spammer",
    "18": "Network-Ssl-Checker",             "38": "Discord-Server-Mute-All",        "58": "Discord-Webhook-Information",
    "19": "Network-Proxy-Checker",           "39": "Discord-Bot-Nuker",              "59": "Discord-Vanity-Url-Sniper",
    "20": "Network-Wifi-Passwords",          "40": "Discord-Bot-Raider",             "60": "Discord-Snowflake-Decoder",
    "61": "Roblox-Cookie-Login",             "71": "Soon",                           "81": "Soon",
    "62": "Roblox-Cookie-Information",       "72": "Soon",                           "82": "Soon",
    "63": "Roblox-Id-Information",           "73": "Soon",                           "83": "Soon",
    "64": "Roblox-Username-Information",     "74": "Soon",                           "84": "Soon",
    "65": "Roblox-Group-Information",        "75": "Soon",                           "85": "Soon",
    "66": "Roblox-Game-Information",         "76": "Soon",                           "86": "Soon",
    "67": "Soon",                            "77": "Soon",                           "87": "Soon",
    "68": "Soon",                            "78": "Soon",                           "88": "Soon",
    "69": "Soon",                            "79": "Soon",                           "89": "Soon",
    "70": "Soon",                            "80": "Soon",                           "90": "Soon",
}

star_required = {"04", "07", "09", "11", "20", "22", "33", "34", "35", "39", "45", "48", "61", "62"}

Connection()
page = LoadPage()

while True:
    try:
        Clear()
        Scroll(Gradient(Menu(page)))

        choice = input(f"{PREFIX}{username_pc}@Buildware{SUFFIX} {red}->{reset} ").strip().lower()

        if choice in ['f', 'feedback']:
            StartProgram('Feedback.py')
        elif choice in ['n', 'next']:
            if page < 3:
                page += 1
        elif choice in ['b', 'back']:
            if page > 1:
                page -= 1
        elif choice in ['?', 'changelog']:
            StartProgram('Changelog-Version.py')
        elif choice in ['!', 'tool', 'info']:
            StartProgram('Tool-Information.py')
        elif choice in ['e', 'extras']:
            StartProgram('Extras-Files.py')
        elif choice in ['p', 'parrot']:
            Clear()
            Title("Parrot Live")
            os.system("curl parrot.live")
        elif choice in options:
            if choice in star_required and not CheckGithubStar():
                continue
            StartProgram(options[choice] + '.py')
        elif choice.zfill(2) in options:
            padded = choice.zfill(2)
            if padded in star_required and not CheckGithubStar():
                continue
            StartProgram(options[padded] + '.py')
        else:
            ErrorChoice()

        SavePage(page)

    except Exception as e:
        Error(e)