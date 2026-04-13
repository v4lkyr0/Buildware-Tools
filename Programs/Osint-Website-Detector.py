# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import re
except Exception as e:
    MissingModule(e)

Title("Osint Website Detector")
Connection()

try:
    url = input(f"{INPUT} Url {red}->{reset} ").strip()
    if not url:
        ErrorInput()

    if not url.startswith("http"):
        url = "https://" + url

    print(f"{LOADING} Detecting Technologies..", reset)

    headers_req = {"User-Agent": RandomUserAgents()}
    response = requests.get(url, headers=headers_req, timeout=15, allow_redirects=True)
    resp_headers = response.headers
    body = response.text[:50000]

    technologies = []

    server = resp_headers.get("Server", "")
    if server:
        technologies.append(("Server", server))

    powered = resp_headers.get("X-Powered-By", "")
    if powered:
        technologies.append(("Powered By", powered))

    if resp_headers.get("X-AspNet-Version") or resp_headers.get("X-AspNetMvc-Version"):
        technologies.append(("Framework", f"ASP.NET {resp_headers.get('X-AspNet-Version', '')} {resp_headers.get('X-AspNetMvc-Version', '')}".strip()))
    if "x-drupal" in str(resp_headers).lower():
        technologies.append(("CMS", "Drupal"))
    if "wp-" in body or "wordpress" in body.lower():
        technologies.append(("CMS", "WordPress"))
    if "joomla" in body.lower():
        technologies.append(("CMS", "Joomla"))

    if "react" in body.lower() or "_reactRootContainer" in body or "__NEXT_DATA__" in body:
        technologies.append(("JS Framework", "React"))
    if "__NEXT_DATA__" in body or "__next" in body:
        technologies.append(("Framework", "Next.js"))
    if "__NUXT__" in body or "nuxt" in body.lower():
        technologies.append(("Framework", "Nuxt.js"))
    if "vue" in body.lower() and ("v-" in body or "Vue." in body):
        technologies.append(("JS Framework", "Vue.js"))
    if "angular" in body.lower() or "ng-" in body:
        technologies.append(("JS Framework", "Angular"))
    if "svelte" in body.lower():
        technologies.append(("JS Framework", "Svelte"))

    if "cloudflare" in str(resp_headers).lower():
        technologies.append(("CDN", "Cloudflare"))
    if "x-amz" in str(resp_headers).lower() or "amazons3" in str(resp_headers).lower():
        technologies.append(("Cloud", "AWS"))
    if "x-vercel" in str(resp_headers).lower() or "vercel" in str(resp_headers).lower():
        technologies.append(("Hosting", "Vercel"))
    if "netlify" in str(resp_headers).lower():
        technologies.append(("Hosting", "Netlify"))
    if "x-github-request-id" in str(resp_headers).lower():
        technologies.append(("Hosting", "GitHub Pages"))

    if "google-analytics" in body.lower() or "gtag" in body or "ga(" in body:
        technologies.append(("Analytics", "Google Analytics"))
    if "gtm.js" in body or "googletagmanager" in body:
        technologies.append(("Analytics", "Google Tag Manager"))

    cookies = resp_headers.get("Set-Cookie", "")
    if "PHPSESSID" in cookies:
        technologies.append(("Language", "PHP"))
    if "JSESSIONID" in cookies:
        technologies.append(("Language", "Java"))
    if "ASP.NET" in cookies:
        technologies.append(("Language", "ASP.NET"))
    if "csrftoken" in cookies.lower() or "django" in body.lower():
        technologies.append(("Framework", "Django"))
    if "laravel" in cookies.lower() or "laravel" in body.lower():
        technologies.append(("Framework", "Laravel"))

    generator_match = re.search(r'<meta[^>]*name=["\']generator["\'][^>]*content=["\']([^"\']+)', body, re.IGNORECASE)
    if generator_match:
        technologies.append(("Generator", generator_match.group(1)))

    if response.url.startswith("https"):
        technologies.append(("Ssl", "Enabled"))

    output = ""
    if technologies:
        for category, tech in technologies:
            output += f" {SUCCESS} {category:20s}:{red} {tech}{reset}\n"
    else:
        output += f" {INFO} No technologies could be reliably detected.{reset}\n"

    Scroll(f"\n{output}")

    Continue()
    Reset()

except Exception as e:
    Error(e)
