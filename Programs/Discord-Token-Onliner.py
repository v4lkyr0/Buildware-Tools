# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import json
    import threading
    import time
    import websocket
except Exception as e:
    MissingModule(e)

Title("Discord Token Onliner")
Connection()

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
        "4": "invisible"
    }
    
    if status_choice not in status_map:
        ErrorChoice()

    status = status_map[status_choice]
    
    ws = websocket.WebSocket()
    ws.settimeout(30)
    ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')
    
    print(f"{LOADING} Connecting to Discord Gateway..", reset)
    
    stop_heartbeat = threading.Event()
    ready_received = False

    while True:
        try:
            result = ws.recv()
            if not result:
                print(f"{ERROR} Connection closed by Discord!", reset)
                break

            data = json.loads(result)
        
            if data['op'] == 10: 
                heartbeat_interval = data['d']['heartbeat_interval']
                print(f"{INFO} Connected to Discord Gateway!", reset)

                def SendHeartbeat():
                    while not stop_heartbeat.is_set():
                        try:
                            heartbeat = {'op': 1, 'd': None}
                            ws.send(json.dumps(heartbeat))
                            time.sleep(heartbeat_interval / 1000)
                        except:
                            break

                heartbeat_thread = threading.Thread(target=SendHeartbeat, daemon=True)
                heartbeat_thread.start()
            
                auth = {'op': 2,
                        'd': {'token': token,
                              'properties': {'$os': platform_pc.lower(),
                                             '$browser': 'RTB',
                                             '$device': f'{platform_pc.lower()} Device'},
                              'presence': {'activities': [],
                                           'status': status,
                                           'since': 0,
                                           'afk': False}}}
                ws.send(json.dumps(auth))
        
            elif data['op'] == 9:
                print(f"{ERROR} Invalid session!", reset)
                stop_heartbeat.set()
                break

            elif data['op'] == 0:
                if data['t'] == 'READY':
                    ready_received = True
                    print(f"{INFO} Keep the tool open to maintain the Token online status.", reset)
                    print(f"{SUCCESS} Token is now online!", reset)

        except:
            print(f"{ERROR} Error while trying to maintain connection!", reset)
            stop_heartbeat.set()
            break

    if not ready_received:
        print(f"{ERROR} Failed to bring Token online!", reset)

    stop_heartbeat.set()
    ws.close()

    Continue()
    Reset()

except Exception as e:
    Error(e)