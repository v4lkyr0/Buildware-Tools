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

Title("Token Spammer")

Scroll(GradientBanner(discord_banner))

try:
    token      = ChoiceToken()
    channel_id = input(f"{INPUT} Channel Id {red}->{reset} ").strip()
    message    = input(f"{INPUT} Message {red}->{reset} ").strip()

    if not channel_id or not channel_id.isdigit():
        ErrorId()

    if not message:
        ErrorInput()

    try:
        message_limit = int(input(f"{INPUT} Total Messages {red}->{reset} ").strip())
        if message_limit < 0:
            message_limit = 0
    except:
        message_limit = 0

    try:
        threads_number = int(input(f"{INPUT} Threads {red}->{reset} ").strip())
        if threads_number <= 0:
            ErrorNumber()
        if threads_number > 50:
            threads_number = 50
    except:
        ErrorNumber()

    print(f"{LOADING} Starting.. Press{red} Ctrl+C{white} to stop.", reset)

    stats = {"sent": 0, "failed": 0}
    lock  = threading.Lock()

    def Spammer():
        with lock:
            if message_limit > 0 and stats["sent"] >= message_limit:
                return

        try:
            headers  = {
                "Authorization": token,
                "Content-Type" : "application/json",
                "User-Agent"   : RandomUserAgents(),
            }
            response = requests.post(
                f"https://discord.com/api/v9/channels/{channel_id}/messages",
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
                print(f"{SUCCESS} Sent | Messages:{red} {stats['sent']:<6}{white} | Channel:{red} {channel_id}", reset)
            else:
                with lock:
                    stats["failed"] += 1
                print(f"{ERROR} Failed | Channel:{red} {channel_id}{white} | Code:{red} {response.status_code}", reset)

        except Exception:
            with lock:
                stats["failed"] += 1
            print(f"{ERROR} Error | Channel:{red} {channel_id}", reset)

    try:
        while True:
            if message_limit > 0 and stats["sent"] >= message_limit:
                break
            threads = [threading.Thread(target=Spammer, daemon=True) for _ in range(threads_number)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
    except KeyboardInterrupt:
        pass

    print(f"\n{SUCCESS} Completed!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)