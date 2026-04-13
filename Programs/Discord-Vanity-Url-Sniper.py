# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import time
except Exception as e:
    MissingModule(e)

Title("Discord Vanity Url Sniper")
Connection()

try:
    token = ChoiceToken()
    
    server_id = input(f"{INPUT} Server ID {red}->{reset} ").strip()
    if not server_id:
        ErrorInput()
    
    vanity_code = input(f"{INPUT} Vanity Code {red}->{reset} ").strip()
    if not vanity_code:
        ErrorInput()
    
    DEFAULT_CHECK_DELAY = 0.5
    MIN_CHECK_DELAY = 0.1
    
    delay = input(f"{INPUT} Check Delay {red}->{reset} ").strip()
    try:
        delay = float(delay)
        if delay < MIN_CHECK_DELAY:
            delay = MIN_CHECK_DELAY
    except ValueError:
        delay = DEFAULT_CHECK_DELAY
    
    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": RandomUserAgents()}
    
    print(f"{LOADING} Verifying Server access..", reset)
    
    guild_response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}", headers=headers)
    
    if guild_response.status_code != 200:
        print(f"{ERROR} Cannot access Server!", reset)
        Continue()
        Reset()
    
    guild_name = guild_response.json().get("name", "Unknown")
    
    print(f"{INFO} Server:{red} {guild_name}", reset)
    print(f"{INFO} Vanity:{red} {vanity_code}", reset)
    print(f"{LOADING} Sniping Vanity Url..", reset)
    
    attempt = 0
    
    while True:
        attempt += 1
        
        try:
            check_response = requests.get(f"https://discord.com/api/v9/invites/{vanity_code}", headers=headers)
            
            if check_response.status_code == 404:
                print(f"{LOADING} Attempt:{red} {attempt:<6} {white}| Status:{red} Available {white}| Claiming..", reset)
                
                claim_response = requests.patch(
                    f"https://discord.com/api/v9/guilds/{server_id}/vanity-url",
                    headers=headers,
                    json={"code": vanity_code}
                )
                
                if claim_response.status_code == 200:
                    print(f"{SUCCESS} Vanity Url claimed!", reset)
                    break
                else:
                    print(f"{ERROR} Failed to claim Vanity Url!", reset)
            else:
                print(f"{LOADING} Attempt:{red} {attempt:<6} {white}| Status:{red} Taken    {white}| Waiting..", reset)
        
        except Exception as e:
            print(f"{ERROR} Attempt:{red} {attempt:<6} {white}| Status:{red} Error    {white}| {e}", reset)
        
        time.sleep(delay)
    
    Continue()
    Reset()

except Exception as e:
    Error(e)