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

Title("Server Unban All")

Scroll(GradientBanner(discord_banner))

try:
    token = ChoiceToken()

    server_id = input(f"{INPUT} Server Id {red}->{reset} ").strip()
    if not server_id or not server_id.isdigit():
        ErrorId()

    try:
        delay = float(input(f"{INPUT} Delay {red}->{reset} ").strip())
        if delay < 0.1:
            delay = 0.1
    except:
        delay = 0.5

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

    print(f"{LOADING} Fetching bans..", reset)

    bans  = []
    after = None

    while True:
        url = f"https://discord.com/api/v9/guilds/{server_id}/bans?limit=1000"
        if after:
            url += f"&after={after}"
        r = ApiGet(url)
        if not r or r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        bans.extend(batch)
        after = batch[-1]["user"]["id"]
        if len(batch) < 1000:
            break
        time.sleep(0.5)

    if not bans:
        print(f"{INFO} No banned users found!", reset)
        Continue()
        Reset()

    print(f"{SUCCESS} Found:{red} {len(bans)}{white} banned user(s)", reset)
    print(f"{LOADING} Unbanning..", reset)

    unbanned_count = 0
    failed_count   = 0

    for ban in bans:
        user     = ban.get("user", {})
        user_id  = user.get("id")
        username = user.get("username", "None")

        if not user_id:
            continue

        resp = ApiDelete(f"https://discord.com/api/v9/guilds/{server_id}/bans/{user_id}")

        if resp and resp.status_code in [200, 204]:
            unbanned_count += 1
            print(f"{SUCCESS} Unbanned:{red} {unbanned_count:<6}{white} | User:{red} {username}", reset)
        else:
            failed_count += 1
            code = resp.status_code if resp else "None"
            print(f"{ERROR} Failed | User:{red} {username}{white} | Code:{red} {code}", reset)

        time.sleep(delay)

    print(f"\n{SUCCESS} Completed!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)