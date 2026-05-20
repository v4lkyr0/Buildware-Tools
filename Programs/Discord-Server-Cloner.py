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

Title("Server Cloner")

Scroll(GradientBanner(discord_banner))

try:
    token = ChoiceToken()

    source_id = input(f"{INPUT} Source Server Id {red}->{reset} ").strip()
    if not source_id or not source_id.isdigit():
        ErrorId()

    target_id = input(f"{INPUT} Target Server Id {red}->{reset} ").strip()
    if not target_id or not target_id.isdigit():
        ErrorId()

    if source_id == target_id:
        print(f"{ERROR} Source and target cannot be the same server!", reset)
        Continue()
        Reset()

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

    def ApiPost(url, json=None):
        while True:
            try:
                r = requests.post(url, headers=headers, json=json or {}, timeout=10)
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

    def ApiPatch(url, json=None):
        while True:
            try:
                r = requests.patch(url, headers=headers, json=json or {}, timeout=10)
                if r.status_code == 429:
                    time.sleep(r.json().get("retry_after", 1))
                    continue
                return r
            except Exception:
                return None

    print(f"{LOADING} Fetching servers..", reset)

    source_response = ApiGet(f"https://discord.com/api/v9/guilds/{source_id}")
    if not source_response or source_response.status_code != 200:
        print(f"{ERROR} Could not access source server!", reset)
        Continue()
        Reset()

    target_response = ApiGet(f"https://discord.com/api/v9/guilds/{target_id}")
    if not target_response or target_response.status_code != 200:
        print(f"{ERROR} Could not access target server!", reset)
        Continue()
        Reset()

    source_data = source_response.json()
    target_data = target_response.json()
    source_name = source_data.get("name", "None")
    target_name = target_data.get("name", "None")

    print(f"{SUCCESS} Source:{red} {source_name}", reset)
    print(f"{SUCCESS} Target:{red} {target_name}", reset)

    print(f"{LOADING} Cloning server name and icon..", reset)

    patch_data = {"name": source_name}
    if source_data.get("icon"):
        patch_data["icon"] = source_data["icon"]

    ApiPatch(f"https://discord.com/api/v9/guilds/{target_id}", json=patch_data)

    print(f"{LOADING} Deleting target channels..", reset)

    channels_response = ApiGet(f"https://discord.com/api/v9/guilds/{target_id}/channels")
    if channels_response and channels_response.status_code == 200:
        for channel in channels_response.json():
            resp = ApiDelete(f"https://discord.com/api/v9/channels/{channel['id']}")
            if resp and resp.status_code == 200:
                print(f"{SUCCESS} Deleted:{red} {channel.get('name', 'None')}", reset)
            else:
                print(f"{ERROR} Failed to delete:{red} {channel.get('name', 'None')}", reset)
            time.sleep(0.3)

    print(f"{LOADING} Cloning roles..", reset)

    roles_response = ApiGet(f"https://discord.com/api/v9/guilds/{source_id}/roles")
    if roles_response and roles_response.status_code == 200:
        roles = sorted(roles_response.json(), key=lambda x: x.get("position", 0))
        for role in roles:
            if role.get("name") == "@everyone" or role.get("managed"):
                continue
            role_data = {
                "name"       : role.get("name"),
                "permissions": role.get("permissions"),
                "color"      : role.get("color", 0),
                "hoist"      : role.get("hoist", False),
                "mentionable": role.get("mentionable", False),
            }
            resp = ApiPost(f"https://discord.com/api/v9/guilds/{target_id}/roles", json=role_data)
            if resp and resp.status_code == 200:
                print(f"{SUCCESS} Created role:{red} {role.get('name', 'None')}", reset)
            else:
                print(f"{ERROR} Failed role:{red} {role.get('name', 'None')}", reset)
            time.sleep(0.3)

    print(f"{LOADING} Cloning channels..", reset)

    source_channels_response = ApiGet(f"https://discord.com/api/v9/guilds/{source_id}/channels")
    if source_channels_response and source_channels_response.status_code == 200:
        source_channels = sorted(source_channels_response.json(), key=lambda x: x.get("position", 0))

        for channel in source_channels:
            channel_data = {
                "name"                 : channel.get("name"),
                "type"                 : channel.get("type"),
                "topic"                : channel.get("topic"),
                "position"             : channel.get("position"),
                "permission_overwrites": channel.get("permission_overwrites", []),
                "nsfw"                 : channel.get("nsfw", False),
                "rate_limit_per_user"  : channel.get("rate_limit_per_user", 0),
            }

            if channel.get("type") == 4:
                channel_data.pop("topic",               None)
                channel_data.pop("nsfw",                None)
                channel_data.pop("rate_limit_per_user", None)

            resp = ApiPost(f"https://discord.com/api/v9/guilds/{target_id}/channels", json=channel_data)

            if resp and resp.status_code == 201:
                print(f"{SUCCESS} Created channel:{red} {channel.get('name', 'None')}", reset)
            else:
                print(f"{ERROR} Failed channel:{red} {channel.get('name', 'None')}", reset)

            time.sleep(0.5)

    print(f"\n{SUCCESS} Server cloned!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)