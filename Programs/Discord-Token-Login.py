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
    from selenium import webdriver
    from selenium.webdriver.chrome.options  import Options as ChromeOptions
    from selenium.webdriver.edge.options    import Options as EdgeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    import time
except Exception as e:
    MissingModule(e)

Title("Token Login")

Scroll(GradientBanner(discord_banner))

try:
    token = ChoiceToken()

    Scroll(f"""
 {PREFIX}01{SUFFIX} Google Chrome
 {PREFIX}02{SUFFIX} Microsoft Edge
 {PREFIX}03{SUFFIX} Mozilla Firefox
""")

    browser_choice = input(f"{INPUT} Browser {red}->{reset} ").strip().lstrip("0")

    if browser_choice not in ["1", "2", "3"]:
        ErrorChoice()

    browser_names = {
        "1": "Google Chrome",
        "2": "Microsoft Edge",
        "3": "Mozilla Firefox",
    }

    browser_name = browser_names[browser_choice]

    print(f"{LOADING} Starting {browser_name}..", reset)

    driver = None

    try:
        if browser_choice == "1":
            options = ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            driver  = webdriver.Chrome(options=options)
        elif browser_choice == "2":
            options = EdgeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            driver  = webdriver.Edge(options=options)
        elif browser_choice == "3":
            options = FirefoxOptions()
            driver  = webdriver.Firefox(options=options)
    except Exception:
        print(f"{ERROR} {browser_name} not installed or driver not found!", reset)
        Continue()
        Reset()

    js_code = f"""
function login(token) {{
    setInterval(() => {{
        document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage.token = `"${{token}}"`;
    }}, 50);
    setTimeout(() => {{
        location.reload();
    }}, 2500);
}}
login("{token}");
"""

    try:
        driver.get("https://discord.com/login")
        time.sleep(2)

        print(f"{LOADING} Injecting..", reset)

        driver.execute_script(js_code)
        time.sleep(5)

        print(f"{SUCCESS} Token injected!", reset)
        print(f"{INFO} If you leave the tool,{red} {browser_name}{white} will close.", reset)

    except Exception:
        print(f"{ERROR} Could not inject token!", reset)
        if driver:
            driver.quit()

    Continue()
    Reset()

except Exception as e:
    Error(e)