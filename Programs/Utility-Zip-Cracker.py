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
    import zipfile
    import subprocess
    import requests
    import os
except Exception as e:
    MissingModule(e)

Title("Zip Cracker")

Scroll(GradientBanner(utilities_banner))

try:
    print(f"{INPUT} Select Zip File {red}->{reset} ", reset)

    filepath = BrowseFile("Select Zip File", [("Zip Files", "*.zip"), ("All Files", "*.*")])

    if not filepath:
        print(f"{ERROR} No file selected!", reset)
        Continue()
        Reset()

    if not os.path.exists(filepath):
        print(f"{ERROR} File not found!", reset)
        Continue()
        Reset()

    print(f"{SUCCESS} File:{red} {os.path.basename(filepath)}", reset)

    seven_zip = None
    for path in [
        r"C:\Program Files\7-Zip\7z.exe",
        r"C:\Program Files (x86)\7-Zip\7z.exe",
    ]:
        if os.path.exists(path):
            seven_zip = path
            break

    if not seven_zip:
        print(f"{ERROR} 7-Zip is not installed!", reset)
        Continue()
        Reset()

    result = subprocess.run(
        [seven_zip, "t", "-p ", filepath],
        capture_output=True, timeout=10
    )
    if result.returncode == 0:
        print(f"{SUCCESS} Zip is not password protected!", reset)
        Continue()
        Reset()

    Scroll(f"""
 {PREFIX}01{SUFFIX} Custom Wordlist
 {PREFIX}02{SUFFIX} Built-in Wordlist
""")

    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    wordlist = []

    if choice == "1":
        print(f"{INPUT} Select Wordlist {red}->{reset} ", reset)
        wordlist_path = BrowseFile("Select Wordlist", [("Text Files", "*.txt"), ("All Files", "*.*")])

        if not wordlist_path:
            print(f"{ERROR} No wordlist selected!", reset)
            Continue()
            Reset()

        try:
            with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
                wordlist = [line.strip() for line in f if line.strip()]
        except Exception:
            print(f"{ERROR} Could not read wordlist!", reset)
            Continue()
            Reset()

    elif choice == "2":
        print(f"{LOADING} Fetching wordlist..", reset)

        wordlist_urls = [
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt",
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt",
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/best1050.txt",
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/top-passwords-shortlist.txt",
            "https://raw.githubusercontent.com/praetorian-inc/Hob0Rules/master/wordlists/wordlist.txt",
            "https://raw.githubusercontent.com/berzerk0/Probable-Wordlists/master/Real-Passwords/Top12Thousand-probable-v2.txt",
            "https://raw.githubusercontent.com/jeanphorn/wordlist/master/passlist.txt",
            "https://raw.githubusercontent.com/duyet/bruteforce-database/master/1000000-password-seclists.txt",
            "https://raw.githubusercontent.com/ignis-sec/Pwdb-Public/master/wordlists/ignis-10k.txt",
            "https://raw.githubusercontent.com/nicholasaleks/CrackQ/master/app/wordlists/rockyou-10.txt",
        ]

        for url in wordlist_urls:
            try:
                r = requests.get(url, timeout=15)
                if r.status_code == 200:
                    wordlist = [line.strip() for line in r.text.splitlines() if line.strip()]
                    break
            except Exception:
                continue

        if not wordlist:
            print(f"{ERROR} Could not fetch wordlist!", reset)
            Continue()
            Reset()

    else:
        ErrorChoice()

    if not wordlist:
        print(f"{ERROR} Wordlist is empty!", reset)
        Continue()
        Reset()

    print(f"{SUCCESS} Wordlist:{red} {len(wordlist)}{white} passwords loaded", reset)
    print(f"{LOADING} Cracking..", reset)

    found = None

    try:
        for i, password in enumerate(wordlist):
            try:
                result = subprocess.run(
                    [seven_zip, "t", f"-p{password}", filepath],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode == 0:
                    found = password
                    print(f"{SUCCESS} Password found:{red} {password}", reset)
                    break
            except Exception:
                pass

    except KeyboardInterrupt:
        print(f"\n{INFO} Stopped.", reset)

    if not found:
        print(f"{ERROR} Password not found!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)