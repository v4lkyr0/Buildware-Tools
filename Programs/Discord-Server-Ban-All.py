# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import time
except Exception as e:
    MissingModule(e)

Title("Discord Server Ban All")
Connection()
CheckGithubStar()

try:
    token = ChoiceToken()
    server_id = input(f"{INPUT} Server ID {red}->{reset} ").strip()
    if not server_id:
        ErrorId()
    
    ban_reason = input(f"{INPUT} Ban Reason {red}->{reset} ").strip()
    if not ban_reason:
        ban_reason = "Banned by Buildware-Tools"
    
    delete_days = input(f"{INPUT} Delete Message History {red}->{reset} ").strip()
    try:
        delete_days = int(delete_days)
        if delete_days < 0 or delete_days > 7:
            delete_days = 0
    except:
        delete_days = 0
    
    delay = input(f"{INPUT} Delay Between Bans {red}->{reset} ").strip()
    try:
        delay = float(delay)
        if delay < 0.1:
            delay = 0.1
    except:
        delay = 0.5
    
    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": RandomUserAgents()}
    
    print(f"{LOADING} Fetching Server members..", reset)
    
    members = []
    limit = 1000
    after = 0
    
    while True:
        response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/members?limit={limit}&after={after}", headers=headers, timeout=10)
        if response.status_code != 200:
            break
        batch = response.json()
        if not batch:
            break
        members.extend(batch)
        after = int(batch[-1]["user"]["id"])
        if len(batch) < limit:
            break
    
    if not members:
        print(f"{ERROR} No members found!", reset)
        Continue()
        Reset()
    
    print(f"{INFO} Found {len(members)} member(s)", reset)
    print(f"{LOADING} Starting ban process..", reset)
    
    banned_count = 0
    
    for member in members:
        user_id = member.get("user", {}).get("id")
        username = member.get("user", {}).get("username", "Unknown")
        
        try:
            ban_data = {"delete_message_days": delete_days, "reason": ban_reason}
            response = requests.put(f"https://discord.com/api/v9/guilds/{server_id}/bans/{user_id}", headers=headers, json=ban_data, timeout=10)
            
            if response.status_code in [200, 204]:
                banned_count += 1
                print(f"{SUCCESS} Banned:{red} {banned_count:<6} {white}| Username:{red} {username}", reset)
            elif response.status_code == 429:
                print(f"{ERROR} Status:{red} Limited {white}| Username:{red} {username}", reset)
                time.sleep(2)
            else:
                print(f"{ERROR} Status:{red} Failed  {white}| Username:{red} {username}", reset)
            
            time.sleep(delay)
        except:
            print(f"{ERROR} Status:{red} Error   {white}| Username:{red} {username}", reset)
    
    print(f"\n{INFO} Total banned:{red} {banned_count}/{len(members)}", reset)
    Continue()
    Reset()

except Exception as e:
    Error(e)
