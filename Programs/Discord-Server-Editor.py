# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
except Exception as e:
    MissingModule(e)

Title("Discord Server Editor")
Connection()

try:
    token = ChoiceToken()
    
    server_id = input(f"{INPUT} Server ID {red}->{reset} ").strip()
    if not server_id:
        ErrorInput()
    
    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": RandomUserAgents()}
    
    print(f"{LOADING} Fetching Server Information..", reset)
    
    guild_response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}", headers=headers)
    
    if guild_response.status_code != 200:
        print(f"{ERROR} Cannot access Server!", reset)
        Continue()
        Reset()
    
    guild_data = guild_response.json()
    current_name = guild_data.get("name", "Unknown")
    
    Scroll(f"""
 {INFO} Current Server Name :{red} {current_name}

 {PREFIX}01{SUFFIX} Change Name
 {PREFIX}02{SUFFIX} Change Description
 {PREFIX}03{SUFFIX} Change AFK Channel
 {PREFIX}04{SUFFIX} Change AFK Timeout
 {PREFIX}05{SUFFIX} Change Verification Level
 {PREFIX}06{SUFFIX} Change System Channel
""")
    
    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")
    
    if choice == "1":
        new_name = input(f"{INPUT} New Name {red}->{reset} ").strip()
        if not new_name:
            ErrorInput()
        
        print(f"{LOADING} Changing Server Name..", reset)
        
        response = requests.patch(
            f"https://discord.com/api/v9/guilds/{server_id}",
            headers=headers,
            json={"name": new_name}
        )
        
        if response.status_code == 200:
            print(f"{SUCCESS} Server Name changed!", reset)
        else:
            print(f"{ERROR} Failed to change Server Name!", reset)
    
    elif choice == "2":
        new_description = input(f"{INPUT} New Description {red}->{reset} ").strip()
        
        print(f"{LOADING} Changing Server Description..", reset)
        
        response = requests.patch(
            f"https://discord.com/api/v9/guilds/{server_id}",
            headers=headers,
            json={"description": new_description}
        )
        
        if response.status_code == 200:
            print(f"{SUCCESS} Server Description changed!", reset)
        else:
            print(f"{ERROR} Failed to change Server Description!", reset)
    
    elif choice == "3":
        channel_id = input(f"{INPUT} AFK Channel ID {red}->{reset} ").strip()
        if not channel_id:
            ErrorInput()
        
        print(f"{LOADING} Changing AFK Channel..", reset)
        
        response = requests.patch(
            f"https://discord.com/api/v9/guilds/{server_id}",
            headers=headers,
            json={"afk_channel_id": channel_id}
        )
        
        if response.status_code == 200:
            print(f"{SUCCESS} AFK Channel changed!", reset)
        else:
            print(f"{ERROR} Failed to change AFK Channel!", reset)
    
    elif choice == "4":
        print(f"{INFO} AFK Timeout values:{red} 60, 300, 900, 1800, 3600", reset)
        timeout = input(f"{INPUT} AFK Timeout {red}->{reset} ").strip()
        
        try:
            timeout = int(timeout)
            if timeout not in [60, 300, 900, 1800, 3600]:
                ErrorInput()
        except:
            ErrorInput()
        
        print(f"{LOADING} Changing AFK Timeout..", reset)
        
        response = requests.patch(
            f"https://discord.com/api/v9/guilds/{server_id}",
            headers=headers,
            json={"afk_timeout": timeout}
        )
        
        if response.status_code == 200:
            print(f"{SUCCESS} AFK Timeout changed!", reset)
        else:
            print(f"{ERROR} Failed to change AFK Timeout!", reset)
    
    elif choice == "5":
        print(f"{INFO} Verification levels:{red} 0=None, 1=Low, 2=Medium, 3=High, 4=Highest", reset)
        level = input(f"{INPUT} Verification Level {red}->{reset} ").strip()
        
        try:
            level = int(level)
            if level not in [0, 1, 2, 3, 4]:
                ErrorInput()
        except:
            ErrorInput()
        
        print(f"{LOADING} Changing Verification Level..", reset)
        
        response = requests.patch(
            f"https://discord.com/api/v9/guilds/{server_id}",
            headers=headers,
            json={"verification_level": level}
        )
        
        if response.status_code == 200:
            print(f"{SUCCESS} Verification Level changed!", reset)
        else:
            print(f"{ERROR} Failed to change Verification Level!", reset)
    
    elif choice == "6":
        channel_id = input(f"{INPUT} System Channel ID {red}->{reset} ").strip()
        if not channel_id:
            ErrorInput()
        
        print(f"{LOADING} Changing System Channel..", reset)
        
        response = requests.patch(
            f"https://discord.com/api/v9/guilds/{server_id}",
            headers=headers,
            json={"system_channel_id": channel_id}
        )
        
        if response.status_code == 200:
            print(f"{SUCCESS} System Channel changed!", reset)
        else:
            print(f"{ERROR} Failed to change System Channel!", reset)
    
    else:
        ErrorChoice()
    
    Continue()
    Reset()

except Exception as e:
    Error(e)