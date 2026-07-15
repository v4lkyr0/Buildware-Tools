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

Title("Token Joiner")

Scroll(GradientBanner(discord_banner))

try:
    token = ChoiceToken()

    invite = input(f"{INPUT} Invite {red}->{reset} ").strip()
    if not invite:
        ErrorInput()

    invite_code = invite.split("/")[-1].strip()

    print(f"{LOADING} Joining..", reset)

    headers = {
        "Authorization": token,
        "Content-Type" : "application/json",
        "User-Agent"   : RandomUserAgents(),
    }

    try:
        response = requests.post(
            f"https://discord.com/api/v9/invites/{invite_code}",
            headers=headers,
            json={},
            timeout=10
        )

        if response.status_code == 200:
            guild = response.json().get("guild", {})
            print(f"{SUCCESS} Joined:{red} {guild.get('name', 'None')}", reset)
        elif response.status_code == 401:
            print(f"{ERROR} Invalid token!", reset)
        elif response.status_code == 404:
            print(f"{ERROR} Invalid invite!", reset)
        elif response.status_code == 429:
            retry = response.json().get("retry_after", 1)
            print(f"{ERROR} Rate limited!", reset)
        elif response.status_code == 403:
            print(f"{ERROR} Cannot join server!", reset)
        else:
            print(f"{ERROR} Could not join server!", reset)

    except requests.exceptions.Timeout:
        print(f"{ERROR} Request timed out!", reset)
    except Exception:
        print(f"{ERROR} Could not join server!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)