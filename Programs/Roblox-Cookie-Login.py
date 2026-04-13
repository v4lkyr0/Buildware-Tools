# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    from selenium import webdriver
    import time
except Exception as e:
    MissingModule(e)

Title("Roblox Cookie Login")
Connection()

try:
    cookie = ChoiceCookie()

    Scroll(f"""
 {PREFIX}01{SUFFIX} Google Chrome
 {PREFIX}02{SUFFIX} Microsoft Edge
 {PREFIX}03{SUFFIX} Mozilla Firefox
""")
    browser_choice = input(f"{INPUT} Browser {red}->{reset} ").strip().lstrip("0")

    BROWSERS = {
        "1": ("Google Chrome",   webdriver.Chrome),
        "2": ("Microsoft Edge",  webdriver.Edge),
        "3": ("Mozilla Firefox", webdriver.Firefox)
    }

    if browser_choice not in BROWSERS:
        ErrorNumber()

    browser_name, driver_class = BROWSERS[browser_choice]

    try:
        print(f"{LOADING} Starting {browser_name}..", reset)
        driver = driver_class()
    except:
        print(f"{ERROR} {browser_name} not installed or driver not updated!", reset)
        Continue()
        Reset()

    try:
        driver.get("https://www.roblox.com")
        print(f"{LOADING} Injecting Roblox Cookie..", reset)
        driver.add_cookie({"name": ".ROBLOSECURITY", "value": cookie, "domain": ".roblox.com"})
        driver.refresh()
        time.sleep(5)
        print(f"{SUCCESS} Roblox Cookie injected!", reset)
        print(f"{INFO} If you leave the tool, {browser_name} will close.", reset)
        Continue()
        Reset()
    except:
        print(f"{ERROR} Failed to inject Roblox Cookie!", reset)
        Continue()
        Reset()

except Exception as e:
    Error(e)
