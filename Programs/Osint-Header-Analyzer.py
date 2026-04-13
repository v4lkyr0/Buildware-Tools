# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
except Exception as e:
    MissingModule(e)

Title("Osint Header Analyzer")
Connection()

security_headers = {
    "Strict-Transport-Security": "Enforces HTTPS connections",
    "Content-Security-Policy": "Prevents XSS and injection attacks",
    "X-Frame-Options": "Prevents clickjacking attacks",
    "X-Content-Type-Options": "Prevents MIME type sniffing",
    "X-XSS-Protection": "XSS filtering (legacy)",
    "Referrer-Policy": "Controls referrer information",
    "Permissions-Policy": "Controls browser feature access",
    "Cross-Origin-Opener-Policy": "Cross-origin isolation",
    "Cross-Origin-Resource-Policy": "Cross-origin resource control",
    "Cross-Origin-Embedder-Policy": "Cross-origin embedding control",
}

try:
    url = input(f"{INPUT} Url {red}->{reset} ").strip()
    if not url:
        ErrorInput()

    if not url.startswith("http"):
        url = "https://" + url

    print(f"{LOADING} Analyzing Headers..", reset)

    headers = {"User-Agent": RandomUserAgents()}
    response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)

    output = ""
    output += f"\n {INFO} Status Code              :{red} {response.status_code}{reset}\n"
    output += f" {INFO} Final Url                :{red} {response.url}{reset}\n"
    output += f" {INFO} Response Time            :{red} {response.elapsed.total_seconds():.3f}s{reset}\n"

    output += f"\n {INFO} Response Headers:\n"

    for header, value in response.headers.items():
        display_value = value[:80] + ".." if len(value) > 80 else value
        output += f" {SUCCESS} {header:40s}:{red} {display_value}{reset}\n"

    output += f"\n {INFO} Security Headers Analysis:\n"

    score = 0
    total = len(security_headers)

    for header, description in security_headers.items():
        value = response.headers.get(header)
        if value:
            output += f" {SUCCESS} {header:40s}:{red} Present{reset}\n"
            score += 1
        else:
            output += f" {ERROR} {header:40s}:{red} Missing ({description}){reset}\n"

    output += f"\n {INFO} Security Score           :{red} {score}/{total}{reset}\n"

    Scroll(output)

    Continue()
    Reset()

except Exception as e:
    Error(e)
