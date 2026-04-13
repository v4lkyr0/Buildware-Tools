# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
except Exception as e:
    MissingModule(e)

Title("Discord Token Leaver")
Connection()

try:
    token = ChoiceToken()
    
    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": RandomUserAgents()}
    guilds_id = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers).json()

    if not guilds_id:
        print(f"{ERROR} No Server found!", reset)
        Continue()
        Reset()

    print(f"{LOADING} Leaving all Servers..", reset)

    for guild in guilds_id:
        try:
            response = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{guild['id']}", headers=headers)
            if response.status_code in [200, 204]:
                print(f"{SUCCESS} Status:{red} Left    {white}| Server:{red} {guild['name']}", reset)
            elif response.status_code == 400:
                response = requests.delete(f"https://discord.com/api/v9/guilds/{guild['id']}", headers=headers)
                if response.status_code in [200, 204]:
                    print(f"{SUCCESS} Status:{red} Left    {white}| Server:{red} {guild['name']}", reset)
                else:
                    print(f"{ERROR} Status:{red} Failed  {white}| Server:{red} {guild['name']}", reset)
            else:
                print(f"{ERROR} Status:{red} Failed  {white}| Server:{red} {guild['name']}", reset)
        except:
            print(f"{ERROR} Status:{red} Error   {white}| Server:{red} {guild['name']}", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)