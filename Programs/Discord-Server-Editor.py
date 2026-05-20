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
    import requests
    import time
except Exception as e:
    MissingModule(e)

Title("Server Editor")

Scroll(GradientBanner(discord_banner))

try:
    token = ChoiceToken()

    server_id = input(f"{INPUT} Server Id {red}->{reset} ").strip()
    if not server_id or not server_id.isdigit():
        ErrorId()

    headers = {
        "Authorization": token,
        "Content-Type" : "application/json",
        "User-Agent"   : RandomUserAgents(),
    }

    def ApiGet(url):
        while True:
            try:
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 429:
                    time.sleep(r.json().get("retry_after", 1))
                    continue
                return r
            except Exception:
                return None

    def ApiPatch(url, json=None):
        while True:
            try:
                r = requests.patch(url, headers=headers, json=json or {}, timeout=10)
                if r.status_code == 429:
                    time.sleep(r.json().get("retry_after", 1))
                    continue
                return r
            except Exception:
                return None

    print(f"{LOADING} Fetching server..", reset)

    guild_response = ApiGet(f"https://discord.com/api/v9/guilds/{server_id}")

    if not guild_response or guild_response.status_code != 200:
        print(f"{ERROR} Could not access server!", reset)
        Continue()
        Reset()

    guild_data   = guild_response.json()
    current_name = guild_data.get("name", "None")
    current_desc = guild_data.get("description", "None")
    current_veri = guild_data.get("verification_level", "None")

    Scroll(f"""
 {INFO} Name               :{red} {current_name}{white}
 {INFO} Description        :{red} {current_desc}{white}
 {INFO} Verification Level :{red} {current_veri}{white}

 {PREFIX}01{SUFFIX} Change Name
 {PREFIX}02{SUFFIX} Change Description
 {PREFIX}03{SUFFIX} Change Afk Channel
 {PREFIX}04{SUFFIX} Change Afk Timeout
 {PREFIX}05{SUFFIX} Change Verification Level
 {PREFIX}06{SUFFIX} Change System Channel
 {PREFIX}07{SUFFIX} Change Locale
""")

    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    if choice == "1":
        new_name = input(f"{INPUT} New Name {red}->{reset} ").strip()
        if not new_name:
            ErrorInput()
        print(f"{LOADING} Changing..", reset)
        resp = ApiPatch(f"https://discord.com/api/v9/guilds/{server_id}", json={"name": new_name})
        if resp and resp.status_code == 200:
            print(f"{SUCCESS} Name changed to:{red} {new_name}", reset)
        else:
            print(f"{ERROR} Could not change name!", reset)

    elif choice == "2":
        new_description = input(f"{INPUT} New Description {red}->{reset} ").strip()
        print(f"{LOADING} Changing..", reset)
        resp = ApiPatch(f"https://discord.com/api/v9/guilds/{server_id}", json={"description": new_description or None})
        if resp and resp.status_code == 200:
            print(f"{SUCCESS} Description changed!", reset)
        else:
            print(f"{ERROR} Could not change description!", reset)

    elif choice == "3":
        channel_id = input(f"{INPUT} Afk Channel Id {red}->{reset} ").strip()
        if not channel_id or not channel_id.isdigit():
            ErrorId()
        print(f"{LOADING} Changing..", reset)
        resp = ApiPatch(f"https://discord.com/api/v9/guilds/{server_id}", json={"afk_channel_id": channel_id})
        if resp and resp.status_code == 200:
            print(f"{SUCCESS} Afk channel changed!", reset)
        else:
            print(f"{ERROR} Could not change afk channel!", reset)

    elif choice == "4":
        print(f"{INFO} Values:{red} 60, 300, 900, 1800, 3600", reset)
        try:
            timeout = int(input(f"{INPUT} Afk Timeout {red}->{reset} ").strip())
            if timeout not in [60, 300, 900, 1800, 3600]:
                ErrorInput()
        except Exception:
            ErrorInput()
        print(f"{LOADING} Changing..", reset)
        resp = ApiPatch(f"https://discord.com/api/v9/guilds/{server_id}", json={"afk_timeout": timeout})
        if resp and resp.status_code == 200:
            print(f"{SUCCESS} Afk timeout changed to:{red} {timeout}s", reset)
        else:
            print(f"{ERROR} Could not change afk timeout!", reset)

    elif choice == "5":
        print(f"{INFO} Levels:{red} 0=None, 1=Low, 2=Medium, 3=High, 4=Highest", reset)
        try:
            level = int(input(f"{INPUT} Verification Level {red}->{reset} ").strip())
            if level not in [0, 1, 2, 3, 4]:
                ErrorInput()
        except Exception:
            ErrorInput()
        print(f"{LOADING} Changing..", reset)
        resp = ApiPatch(f"https://discord.com/api/v9/guilds/{server_id}", json={"verification_level": level})
        if resp and resp.status_code == 200:
            print(f"{SUCCESS} Verification level changed to:{red} {level}", reset)
        else:
            print(f"{ERROR} Could not change verification level!", reset)

    elif choice == "6":
        channel_id = input(f"{INPUT} System Channel Id {red}->{reset} ").strip()
        if not channel_id or not channel_id.isdigit():
            ErrorId()
        print(f"{LOADING} Changing..", reset)
        resp = ApiPatch(f"https://discord.com/api/v9/guilds/{server_id}", json={"system_channel_id": channel_id})
        if resp and resp.status_code == 200:
            print(f"{SUCCESS} System channel changed!", reset)
        else:
            print(f"{ERROR} Could not change system channel!", reset)

    elif choice == "7":
        print(f"{INFO} Example:{red} en-US, fr, de, es-ES, pt-BR, ja, zh-CN", reset)
        locale = input(f"{INPUT} Locale {red}->{reset} ").strip()
        if not locale:
            ErrorInput()
        print(f"{LOADING} Changing..", reset)
        resp = ApiPatch(f"https://discord.com/api/v9/guilds/{server_id}", json={"preferred_locale": locale})
        if resp and resp.status_code == 200:
            print(f"{SUCCESS} Locale changed to:{red} {locale}", reset)
        else:
            print(f"{ERROR} Could not change locale!", reset)

    else:
        ErrorChoice()

    Continue()
    Reset()

except Exception as e:
    Error(e)