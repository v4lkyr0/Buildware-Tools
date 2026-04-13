# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import time
except Exception as e:
    MissingModule(e)

Title("Discord Server Unban All")
Connection()

try:
    token = ChoiceToken()
    
    server_id = input(f"{INPUT} Server Id {red}->{reset} ").strip()
    if not server_id:
        ErrorId()
    
    DEFAULT_ACTION_DELAY = 0.5
    MIN_ACTION_DELAY = 0.1
    
    delay = input(f"{INPUT} Delay {red}->{reset} ").strip()
    try:
        delay = float(delay)
        if delay < MIN_ACTION_DELAY:
            delay = MIN_ACTION_DELAY
    except ValueError:
        delay = DEFAULT_ACTION_DELAY
    
    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": RandomUserAgents()}
    
    print(f"{LOADING} Fetching banned users..", reset)
    
    bans_response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/bans", headers=headers)
    
    if bans_response.status_code != 200:
        print(f"{ERROR} Cannot access Server bans!", reset)
        Continue()
        Reset()
    
    bans = bans_response.json()
    
    if not bans:
        print(f"{INFO} No banned users found!", reset)
        Continue()
        Reset()
    
    print(f"{INFO} Found {len(bans)} banned user(s)", reset)
    print(f"{LOADING} Starting unban process..", reset)
    
    unbanned_count = 0
    
    for ban in bans:
        user_id = ban.get("user", {}).get("id")
        username = ban.get("user", {}).get("username", "Unknown")
        
        try:
            response = requests.delete(f"https://discord.com/api/v9/guilds/{server_id}/bans/{user_id}", headers=headers)
            
            if response.status_code in [200, 204]:
                unbanned_count += 1
                print(f"{SUCCESS} Unbanned:{red} {unbanned_count:<6} {white}| Username:{red} {username}", reset)
            else:
                print(f"{ERROR} Status:{red} Failed  {white}| Username:{red} {username}", reset)
            
            time.sleep(delay)
        except:
            print(f"{ERROR} Status:{red} Error   {white}| Username:{red} {username}", reset)
    
    print(f"\n{INFO} Total unbanned:{red} {unbanned_count}/{len(bans)}", reset)
    
    Continue()
    Reset()

except Exception as e:
    Error(e)
