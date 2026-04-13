# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    from datetime import datetime
except Exception as e:
    MissingModule(e)

Title("Roblox Cookie Information")
Connection()

try:
    cookie = ChoiceCookie()

    print(f"{LOADING} Retrieving Information..", reset)

    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie

    auth = session.get("https://users.roblox.com/v1/users/authenticated", timeout=10)

    status = "Valid" if auth.status_code == 200 else "Invalid"

    if auth.status_code != 200:
        print(f"{ERROR} Invalid or expired Roblox Cookie!", reset)
        Continue()
        Reset()

    auth_data = auth.json()
    user_id = auth_data.get("id")
    username = auth_data.get("name", "N/A")

    user = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=10).json()

    robux = "N/A"
    try:
        eco = session.get(f"https://economy.roblox.com/v1/users/{user_id}/currency", timeout=10).json()
        robux = eco.get("robux", "N/A")
    except:
        pass

    friends_count = "N/A"
    try:
        fc = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count", timeout=10).json()
        friends_count = fc.get("count", "N/A")
    except:
        pass

    followers_count = "N/A"
    try:
        fl = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count", timeout=10).json()
        followers_count = fl.get("count", "N/A")
    except:
        pass

    following_count = "N/A"
    try:
        fw = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followings/count", timeout=10).json()
        following_count = fw.get("count", "N/A")
    except:
        pass

    groups_count = "N/A"
    groups_list = []
    try:
        gr = requests.get(f"https://groups.roblox.com/v1/users/{user_id}/groups/roles", timeout=10).json()
        groups_data = gr.get("data", [])
        groups_count = len(groups_data)
        groups_list = [(g.get("group", {}).get("name", "N/A"), g.get("role", {}).get("name", "N/A")) for g in groups_data[:10]]
    except:
        pass

    collectibles_count = "N/A"
    try:
        inv = requests.get(f"https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles?limit=10&sortOrder=Desc", timeout=10).json()
        collectibles_count = len(inv.get("data", []))
    except:
        pass

    avatar_url = "N/A"
    try:
        th = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=420x420&format=Png&isCircular=false", timeout=10).json()
        avatar_url = th.get("data", [{}])[0].get("imageUrl", "N/A")
    except:
        pass

    email_status = "N/A"
    try:
        settings = session.get("https://accountsettings.roblox.com/v1/email", timeout=10).json()
        email_verified = settings.get("verified", False)
        email_addr = settings.get("emailAddress", "N/A")
        email_status = f"{email_addr} (Verified: {email_verified})"
    except:
        pass

    pin_status = "N/A"
    try:
        pin = session.get("https://auth.roblox.com/v1/account/pin", timeout=10).json()
        pin_status = "Enabled" if pin.get("isEnabled", False) else "Disabled"
    except:
        pass

    presence = "N/A"
    try:
        pr = requests.post("https://presence.roblox.com/v1/presence/users", json={"userIds": [user_id]}, timeout=10).json()
        presence_data = pr.get("userPresences", [{}])[0]
        presence_types = {0: "Offline", 1: "Online", 2: "In-Game", 3: "In Studio"}
        presence = presence_types.get(presence_data.get("userPresenceType", 0), "Unknown")
        last_location = presence_data.get("lastLocation", "")
        if last_location:
            presence += f" ({last_location})"
    except:
        pass

    prev_names = []
    try:
        pn = requests.get(f"https://users.roblox.com/v1/users/{user_id}/username-history?limit=10&sortOrder=Desc", timeout=10).json()
        prev_names = [n.get("name", "") for n in pn.get("data", []) if n.get("name")]
    except:
        pass

    created = user.get("created", "N/A")
    if created and created != "N/A":
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            created = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except:
            created = created[:10]

    output = f"""
 {INFO} Status                   :{red} {status}
 {INFO} Roblox Cookie            :{red} {cookie[:30]}..
 {INFO} User Id                  :{red} {user_id}
 {INFO} Username                 :{red} {username}
 {INFO} Display Name             :{red} {user.get('displayName', 'N/A')}
 {INFO} Bio                      :{red} {(user.get('description', 'N/A') or 'N/A')[:100]}
 {INFO} Created                  :{red} {created}
 {INFO} Banned                   :{red} {user.get('isBanned', False)}
 {INFO} Verified Badge           :{red} {user.get('hasVerifiedBadge', False)}
 {INFO} Email                    :{red} {email_status}
 {INFO} Account Pin              :{red} {pin_status}
 {INFO} Presence                 :{red} {presence}
 {INFO} Robux Balance            :{red} {robux}
 {INFO} Friends                  :{red} {friends_count}
 {INFO} Followers                :{red} {followers_count}
 {INFO} Following                :{red} {following_count}
 {INFO} Groups                   :{red} {groups_count}
 {INFO} Collectibles             :{red} {collectibles_count}
 {INFO} Previous Usernames       :{red} {', '.join(prev_names) if prev_names else 'None'}
 {INFO} Avatar                   :{red} {avatar_url}
 {INFO} Profile Url              :{red} https://www.roblox.com/users/{user_id}/profile{reset}
"""

    if groups_list:
        output += f"\n {INFO} Top Groups:\n"
        for name, role in groups_list:
            output += f" {SUCCESS} {red}{name} ({role}){reset}\n"

    Scroll(output)

    Continue()
    Reset()

except Exception as e:
    Error(e)
