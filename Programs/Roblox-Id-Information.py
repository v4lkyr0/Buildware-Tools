# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    from datetime import datetime
except Exception as e:
    MissingModule(e)

Title("Roblox Id Information")
Connection()

try:
    user_id = input(f"{INPUT} Roblox User Id {red}->{reset} ").strip()
    if not user_id or not user_id.isdigit():
        ErrorId()

    print(f"{LOADING} Retrieving User Information..", reset)

    response = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=10)

    if response.status_code != 200:
        print(f"{ERROR} User not found!", reset)
        Continue()
        Reset()

    data = response.json()

    username = data.get("name", "N/A")
    display_name = data.get("displayName", "N/A")
    description = data.get("description", "") or "N/A"
    is_banned = data.get("isBanned", False)
    has_badge = data.get("hasVerifiedBadge", False)
    created = data.get("created", "N/A")
    external_app_display_name = data.get("externalAppDisplayName", "N/A")

    if created and created != "N/A":
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            created = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except:
            created = created[:10]

    friends = "N/A"
    try:
        fc = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count", timeout=10).json()
        friends = fc.get("count", "N/A")
    except:
        pass

    followers = "N/A"
    try:
        fl = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count", timeout=10).json()
        followers = fl.get("count", "N/A")
    except:
        pass

    following = "N/A"
    try:
        fw = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followings/count", timeout=10).json()
        following = fw.get("count", "N/A")
    except:
        pass

    groups_count = "N/A"
    try:
        gr = requests.get(f"https://groups.roblox.com/v1/users/{user_id}/groups/roles", timeout=10).json()
        groups_count = len(gr.get("data", []))
    except:
        pass

    avatar_url = "N/A"
    try:
        th = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=420x420&format=Png&isCircular=false", timeout=10).json()
        avatar_url = th.get("data", [{}])[0].get("imageUrl", "N/A")
    except:
        pass

    prev_names = []
    try:
        pn = requests.get(f"https://users.roblox.com/v1/users/{user_id}/username-history?limit=10&sortOrder=Desc", timeout=10).json()
        prev_names = [n.get("name", "") for n in pn.get("data", []) if n.get("name")]
    except:
        pass

    Scroll(f"""
 {INFO} User Id                  :{red} {user_id}
 {INFO} Username                 :{red} {username}
 {INFO} Display Name             :{red} {display_name}
 {INFO} Bio                      :{red} {description[:150]}
 {INFO} Created                  :{red} {created}
 {INFO} Banned                   :{red} {is_banned}
 {INFO} Verified Badge           :{red} {has_badge}
 {INFO} Friends                  :{red} {friends}
 {INFO} Followers                :{red} {followers}
 {INFO} Following                :{red} {following}
 {INFO} Groups                   :{red} {groups_count}
 {INFO} Previous Usernames       :{red} {', '.join(prev_names) if prev_names else 'None'}
 {INFO} Avatar                   :{red} {avatar_url}
 {INFO} Profile Url              :{red} https://www.roblox.com/users/{user_id}/profile
""")

    Continue()
    Reset()

except Exception as e:
    Error(e)
