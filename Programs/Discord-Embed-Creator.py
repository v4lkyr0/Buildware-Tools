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

Title("Embed Creator")

Scroll(GradientBanner(discord_banner))

try:
    webhook = ChoiceWebhook()

    embed_title       = input(f"{INPUT} Title {red}->{reset} ").strip()
    embed_description = input(f"{INPUT} Description {red}->{reset} ").strip()
    embed_color       = input(f"{INPUT} Color {red}->{reset} ").strip()
    embed_footer      = input(f"{INPUT} Footer {red}->{reset} ").strip()
    embed_footer_icon = input(f"{INPUT} Footer Icon Url {red}->{reset} ").strip()
    embed_image       = input(f"{INPUT} Image Url {red}->{reset} ").strip()
    embed_thumbnail   = input(f"{INPUT} Thumbnail Url {red}->{reset} ").strip()
    embed_author      = input(f"{INPUT} Author Name {red}->{reset} ").strip()
    embed_author_url  = input(f"{INPUT} Author Url {red}->{reset} ").strip()
    embed_author_icon = input(f"{INPUT} Author Icon Url {red}->{reset} ").strip()
    embed_url         = input(f"{INPUT} Title Url {red}->{reset} ").strip()
    use_timestamp     = input(f"{INPUT} Timestamp {YESORNO} {red}->{reset} ").strip().lower()
    add_fields        = input(f"{INPUT} Add Fields {YESORNO} {red}->{reset} ").strip().lower()

    fields = []

    if add_fields in ["y", "yes"]:
        print(f"{INFO} Leave{red} Field Name{white} empty to stop adding fields.", reset)
        while len(fields) < 25:
            field_name = input(f"{INPUT} Field Name {red}->{reset} ").strip()
            if not field_name:
                break
            field_value  = input(f"{INPUT} Field Value {red}->{reset} ").strip()
            field_inline = input(f"{INPUT} Inline {YESORNO} {red}->{reset} ").strip().lower()
            fields.append({
                "name"  : field_name[:256],
                "value" : field_value[:1024] if field_value else "\u200b",
                "inline": field_inline in ["y", "yes"],
            })

    embed = {}

    if embed_title:
        embed["title"] = embed_title[:256]

    if embed_description:
        embed["description"] = embed_description[:4096]

    if embed_color:
        try:
            color = embed_color.lstrip("#")
            embed["color"] = int(color, 16)
        except:
            embed["color"] = 0xFF0000

    if embed_footer:
        embed["footer"] = {"text": embed_footer[:2048]}
        if embed_footer_icon:
            embed["footer"]["icon_url"] = embed_footer_icon

    if embed_image:
        embed["image"] = {"url": embed_image}

    if embed_thumbnail:
        embed["thumbnail"] = {"url": embed_thumbnail}

    if embed_author:
        embed["author"] = {"name": embed_author[:256]}
        if embed_author_url:
            embed["author"]["url"] = embed_author_url
        if embed_author_icon:
            embed["author"]["icon_url"] = embed_author_icon

    if embed_url:
        embed["url"] = embed_url

    if use_timestamp in ["y", "yes"]:
        embed["timestamp"] = datetime.now(timezone.utc).isoformat()

    if fields:
        embed["fields"] = fields

    if not embed:
        print(f"{ERROR} No embed data provided!", reset)
        Continue()
        Reset()

    print(f"{LOADING} Sending..", reset)

    response = requests.post(
        webhook,
        json={"embeds": [embed]},
        timeout=10
    )

    if response.status_code in [200, 204]:
        print(f"{SUCCESS} Embed sent!", reset)
    elif response.status_code == 429:
        print(f"{ERROR} Rate limited!", reset)
    elif response.status_code == 400:
        print(f"{ERROR} Invalid embed data!", reset)
    else:
        print(f"{ERROR} Could not send embed!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)