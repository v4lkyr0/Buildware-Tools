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

Title("Token Status Changer")

Scroll(GradientBanner(discord_banner))

try:
    token      = ChoiceToken()
    new_status = input(f"{INPUT} Status {red}->{reset} ").strip()

    if len(new_status) > 128:
        print(f"{ERROR} Status too long!", reset)
        Continue()
        Reset()

    headers = {
        "Authorization": token,
        "Content-Type" : "application/json",
        "User-Agent"   : RandomUserAgents(),
    }

    print(f"{LOADING} Changing..", reset)

    try:
        response = requests.patch(
            "https://discord.com/api/v9/users/@me/settings",
            headers=headers,
            json={"custom_status": {"text": new_status}},
            timeout=10
        )

        if response.status_code == 200:
            print(f"{SUCCESS} Status changed!", reset)
        elif response.status_code == 401:
            print(f"{ERROR} Invalid token!", reset)
        elif response.status_code == 429:
            retry = response.json().get("retry_after", 1)
            print(f"{ERROR} Rate limited!", reset)
        else:
            print(f"{ERROR} Could not change status!", reset)

    except requests.exceptions.Timeout:
        print(f"{ERROR} Request timed out!", reset)
    except Exception:
        print(f"{ERROR} Could not change status!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)