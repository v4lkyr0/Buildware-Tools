# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import time
except Exception as e:
    MissingModule(e)

Title("Network Website Status")
Connection()

try:
    urls = []
    while True:
        url = input(f"{INPUT} Url {red}->{reset} ").strip()
        if not url:
            break
        if not url.startswith("http"):
            url = "https://" + url
        urls.append(url)

    if not urls:
        ErrorInput()

    print(f"{LOADING} Checking Websites..", reset)

    headers = {"User-Agent": RandomUserAgents()}
    output = ""

    for url in urls:
        try:
            start = time.time()
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            elapsed = time.time() - start

            status = response.status_code
            if 200 <= status < 300:
                output += f"{SUCCESS} Status:{red} Online  {white}| Code:{red} {status} {white}| Time:{red} {elapsed:.3f}s {white}| Url:{red} {url}{reset}\n"
            elif 300 <= status < 400:
                output += f"{INFO} Status:{red} Redirect{white}| Code:{red} {status} {white}| Time:{red} {elapsed:.3f}s {white}| Url:{red} {url}{reset}\n"
            else:
                output += f"{ERROR} Status:{red} Error   {white}| Code:{red} {status} {white}| Time:{red} {elapsed:.3f}s {white}| Url:{red} {url}{reset}\n"

        except requests.exceptions.ConnectionError:
            output += f"{ERROR} Status:{red} Offline {white}| Url:{red} {url}{reset}\n"
        except requests.exceptions.Timeout:
            output += f"{ERROR} Status:{red} Timeout {white}| Url:{red} {url}{reset}\n"
        except Exception:
            output += f"{ERROR} Status:{red} Error   {white}| Url:{red} {url}{reset}\n"

    Scroll(f"\n{output}")

    Continue()
    Reset()

except Exception as e:
    Error(e)
