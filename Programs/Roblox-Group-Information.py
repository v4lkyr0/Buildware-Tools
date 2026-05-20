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
    from datetime import datetime
except Exception as e:
    MissingModule(e)

Title("Group Information")

Scroll(GradientBanner(roblox_banner))

try:
    group_id = input(f"{INPUT} Group Id {red}->{reset} ").strip()
    if not group_id or not group_id.isdigit():
        ErrorId()

    print(f"{LOADING} Fetching..", reset)

    try:
        response = requests.get(f"https://groups.roblox.com/v1/groups/{group_id}", timeout=10)
    except Exception:
        print(f"{ERROR} Could not connect!", reset)
        Continue()
        Reset()

    if response.status_code != 200:
        print(f"{ERROR} Group not found!", reset)
        Continue()
        Reset()

    data          = response.json()
    name          = data.get("name",               "None")
    description   = (data.get("description") or "None")[:200]
    member_count  = data.get("memberCount",         "None")
    is_public     = data.get("publicEntryAllowed",  "None")
    is_locked     = data.get("isLocked",            False)
    is_verified   = data.get("hasVerifiedBadge",    False)
    shout         = data.get("shout",               {})
    owner         = data.get("owner",               {})
    owner_name    = owner.get("username",    "None") if owner else "No Owner"
    owner_display = owner.get("displayName", "None") if owner else "None"

    def FormatDate(value):
        if not value or value == "None":
            return "None"
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except Exception:
            return value[:10]

    created = FormatDate(data.get("created", "None"))
    updated = FormatDate(data.get("updated", "None"))

    icon_url = "None"
    try:
        th       = requests.get(f"https://thumbnails.roblox.com/v1/groups/icons?groupIds={group_id}&size=420x420&format=Png&isCircular=false", timeout=10).json()
        icon_url = th.get("data", [{}])[0].get("imageUrl", "None")
    except Exception:
        pass

    roles = []
    try:
        rl    = requests.get(f"https://groups.roblox.com/v1/groups/{group_id}/roles", timeout=10).json()
        roles = [(r.get("name", "None"), r.get("memberCount", 0), r.get("rank", 0)) for r in rl.get("roles", [])]
        roles.sort(key=lambda x: x[2], reverse=True)
    except Exception:
        pass

    Scroll(f"""
 {SUCCESS} Group Id       :{red} {group_id}{white}
 {SUCCESS} Name           :{red} {name}{white}
 {SUCCESS} Description    :{red} {description}{white}
 {SUCCESS} Members        :{red} {f'{member_count:,}' if isinstance(member_count, int) else member_count}{white}
 {SUCCESS} Public Entry   :{red} {is_public}{white}
 {SUCCESS} Locked         :{red} {is_locked}{white}
 {SUCCESS} Verified Badge :{red} {is_verified}{white}
 {SUCCESS} Created        :{red} {created}{white}
 {SUCCESS} Updated        :{red} {updated}{white}
 {SUCCESS} Owner          :{red} {owner_name} ({owner_display}){white}
 {SUCCESS} Icon           :{red} {icon_url}{white}
 {SUCCESS} Group Url      :{red} https://www.roblox.com/groups/{group_id}{white}
""")

    if shout and shout.get("body"):
        poster = shout.get("poster", {}).get("username", "None")
        print(f"{INFO} Shout by{red} {poster}{white} :{red} {shout['body'][:200]}", reset)

    if roles:
        print(f"\n{INFO} Roles:", reset)
        for role_name, role_members, role_rank in roles:
            print(f" {PREFIX}{role_rank:3d}{SUFFIX} {role_name:<25}{red} {f'{role_members:,}' if isinstance(role_members, int) else role_members} members", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)