# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import threading
except Exception as e:
    MissingModule(e)

Title("Discord Token Spammer")
Connection()

try:
    token          = ChoiceToken()
    channel_id     = input(f"{INPUT} Channel Id {red}->{reset} ").strip()
    message        = input(f"{INPUT} Message {red}->{reset} ").strip()
    
    message_limit_input = input(f"{INPUT} Total Messages {red}->{reset} ").strip()
    try:
        message_limit = int(message_limit_input)
        if message_limit < 0:
            message_limit = 0
    except ValueError:
        message_limit = 0
    
    try:
        threads_number = int(input(f"{INPUT} Threads {red}->{reset} ").strip())
    except ValueError:
        ErrorNumber()

    if not channel_id or not message:
        ErrorInput()
    if threads_number <= 0:
        ErrorNumber()

    print(f"{LOADING} Starting Token Spammer..", reset)
    
    message_count = 0
    max_messages_reached = False

    def Spammer(token, channel_id, message):
        global message_count, max_messages_reached
        
        if message_limit > 0 and message_count >= message_limit:
            max_messages_reached = True
            return
        
        try:
            headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": RandomUserAgents()}
            payload = {"content": message}

            response = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=payload)
            if response.status_code in [200, 201]:
                message_count += 1
                print(f"{SUCCESS} Status:{red} Sent    {white}| Messages:{red} {message_count:<6} {white}| Channel:{red} {channel_id}", reset)
            else:
                print(f"{ERROR} Status:{red} Failed  {white}| Channel Id:{red} {channel_id}", reset)
        except:
            print(f"{ERROR} Status:{red} Error   {white}| Channel Id:{red} {channel_id}", reset)

    def Request():
        threads = []
        try:
            for _ in range(threads_number):
                if message_limit > 0 and message_count >= message_limit:
                    break
                t = threading.Thread(target=Spammer, args=(token, channel_id, message))
                t.start()
                threads.append(t)
        except:
            ErrorNumber()

        for thread in threads:
            thread.join()

    while True:
        if message_limit > 0 and message_count >= message_limit:
            print(f"\n{INFO} Message limit reached:{red} {message_count}", reset)
            break
        Request()
    
    Continue()
    Reset()

except Exception as e:
    Error(e)