# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import json
except Exception as e:
    MissingModule(e)

Title("Osint Subdomain Finder")
Connection()

try:
    domain = input(f"{INPUT} Domain {red}->{reset} ").strip().lower()
    if not domain:
        ErrorInput()

    domain = domain.replace("http://", "").replace("https://", "").split("/")[0]

    print(f"{LOADING} Searching For Subdomains..", reset)

    response = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=30)

    if response.status_code != 200:
        print(f"{ERROR} Could not query crt.sh!", reset)
        Continue()
        Reset()

    data = response.json()

    subdomains = set()
    for entry in data:
        name_value = entry.get("name_value", "")
        for name in name_value.split("\n"):
            name = name.strip().lower()
            if name and name.endswith(domain) and "*" not in name:
                subdomains.add(name)

    subdomains = sorted(subdomains)

    if not subdomains:
        print(f"{ERROR} No subdomains found!", reset)
        Continue()
        Reset()

    pad = len(str(len(subdomains)))
    output = f"\n {INFO} Found {len(subdomains)} unique subdomains\n"

    for i, sub in enumerate(subdomains, 1):
        output += f" {PREFIX}{str(i).zfill(pad)}{SUFFIX} {red}{sub}{reset}\n"

    output_dir = os.path.join(tool_path, "Programs", "Output", "SubdomainFinder")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"subdomains_{domain}.txt")

    with open(output_file, "w", encoding="utf-8") as f:
        for sub in subdomains:
            f.write(sub + "\n")

    output += f"\n {SUCCESS} Results saved to {red}Output/SubdomainFinder/subdomains_{domain}.txt{reset}\n"

    Scroll(output)

    if platform_pc == "Windows":
        os.startfile(output_dir)
    else:
        subprocess.Popen(['xdg-open', output_dir])

    Continue()
    Reset()

except Exception as e:
    Error(e)
