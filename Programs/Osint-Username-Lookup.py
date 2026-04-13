# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import time
except Exception as e:
    MissingModule(e)

Title("Osint Username Lookup")
Connection()

platforms = {
    "GitHub":        "https://github.com/{}",
    "Twitter / X":   "https://x.com/{}",
    "Instagram":     "https://www.instagram.com/{}/",
    "Reddit":        "https://www.reddit.com/user/{}/",
    "TikTok":        "https://www.tiktok.com/@{}",
    "Pinterest":     "https://www.pinterest.com/{}/",
    "Twitch":        "https://www.twitch.tv/{}",
    "YouTube":       "https://www.youtube.com/@{}",
    "GitLab":        "https://gitlab.com/{}",
    "Steam":         "https://steamcommunity.com/id/{}",
    "SoundCloud":    "https://soundcloud.com/{}",
    "Medium":        "https://medium.com/@{}",
    "Spotify":       "https://open.spotify.com/user/{}",
    "Roblox":        "https://www.roblox.com/user.aspx?username={}",
    "Replit":        "https://replit.com/@{}",
    "HackerOne":     "https://hackerone.com/{}",
    "Keybase":       "https://keybase.io/{}",
    "Pastebin":      "https://pastebin.com/u/{}",
    "DeviantArt":    "https://www.deviantart.com/{}",
    "Flickr":        "https://www.flickr.com/people/{}/",
}

try:
    username = input(f"{INPUT} Username {red}->{reset} ").strip()
    if not username:
        ErrorInput()

    print(f"{LOADING} Searching For Username..", reset)

    found = 0
    not_found = 0
    output = ""

    headers = {"User-Agent": RandomUserAgents()}

    for platform, url_template in platforms.items():
        url = url_template.format(username)
        try:
            response = requests.get(url, headers=headers, timeout=8, allow_redirects=True)

            if response.status_code == 200 and username.lower() in response.url.lower():
                output += f" {SUCCESS} {platform:18s}:{red} {url}{reset}\n"
                found += 1
            else:
                output += f" {ERROR} {platform:18s}:{red} Not Found{reset}\n"
                not_found += 1
        except:
            output += f" {ERROR} {platform:18s}:{red} Timeout / Error{reset}\n"
            not_found += 1

        time.sleep(0.3)

    output += f"\n{INFO} Total found:{red} {found}/{found + not_found}{reset}\n"

    Scroll(f"\n{output}")

    Continue()
    Reset()

except Exception as e:
    Error(e)
