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

Title("Id Information")

Scroll(GradientBanner(roblox_banner))

try:
    user_id = input(f"{INPUT} User Id {red}->{reset} ").strip()
    if not user_id or not user_id.isdigit():
        ErrorId()

    print(f"{LOADING} Fetching..", reset)

    try:
        response = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=10)
    except Exception:
        print(f"{ERROR} Could not connect!", reset)
        Continue()
        Reset()

    if response.status_code != 200:
        print(f"{ERROR} User not found!", reset)
        Continue()
        Reset()

    data         = response.json()
    username     = data.get("name",             "None")
    display_name = data.get("displayName",      "None")
    description  = (data.get("description") or "None")[:150]
    is_banned    = data.get("isBanned",         False)
    has_badge    = data.get("hasVerifiedBadge", False)

    created = data.get("created", "None")
    if created and created != "None":
        try:
            dt      = datetime.fromisoformat(created.replace("Z", "+00:00"))
            created = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except Exception:
            created = created[:10]

    friends = "None"
    try:
        fc      = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count", timeout=10).json()
        friends = fc.get("count", "None")
    except Exception:
        pass

    followers = "None"
    try:
        fl        = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count", timeout=10).json()
        followers = fl.get("count", "None")
    except Exception:
        pass

    following = "None"
    try:
        fw        = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followings/count", timeout=10).json()
        following = fw.get("count", "None")
    except Exception:
        pass

    groups_count = "None"
    try:
        gr           = requests.get(f"https://groups.roblox.com/v1/users/{user_id}/groups/roles", timeout=10).json()
        groups_count = len(gr.get("data", []))
    except Exception:
        pass

    avatar_url = "None"
    try:
        th         = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=420x420&format=Png&isCircular=false", timeout=10).json()
        avatar_url = th.get("data", [{}])[0].get("imageUrl", "None")
    except Exception:
        pass

    prev_names = []
    try:
        pn         = requests.get(f"https://users.roblox.com/v1/users/{user_id}/username-history?limit=10&sortOrder=Desc", timeout=10).json()
        prev_names = [n.get("name", "") for n in pn.get("data", []) if n.get("name")]
    except Exception:
        pass

    Scroll(f"""
 {SUCCESS} User Id            :{red} {user_id}{white}
 {SUCCESS} Username           :{red} {username}{white}
 {SUCCESS} Display Name       :{red} {display_name}{white}
 {SUCCESS} Bio                :{red} {description}{white}
 {SUCCESS} Created            :{red} {created}{white}
 {SUCCESS} Banned             :{red} {is_banned}{white}
 {SUCCESS} Verified Badge     :{red} {has_badge}{white}
 {SUCCESS} Friends            :{red} {friends}{white}
 {SUCCESS} Followers          :{red} {followers}{white}
 {SUCCESS} Following          :{red} {following}{white}
 {SUCCESS} Groups             :{red} {groups_count}{white}
 {SUCCESS} Previous Usernames :{red} {', '.join(prev_names) if prev_names else 'None'}{white}
 {SUCCESS} Avatar             :{red} {avatar_url}{white}
 {SUCCESS} Profile            :{red} https://www.roblox.com/users/{user_id}/profile{white}
""")

    Continue()
    Reset()

except Exception as e:
    Error(e)