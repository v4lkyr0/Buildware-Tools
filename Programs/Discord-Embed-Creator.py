# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
except Exception as e:
    MissingModule(e)

Title("Discord Embed Creator")
Connection()

try:
    webhook = ChoiceWebhook()
    
    print()
    embed_title = input(f"{INPUT} Embed Title {red}->{reset} ").strip()
    embed_description = input(f"{INPUT} Embed Description {red}->{reset} ").strip()
    embed_color = input(f"{INPUT} Embed Color {red}->{reset} ").strip()
    embed_footer = input(f"{INPUT} Footer Text {red}->{reset} ").strip()
    embed_footer_icon = input(f"{INPUT} Footer Icon URL {red}->{reset} ").strip()
    embed_image = input(f"{INPUT} Image URL {red}->{reset} ").strip()
    embed_thumbnail = input(f"{INPUT} Thumbnail URL {red}->{reset} ").strip()
    embed_author = input(f"{INPUT} Author Name {red}->{reset} ").strip()
    embed_author_url = input(f"{INPUT} Author URL {red}->{reset} ").strip()
    embed_author_icon = input(f"{INPUT} Author Icon URL {red}->{reset} ").strip()
    embed_url = input(f"{INPUT} Title URL {red}->{reset} ").strip()
    
    use_timestamp = input(f"{INPUT} Add Current Timestamp? {YESORNO} {red}->{reset} ").strip().lower()
    
    add_fields = input(f"{INPUT} Add Embed Fields? {YESORNO} {red}->{reset} ").strip().lower()
    fields = []
    if add_fields in ['y', 'yes']:
        while True:
            field_name = input(f"{INPUT} Field Name {red}->{reset} ").strip()
            if not field_name:
                break
            field_value = input(f"{INPUT} Field Value {red}->{reset} ").strip()
            field_inline = input(f"{INPUT} Inline? {YESORNO} {red}->{reset} ").strip().lower()
            fields.append({
                "name": field_name,
                "value": field_value if field_value else "No value",
                "inline": field_inline in ['y', 'yes']
            })
    
    embed = {}
    
    if embed_title:
        embed["title"] = embed_title[:256]
    if embed_description:
        embed["description"] = embed_description[:4096]
    if embed_color:
        try:
            embed["color"] = int(embed_color, 16)
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
    if use_timestamp in ['y', 'yes']:
        from datetime import datetime, timezone
        embed["timestamp"] = datetime.now(timezone.utc).isoformat()
    if fields:
        embed["fields"] = fields[:25]
    
    if not embed:
        print(f"{ERROR} No embed data provided!", reset)
        Continue()
        Reset()
    
    print(f"{LOADING} Sending Embed..", reset)
    
    payload = {"embeds": [embed]}
    
    response = requests.post(webhook, json=payload)
    
    if response.status_code in [200, 204]:
        print(f"{SUCCESS} Embed sent!", reset)
    else:
        print(f"{ERROR} Failed to send Embed!", reset)
    
    Continue()
    Reset()

except Exception as e:
    Error(e)
