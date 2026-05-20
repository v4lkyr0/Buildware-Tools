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

Title("Server Ban All")

Scroll(GradientBanner(discord_banner))

try:
    token     = ChoiceToken()

    server_id = input(f"{INPUT} Server Id {red}->{reset} ").strip()
    if not server_id or not server_id.isdigit():
        ErrorId()

    ban_reason = input(f"{INPUT} Reason {red}->{reset} ").strip()
    if not ban_reason:
        ban_reason = "Banned by Buildware-Tools"

    try:
        delete_days = int(input(f"{INPUT} Delete Message History {red}->{reset} ").strip())
        if delete_days < 0 or delete_days > 7:
            delete_days = 0
    except:
        delete_days = 0

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

    def ApiPut(url, json=None):
        while True:
            try:
                r = requests.put(url, headers=headers, json=json or {}, timeout=10)
                if r.status_code == 429:
                    time.sleep(r.json().get("retry_after", 1))
                    continue
                return r
            except Exception:
                return None

    print(f"{LOADING} Fetching members..", reset)

    members = []
    after   = 0

    while True:
        r = ApiGet(f"https://discord.com/api/v9/guilds/{server_id}/members?limit=1000&after={after}")
        if not r or r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        members.extend(batch)
        after = int(batch[-1]["user"]["id"])
        if len(batch) < 1000:
            break
        time.sleep(0.5)

    if not members:
        print(f"{ERROR} No members found!", reset)
        Continue()
        Reset()

    print(f"{SUCCESS} Found:{red} {len(members)}{white} member(s)", reset)
    print(f"{LOADING} Banning..", reset)

    banned_count = 0
    failed_count = 0

    for member in members:
        user    = member.get("user", {})
        user_id = user.get("id")
        username = user.get("username", "None")

        if not user_id:
            continue

        if user.get("bot"):
            continue

        resp = ApiPut(
            f"https://discord.com/api/v9/guilds/{server_id}/bans/{user_id}",
            json={"delete_message_days": delete_days, "reason": ban_reason}
        )

        if resp and resp.status_code in [200, 204]:
            banned_count += 1
            print(f"{SUCCESS} Banned:{red} {banned_count:<6}{white} | User:{red} {username}", reset)
        else:
            failed_count += 1
            code = resp.status_code if resp else "None"
            print(f"{ERROR} Failed | User:{red} {username}{white} | Code:{red} {code}", reset)

        time.sleep(delay)

    Scroll(f"""
 {SUCCESS} Banned :{red} {banned_count}{white}
 {SUCCESS} Failed :{red} {failed_count}{white}
""")

    Continue()
    Reset()

except Exception as e:
    Error(e)