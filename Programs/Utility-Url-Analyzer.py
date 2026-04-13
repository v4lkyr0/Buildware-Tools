# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    from urllib.parse import urlparse
except Exception as e:
    MissingModule(e)

Title("Utility Url Analyzer")
Connection()

try:
    url = input(f"{INPUT} Url {red}->{reset} ").strip()
    if not url:
        ErrorInput()

    if not url.startswith("http"):
        url = "https://" + url

    print(f"{LOADING} Analyzing Url..", reset)

    parsed = urlparse(url)

    headers = {"User-Agent": RandomUserAgents()}
    session = requests.Session()
    response = session.get(url, headers=headers, timeout=15, allow_redirects=True)

    output = ""
    output += f"\n {INFO} Url Structure\n"
    output += f" {SUCCESS} Full Url                 :{red} {url}{reset}\n"
    output += f" {SUCCESS} Scheme                   :{red} {parsed.scheme}{reset}\n"
    output += f" {SUCCESS} Hostname                 :{red} {parsed.hostname}{reset}\n"
    output += f" {SUCCESS} Port                     :{red} {parsed.port or 'Default'}{reset}\n"
    output += f" {SUCCESS} Path                     :{red} {parsed.path or '/'}{reset}\n"
    output += f" {SUCCESS} Query String             :{red} {parsed.query or 'None'}{reset}\n"
    output += f" {SUCCESS} Fragment                 :{red} {parsed.fragment or 'None'}{reset}\n"

    output += f"\n {INFO} Redirect Chain\n"

    if response.history:
        for i, resp in enumerate(response.history):
            output += f" {PREFIX}{i+1}{SUFFIX} [{resp.status_code}] {red}{resp.url}{reset}\n"
        output += f" {PREFIX}F{SUFFIX} [{response.status_code}] {red}{response.url}{reset}\n"
    else:
        output += f" {INFO} No redirects detected.{reset}\n"
        output += f" {SUCCESS} [{response.status_code}] {red}{response.url}{reset}\n"

    output += f"\n {INFO} Response Details\n"
    output += f" {SUCCESS} Final Status Code        :{red} {response.status_code}{reset}\n"
    output += f" {SUCCESS} Content Type             :{red} {response.headers.get('Content-Type', 'N/A')}{reset}\n"
    output += f" {SUCCESS} Content Length           :{red} {len(response.content):,} bytes{reset}\n"
    output += f" {SUCCESS} Server                   :{red} {response.headers.get('Server', 'N/A')}{reset}\n"
    output += f" {SUCCESS} Response Time            :{red} {response.elapsed.total_seconds():.3f}s{reset}\n"
    output += f" {SUCCESS} Encoding                 :{red} {response.encoding or 'N/A'}{reset}\n"

    cookies = response.cookies
    if cookies:
        output += f"\n {INFO} Cookies:\n"
        for cookie in cookies:
            output += f" {SUCCESS} {cookie.name}:{red} {cookie.value[:50]}{'...' if len(cookie.value) > 50 else ''}{reset}\n"

    Scroll(output)

    Continue()
    Reset()

except Exception as e:
    Error(e)
