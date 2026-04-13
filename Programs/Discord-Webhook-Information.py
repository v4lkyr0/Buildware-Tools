# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
except Exception as e:
    MissingModule(e)

Title("Discord Webhook Information")
Connection()

try:
    webhook = ChoiceWebhook()

    print(f"{LOADING} Retrieving Webhook Information..", reset)

    response = requests.get(webhook, headers={"User-Agent": RandomUserAgents()})
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"{ERROR} Failed to retrieve Webhook Information!", reset)
        Continue()
        Reset()

    webhook_url = webhook
    webhook_name = data.get('name', 'None')
    webhook_id = data.get('id', 'None')
    webhook_token = webhook.split("/")[-1] if "/" in webhook else "None"
    
    webhook_avatar = data.get('avatar')
    if webhook_avatar:
        webhook_avatar_url = f"https://cdn.discordapp.com/avatars/{webhook_id}/{webhook_avatar}.png"
    else:
        webhook_avatar_url = "None"

    if 'user' in data:
        webhook_creator = data['user'].get('username', 'None')
    else:
        webhook_creator = "None"

    webhook_type_raw = data.get('type')
    if webhook_type_raw == 1:
        webhook_type = "Incoming Webhook"
    elif webhook_type_raw == 2:
        webhook_type = "Channel Follower Webhook"
    elif webhook_type_raw == 3:
        webhook_type = "Application Webhook"
    else:
        webhook_type = f"Unknown {red}({white}{webhook_type_raw}{red})" if webhook_type_raw else "None"

    webhook_server_id = data.get('guild_id', 'None')
    webhook_channel_id = data.get('channel_id', 'None')

    Scroll(f"""
 {SUCCESS} Url        :{red} {webhook_url}
 {SUCCESS} Id         :{red} {webhook_id}
 {SUCCESS} Name       :{red} {webhook_name}
 {SUCCESS} Token      :{red} {webhook_token}
 {SUCCESS} Avatar Url :{red} {webhook_avatar_url}
 {SUCCESS} Type       :{red} {webhook_type}
 {SUCCESS} Server Id  :{red} {webhook_server_id}
 {SUCCESS} Channel Id :{red} {webhook_channel_id}
 {SUCCESS} Creator    :{red} {webhook_creator} {reset}
""")

    Continue()
    Reset()

except Exception as e:
    Error(e)