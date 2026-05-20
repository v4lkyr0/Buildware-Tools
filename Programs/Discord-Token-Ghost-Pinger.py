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

Title("Token Ghost Pinger")

Scroll(GradientBanner(discord_banner))

try:
    token = ChoiceToken()

    message = input(f"{INPUT} Message {red}->{reset} ").strip()

    try:
        delay_delete = float(input(f"{INPUT} Delay Before Delete {red}->{reset} ").strip())
        if delay_delete < 0:
            delay_delete = 0.1
    except:
        delay_delete = 0.1

    try:
        delay_between = float(input(f"{INPUT} Delay Between Pings {red}->{reset} ").strip())
        if delay_between < 0:
            delay_between = 0.5
    except:
        delay_between = 0.5

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

    def ApiPost(url, json=None):
        while True:
            try:
                r = requests.post(url, headers=headers, json=json or {}, timeout=10)
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

    print(f"{LOADING} Fetching friends..", reset)

    r = ApiGet("https://discord.com/api/v9/users/@me/relationships")

    if not r or r.status_code != 200:
        print(f"{ERROR} Could not fetch friends!", reset)
        Continue()
        Reset()

    friends = [rel for rel in r.json() if rel.get("type") == 1]

    if not friends:
        print(f"{ERROR} No friends found!", reset)
        Continue()
        Reset()

    print(f"{SUCCESS} Found:{red} {len(friends)}{white} friend(s)", reset)
    print(f"{LOADING} Starting..", reset)

    pinged_count = 0
    failed_count = 0

    for friend in friends:
        user_id  = friend.get("id")
        username = friend.get("user", {}).get("username", "None")

        if not user_id:
            continue

        dm_response = ApiPost(
            "https://discord.com/api/v9/users/@me/channels",
            json={"recipient_id": user_id}
        )

        if not dm_response or dm_response.status_code != 200:
            failed_count += 1
            print(f"{ERROR} Failed | User:{red} {username}", reset)
            time.sleep(delay_between)
            continue

        channel_id   = dm_response.json().get("id")
        ping_content = f"<@{user_id}> {message}" if message else f"<@{user_id}>"

        ping_response = ApiPost(
            f"https://discord.com/api/v9/channels/{channel_id}/messages",
            json={"content": ping_content}
        )

        if not ping_response or ping_response.status_code not in [200, 201]:
            failed_count += 1
            print(f"{ERROR} Failed | User:{red} {username}", reset)
            time.sleep(delay_between)
            continue

        message_id = ping_response.json().get("id")

        time.sleep(delay_delete)

        delete_response = ApiDelete(
            f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}"
        )

        if delete_response and delete_response.status_code == 204:
            pinged_count += 1
            print(f"{SUCCESS} Pinged | User:{red} {username}", reset)
        else:
            failed_count += 1
            print(f"{ERROR} Failed | User:{red} {username}", reset)

        time.sleep(delay_between)

    print(f"\n{SUCCESS} Completed!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)