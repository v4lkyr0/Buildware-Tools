# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
except Exception as e:
    MissingModule(e)

Title("Osint Email Breach Checker")
Connection()

try:
    email = input(f"{INPUT} Email Address {red}->{reset} ").strip()
    if not email or "@" not in email:
        ErrorInput()

    print(f"{LOADING} Checking For Breaches..", reset)

    headers = {"User-Agent": RandomUserAgents()}

    output = ""

    try:
        response = requests.get(f"https://api.xposedornot.com/v1/check-email/{email}", headers=headers, timeout=15)

        if response.status_code == 404:
            output += f" {SUCCESS} No breaches found!{reset}\n"
            output += f" {INFO} This email does not appear in known breach databases{reset}\n"

        elif response.status_code == 200:
            data = response.json()
            breaches = data.get("breaches", [])

            if not breaches:
                breaches_str = data.get("Exposed in", "")
                if breaches_str:
                    breaches = [b.strip() for b in breaches_str.split(";") if b.strip()]

            if breaches:
                pad = len(str(len(breaches)))
                output += f" {ERROR} Email found in{red} {len(breaches)} {white}Breaches!{reset}\n"
                for i, breach in enumerate(breaches, 1):
                    if isinstance(breach, dict):
                        name = breach.get("name", breach.get("breach", "Unknown"))
                    else:
                        name = str(breach)
                    output += f" {PREFIX}{str(i).zfill(pad)}{SUFFIX} {red}{name}{reset}\n"
            else:
                output += f" {SUCCESS} No breaches found!{reset}\n"
        else:
            output += f" {INFO} Could not determine breach status{reset}\n"
            output += f" {INFO} Try again later or check manually at:{red} https://haveibeenpwned.com/{reset}\n"

    except requests.exceptions.Timeout:
        output += f" {ERROR} Request timed out!{reset}\n"
    except:
        output += f" {INFO} Breach check API unavailable{reset}\n"
        output += f" {INFO} Check manually at:{red} https://haveibeenpwned.com/{reset}\n"

    Scroll(f"\n{output}")

    Continue()
    Reset()

except Exception as e:
    Error(e)
