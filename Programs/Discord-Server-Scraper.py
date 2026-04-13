# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    from datetime import datetime
    import json
    import requests
except Exception as e:
    MissingModule(e)

Title("Discord Server Scraper")
Connection()
CheckGithubStar()

try:
    token = ChoiceToken()
    
    server_id = input(f"{INPUT} Server ID {red}->{reset} ").strip()
    if not server_id:
        ErrorInput()
    
    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": RandomUserAgents()}
    
    print(f"{LOADING} Fetching Server Information..", reset)
    
    guild_response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}?with_counts=true", headers=headers)
    
    if guild_response.status_code != 200:
        print(f"{ERROR} Cannot access Server!", reset)
        Continue()
        Reset()
    
    guild_data = guild_response.json()
    
    print(f"{LOADING} Fetching Channels..", reset)
    channels_response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/channels", headers=headers)
    channels = channels_response.json() if channels_response.status_code == 200 else []
    
    print(f"{LOADING} Fetching Roles..", reset)
    roles_response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/roles", headers=headers)
    roles = roles_response.json() if roles_response.status_code == 200 else []
    
    print(f"{LOADING} Fetching Members..", reset)
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
        print(f"{LOADING} Members scraped:{red} {len(members)}", reset)
        
        if len(batch) < limit:
            break
    
    scrape_data = {
        "server_info": {
            "name": guild_data.get("name"),
            "id": guild_data.get("id"),
            "owner_id": guild_data.get("owner_id"),
            "icon": guild_data.get("icon"),
            "description": guild_data.get("description"),
            "member_count": guild_data.get("approximate_member_count"),
            "presence_count": guild_data.get("approximate_presence_count"),
            "verification_level": guild_data.get("verification_level"),
            "vanity_url": guild_data.get("vanity_url_code")
        },
        "channels": [{"id": c.get("id"), "name": c.get("name"), "type": c.get("type"), "position": c.get("position")} for c in channels],
        "roles": [{"id": r.get("id"), "name": r.get("name"), "color": r.get("color"), "position": r.get("position")} for r in roles],
        "members": [{"username": m.get("user", {}).get("username"), "id": m.get("user", {}).get("id"), "discriminator": m.get("user", {}).get("discriminator"), "nick": m.get("nick")} for m in members]
    }
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Server_{guild_data.get('name', server_id)}_{timestamp}.json"
    output_path = os.path.join(tool_path, "Programs", "Output", "DiscordServerScraper", filename)
    
    os.makedirs(os.path.join(tool_path, "Programs", "Output", "DiscordServerScraper"), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scrape_data, f, indent=4, ensure_ascii=False)
    
    Scroll(f"""
 {INFO} Name     :{red} {guild_data.get('name')}
 {INFO} Members  :{red} {len(members)}
 {INFO} Channels :{red} {len(channels)}
 {INFO} Roles    :{red} {len(roles)}
 {INFO} File     :{red} {filename}
""")
    print(f"{SUCCESS} Server scraped!", reset)

    output_dir = os.path.join(tool_path, "Programs", "Output", "DiscordServerScraper")
    if platform_pc == "Windows":
        os.startfile(output_dir)
    else:
        subprocess.Popen(['xdg-open', output_dir])
    
    Continue()
    Reset()

except Exception as e:
    Error(e)