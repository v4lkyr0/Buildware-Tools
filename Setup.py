# Copyright (c) 2025-2026 v4lkyr0 — Buildware-Tools
# See the file 'LICENSE' for copying permission.
# --------------------------------------------------------
# EN: Non-commercial use only. Do not sell, remove credits
#     or redistribute without prior written permission.
# FR: Usage non-commercial uniquement. Ne pas vendre, supprimer
#     les crédits ou redistribuer sans autorisation écrite.

from Programs.Core.Config import *

import os
import sys
import subprocess
import ctypes
import importlib.util
import webbrowser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

minimum_python = (3, 10)

def Clear():
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("clear")
 
def Title(title):
    if sys.platform.startswith("win"):
        ctypes.windll.kernel32.SetConsoleTitleW(f"{name_tool} v{version_tool} - [{title}]")
    elif sys.platform.startswith("linux"):
        sys.stdout.write(f"\x1b]2;{name_tool} v{version_tool} - [{title}]\x07")
    elif sys.platform.startswith("darwin"):
        sys.stdout.write(f"\x1b]2;{name_tool} v{version_tool} - [{title}]\x07")

def OpenLinks():
    try:
        webbrowser.open(github_url)
        webbrowser.open(gunslol_url)
    except Exception:
        pass

def CheckPython():
    python_link = "https://www.python.org/downloads/"
    current = sys.version_info[:2]
    if current < minimum_python:
        print(f"[x] {name_tool} requires Python {minimum_python[0]}.{minimum_python[1]} or higher.")
        print(f"[x] Your current version is Python {current[0]}.{current[1]}.")
        print(f"[!]  Download the latest version at: {python_link}")
        webbrowser.open(python_link)
        sys.exit(1)
    print(f"[+] Python {current[0]}.{current[1]} detected.")

def GetMissingModules():
    requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
    missing           = []

    try:
        with open(requirements_path, "r") as f:
            packages = [line.strip() for line in f if line.strip()]
    except Exception:
        print(f"[x] requirements.txt not found!")
        sys.exit(1)

    import_map = {
        "pillow"           : "PIL",
        "beautifulsoup4"   : "bs4",
        "pycryptodome"     : "Crypto",
        "pyzipper"         : "pyzipper",
        "websocket-client" : "websocket",
        "dnspython"        : "dns",
        "pyspeedtest"      : "speedtest",
        "icmplib"          : "icmplib",
    }

    for package in packages:
        import_name = import_map.get(package, package)
        if importlib.util.find_spec(import_name) is None:
            missing.append(package)
 
    return missing

def InstallModules(missing):
    print(f"\n[!] Upgrading pip..")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"],
        check=False,
        stderr=subprocess.DEVNULL
    )

    for package in missing:
        print(f"[!] Installing {package}..")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package, "-q"],
            check=False,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            print(f"[+] {package} installed.")
        else:
            print(f"[x] Failed to install {package}!")

Clear()
Title("Setup")

print(f"[~] Installing required modules for {name_tool}..")

CheckPython()

print("[~] Checking dependencies..")
missing = GetMissingModules()

if not missing:
    print("[+] All dependencies are already installed.")
else:
    print(f"[x] Missing modules!")
    InstallModules(missing)

print(f"\n[~] Opening {name_tool}..")

OpenLinks()
 
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "Buildware.py")])