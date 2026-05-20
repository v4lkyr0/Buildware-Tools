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
    from datetime import datetime, timezone
except Exception as e:
    MissingModule(e)

Title("Token Information")

Scroll(GradientBanner(discord_banner))

try:
    token   = ChoiceToken()
    headers = {
        "Authorization": token,
        "Content-Type" : "application/json",
        "User-Agent"   : RandomUserAgents(),
    }

    print(f"{LOADING} Fetching..", reset)

    try:
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
    except Exception:
        print(f"{ERROR} Could not connect!", reset)
        Continue()
        Reset()

    if response.status_code != 200:
        print(f"{ERROR} Invalid token!", reset)
        Continue()
        Reset()

    api      = response.json()
    user_id  = api.get("id")
    username = api.get("username")
    avatar   = api.get("avatar")

    try:
        created_at = datetime.fromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        created_at = "None"

    try:
        nitro_map  = {0: "No Nitro", 1: "Nitro Classic", 2: "Nitro Boost", 3: "Nitro Basic"}
        nitro_type = nitro_map.get(api.get("premium_type", 0), "No Nitro")
    except Exception:
        nitro_type = "No Nitro"

    try:
        mfa_type_map = {1: "Sms", 2: "App", 3: "WebAuthn"}
        mfa_type_raw = api.get("authenticator_types", [])
        mfa_type     = ", ".join([mfa_type_map.get(m, f"Other ({m})") for m in mfa_type_raw]) if mfa_type_raw else "None"
    except Exception:
        mfa_type = "None"

    try:
        linked_users_raw = api.get("linked_users", [])
        linked_users     = ", ".join([str(u) for u in linked_users_raw]) if linked_users_raw else "None"
    except Exception:
        linked_users = "None"

    try:
        if avatar:
            av_gif     = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}.gif"
            av_check   = requests.get(av_gif, timeout=5)
            avatar_url = av_gif if av_check.status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}.png"
        else:
            avatar_url = "None"
    except Exception:
        avatar_url = "None"

    try:
        billing = requests.get("https://discord.com/api/v9/users/@me/billing/payment-sources", headers=headers, timeout=10).json()
        if billing and isinstance(billing, list):
            payment_map     = {1: "Credit Card", 2: "PayPal"}
            payment_methods = ", ".join([payment_map.get(m.get("type"), "Other") for m in billing])
        else:
            payment_methods = "None"
    except Exception:
        payment_methods = "None"

    try:
        gift_codes = requests.get("https://discord.com/api/v9/users/@me/outbound-promotions/codes", headers=headers, timeout=10).json()
        gift       = ", ".join([f"{g.get('promotion', {}).get('outbound_title', 'None')} -> {g.get('code', 'None')}" for g in gift_codes]) if gift_codes else "None"
    except Exception:
        gift = "None"

    try:
        guilds_response    = requests.get("https://discord.com/api/v9/users/@me/guilds?with_counts=true", headers=headers, timeout=10)
        guilds             = guilds_response.json() if guilds_response.status_code == 200 else []
        guild_count        = len(guilds)
        owner_guilds       = [g for g in guilds if g.get("owner")]
        owner_guilds_count = len(owner_guilds)
        owner_guilds_names = "\n" + ", ".join(f"{g.get('name', 'None')} {red}({white}{g.get('id', 'None')}{red})" for g in owner_guilds) if owner_guilds else ""
    except Exception:
        guild_count        = "None"
        owner_guilds_count = "None"
        owner_guilds_names = ""

    try:
        relationships = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=headers, timeout=10).json()
        friends_list  = [
            f"{f.get('user', {}).get('username', 'None')} {red}({white}{f.get('user', {}).get('id', 'None')}{red})"
            for f in relationships if f.get("type") == 1
        ]
        friends = f"{len(friends_list)}\n{', '.join(friends_list)}" if friends_list else "None"
    except Exception:
        friends = "None"

    Scroll(f"""
 {SUCCESS} Status            :{red} Valid{white}
 {SUCCESS} Token             :{red} {token}{white}
 {SUCCESS} Username          :{red} {username or 'None'}{white}
 {SUCCESS} Display Name      :{red} {api.get('global_name') or 'None'}{white}
 {SUCCESS} User Id           :{red} {user_id or 'None'}{white}
 {SUCCESS} Created At        :{red} {created_at}{white}
 {SUCCESS} Country           :{red} {api.get('locale') or 'None'}{white}
 {SUCCESS} Email             :{red} {api.get('email') or 'None'}{white}
 {SUCCESS} Email Verified    :{red} {api.get('verified')}{white}
 {SUCCESS} Phone             :{red} {api.get('phone') or 'None'}{white}
 {SUCCESS} Nitro             :{red} {nitro_type}{white}
 {SUCCESS} Linked Users      :{red} {linked_users}{white}
 {SUCCESS} Avatar Decoration :{red} {api.get('avatar_decoration') or 'None'}{white}
 {SUCCESS} Avatar Url        :{red} {avatar_url}{white}
 {SUCCESS} Accent Color      :{red} {api.get('accent_color') or 'None'}{white}
 {SUCCESS} Banner            :{red} {api.get('banner') or 'None'}{white}
 {SUCCESS} Banner Color      :{red} {api.get('banner_color') or 'None'}{white}
 {SUCCESS} Flags             :{red} {api.get('flags')}{white}
 {SUCCESS} Public Flags      :{red} {api.get('public_flags')}{white}
 {SUCCESS} Nsfw Allowed      :{red} {api.get('nsfw_allowed')}{white}
 {SUCCESS} Mfa Enabled       :{red} {api.get('mfa_enabled')}{white}
 {SUCCESS} Mfa Type          :{red} {mfa_type}{white}
 {SUCCESS} Billing           :{red} {payment_methods}{white}
 {SUCCESS} Gift Codes        :{red} {gift}{white}
 {SUCCESS} Guilds            :{red} {guild_count}{white}
 {SUCCESS} Owner Guilds      :{red} {owner_guilds_count}{owner_guilds_names}{white}
 {SUCCESS} Bio               :{red} {api.get('bio') or 'None'}{white}
 {SUCCESS} Friends           :{red} {friends}{white}
""")

    Continue()
    Reset()

except Exception as e:
    Error(e)