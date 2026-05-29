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
    import json
    import threading
    import time
    import websocket
except Exception as e:
    MissingModule(e)

Title("Token Onliner")

Scroll(GradientBanner(discord_banner))

try:
    token = ChoiceToken()

    Scroll(f"""
 {PREFIX}01{SUFFIX} Online
 {PREFIX}02{SUFFIX} Idle
 {PREFIX}03{SUFFIX} Do Not Disturb
 {PREFIX}04{SUFFIX} Invisible
""")

    status_choice = input(f"{INPUT} Status {red}->{reset} ").strip().lstrip("0")

    status_map = {
        "1": "online",
        "2": "idle",
        "3": "dnd",
        "4": "invisible",
    }

    if status_choice not in status_map:
        ErrorChoice()

    status         = status_map[status_choice]
    stop_event     = threading.Event()
    max_reconnects = 5
    state          = {"ready": False, "reconnect_count": 0}

    def Connect():
        while state["reconnect_count"] <= max_reconnects and not stop_event.is_set():
            try:
                if state["reconnect_count"] == 0:
                    print(f"{LOADING} Connecting..", reset)
                else:
                    print(f"{LOADING} Reconnecting.. ({state['reconnect_count']}/{max_reconnects})", reset)

                ws       = websocket.WebSocket()
                sequence = None

                ws.settimeout(30)
                ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")

                heartbeat_interval = None

                def SendHeartbeat():
                    while not stop_event.is_set():
                        try:
                            ws.send(json.dumps({"op": 1, "d": sequence}))
                            time.sleep(heartbeat_interval / 1000)
                        except Exception:
                            break

                while not stop_event.is_set():
                    try:
                        result = ws.recv()
                    except Exception:
                        break

                    if not result:
                        break

                    try:
                        data = json.loads(result)
                    except Exception:
                        continue

                    op = data.get("op")
                    t  = data.get("t")

                    if data.get("s"):
                        sequence = data["s"]

                    if op == 10:
                        heartbeat_interval = data["d"]["heartbeat_interval"]
                        threading.Thread(target=SendHeartbeat, daemon=True).start()
                        ws.send(json.dumps({
                            "op": 2,
                            "d" : {
                                "token"     : token,
                                "properties": {"$os": platform_pc.lower(), "$browser": "discord.py", "$device": platform_pc.lower()},
                                "presence"  : {"activities": [], "status": status, "since": 0, "afk": False},
                            }
                        }))

                    elif op == 11:
                        pass

                    elif op == 9:
                        print(f"{ERROR} Invalid session!", reset)
                        stop_event.set()
                        break

                    elif op == 7:
                        print(f"{LOADING} Reconnecting (server request)..", reset)
                        break

                    elif op == 0 and t == "READY":
                        state["ready"]           = True
                        state["reconnect_count"] = 0
                        print(f"{SUCCESS} Token is now {status}!", reset)
                        print(f"{INFO} Keep the tool open to maintain the status.", reset)

                try:
                    ws.close()
                except Exception:
                    pass

            except KeyboardInterrupt:
                stop_event.set()
                break
            except Exception:
                pass

            if not stop_event.is_set():
                state["reconnect_count"] += 1
                if state["reconnect_count"] <= max_reconnects:
                    time.sleep(5)
                else:
                    print(f"{ERROR} Max reconnects reached!", reset)
                    break

    try:
        Connect()
    except KeyboardInterrupt:
        stop_event.set()

    if not state["ready"]:
        print(f"{ERROR} Could not bring token online!", reset)
    else:
        print(f"{INFO} Disconnected.", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)