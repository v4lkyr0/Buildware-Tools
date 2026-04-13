# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import threading
    import time
except Exception as e:
    MissingModule(e)

Title("Discord Token Mass Dm")
Connection()
CheckGithubStar()

try:
    token = ChoiceToken()
    message = input(f"{INPUT} Message {red}->{reset} ").strip()
    if not message:
        ErrorInput()

    try:
        repetitions = int(input(f"{INPUT} Repetitions {red}->{reset} ").strip())
    except:
        ErrorNumber()

    if repetitions <= 0:
        ErrorNumber()

    print(f"{LOADING} Sending Dm..", reset)

    sent_count = 0
    failed_count = 0

    def MassDm(token, channels, message):
        global sent_count, failed_count
        for channel in channels:
            for user in [x["username"] for x in channel.get("recipients", [])]:
                try:
                    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": RandomUserAgents()}
                    response = requests.post(f"https://discord.com/api/v9/channels/{channel['id']}/messages", headers=headers, json={"content": message})
                    if response.status_code in [200, 201]:
                        sent_count += 1
                        print(f"{SUCCESS} Status:{red} Sent    {white}| Username:{red} {user} {white}| Total:{red} {sent_count}", reset)
                    else:
                        failed_count += 1
                        print(f"{ERROR} Status:{red} Failed  {white}| Username:{red} {user}", reset)
                except:
                    failed_count += 1
                    print(f"{ERROR} Status:{red} Error   {white}| Username:{red} {user}", reset)
                time.sleep(0.1)

    channel_ids = requests.get("https://discord.com/api/v9/users/@me/channels", headers={'Authorization': token, 'User-Agent': RandomUserAgents()}).json()

    if not channel_ids:
        print(f"{ERROR} No Dm found!", reset)
        Continue()
        Reset()

    CHUNK_SIZE = 3
    threads = []

    for _ in range(repetitions):
        for channel_chunk in [channel_ids[j:j+CHUNK_SIZE] for j in range(0, len(channel_ids), CHUNK_SIZE)]:
            t = threading.Thread(target=MassDm, args=(token, channel_chunk, message))
            t.start()
            threads.append(t)
            time.sleep(0.1)

    for thread in threads:
        thread.join()
    
    print(f"\n{INFO} Mass Dm Summary:", reset)
    print(f"{SUCCESS} Messages Sent:{red} {sent_count}", reset)
    print(f"{ERROR} Messages Failed:{red} {failed_count}", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)