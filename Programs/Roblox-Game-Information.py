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
except Exception as e:
    MissingModule(e)

Title("Game Information")

Scroll(GradientBanner(roblox_banner))

try:
    Scroll(f"""
 {PREFIX}01{SUFFIX} Universe Id
 {PREFIX}02{SUFFIX} Place Id
""")

    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    if choice == "1":
        universe_id = input(f"{INPUT} Universe Id {red}->{reset} ").strip()
        if not universe_id or not universe_id.isdigit():
            ErrorId()

    elif choice == "2":
        place_id = input(f"{INPUT} Place Id {red}->{reset} ").strip()
        if not place_id or not place_id.isdigit():
            ErrorId()

        print(f"{LOADING} Resolving..", reset)

        try:
            r = requests.get(f"https://apis.roblox.com/universes/v1/places/{place_id}/universe", timeout=10)
        except Exception:
            print(f"{ERROR} Could not connect!", reset)
            Continue()
            Reset()

        if r.status_code != 200:
            print(f"{ERROR} Could not resolve place id!", reset)
            Continue()
            Reset()

        universe_id = str(r.json().get("universeId", ""))
        if not universe_id:
            ErrorId()

    else:
        ErrorChoice()

    print(f"{LOADING} Fetching..", reset)

    try:
        response = requests.get(f"https://games.roblox.com/v1/games?universeIds={universe_id}", timeout=10)
    except Exception:
        print(f"{ERROR} Could not connect!", reset)
        Continue()
        Reset()

    if response.status_code != 200:
        print(f"{ERROR} Game not found!", reset)
        Continue()
        Reset()

    games = response.json().get("data", [])

    if not games:
        print(f"{ERROR} No game data found!", reset)
        Continue()
        Reset()

    game          = games[0]
    name          = game.get("name",         "None")
    description   = (game.get("description") or "None")[:200]
    creator_name  = game.get("creator", {}).get("name", "None")
    creator_type  = game.get("creator", {}).get("type", "None")
    playing       = game.get("playing",      "None")
    visits        = game.get("visits",       "None")
    max_players   = game.get("maxPlayers",   "None")
    created       = game.get("created",      "None")
    updated       = game.get("updated",      "None")
    favorited     = game.get("favoritedCount", "None")
    genre         = game.get("genre",        "None")
    price         = game.get("price")
    root_place_id = game.get("rootPlaceId",  "None")

    if created and created != "None":
        created = created[:10]
    if updated and updated != "None":
        updated = updated[:10]

    votes_up   = "None"
    votes_down = "None"
    try:
        votes      = requests.get(f"https://games.roblox.com/v1/games/votes?universeIds={universe_id}", timeout=10).json()
        vote_data  = votes.get("data", [{}])[0]
        votes_up   = vote_data.get("upVotes",   "None")
        votes_down = vote_data.get("downVotes", "None")
    except Exception:
        pass

    thumb_url = "None"
    try:
        th        = requests.get(f"https://thumbnails.roblox.com/v1/games/icons?universeIds={universe_id}&size=512x512&format=Png&isCircular=false", timeout=10).json()
        thumb_url = th.get("data", [{}])[0].get("imageUrl", "None")
    except Exception:
        pass

    Scroll(f"""
 {SUCCESS} Universe Id   :{red} {universe_id}{white}
 {SUCCESS} Root Place Id :{red} {root_place_id}{white}
 {SUCCESS} Name          :{red} {name}{white}
 {SUCCESS} Description   :{red} {description}{white}
 {SUCCESS} Creator       :{red} {creator_name} ({creator_type}){white}
 {SUCCESS} Genre         :{red} {genre}{white}
 {SUCCESS} Price         :{red} {price if price else 'Free'}{white}
 {SUCCESS} Created       :{red} {created}{white}
 {SUCCESS} Updated       :{red} {updated}{white}
 {SUCCESS} Playing       :{red} {f'{playing:,}' if isinstance(playing, int) else playing}{white}
 {SUCCESS} Visits        :{red} {f'{visits:,}' if isinstance(visits, int) else visits}{white}
 {SUCCESS} Max Players   :{red} {max_players}{white}
 {SUCCESS} Favorites     :{red} {f'{favorited:,}' if isinstance(favorited, int) else favorited}{white}
 {SUCCESS} Upvotes       :{red} {votes_up}{white}
 {SUCCESS} Downvotes     :{red} {votes_down}{white}
 {SUCCESS} Thumbnail     :{red} {thumb_url}{white}
 {SUCCESS} Game Url      :{red} https://www.roblox.com/games/{root_place_id}{white}
""")

    Continue()
    Reset()

except Exception as e:
    Error(e)