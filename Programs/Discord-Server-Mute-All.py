# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    from datetime import datetime, timedelta, timezone
    import requests
    import time
except Exception as e:
    MissingModule(e)

Title("Discord Server Mute All")
Connection()

try:
    token = ChoiceToken()
    
    server_id = input(f"{INPUT} Server Id {red}->{reset} ").strip()
    if not server_id:
        ErrorId()
    
    DEFAULT_MUTE_DURATION = 60
    PERMANENT_MUTE = 0
    
    duration = input(f"{INPUT} Mute Duration {red}->{reset} ").strip()
    try:
        duration = int(duration)
        if duration < 0:
            duration = PERMANENT_MUTE
    except ValueError:
        duration = DEFAULT_MUTE_DURATION
    
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
    
    print(f"{LOADING} Fetching Server members..", reset)
    
    members = []
    limit = 1000
    after = 0
    
    while True:
        members_response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/members?limit={limit}&after={after}", headers=headers)
        
        if members_response.status_code != 200:
            break
        
        batch = members_response.json()
        
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
    print(f"{LOADING} Starting mute process..", reset)
    
    if duration > 0:
        timeout_until = (datetime.now(timezone.utc) + timedelta(minutes=duration)).isoformat()
    else:
        timeout_until = (datetime.now(timezone.utc) + timedelta(days=28)).isoformat()
    
    muted_count = 0
    
    for member in members:
        user_id = member.get("user", {}).get("id")
        username = member.get("user", {}).get("username", "Unknown")
        
        try:
            response = requests.patch(
                f"https://discord.com/api/v9/guilds/{server_id}/members/{user_id}",
                headers=headers,
                json={"communication_disabled_until": timeout_until}
            )
            
            if response.status_code == 200:
                muted_count += 1
                print(f"{SUCCESS} Muted:{red} {muted_count:<6} {white}| Username:{red} {username}", reset)
            else:
                print(f"{ERROR} Status:{red} Failed  {white}| Username:{red} {username}", reset)
            
            time.sleep(delay)
        except:
            print(f"{ERROR} Status:{red} Error   {white}| Username:{red} {username}", reset)
    
    print(f"\n{INFO} Total muted:{red} {muted_count}/{len(members)}", reset)
    
    Continue()
    Reset()

except Exception as e:
    Error(e)
