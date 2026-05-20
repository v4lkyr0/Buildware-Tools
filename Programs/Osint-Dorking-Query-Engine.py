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
    import webbrowser
    from urllib.parse import quote_plus
except Exception as e:
    MissingModule(e)

Title("Dorking Query Engine")

Scroll(GradientBanner(osint_banner))

try:
    Scroll(f"""
 {PREFIX}01{SUFFIX} Site Search
 {PREFIX}02{SUFFIX} File Type Search
 {PREFIX}03{SUFFIX} Login Pages
 {PREFIX}04{SUFFIX} Exposed Files
 {PREFIX}05{SUFFIX} Cameras & Devices
 {PREFIX}06{SUFFIX} Sensitive Directories
 {PREFIX}07{SUFFIX} Email Addresses
 {PREFIX}08{SUFFIX} Subdomains
 {PREFIX}09{SUFFIX} SQL Errors
 {PREFIX}10{SUFFIX} Config Files
 {PREFIX}11{SUFFIX} Open Redirects
 {PREFIX}12{SUFFIX} API Keys & Tokens
 {PREFIX}13{SUFFIX} Custom Dork
""")

    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    dork   = ""
    target = ""

    if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]:
        target = input(f"{INPUT} Target {red}->{reset} ").strip()
        target = target.removeprefix("https://").removeprefix("http://").rstrip("/")
        if not target:
            ErrorInput()

    if choice == "1":
        keyword = input(f"{INPUT} Keyword {red}->{reset} ").strip()
        dork    = f"site:{target} {keyword}".strip()

    elif choice == "2":
        filetype = input(f"{INPUT} File Type {red}->{reset} ").strip()
        keyword  = input(f"{INPUT} Keyword {red}->{reset} ").strip()
        if not filetype:
            ErrorInput()
        dork = f"site:{target} filetype:{filetype} {keyword}".strip()

    elif choice == "3":
        dork = f'site:{target} inurl:login OR inurl:signin OR inurl:admin OR inurl:dashboard OR inurl:portal OR inurl:wp-login'

    elif choice == "4":
        dork = f'site:{target} intitle:"index of" OR inurl:"/backup" OR inurl:"/.git" OR inurl:"/.env" OR filetype:log OR filetype:sql OR filetype:bak'

    elif choice == "5":
        dork = f'site:{target} inurl:"/view.shtml" OR inurl:"/ViewerFrame" OR inurl:"/axis-cgi/" OR intitle:"Live View / - AXIS" OR intitle:"webcamXP" OR inurl:8080'

    elif choice == "6":
        dork = f'site:{target} intitle:"index of" OR inurl:/admin OR inurl:/config OR inurl:/backup OR inurl:/uploads OR inurl:/private'

    elif choice == "7":
        dork = f'site:{target} intext:"@{target}" OR "@gmail.com" OR "@hotmail.com" OR "@yahoo.com"'

    elif choice == "8":
        dork = f'site:*.{target} -www'

    elif choice == "9":
        dork = f'site:{target} intext:"sql syntax" OR intext:"mysql_fetch" OR intext:"Warning: mysql" OR intext:"ORA-" OR intext:"SQLite" OR intext:"SQL error"'

    elif choice == "10":
        dork = f'site:{target} filetype:env OR filetype:cfg OR filetype:conf OR filetype:ini OR filetype:json OR filetype:yml OR filetype:xml inurl:config'

    elif choice == "11":
        dork = f'site:{target} inurl:redirect= OR inurl:url= OR inurl:goto= OR inurl:return= OR inurl:next= OR inurl:dest='

    elif choice == "12":
        dork = f'site:{target} intext:"api_key" OR intext:"api_secret" OR intext:"access_token" OR intext:"auth_token" OR intext:"client_secret" OR intext:"password"'

    elif choice == "13":
        dork = input(f"{INPUT} Dork {red}->{reset} ").strip()
        if not dork:
            ErrorInput()

    else:
        ErrorChoice()

    if not dork:
        ErrorInput()

    engines = {
        "1": ("Google",    f"https://www.google.com/search?q={quote_plus(dork)}"),
        "2": ("Bing",      f"https://www.bing.com/search?q={quote_plus(dork)}"),
        "3": ("DuckDuckGo",f"https://duckduckgo.com/?q={quote_plus(dork)}"),
        "4": ("All",       None),
    }

    Scroll(f"""
 {PREFIX}01{SUFFIX} Google
 {PREFIX}02{SUFFIX} Bing
 {PREFIX}03{SUFFIX} DuckDuckGo
 {PREFIX}04{SUFFIX} All
""")

    engine_choice = input(f"{INPUT} Engine {red}->{reset} ").strip().lstrip("0")

    if engine_choice not in engines:
        ErrorChoice()

    print(f"{LOADING} Opening..", reset)
    print(f"{SUCCESS} Dork:{red} {dork}", reset)

    try:
        if engine_choice == "4":
            for _, (name, url) in engines.items():
                if url:
                    webbrowser.open(url)
        else:
            _, (name, url) = list(engines.items())[int(engine_choice) - 1]
            webbrowser.open(url)
    except Exception:
        print(f"{ERROR} Could not open browser!", reset)
        print(f"{INFO} Url:{red} {engines.get(engine_choice, ('', ('', '')))[1]}", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)