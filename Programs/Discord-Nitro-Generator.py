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
    import random
    import string
    import threading
    import json
except Exception as e:
    MissingModule(e)

Title("Nitro Generator")

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

    def SendWebhook(code):
        try:
            payload = {
                "embeds"    : [{
                    "title"      : "Nitro Found!",
                    "description": f"**Code:**\n```discord.gift/{code}```",
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

    def GenerateCode():
        return "".join(random.choices(string.ascii_letters + string.digits, k=16))

    def CheckCode():
        code = GenerateCode()
        try:
            response = requests.get(
                f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true",
                headers={"User-Agent": RandomUserAgents()},
                timeout=10
            )

            if response.status_code == 200:
                with lock:
                    found_count += 1
                print(f"{SUCCESS} Valid  | Code:{red} discord.gift/{code}", reset)
                threading.Thread(target=SendWebhook, args=(code,), daemon=True).start()

            elif response.status_code == 429:
                pass
            else:
                print(f"{ERROR} Invalid | Code:{red} discord.gift/{code}", reset)
        except Exception:
            pass

    try:
        while True:
            threads = [threading.Thread(target=CheckCode, daemon=True) for _ in range(threads_number)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
    except KeyboardInterrupt:
        print(f"\n{SUCCESS} Found:{red} {found_count}{white} code(s)!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)