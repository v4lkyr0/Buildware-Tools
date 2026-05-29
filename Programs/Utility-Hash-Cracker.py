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
    import hashlib
    import requests
except Exception as e:
    MissingModule(e)

Title("Hash Cracker")

Scroll(GradientBanner(utilities_banner))

try:
    hash_input = input(f"{INPUT} Hash {red}->{reset} ").strip()

    if not hash_input:
        ErrorInput()

    hash_types = {
        8  : ["crc32"],
        16 : ["md5_half"],
        32 : ["md5", "ntlm", "md4", "ripemd128"],
        40 : ["sha1", "ripemd160", "haval160"],
        48 : ["tiger192", "haval192"],
        56 : ["sha224", "haval224"],
        64 : ["sha256", "sha3_256", "ripemd256", "blake2s", "haval256"],
        96 : ["sha384", "sha3_384"],
        128: ["sha512", "sha3_512", "ripemd512", "blake2b", "whirlpool"],
    }

    supported = [
        "md5", "sha1", "sha224", "sha256", "sha384", "sha512",
        "sha3_256", "sha3_384", "sha3_512", "blake2s", "blake2b",
        "md4", "ripemd160", "ripemd256", "ripemd128",
    ]

    length     = len(hash_input)
    candidates = hash_types.get(length, [])

    if not candidates:
        print(f"{ERROR} Unsupported hash type!", reset)
        Continue()
        Reset()

    hash_type = next((h for h in candidates if h in supported), None)

    if not hash_type:
        print(f"{ERROR} Could not crack this hash type!", reset)
        Continue()
        Reset()

    print(f"{INFO} Using:{red} {hash_type.upper()}", reset)

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

    def HashPassword(password):
        try:
            if hash_type == "blake2s":
                return hashlib.blake2s(password.encode("utf-8")).hexdigest()
            elif hash_type == "blake2b":
                return hashlib.blake2b(password.encode("utf-8")).hexdigest()
            else:
                return hashlib.new(hash_type, password.encode("utf-8")).hexdigest()
        except Exception:
            return None

    found = None

    try:
        for password in wordlist:
            hashed = HashPassword(password)
            if hashed and hashed == hash_input.lower():
                found = password
                print(f"{SUCCESS} Password found:{red} {password}", reset)
                break

    except KeyboardInterrupt:
        print(f"\n{INFO} Stopped.", reset)

    if not found:
        print(f"{ERROR} Password not found!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)