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
    import threading
except Exception as e:
    MissingModule(e)

Title("Username Tracker")

Scroll(GradientBanner(osint_banner))

try:
    username = input(f"{INPUT} Username {red}->{reset} ").strip()

    if not username:
        ErrorInput()

    print(f"{LOADING} Tracking..", reset)

    sites = {
        "Instagram"   : f"https://www.instagram.com/{username}",
        "TikTok"      : f"https://www.tiktok.com/@{username}",
        "X"           : f"https://x.com/{username}",
        "YouTube"     : f"https://www.youtube.com/@{username}",
        "Facebook"    : f"https://www.facebook.com/{username}",
        "Snapchat"    : f"https://www.snapchat.com/add/{username}",
        "Pinterest"   : f"https://www.pinterest.com/{username}",
        "Reddit"      : f"https://www.reddit.com/user/{username}",
        "Tumblr"      : f"https://{username}.tumblr.com",
        "Twitch"      : f"https://www.twitch.tv/{username}",
        "Kick"        : f"https://kick.com/{username}",
        "Rumble"      : f"https://rumble.com/user/{username}",
        "Odysee"      : f"https://odysee.com/@{username}",
        "Linkedin"    : f"https://www.linkedin.com/in/{username}",
        "Vimeo"       : f"https://vimeo.com/{username}",
        "Dailymotion" : f"https://www.dailymotion.com/{username}",
        "Soundcloud"  : f"https://soundcloud.com/{username}",
        "Mixcloud"    : f"https://www.mixcloud.com/{username}",
        "Bandcamp"    : f"https://{username}.bandcamp.com",
        "Flickr"      : f"https://www.flickr.com/people/{username}",
        "Behance"     : f"https://www.behance.net/{username}",
        "Dribbble"    : f"https://dribbble.com/{username}",
        "Deviantart"  : f"https://www.deviantart.com/{username}",
        "500px"       : f"https://500px.com/p/{username}",
        "Unsplash"    : f"https://unsplash.com/@{username}",
        "Vsco"        : f"https://vsco.co/{username}",
        "Periscope"   : f"https://www.periscope.tv/{username}",
        "Clubhouse"   : f"https://www.joinclubhouse.com/@{username}",
        "Mastodon"    : f"https://mastodon.social/@{username}",
        "Bluesky"     : f"https://bsky.app/profile/{username}",
        "Spotify"     : f"https://open.spotify.com/user/{username}",
        "Deezer"      : f"https://www.deezer.com/profile/{username}",
        "Lastfm"      : f"https://www.last.fm/user/{username}",
        "GitHub"      : f"https://github.com/{username}",
        "GitLab"      : f"https://gitlab.com/{username}",
        "Replit"      : f"https://replit.com/@{username}",
        "Hackerrank"  : f"https://www.hackerrank.com/{username}",
        "Leetcode"    : f"https://leetcode.com/{username}",
        "Codecademy"  : f"https://www.codecademy.com/profiles/{username}",
        "Dev.to"      : f"https://dev.to/{username}",
        "Medium"      : f"https://medium.com/@{username}",
        "Npmjs"       : f"https://www.npmjs.com/~{username}",
        "Pypi"        : f"https://pypi.org/user/{username}",
        "Keybase"     : f"https://keybase.io/{username}",
        "Hashnode"    : f"https://hashnode.com/@{username}",
        "Codepen"     : f"https://codepen.io/{username}",
        "Kaggle"      : f"https://www.kaggle.com/{username}",
        "Steam"       : f"https://steamcommunity.com/id/{username}",
        "Roblox"      : f"https://www.roblox.com/user.aspx?username={username}",
        "Minecraft"   : f"https://namemc.com/profile/{username}",
        "Psn"         : f"https://psnprofiles.com/{username}",
        "Xbox"        : f"https://xboxgamertag.com/search/{username}",
        "Faceit"      : f"https://www.faceit.com/en/players/{username}",
        "Battlenet"   : f"https://overwatch.blizzard.com/en-us/career/{username}/",
        "Patreon"     : f"https://www.patreon.com/{username}",
        "Producthunt" : f"https://www.producthunt.com/@{username}",
        "Linktree"    : f"https://linktr.ee/{username}",
        "Cashapp"     : f"https://cash.app/${username}",
        "Paypal"      : f"https://www.paypal.com/paypalme/{username}",
        "Trello"      : f"https://trello.com/{username}",
        "Gravatar"    : f"https://gravatar.com/{username}",
        "About.me"    : f"https://about.me/{username}",
        "Slides"      : f"https://slides.com/{username}",
        "Wordpress"   : f"https://{username}.wordpress.com",
        "Blogger"     : f"https://{username}.blogspot.com",
        "Substack"    : f"https://{username}.substack.com",
    }

    found     = []
    lock      = threading.Lock()
    semaphore = threading.Semaphore(20)

    def CheckSite(site, url):
        with semaphore:
            try:
                response = requests.get(
                    url,
                    headers       = {"User-Agent": RandomUserAgents()},
                    timeout       = 5,
                    allow_redirects = True
                )
                if response.status_code == 200:
                    with lock:
                        found.append(url)
                        print(f"{SUCCESS} {site:<16} :{red} {url}", reset)
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.ConnectionError:
                pass
            except Exception:
                pass

    threads = [threading.Thread(target=CheckSite, args=(site, url), daemon=True) for site, url in sites.items()]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    if not found:
        print(f"{ERROR} No accounts found!", reset)
    else:
        print(f"\n{SUCCESS} Found:{red} {len(found)} account(s) across {len(sites)} sites", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)