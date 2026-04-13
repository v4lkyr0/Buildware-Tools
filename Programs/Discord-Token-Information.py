# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    from datetime import datetime, timezone
except Exception as e:
    MissingModule(e)

Title("Discord Token Information")
Connection()

try:
    token = ChoiceToken()

    print(f"{LOADING} Retrieving Information..", reset)

    headers  = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': RandomUserAgents()}
    api      = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': token, 'User-Agent': RandomUserAgents()}).json()
    response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)

    status = "Valid" if response.status_code == 200 else "Invalid"

    username          = api.get('username')
    display_name      = api.get('global_name')
    user_id           = api.get('id')
    country           = api.get('locale')
    email             = api.get('email')
    email_verified    = api.get('verified')
    phone             = api.get('phone')
    avatar_decoration = api.get('avatar_decoration')
    avatar            = api.get('avatar')
    accent_color      = api.get('accent_color')
    banner            = api.get('banner')
    banner_color      = api.get('banner_color')
    flags             = api.get('flags')
    public_flags      = api.get('public_flags')
    nsfw_allowed      = api.get('nsfw_allowed')
    mfa_enabled       = api.get('mfa_enabled')
    bio               = api.get('bio')

    try:
        linked_users_raw = api.get('linked_users')
        linked_users = ', '.join([str(u) for u in linked_users_raw]) if linked_users_raw else "None"
    except:
        linked_users = "None"

    try:
        mfa_type_map = {1: 'SMS', 2: 'App', 3: 'WebAuthn'}
        mfa_type_raw = api.get('authenticator_types', [])
        mfa_type     = ', '.join([mfa_type_map.get(m, f'Other ({m})') for m in mfa_type_raw]) if mfa_type_raw else "None"
    except:
        mfa_type = "None"

    try:
        created_at_raw = datetime.fromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000, timezone.utc)
        created_at     = created_at_raw.strftime('%Y-%m-%d %H:%M:%S')
    except:
        created_at = "None"

    try:
        premium_map = {0: "No Nitro", 1: "Nitro Classic", 2: "Nitro Boost"}
        nitro_type  = premium_map.get(api.get('premium_type'), "No Nitro")
    except:
        nitro_type = "No Nitro"

    try:
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}.gif" if requests.get(f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}.png"
    except:
        avatar_url = "No Avatar"

    try:
        billing = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers={'Authorization': token, 'User-Agent': RandomUserAgents()}).json()
        if billing:
            payment_map     = {1: 'Credit Card', 2: 'PayPal'}
            payment_methods = ', '.join([payment_map.get(m['type'], 'Other') for m in billing])
        else:
            payment_methods = 'No Payment Methods'
    except:
        payment_methods = 'No Payment Methods'

    try:
        gift_codes = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': token, 'User-Agent': RandomUserAgents()}).json()
        gift = ', '.join([f"{g.get('promotion', {}).get('outbound_title', 'Unknown')} -> {g.get('code', 'Unknown')}" for g in gift_codes]) if gift_codes else 'No Gift Codes'
    except:
        gift = 'No Gift Codes'

    try:
        guilds_response = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': token, 'User-Agent': RandomUserAgents()})
        if guilds_response.status_code == 200:
            guilds       = guilds_response.json()
            guild_count  = len(guilds)
            owner_guilds = [g for g in guilds if g.get('owner')]
            owner_guilds_count = len(owner_guilds)
            if owner_guilds:
                owner_guilds_names = '\n' + ', '.join(f"{g.get('name')} {red}({white}{g.get('id')}{red})" for g in owner_guilds)
            else:
                owner_guilds_names = ''
        else:
            guild_count        = 'None'
            owner_guilds_count = 'None'
            owner_guilds_names = ''
    except:
        guild_count        = 'None'
        owner_guilds_count = 'None'
        owner_guilds_names = ''

    try:
        relationships = requests.get('https://discord.com/api/v9/users/@me/relationships', headers={'Authorization': token, 'User-Agent': RandomUserAgents()}).json()
        friends_list  = []
        for friend in relationships:
            if friend.get('type') != 1:
                continue
            user_data  = friend.get('user', {})
            friend_str = f"{user_data.get('username', 'Unknown')} {red}({white}{user_data.get('id', 'Unknown')}{red})"
            if len('\n'.join(friends_list)) + len(friend_str) >= 1024:
                continue
            friends_list.append(friend_str)
        friends = f"{len(friends_list)}\n{', '.join(friends_list)}" if friends_list else 'None'
    except:
        friends = 'None'

    Scroll(f"""
 {INFO} Status            :{red} {status}
 {INFO} Token             :{red} {token}
 {INFO} Username          :{red} {username}
 {INFO} Display Name      :{red} {display_name}
 {INFO} User Id           :{red} {user_id}
 {INFO} Created At        :{red} {created_at}
 {INFO} Country           :{red} {country}
 {INFO} Email             :{red} {email}
 {INFO} Email Verified    :{red} {email_verified}
 {INFO} Phone             :{red} {phone}
 {INFO} Nitro             :{red} {nitro_type}
 {INFO} Linked Users      :{red} {linked_users}
 {INFO} Avatar Decoration :{red} {avatar_decoration}
 {INFO} Avatar            :{red} {avatar}
 {INFO} Avatar Url        :{red} {avatar_url}
 {INFO} Accent Color      :{red} {accent_color}
 {INFO} Banner            :{red} {banner}
 {INFO} Banner Color      :{red} {banner_color}
 {INFO} Flags             :{red} {flags}
 {INFO} Public Flags      :{red} {public_flags}
 {INFO} NSFW Allowed      :{red} {nsfw_allowed}
 {INFO} MFA Enabled       :{red} {mfa_enabled}
 {INFO} MFA Type          :{red} {mfa_type}
 {INFO} Billing           :{red} {payment_methods}
 {INFO} Gift Codes        :{red} {gift}
 {INFO} Guilds            :{red} {guild_count}
 {INFO} Owner Guilds      :{red} {owner_guilds_count}{owner_guilds_names}
 {INFO} Bio               :{red} {bio}
 {INFO} Friends           :{red} {friends}{reset}
""")
    Continue()
    Reset()

except Exception as e:
    Error(e)