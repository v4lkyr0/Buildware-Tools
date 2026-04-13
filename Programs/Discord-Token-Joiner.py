# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
except Exception as e:
    MissingModule(e)

Title("Discord Token Joiner")
Connection()

try:
    token = ChoiceToken()

    invite_input = input(f"{INPUT} Server Invitation {red}->{reset} ").strip()
    if not invite_input:
        ErrorInput()

    invite_code = invite_input.split("/")[-1]

    print(f"{LOADING} Joining Server..", reset)

    headers = {"Authorization": token, "User-Agent": RandomUserAgents()}
    response = requests.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=headers)

    if response.status_code == 200:
        print(f"{SUCCESS} Token joined Server!", reset)
    else:
        print(f"{ERROR} Failed to join Server!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)