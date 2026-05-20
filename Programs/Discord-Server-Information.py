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
    import requests
except Exception as e:
    MissingModule(e)

Title("Server Information")

Scroll(GradientBanner(discord_banner))

try:
    invite = input(f"{INPUT} Invite {red}->{reset} ").strip()

    if not invite:
        ErrorInput()

    invite_code = invite.split("/")[-1].strip()

    print(f"{LOADING} Fetching..", reset)

    try:
        response = requests.get(
            f"https://discord.com/api/v9/invites/{invite_code}?with_counts=true&with_expiration=true",
            timeout=10
        )
    except Exception:
        print(f"{ERROR} Could not connect!", reset)
        Continue()
        Reset()

    if response.status_code != 200:
        ErrorUrl()

    data         = response.json()
    server_info  = data.get("guild", {})
    inviter_info = data.get("inviter", {})
    channel_info = data.get("channel", {})

    type_value         = data.get("type",      0)
    code_value         = data.get("code",      "None")
    expires_at         = data.get("expires_at","None")
    max_uses           = data.get("max_uses",  0)
    uses               = data.get("uses",      "None")
    server_id          = server_info.get("id",                          "None")
    server_name        = server_info.get("name",                        "None")
    server_description = server_info.get("description",                 "None")
    server_icon        = server_info.get("icon",                        "None")
    server_features    = server_info.get("features",                    [])
    server_nsfw_level  = server_info.get("nsfw_level",                  "None")
    server_nsfw        = server_info.get("nsfw",                        "None")
    server_flags       = server_info.get("flags",                       "None")
    server_verif_level = server_info.get("verification_level",          "None")
    server_premium     = server_info.get("premium_subscription_count",  "None")
    server_members     = data.get("approximate_member_count",           "None")
    server_online      = data.get("approximate_presence_count",         "None")
    channel_id         = channel_info.get("id",   "None")
    channel_name       = channel_info.get("name", "None")
    channel_type       = channel_info.get("type", "None")

    inviter_id           = inviter_info.get("id",           "None")
    inviter_username     = inviter_info.get("username",     "None")
    inviter_display_name = inviter_info.get("global_name",  "None")
    inviter_avatar       = inviter_info.get("avatar",       "None")
    inviter_public_flags = inviter_info.get("public_flags", "None")
    inviter_flags        = inviter_info.get("flags",        "None")
    inviter_banner       = inviter_info.get("banner",       "None")
    inviter_accent_color = inviter_info.get("accent_color", "None")
    inviter_banner_color = inviter_info.get("banner_color", "None")

    type_map   = {0: "Standard Server", 1: "Group Dm", 2: "Community Server", 3: "Scheduled Event"}
    type_value = type_map.get(type_value, str(type_value))

    try:
        dt         = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        expires_at = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        expires_at = "Unlimited"

    max_uses = "Unlimited" if max_uses == 0 else max_uses
    uses     = "No permission" if uses is None else uses

    try:
        if server_icon and server_icon.startswith("a_"):
            server_icon_url = f"https://cdn.discordapp.com/icons/{server_id}/{server_icon}.gif"
        elif server_icon:
            server_icon_url = f"https://cdn.discordapp.com/icons/{server_id}/{server_icon}.png"
        else:
            server_icon_url = "None"
    except Exception:
        server_icon_url = "None"

    channel_type_map = {
        0: "Text Channel",   2: "Voice Channel",  4: "Category",
        5: "Announcement",   10: "News Thread",   11: "Public Thread",
        12: "Private Thread", 13: "Stage Channel", 15: "Forum Channel",
    }
    channel_type = channel_type_map.get(channel_type, str(channel_type) if channel_type != "None" else "None")

    features_str = ", ".join(server_features) if server_features else "None"

    Scroll(f"""
 {SUCCESS} Invite                      :{red} {invite}{white}
 {SUCCESS} Type                        :{red} {type_value}{white}
 {SUCCESS} Code                        :{red} {code_value}{white}
 {SUCCESS} Expires At                  :{red} {expires_at}{white}
 {SUCCESS} Max Uses                    :{red} {max_uses}{white}
 {SUCCESS} Uses                        :{red} {uses}{white}
 {SUCCESS} Server Id                   :{red} {server_id}{white}
 {SUCCESS} Server Name                 :{red} {server_name}{white}
 {SUCCESS} Server Members              :{red} {server_members}{white}
 {SUCCESS} Server Online               :{red} {server_online}{white}
 {SUCCESS} Channel Id                  :{red} {channel_id}{white}
 {SUCCESS} Channel Name                :{red} {channel_name}{white}
 {SUCCESS} Channel Type                :{red} {channel_type}{white}
 {SUCCESS} Server Description          :{red} {server_description}{white}
 {SUCCESS} Server Icon Url             :{red} {server_icon_url}{white}
 {SUCCESS} Server Features             :{red} {features_str}{white}
 {SUCCESS} Server Nsfw Level           :{red} {server_nsfw_level}{white}
 {SUCCESS} Server Nsfw                 :{red} {server_nsfw}{white}
 {SUCCESS} Server Flags                :{red} {server_flags}{white}
 {SUCCESS} Server Verification Level   :{red} {server_verif_level}{white}
 {SUCCESS} Server Premium Subscription :{red} {server_premium}{white}

 {SUCCESS} Inviter Id                  :{red} {inviter_id}{white}
 {SUCCESS} Inviter Username            :{red} {inviter_username}{white}
 {SUCCESS} Inviter Display Name        :{red} {inviter_display_name}{white}
 {SUCCESS} Inviter Avatar              :{red} {inviter_avatar}{white}
 {SUCCESS} Inviter Public Flags        :{red} {inviter_public_flags}{white}
 {SUCCESS} Inviter Flags               :{red} {inviter_flags}{white}
 {SUCCESS} Inviter Banner              :{red} {inviter_banner}{white}
 {SUCCESS} Inviter Accent Color        :{red} {inviter_accent_color}{white}
 {SUCCESS} Inviter Banner Color        :{red} {inviter_banner_color}{white}
""")

    Continue()
    Reset()

except Exception as e:
    Error(e)