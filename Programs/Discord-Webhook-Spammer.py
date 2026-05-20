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
    import threading
    import time
except Exception as e:
    MissingModule(e)

Title("Webhook Spammer")

Scroll(GradientBanner(discord_banner))

try:
    webhook = ChoiceWebhook()

    message = input(f"{INPUT} Message {red}->{reset} ").strip()
    if not message:
        ErrorInput()

    try:
        amount = int(input(f"{INPUT} Amount {red}->{reset} ").strip())
        if amount <= 0:
            ErrorNumber()
    except:
        ErrorNumber()

    try:
        threads_number = int(input(f"{INPUT} Threads {red}->{reset} ").strip())
        if threads_number <= 0:
            ErrorNumber()
        if threads_number > 50:
            threads_number = 50
    except:
        ErrorNumber()

    print(f"{LOADING} Starting..", reset)

    stats = {"sent": 0, "failed": 0}
    lock  = threading.Lock()
    stop  = threading.Event()

    def Spam():
        while not stop.is_set():
            with lock:
                if stats["sent"] >= amount:
                    break

            try:
                response = requests.post(
                    webhook,
                    json={"content": message},
                    headers={"Content-Type": "application/json", "User-Agent": RandomUserAgents()},
                    timeout=10
                )

                if response.status_code == 204:
                    with lock:
                        stats["sent"] += 1
                    print(f"{SUCCESS} Sent | Messages:{red} {stats['sent']}", reset)

                elif response.status_code == 429:
                    retry = response.json().get("retry_after", 1)
                    print(f"{ERROR} Rate limited!", reset)
                    time.sleep(retry)

                else:
                    with lock:
                        stats["failed"] += 1
                    print(f"{ERROR} Failed | Code:{red} {response.status_code}", reset)

            except requests.exceptions.Timeout:
                with lock:
                    stats["failed"] += 1
                print(f"{ERROR} Timeout!", reset)
            except Exception:
                with lock:
                    stats["failed"] += 1
                print(f"{ERROR} Error!", reset)

            time.sleep(0.1)

    try:
        threads = [threading.Thread(target=Spam, daemon=True) for _ in range(threads_number)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        stop.set()

    print(f"\n{SUCCESS} Completed!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)