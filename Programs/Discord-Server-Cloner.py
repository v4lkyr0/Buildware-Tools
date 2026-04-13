# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import time
except Exception as e:
    MissingModule(e)

Title("Discord Server Cloner")
Connection()
CheckGithubStar()

try:
    token = ChoiceToken()
    
    source_id = input(f"{INPUT} Source Server ID {red}->{reset} ").strip()
    if not source_id:
        ErrorInput()
    
    target_id = input(f"{INPUT} Target Server ID {red}->{reset} ").strip()
    if not target_id:
        ErrorInput()
    
    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": RandomUserAgents()}
    
    print(f"{LOADING} Fetching Source Server..", reset)
    
    source_response = requests.get(f"https://discord.com/api/v9/guilds/{source_id}", headers=headers)
    
    if source_response.status_code != 200:
        print(f"{ERROR} Cannot access Source Server!", reset)
        Continue()
        Reset()
    
    source_data = source_response.json()
    source_name = source_data.get("name", "Unknown")
    
    print(f"{LOADING} Fetching Target Server..", reset)
    
    target_response = requests.get(f"https://discord.com/api/v9/guilds/{target_id}", headers=headers)
    
    if target_response.status_code != 200:
        print(f"{ERROR} Cannot access Target Server!", reset)
        Continue()
        Reset()
    
    target_data = target_response.json()
    target_name = target_data.get("name", "Unknown")
    
    print(f"{INFO} Source:{red} {source_name}", reset)
    print(f"{INFO} Target:{red} {target_name}", reset)
    print(f"{LOADING} Cloning Server..", reset)
    
    print(f"{LOADING} Deleting Target channels..", reset)
    
    channels_response = requests.get(f"https://discord.com/api/v9/guilds/{target_id}/channels", headers=headers)
    
    if channels_response.status_code == 200:
        channels = channels_response.json()
        for channel in channels:
            try:
                requests.delete(f"https://discord.com/api/v9/channels/{channel['id']}", headers=headers)
                print(f"{SUCCESS} Deleted:{red} {channel.get('name', 'Unknown')}", reset)
                time.sleep(0.3)
            except:
                pass
    
    print(f"{LOADING} Cloning channels..", reset)
    
    source_channels_response = requests.get(f"https://discord.com/api/v9/guilds/{source_id}/channels", headers=headers)
    
    if source_channels_response.status_code == 200:
        source_channels = sorted(source_channels_response.json(), key=lambda x: x.get("position", 0))
        
        for channel in source_channels:
            try:
                channel_data = {
                    "name": channel.get("name"),
                    "type": channel.get("type"),
                    "topic": channel.get("topic"),
                    "position": channel.get("position"),
                    "permission_overwrites": channel.get("permission_overwrites", []),
                    "nsfw": channel.get("nsfw", False),
                    "rate_limit_per_user": channel.get("rate_limit_per_user", 0)
                }
                
                create_response = requests.post(
                    f"https://discord.com/api/v9/guilds/{target_id}/channels",
                    headers=headers,
                    json=channel_data
                )
                
                if create_response.status_code == 201:
                    print(f"{SUCCESS} Created:{red} {channel.get('name', 'Unknown')}", reset)
                else:
                    print(f"{ERROR} Failed:{red} {channel.get('name', 'Unknown')}", reset)
                
                time.sleep(0.5)
            except:
                print(f"{ERROR} Error:{red} {channel.get('name', 'Unknown')}", reset)
    
    print(f"{SUCCESS} Server cloned!", reset)
    
    Continue()
    Reset()

except Exception as e:
    Error(e)