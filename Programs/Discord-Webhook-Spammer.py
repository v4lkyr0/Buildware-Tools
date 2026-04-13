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

Title("Discord Webhook Spammer")
Connection()

try:
    webhook = ChoiceWebhook()

    print()
    message = input(f"{INPUT} Message {red}->{reset} ").strip()
    if not message:
        ErrorInput()

    try:
        amount = int(input(f"{INPUT} Amount {red}->{reset} ").strip())
    except ValueError:
        ErrorNumber()

    if amount <= 0:
        ErrorNumber()

    try:
        threads = int(input(f"{INPUT} Threads {red}->{reset} ").strip())
    except ValueError:
        ErrorNumber()

    if threads <= 0:
        ErrorNumber()

    print()

    print(f"{LOADING} Starting Webhook Spammer..", reset)

    success_count = 0
    lock = threading.Lock()

    def Spam():
        global success_count, lock

        while success_count < amount:
            try:
                time.sleep(0.1)

                headers = {"Content-Type": "application/json", "User-Agent": RandomUserAgents()}
                data = {"content": message}

                response = requests.post(webhook, json=data, headers=headers)
                if response.status_code == 204:
                    with lock:
                        success_count += 1
                        print(f"{SUCCESS} Status:{red} Sent         {white}| Message:{red} {message}", reset)
                elif response.status_code == 429:
                    try:
                        retry_after = response.json().get("retry_after", 1)
                    except:
                        retry_after = 1
                    print(f"{ERROR} Status:{red} Rate Limited {white}| Message:{red} {message}", reset)
                    time.sleep(retry_after)
                else:
                    print(f"{ERROR} Status:{red} Not Sent     {white}| Message:{red} {message}", reset)
            except:
                print(f"{ERROR} Status:{red} Error        {white}| Message:{red} {message}", reset)

    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=Spam)
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()

    Continue()
    Reset()

except Exception as e:
    Error(e)