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
    import base64
    from pathlib import Path
    import requests
except Exception as e:
    MissingModule(e)

Title("Token Image Changer")

Scroll(GradientBanner(discord_banner))

def HasNitro(token):
    try:
        headers  = {"Authorization": token, "User-Agent": RandomUserAgents()}
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("premium_type", 0) in [1, 2]
    except Exception:
        pass
    return False

def ChangeImage(token, image_path, field, label):
    print(f"{LOADING} Changing..", reset)

    headers    = {
        "Authorization": token,
        "Content-Type" : "application/json",
        "User-Agent"   : RandomUserAgents(),
    }
    mime_types = {
        ".png" : "image/png",
        ".jpg" : "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif" : "image/gif",
    }

    try:
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        print(f"{ERROR} Could not read image file!", reset)
        return

    ext       = Path(image_path).suffix.lower()
    mime_type = mime_types.get(ext, "image/png")

    try:
        response = requests.patch(
            "https://discord.com/api/v9/users/@me",
            headers=headers,
            json={field: f"data:{mime_type};base64,{image_data}"},
            timeout=10
        )

        if response.status_code == 200:
            print(f"{SUCCESS} {label} changed!", reset)
        elif response.status_code == 401:
            print(f"{ERROR} Invalid token!", reset)
        elif response.status_code == 429:
            retry = response.json().get("retry_after", 1)
            print(f"{ERROR} Rate limited!", reset)
        else:
            print(f"{ERROR} Could not change {label}!", reset)

    except requests.exceptions.Timeout:
        print(f"{ERROR} Request timed out!", reset)
    except Exception:
        print(f"{ERROR} Could not change {label}!", reset)

try:
    token = ChoiceToken()

    Scroll(f"""
 {PREFIX}01{SUFFIX} Profile Picture
 {PREFIX}02{SUFFIX} Banner
""")

    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    if choice == "1":
        field      = "avatar"
        label      = "Profile Picture"
        title_text = "Select Profile Picture"
    elif choice == "2":
        field      = "banner"
        label      = "Banner"
        title_text = "Select Banner"
    else:
        ErrorChoice()

    has_nitro  = HasNitro(token)
    file_types = [("Image Files", "*.png;*.jpg;*.jpeg;*.gif")] if has_nitro else [("Image Files", "*.png;*.jpg;*.jpeg")]

    if not has_nitro and field == "banner":
        print(f"{ERROR} Banner requires Nitro!", reset)
        Continue()
        Reset()

    image_path = BrowseFile(title_text, file_types)

    if not image_path:
        print(f"{ERROR} No image selected!", reset)
        Continue()
        Reset()

    print(f"{INFO} Image:{red} {image_path}", reset)

    ChangeImage(token, image_path, field, label)

    Continue()
    Reset()

except Exception as e:
    Error(e)