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

Title("Vanity Url Sniper")

Scroll(GradientBanner(discord_banner))

try:
    token = ChoiceToken()

    server_id = input(f"{INPUT} Server Id {red}->{reset} ").strip()
    if not server_id or not server_id.isdigit():
        ErrorId()

    vanity_code = input(f"{INPUT} Vanity Code {red}->{reset} ").strip()
    if not vanity_code:
        ErrorInput()

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

    print(f"{LOADING} Fetching server..", reset)

    try:
        guild_response = requests.get(
            f"https://discord.com/api/v9/guilds/{server_id}",
            headers=headers,
            timeout=10
        )
    except Exception:
        print(f"{ERROR} Could not connect!", reset)
        Continue()
        Reset()

    if guild_response.status_code != 200:
        print(f"{ERROR} Could not access server!", reset)
        Continue()
        Reset()

    guild_name = guild_response.json().get("name", "None")

    print(f"{SUCCESS} Server:{red} {guild_name}", reset)
    print(f"{SUCCESS} Vanity:{red} {vanity_code}", reset)
    print(f"{LOADING} Sniping.. Press{red} Ctrl+C{white} to stop.", reset)

    attempt = 0

    try:
        while True:
            attempt += 1

            try:
                check_response = requests.get(
                    f"https://discord.com/api/v9/invites/{vanity_code}",
                    headers=headers,
                    timeout=10
                )

                if check_response.status_code == 429:
                    retry = check_response.json().get("retry_after", 1)
                    time.sleep(retry)
                    continue

                if check_response.status_code == 404:
                    print(f"{LOADING} Attempt:{red} {attempt:<6}{white} | Available! Claiming..", reset)

                    try:
                        claim_response = requests.patch(
                            f"https://discord.com/api/v9/guilds/{server_id}/vanity-url",
                            headers=headers,
                            json={"code": vanity_code},
                            timeout=10
                        )

                        if claim_response.status_code == 200:
                            print(f"{SUCCESS} Vanity url claimed:{red} {vanity_code}", reset)
                            break
                        elif claim_response.status_code == 429:
                            retry = claim_response.json().get("retry_after", 1)
                            print(f"{ERROR} Rate limited!", reset)
                            time.sleep(retry)
                            continue
                        else:
                            print(f"{ERROR} Could not claim!", reset)
                    except Exception:
                        print(f"{ERROR} Could not claim vanity url!", reset)
                else:
                    print(f"{LOADING} Attempt:{red} {attempt:<6}{white} | Taken", reset)

            except requests.exceptions.Timeout:
                print(f"{ERROR} Timeout on attempt:{red} {attempt}", reset)
            except Exception:
                print(f"{ERROR} Error on attempt:{red} {attempt}", reset)

            time.sleep(delay)

    except KeyboardInterrupt:
        print(f"\n{INFO} Stopped.", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)