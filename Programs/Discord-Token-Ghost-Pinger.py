# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import time
except Exception as e:
    MissingModule(e)

Title("Discord Token Ghost Pinger")
Connection()

try:
    token = ChoiceToken()
    
    message = input(f"{INPUT} Message {red}->{reset} ").strip()

    delay_delete = input(f"{INPUT} Delay Before Delete {red}->{reset} ").strip()
    try:
        delay_delete = float(delay_delete)
        if delay_delete < 0:
            delay_delete = 0.1
    except:
        delay_delete = 0.1

    delay_between = input(f"{INPUT} Delay Between Pings {red}->{reset} ").strip()
    try:
        delay_between = float(delay_between)
        if delay_between < 0:
            delay_between = 0.5
    except:
        delay_between = 0.5

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": RandomUserAgents()
    }

    print(f"{LOADING} Fetching Friends..", reset)

    relationships = requests.get(
        "https://discord.com/api/v9/users/@me/relationships",
        headers=headers
    ).json()

    friends = [r for r in relationships if r.get("type") == 1]

    if not friends:
        print(f"{ERROR} No Friends found!", reset)
        Continue()
        Reset()

    print(f"{INFO} {len(friends)} Friend(s) found!", reset)
    print(f"{LOADING} Starting Ghost Pinger..", reset)

    for friend in friends:
        user_id  = friend["id"]
        username = friend["user"]["username"]

        try:
            dm_response = requests.post(
                "https://discord.com/api/v9/users/@me/channels",
                headers=headers,
                json={"recipient_id": user_id}
            )

            if dm_response.status_code != 200:
                print(f"{ERROR} Status:{red} Failed  {white}| Username:{red} {username}", reset)
                time.sleep(delay_between)
                continue

            channel_id = dm_response.json()["id"]

            ping_content = f"<@{user_id}> {message}" if message else f"<@{user_id}>"

            ping_response = requests.post(
                f"https://discord.com/api/v9/channels/{channel_id}/messages",
                headers=headers,
                json={"content": ping_content}
            )

            if ping_response.status_code not in [200, 201]:
                print(f"{ERROR} Status:{red} Failed  {white}| Username:{red} {username}", reset)
                time.sleep(delay_between)
                continue

            message_id = ping_response.json()["id"]
            
            time.sleep(delay_delete)

            delete_response = requests.delete(
                f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}",
                headers=headers
            )

            if delete_response.status_code == 204:
                print(f"{SUCCESS} Status:{red} Pinged  {white}| Username:{red} {username}", reset)
            else:
                print(f"{ERROR} Status:{red} Failed  {white}| Username:{red} {username}", reset)

        except:
            print(f"{ERROR} Status:{red} Error   {white}| Username:{red} {username}", reset)

        time.sleep(delay_between)

    Continue()
    Reset()

except Exception as e:
    Error(e)