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
    import threading
    import time
except Exception as e:
    MissingModule(e)

Title("Token Mass Dm")

Scroll(GradientBanner(discord_banner))

try:
    token = ChoiceToken()

    message = input(f"{INPUT} Message {red}->{reset} ").strip()
    if not message:
        ErrorInput()

    try:
        repetitions = int(input(f"{INPUT} Repetitions {red}->{reset} ").strip())
        if repetitions <= 0:
            ErrorNumber()
    except:
        ErrorNumber()

    headers = {
        "Authorization": token,
        "Content-Type" : "application/json",
        "User-Agent"   : RandomUserAgents(),
    }

    print(f"{LOADING} Fetching DMs..", reset)

    try:
        r = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers, timeout=10)
        if r.status_code != 200:
            print(f"{ERROR} Could not fetch DMs!", reset)
            Continue()
            Reset()
        channels = r.json()
    except Exception:
        print(f"{ERROR} Could not connect!", reset)
        Continue()
        Reset()

    dm_channels = [c for c in channels if c.get("type") == 1]

    if not dm_channels:
        print(f"{ERROR} No DMs found!", reset)
        Continue()
        Reset()

    print(f"{SUCCESS} Found:{red} {len(dm_channels)}{white} DM(s)", reset)
    print(f"{LOADING} Sending..", reset)

    sent_count   = 0
    failed_count = 0
    lock         = threading.Lock()

    stats = {"sent": 0, "failed": 0}

    def SendDm(channel):
        recipients = channel.get("recipients", [])
        username   = recipients[0].get("username", "None") if recipients else "None"

        try:
            response = requests.post(
                f"https://discord.com/api/v9/channels/{channel['id']}/messages",
                headers=headers,
                json={"content": message},
                timeout=10
            )

            if response.status_code == 429:
                retry = response.json().get("retry_after", 1)
                time.sleep(retry)
                return

            if response.status_code in [200, 201]:
                with lock:
                    stats["sent"] += 1
                print(f"{SUCCESS} Sent | User:{red} {username}{white} | Total:{red} {stats['sent']}", reset)
            else:
                with lock:
                    stats["failed"] += 1
                print(f"{ERROR} Failed | User:{red} {username}{white} | Code:{red} {response.status_code}", reset)

        except Exception:
            with lock:
                stats["failed"] += 1
            print(f"{ERROR} Error | User:{red} {username}", reset)

        time.sleep(0.5)

    for _ in range(repetitions):
        threads = [threading.Thread(target=SendDm, args=(channel,), daemon=True) for channel in dm_channels]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    print(f"\n{SUCCESS} Completed!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)