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
    from datetime import datetime
    import json
    import requests
    import time
except Exception as e:
    MissingModule(e)

Title("Server Scraper")

Scroll(GradientBanner(discord_banner))

try:
    token     = ChoiceToken()
    server_id = input(f"{INPUT} Server Id {red}->{reset} ").strip()

    if not server_id or not server_id.isdigit():
        ErrorId()

    headers = {
        "Authorization": token,
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

    print(f"{LOADING} Fetching server..", reset)

    guild_response = ApiGet(f"https://discord.com/api/v9/guilds/{server_id}?with_counts=true")

    if not guild_response or guild_response.status_code != 200:
        print(f"{ERROR} Could not access server!", reset)
        Continue()
        Reset()

    guild_data = guild_response.json()

    print(f"{LOADING} Fetching channels..", reset)

    channels_response = ApiGet(f"https://discord.com/api/v9/guilds/{server_id}/channels")
    channels          = channels_response.json() if channels_response and channels_response.status_code == 200 else []

    print(f"{LOADING} Fetching roles..", reset)

    roles_response = ApiGet(f"https://discord.com/api/v9/guilds/{server_id}/roles")
    roles          = roles_response.json() if roles_response and roles_response.status_code == 200 else []

    print(f"{LOADING} Fetching members..", reset)

    members = []
    after   = 0

    while True:
        r = ApiGet(f"https://discord.com/api/v9/guilds/{server_id}/members?limit=1000&after={after}")
        if not r or r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        members.extend(batch)
        after = int(batch[-1]["user"]["id"])
        print(f"{LOADING} Members:{red} {len(members)}", reset)
        if len(batch) < 1000:
            break
        time.sleep(0.5)

    scrape_data = {
        "server_info": {
            "name"              : guild_data.get("name"),
            "id"                : guild_data.get("id"),
            "owner_id"          : guild_data.get("owner_id"),
            "description"       : guild_data.get("description"),
            "member_count"      : guild_data.get("approximate_member_count"),
            "presence_count"    : guild_data.get("approximate_presence_count"),
            "verification_level": guild_data.get("verification_level"),
            "vanity_url"        : guild_data.get("vanity_url_code"),
        },
        "channels": [
            {"id": c.get("id"), "name": c.get("name"), "type": c.get("type"), "position": c.get("position")}
            for c in channels
        ],
        "roles": [
            {"id": r.get("id"), "name": r.get("name"), "color": r.get("color"), "position": r.get("position")}
            for r in roles
        ],
        "members": [
            {
                "username"     : m.get("user", {}).get("username"),
                "id"           : m.get("user", {}).get("id"),
                "discriminator": m.get("user", {}).get("discriminator"),
                "nick"         : m.get("nick"),
                "bot"          : m.get("user", {}).get("bot", False),
            }
            for m in members
        ],
    }

    timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename    = f"Server_{guild_data.get('name', server_id)}_{timestamp}.json"
    output_dir  = os.path.join(tool_path, "Programs", "Output", "ServerScraper")
    output_path = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scrape_data, f, indent=4, ensure_ascii=False)

    Scroll(f"""
 {SUCCESS} Name     :{red} {guild_data.get('name', 'None')}{white}
 {SUCCESS} Members  :{red} {len(members)}{white}
 {SUCCESS} Channels :{red} {len(channels)}{white}
 {SUCCESS} Roles    :{red} {len(roles)}{white}
 {SUCCESS} File     :{red} {filename}{white}
""")

    if platform_pc == "Windows":
        os.startfile(output_dir)
    else:
        subprocess.Popen(["xdg-open", output_dir])

    Continue()
    Reset()

except Exception as e:
    Error(e)