# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import base64
    from pathlib import Path
    import requests
    import tkinter as tk
    from tkinter import filedialog
except Exception as e:
    MissingModule(e)

Title("Discord Token Image Changer")
Connection()

try:
    token = ChoiceToken()

    def HasNitro(token):
        try:
            headers = {"Authorization": token, "User-Agent": RandomUserAgents()}
            response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
            if response.status_code == 200:
                user = response.json()
                premium_type = user.get("premium_type", 0)
                return premium_type in [1, 2]
        except:
            pass
        return False

    def ChoiceImage(title_text):
        root = tk.Tk()
        root.withdraw()

        try:
            root.iconbitmap(os.path.join(tool_path, 'Programs', 'Images', 'BuildwareIcon.ico'))
        except:
            pass

        if HasNitro(token):
            file_types = [("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
        else:
            file_types = [("Image Files", "*.png;*.jpg;*.jpeg")]

        file_path = filedialog.askopenfilename(title=f"{name_tool} {version_tool} - {title_text}", filetypes=file_types)
        return file_path

    def ChangeImage(token, image_path, field, label):
        print(f"{LOADING} Changing {label}..", reset)

        headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": RandomUserAgents()}

        try:
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')

            ext = Path(image_path).suffix.lower()
            mime_types = {
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".gif": "image/gif"
            }
            mime_type = mime_types.get(ext, "image/png")

            data_string = f"data:{mime_type};base64,{image_data}"
            payload = {field: data_string}

            try:
                response = requests.patch("https://discord.com/api/v9/users/@me", headers=headers, json=payload)
                if response.status_code == 200:
                    print(f"{SUCCESS} {label} changed!", reset)
                    return response.json()
                else:
                    print(f"{ERROR} Failed to change {label}!", reset)
                    return None
            except:
                print(f"{ERROR} Error while trying to change {label}!", reset)
                return None

        except:
            print(f"{ERROR} Could not read the Image file!", reset)
            return None

    Scroll(f"""
 {PREFIX}01{SUFFIX} Profile Picture
 {PREFIX}02{SUFFIX} Banner
""")

    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    if choice == "1":
        field = "avatar"
        label = "Profile Picture"
        title_text = "Select Profile Picture"
    elif choice == "2":
        field = "banner"
        label = "Banner"
        title_text = "Select Banner Image"
    else:
        ErrorChoice()

    print(f"{INPUT} Select Image {red}->", reset)

    image_path = ChoiceImage(title_text)
    if not image_path:
        print(f"{ERROR} No Image selected!", reset)
        time.sleep(2)
        Reset()
        sys.exit()

    print(f"{INFO} Image selected:{red} {image_path}", reset)

    ChangeImage(token, image_path, field, label)
    Continue()
    Reset()

except Exception as e:
    Error(e)