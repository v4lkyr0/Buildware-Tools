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

Title("Bot Raider")

Scroll(GradientBanner(discord_banner))

try:
    bot_token = ChoiceBot()

    server_id = input(f"{INPUT} Server Id {red}->{reset} ").strip()
    if not server_id or not server_id.isdigit():
        ErrorId()

    message = input(f"{INPUT} Message {red}->{reset} ").strip()
    if not message:
        ErrorInput()

    try:
        message_limit = int(input(f"{INPUT} Total Messages {red}->{reset} ").strip())
        if message_limit < 0:
            message_limit = 0
    except:
        message_limit = 0

    try:
        delay = float(input(f"{INPUT} Delay {red}->{reset} ").strip())
        if delay < 0.1:
            delay = 0.1
    except:
        delay = 0.5

    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type" : "application/json",
        "User-Agent"   : RandomUserAgents(),
    }

    print(f"{LOADING} Fetching channels..", reset)

    try:
        channels_response = requests.get(
            f"https://discord.com/api/v9/guilds/{server_id}/channels",
            headers=headers,
            timeout=10
        )
    except Exception:
        print(f"{ERROR} Could not connect!", reset)
        Continue()
        Reset()

    if channels_response.status_code != 200:
        print(f"{ERROR} Could not fetch channels!", reset)
        Continue()
        Reset()

    channels      = channels_response.json()
    text_channels = [c for c in channels if c.get("type") == 0]

    if not text_channels:
        print(f"{ERROR} No text channels found!", reset)
        Continue()
        Reset()

    print(f"{SUCCESS} Found:{red} {len(text_channels)}{white} channel(s)", reset)
    print(f"{LOADING} Starting raid..", reset)

    message_count = 0
    failed_count  = 0

    try:
        while True:
            if message_limit > 0 and message_count >= message_limit:
                break

            for channel in text_channels:
                if message_limit > 0 and message_count >= message_limit:
                    break

                channel_id   = channel.get("id")
                channel_name = channel.get("name", "None")

                try:
                    response = requests.post(
                        f"https://discord.com/api/v9/channels/{channel_id}/messages",
                        headers=headers,
                        json={"content": message},
                        timeout=10
                    )

                    if response.status_code == 429:
                        retry = response.json().get("retry_after", 1)
                        print(f"{LOADING} Rate limited, waiting {round(retry, 1)}s..", reset)
                        time.sleep(retry)
                        continue

                    if response.status_code in [200, 201]:
                        message_count += 1
                        print(f"{SUCCESS} Sent:{red} {message_count:<6}{white} | Channel:{red} {channel_name}", reset)
                    else:
                        failed_count += 1
                        print(f"{ERROR} Failed | Channel:{red} {channel_name}{white} | Code:{red} {response.status_code}", reset)

                except requests.exceptions.Timeout:
                    failed_count += 1
                    print(f"{ERROR} Timeout | Channel:{red} {channel_name}", reset)
                except Exception:
                    failed_count += 1
                    print(f"{ERROR} Error | Channel:{red} {channel_name}", reset)

                time.sleep(delay)

    except KeyboardInterrupt:
        pass

    print(f"\n{SUCCESS} Completed!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)