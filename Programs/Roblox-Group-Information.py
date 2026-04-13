# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    from datetime import datetime
except Exception as e:
    MissingModule(e)

Title("Roblox Group Information")
Connection()

try:
    group_id = input(f"{INPUT} Group Id {red}->{reset} ").strip()
    if not group_id or not group_id.isdigit():
        ErrorId()

    print(f"{LOADING} Retrieving Group Information..", reset)

    response = requests.get(f"https://groups.roblox.com/v1/groups/{group_id}", timeout=10)

    if response.status_code != 200:
        print(f"{ERROR} Group not found!", reset)
        Continue()
        Reset()

    data = response.json()

    name = data.get("name", "N/A")
    description = data.get("description", "") or "N/A"
    member_count = data.get("memberCount", "N/A")
    is_public = data.get("publicEntryAllowed", "N/A")
    is_locked = data.get("isLocked", False)
    is_verified = data.get("hasVerifiedBadge", False)
    shout = data.get("shout", {})

    owner = data.get("owner", {})
    owner_name = owner.get("username", "N/A") if owner else "No Owner"
    owner_id = owner.get("userId", "N/A") if owner else "N/A"
    owner_display = owner.get("displayName", "N/A") if owner else "N/A"

    created = data.get("created", "N/A")
    if created and created != "N/A":
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            created = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except:
            created = created[:10]

    updated = data.get("updated", "N/A")
    if updated and updated != "N/A":
        try:
            dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
            updated = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except:
            updated = updated[:10]

    icon_url = "N/A"
    try:
        th = requests.get(f"https://thumbnails.roblox.com/v1/groups/icons?groupIds={group_id}&size=420x420&format=Png&isCircular=false", timeout=10).json()
        icon_url = th.get("data", [{}])[0].get("imageUrl", "N/A")
    except:
        pass

    roles = []
    try:
        rl = requests.get(f"https://groups.roblox.com/v1/groups/{group_id}/roles", timeout=10).json()
        roles = [(r.get("name", "N/A"), r.get("memberCount", 0), r.get("rank", 0)) for r in rl.get("roles", [])]
        roles.sort(key=lambda x: x[2], reverse=True)
    except:
        pass

    output = f"""
 {INFO} Group Id                 :{red} {group_id}
 {INFO} Name                     :{red} {name}
 {INFO} Description              :{red} {description[:200]}
 {INFO} Members                  :{red} {f'{member_count:,}' if isinstance(member_count, int) else member_count}
 {INFO} Public Entry             :{red} {is_public}
 {INFO} Locked                   :{red} {is_locked}
 {INFO} Verified Badge           :{red} {is_verified}
 {INFO} Created                  :{red} {created}
 {INFO} Updated                  :{red} {updated}
 {INFO} Owner                    :{red} {owner_name} ({owner_display})
 {INFO} Icon                     :{red} {icon_url}
 {INFO} Group Url                :{red} https://www.roblox.com/groups/{group_id}
"""

    if shout and shout.get("body"):
        poster = shout.get("poster", {}).get("username", "Unknown")
        output += f"\n {INFO} Shout by{red} {poster} {white}:{red} {shout['body'][:200]}{reset}\n"

    if roles:
        output += f"\n {INFO} Roles:\n"
        for role_name, role_members, role_rank in roles:
            output += f" {PREFIX}{role_rank:3d}{SUFFIX} {role_name:25s}:{red} {f'{role_members:,}' if isinstance(role_members, int) else role_members} members{reset}\n"

    Scroll(output)

    Continue()
    Reset()

except Exception as e:
    Error(e)
