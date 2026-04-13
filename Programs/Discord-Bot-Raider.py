# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import time
except Exception as e:
    MissingModule(e)

Title("Discord Bot Raider")
Connection()

try:
    bot_token = ChoiceBot()
    
    server_id = input(f"{INPUT} Server ID {red}->{reset} ").strip()
    if not server_id:
        ErrorId()
    
    message = input(f"{INPUT} Spam Message {red}->{reset} ").strip()
    if not message:
        ErrorInput()
    
    message_limit_input = input(f"{INPUT} Total Messages {red}->{reset} ").strip()
    try:
        message_limit = int(message_limit_input)
        if message_limit < 0:
            message_limit = 0
    except ValueError:
        message_limit = 0
    
    DEFAULT_MESSAGE_DELAY = 0.5
    MIN_MESSAGE_DELAY = 0.1
    
    delay = input(f"{INPUT} Delay Between Messages {red}->{reset} ").strip()
    try:
        delay = float(delay)
        if delay < MIN_MESSAGE_DELAY:
            delay = MIN_MESSAGE_DELAY
    except ValueError:
        delay = DEFAULT_MESSAGE_DELAY
    
    headers = {"Authorization": f"Bot {bot_token}", "Content-Type": "application/json", "User-Agent": RandomUserAgents()}
    
    print(f"{LOADING} Fetching Server channels..", reset)
    
    channels_response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/channels", headers=headers)
    
    if channels_response.status_code != 200:
        print(f"{ERROR} Cannot access Server!", reset)
        Continue()
        Reset()
    
    channels = channels_response.json()
    text_channels = [c for c in channels if c.get("type") == 0]
    
    if not text_channels:
        print(f"{ERROR} No text channels found!", reset)
        Continue()
        Reset()
    
    print(f"{INFO} Found {len(text_channels)} text channel(s)", reset)
    print(f"{LOADING} Starting raid..", reset)
    
    message_count = 0
    
    while True:
        if message_limit > 0 and message_count >= message_limit:
            print(f"\n{INFO} Message limit reached:{red} {message_count}", reset)
            break
        
        for channel in text_channels:
            try:
                channel_id = channel.get("id")
                channel_name = channel.get("name", "Unknown")
                
                response = requests.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/messages",
                    headers=headers,
                    json={"content": message}
                )
                
                if response.status_code in [200, 201]:
                    message_count += 1
                    print(f"{SUCCESS} Messages:{red} {message_count:<6} {white}| Channel:{red} {channel_name}", reset)
                else:
                    print(f"{ERROR} Status:{red} Failed  {white}| Channel:{red} {channel_name}", reset)
                
                time.sleep(delay)
            
            except KeyboardInterrupt:
                print(f"\n{INFO} Raid stopped by user", reset)
                print(f"{INFO} Total messages sent:{red} {message_count}", reset)
                Continue()
                Reset()
            except Exception as e:
                print(f"{ERROR} Status:{red} Error   {white}| Error:{red} {e}", reset)
    
    print(f"\n{INFO} Raid completed", reset)
    print(f"{INFO} Total messages sent:{red} {message_count}", reset)
    Continue()
    Reset()

except Exception as e:
    Error(e)
