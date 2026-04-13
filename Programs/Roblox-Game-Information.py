# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
except Exception as e:
    MissingModule(e)

Title("Roblox Game Information")
Connection()

try:
    Scroll(f"""
 {PREFIX}01{SUFFIX} Search by Universe Id
 {PREFIX}02{SUFFIX} Search by Place Id
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
        print(f"{LOADING} Resolving Place Id..", reset)
        r = requests.get(f"https://apis.roblox.com/universes/v1/places/{place_id}/universe", timeout=10)
        if r.status_code != 200:
            print(f"{ERROR} Could not resolve Place Id!", reset)
            Continue()
            Reset()
        universe_id = str(r.json().get("universeId", ""))
        if not universe_id:
            ErrorId()
    else:
        ErrorChoice()

    print(f"{LOADING} Retrieving Game Information..", reset)

    response = requests.get(f"https://games.roblox.com/v1/games?universeIds={universe_id}", timeout=10)

    if response.status_code != 200:
        print(f"{ERROR} Game not found!", reset)
        Continue()
        Reset()

    games = response.json().get("data", [])
    if not games:
        print(f"{ERROR} No game data found!", reset)
        Continue()
        Reset()

    game = games[0]

    name = game.get("name", "N/A")
    description = game.get("description", "") or "N/A"
    creator_name = game.get("creator", {}).get("name", "N/A")
    creator_type = game.get("creator", {}).get("type", "N/A")
    creator_id = game.get("creator", {}).get("id", "N/A")
    playing = game.get("playing", "N/A")
    visits = game.get("visits", "N/A")
    max_players = game.get("maxPlayers", "N/A")
    created = game.get("created", "N/A")
    updated = game.get("updated", "N/A")
    favorited_count = game.get("favoritedCount", "N/A")
    genre = game.get("genre", "N/A")
    price = game.get("price", "Free")
    is_favorited = game.get("isFavoritedByUser", False)
    root_place_id = game.get("rootPlaceId", "N/A")

    if created and created != "N/A":
        created = created[:10]
    if updated and updated != "N/A":
        updated = updated[:10]

    votes_up = "N/A"
    votes_down = "N/A"
    try:
        votes = requests.get(f"https://games.roblox.com/v1/games/votes?universeIds={universe_id}", timeout=10).json()
        vote_data = votes.get("data", [{}])[0]
        votes_up = vote_data.get("upVotes", "N/A")
        votes_down = vote_data.get("downVotes", "N/A")
    except:
        pass

    thumb_url = "N/A"
    try:
        th = requests.get(f"https://thumbnails.roblox.com/v1/games/icons?universeIds={universe_id}&size=512x512&format=Png&isCircular=false", timeout=10).json()
        thumb_url = th.get("data", [{}])[0].get("imageUrl", "N/A")
    except:
        pass

    Scroll(f"""
 {INFO} Universe Id              :{red} {universe_id}
 {INFO} Root Place Id            :{red} {root_place_id}
 {INFO} Name                     :{red} {name}
 {INFO} Description              :{red} {description[:200]}
 {INFO} Creator                  :{red} {creator_name} ({creator_type})
 {INFO} Genre                    :{red} {genre}
 {INFO} Price                    :{red} {price if price else 'Free'}
 {INFO} Created                  :{red} {created}
 {INFO} Updated                  :{red} {updated}
 {INFO} Currently Playing        :{red} {f'{playing:,}' if isinstance(playing, int) else playing}
 {INFO} Total Visits             :{red} {f'{visits:,}' if isinstance(visits, int) else visits}
 {INFO} Max Players              :{red} {max_players}
 {INFO} Favorites                :{red} {f'{favorited_count:,}' if isinstance(favorited_count, int) else favorited_count}
 {INFO} Upvotes                  :{red} {votes_up}
 {INFO} Downvotes                :{red} {votes_down}
 {INFO} Thumbnail                :{red} {thumb_url}
 {INFO} Game Url                 :{red} https://www.roblox.com/games/{root_place_id}
""")

    Continue()
    Reset()

except Exception as e:
    Error(e)
