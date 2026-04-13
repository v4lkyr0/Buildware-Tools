# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    from datetime import datetime
except Exception as e:
    MissingModule(e)

Title("Roblox Username Information")
Connection()

try:
    username = input(f"{INPUT} Roblox Username {red}->{reset} ").strip()
    if not username:
        ErrorInput()

    print(f"{LOADING} Looking Up Username..", reset)

    response = requests.post(
        "https://users.roblox.com/v1/usernames/users",
        json={"usernames": [username], "excludeBannedUsers": False},
        timeout=10
    )

    if response.status_code != 200:
        print(f"{ERROR} API error!", reset)
        Continue()
        Reset()

    users = response.json().get("data", [])
    if not users:
        print(f"{ERROR} Username not found!", reset)
        Continue()
        Reset()

    user_id = users[0].get("id")
    requested_name = users[0].get("requestedUsername", username)

    user = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=10).json()

    display_name = user.get("displayName", "N/A")
    description = user.get("description", "") or "N/A"
    is_banned = user.get("isBanned", False)
    has_badge = user.get("hasVerifiedBadge", False)
    created = user.get("created", "N/A")

    if created and created != "N/A":
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            created = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except:
            created = created[:10]

    friends = followers = following = groups_count = "N/A"
    try:
        friends = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count", timeout=10).json().get("count", "N/A")
    except: pass
    try:
        followers = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count", timeout=10).json().get("count", "N/A")
    except: pass
    try:
        following = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followings/count", timeout=10).json().get("count", "N/A")
    except: pass
    try:
        gr = requests.get(f"https://groups.roblox.com/v1/users/{user_id}/groups/roles", timeout=10).json()
        groups_count = len(gr.get("data", []))
    except: pass

    avatar_url = "N/A"
    try:
        th = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=420x420&format=Png&isCircular=false", timeout=10).json()
        avatar_url = th.get("data", [{}])[0].get("imageUrl", "N/A")
    except: pass

    presence = "N/A"
    try:
        pr = requests.post("https://presence.roblox.com/v1/presence/users", json={"userIds": [user_id]}, timeout=10).json()
        presence_data = pr.get("userPresences", [{}])[0]
        presence_types = {0: "Offline", 1: "Online (Website)", 2: "In-Game", 3: "In Studio"}
        presence = presence_types.get(presence_data.get("userPresenceType", 0), "Unknown")
        last_location = presence_data.get("lastLocation", "")
        if last_location:
            presence += f" ({last_location})"
    except: pass

    prev_names = []
    try:
        pn = requests.get(f"https://users.roblox.com/v1/users/{user_id}/username-history?limit=10&sortOrder=Desc", timeout=10).json()
        prev_names = [n.get("name", "") for n in pn.get("data", []) if n.get("name")]
    except: pass

    Scroll(f"""
 {INFO} User Id                  :{red} {user_id}
 {INFO} Username                 :{red} {user.get('name', username)}
 {INFO} Display Name             :{red} {display_name}
 {INFO} Bio                      :{red} {description[:150]}
 {INFO} Created                  :{red} {created}
 {INFO} Banned                   :{red} {is_banned}
 {INFO} Verified Badge           :{red} {has_badge}
 {INFO} Status                   :{red} {presence}
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
