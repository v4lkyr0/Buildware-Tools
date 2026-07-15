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

Title("Token Leaver")

Scroll(GradientBanner(discord_banner))

try:
    token   = ChoiceToken()
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

    print(f"{LOADING} Fetching servers..", reset)

    r = ApiGet("https://discord.com/api/v9/users/@me/guilds")

    if not r or r.status_code != 200:
        print(f"{ERROR} Could not fetch servers!", reset)
        Continue()
        Reset()

    guilds = r.json()

    if not guilds:
        print(f"{ERROR} No servers found!", reset)
        Continue()
        Reset()

    print(f"{SUCCESS} Found:{red} {len(guilds)}{white} server(s)", reset)
    print(f"{LOADING} Leaving..", reset)

    left_count   = 0
    failed_count = 0

    for guild in guilds:
        guild_id   = guild.get("id")
        guild_name = guild.get("name", "None")

        if not guild_id:
            continue

        resp = ApiDelete(f"https://discord.com/api/v9/users/@me/guilds/{guild_id}")

        if resp and resp.status_code in [200, 204]:
            left_count += 1
            print(f"{SUCCESS} Left:{red} {guild_name}", reset)
        elif resp and resp.status_code == 400:
            resp2 = ApiDelete(f"https://discord.com/api/v9/guilds/{guild_id}")
            if resp2 and resp2.status_code in [200, 204]:
                left_count += 1
                print(f"{SUCCESS} Left:{red} {guild_name}", reset)
            else:
                failed_count += 1
                print(f"{ERROR} Failed:{red} {guild_name}", reset)
        else:
            failed_count += 1
            code = resp.status_code if resp else "None"
            print(f"{ERROR} Failed:{red} {guild_name}{white} | Code:{red} {code}", reset)

        time.sleep(0.5)

    print(f"\n{SUCCESS} Completed!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)