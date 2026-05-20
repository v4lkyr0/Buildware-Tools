# Copyright (c) 2025-2026 v4lkyr0 — Buildware-Tools
# See the file 'LICENSE' for copying permission.
# --------------------------------------------------------
# EN: Non-commercial use only. Do not sell, remove credits
#     or redistribute without prior written permission.
# FR: Usage non-commercial uniquement. Ne pas vendre, supprimer
#     les crédits ou redistribuer sans autorisation écrite.

from .Config import *

try:
    import inspect
    import webbrowser
    from colorama import Fore
    import ctypes
    import json
    import shutil
    import os
    import random
    import requests
    import subprocess
    import sys
    import time
    if sys.platform == "win32":
        os.system("chcp 65001 >nul 2>&1")
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception as e:
    print(f'Required Python modules for {name_tool} are not installed. Please run "Setup.py" to install them.')
    input(f"Error: {e}")

try:
    import tkinter as tk
    from tkinter import filedialog
except Exception:
    tk = None
    filedialog = None

username_webhook = name_tool
avatar_webhook   = "https://i.imgur.com/G8QR0f7.png"
color_embed      = 0x880000

red    = Fore.RED
white  = Fore.WHITE
green  = Fore.GREEN
reset  = Fore.RESET
blue   = Fore.BLUE
cyan   = Fore.CYAN
yellow = Fore.YELLOW

PREFIX  = f"{red}[{white}"
SUFFIX  = f"{red}]{white}"
PREFIX1 = f"{red}{{{white}"
SUFFIX1 = f"{red}}}{white}"

YESORNO = f"{red}({white}y/n{red}){white}"
INPUT   = f"{PREFIX}>{SUFFIX}"
INFO    = f"{PREFIX}?{SUFFIX}"
ERROR   = f"{PREFIX}x{SUFFIX}"
SUCCESS = f"{PREFIX}+{SUFFIX}"
LOADING = f"{PREFIX}~{SUFFIX}"

def ColorText(r, g, b, char):
    return f"\033[38;2;{r};{g};{b}m{char}"

tool_path = os.path.dirname(os.path.abspath(__file__)).split("Programs\\")[0].split("Programs/")[0].strip()

try:
    username_pc = os.getlogin()
except Exception:
    username_pc = "user"

try:
    if sys.platform.startswith("win"):
        platform_pc = "Windows"
    elif sys.platform.startswith("linux"):
        platform_pc = "Linux"
    elif sys.platform.startswith("darwin"):
        platform_pc = "macOS"
    else:
        platform_pc = "Unknown"
except Exception:
    platform_pc = "None"

def Connection():
    try:
        requests.get("https://www.google.com", timeout=5)
    except Exception:
        print(f"{ERROR} An internet connection is required to use this feature!", reset)
        Continue()
        Reset()

data_file         = os.path.join(tool_path, "Programs", "Extras", "Config.json")
github_repo_owner = "v4lkyr0"
github_repo_name  = name_tool

def LoadData():
    if os.path.exists(data_file):
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"launched": True, "configured": False, "auto_update": False, "skip_animation": False, "webhooks": [], "tokens": [], "bots": [], "cookies": [], "github_star": "", "page": 1, "plugins_visible": ["Example Plugin"]}

def SaveData(data):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def DecodePat(data):
    import base64
    return base64.b64decode(data.encode()).decode()

def EncodePat(pat):
    import base64
    return base64.b64encode(pat.encode()).decode()

def CheckGithubStar():
    if os.environ.get("star_verified") == "1":
        return True

    data       = LoadData()
    cached_pat = data.get("github_star", "")

    if cached_pat:
        try:
            pat     = DecodePat(cached_pat)
            headers = {"Authorization": f"token {pat}", "Accept": "application/vnd.github.v3+json"}
            print(f"\n{LOADING} Verifying..", reset)
            r = requests.get("https://api.github.com/user", headers=headers, timeout=10)
            if r.status_code == 200:
                username = r.json().get("login", "")
                if IsStargazer(username.lower(), headers):
                    print(f"{SUCCESS} Verified as:{red} {username}{reset}", reset)
                    os.environ["star_verified"] = "1"
                    time.sleep(1)
                    return True
                else:
                    print(f"{ERROR} {red}{username}{reset} has removed the star from the repository!", reset)
                    print(f"{INFO} Please star {red}{github_url}{reset} and try again.", reset)
            else:
                print(f"{ERROR} Verification failed!", reset)
            data["github_star"] = ""
            SaveData(data)
        except:
            print(f"{ERROR} Verification failed!", reset)
            data["github_star"] = ""
            SaveData(data)

    print(f"{INFO} This feature requires you to star the GitHub repository.", reset)
    print(f"{INFO} You need a GitHub Personal Access Token to verify your identity.", reset)
    print(f"{INFO} Link:{red} https://github.com/settings/tokens", reset)

    open_tutorial = input(f"\n{INPUT} Open the tutorial on how to get a GitHub Token? {YESORNO} {red}->{reset} ").strip().lower()
    if open_tutorial in ["y", "yes"]:
        webbrowser.open("https://www.youtube.com/watch?v=X2j8u1hB0aQ")

    print()
    pat = input(f"{INPUT} GitHub Token {red}->{reset} ").strip()
    if not pat:
        print(f"{ERROR} No token provided!", reset)
        time.sleep(2)
        sys.exit()

    print(f"{LOADING} Authenticating..", reset)
    try:
        headers  = {"Authorization": f"token {pat}", "Accept": "application/vnd.github.v3+json"}
        r        = requests.get("https://api.github.com/user", headers=headers, timeout=10)
        if r.status_code != 200:
            print(f"{ERROR} Invalid GitHub token!", reset)
            time.sleep(2)
            sys.exit()

        username = r.json().get("login", "Unknown")
        print(f"{SUCCESS} Authenticated as:{red} {username}{reset}", reset)

        print(f"{LOADING} Checking star..", reset)
        if IsStargazer(username.lower(), headers):
            data                = LoadData()
            data["github_star"] = EncodePat(pat)
            SaveData(data)
            print(f"{SUCCESS} Star verified!", reset)
            os.environ["star_verified"] = "1"
            time.sleep(1)
            return True
        else:
            print(f"{ERROR} {username} has not starred the repository!", reset)
            print(f"{INFO} Please star {github_url} and try again.", reset)
            time.sleep(3)
            sys.exit()
    except:
        print(f"{ERROR} Could not verify. Check your connection.", reset)
        time.sleep(2)
        sys.exit()

def IsStargazer(username, headers):
    page = 1
    while True:
        r = requests.get(
            f"https://api.github.com/repos/{github_repo_owner}/{github_repo_name}/stargazers?per_page=100&page={page}",
            headers=headers, timeout=10
        )
        if r.status_code != 200:
            return False
        users = r.json()
        if not users:
            return False
        for u in users:
            if u.get("login", "").lower() == username:
                return True
        if len(users) < 100:
            return False
        page += 1

def ParseVersion(v):
    try:
        return tuple(int(x) for x in v.strip("v").split("."))
    except Exception:
        return (0,)

def Update():
    url = f"https://api.github.com/repos/{github_repo_owner}/{github_repo_name}/releases/latest"
    try:
        response       = requests.get(url, timeout=10)
        response.raise_for_status()
        release        = response.json()
        github_version = release['tag_name']
    except:
        return ""

    if ParseVersion(github_version) <= ParseVersion(version_tool):
        return ""

    data        = LoadData()
    auto_update = data.get("auto_update", False)

    if not auto_update:
        print(f"{INFO} New version available! {version_tool} {red}->{white} {github_version} {red}|{white} Link:{red} {github_url}/releases/latest", reset)
        return ""

    print(f"{LOADING} Auto-update: {version_tool} {red}->{white} {github_version} {red}|{white} Downloading...", reset)

    try:
        import tempfile
        import zipfile
        import shutil

        zipball_url  = release.get("zipball_url", f"https://api.github.com/repos/{github_repo_owner}/{github_repo_name}/zipball/{github_version}")
        zip_response = requests.get(zipball_url, stream=True, timeout=60)
        zip_response.raise_for_status()

        with tempfile.TemporaryDirectory() as tmp_dir:
            zip_path = os.path.join(tmp_dir, "update.zip")

            with open(zip_path, "wb") as f:
                for chunk in zip_response.iter_content(chunk_size=8192):
                    f.write(chunk)

            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(tmp_dir)

            extracted_dirs = [
                d for d in os.listdir(tmp_dir)
                if os.path.isdir(os.path.join(tmp_dir, d)) and d != "__MACOSX"
            ]
            if not extracted_dirs:
                raise Exception("Empty archive")

            src_dir    = os.path.join(tmp_dir, extracted_dirs[0])
            inner_dirs = [
                d for d in os.listdir(src_dir)
                if os.path.isdir(os.path.join(src_dir, d))
            ]

            if inner_dirs and len(os.listdir(src_dir)) == 1:
                src_dir = os.path.join(src_dir, inner_dirs[0])

            for item in os.listdir(src_dir):
                src = os.path.join(src_dir, item)
                dst = os.path.join(tool_path, item)
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                    else:
                        shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

        print(f"{SUCCESS} Updated to {github_version}", reset)
        time.sleep(1.5)

        if platform_pc == "Windows":
            subprocess.Popen(['python', os.path.join(tool_path, 'Buildware.py')])
        else:
            subprocess.Popen(['python3', os.path.join(tool_path, 'Buildware.py')])

        sys.exit(0)

    except Exception as e:
        print(f"{ERROR} Auto-update failed! |{white} Link:{red} {github_url}/releases/latest", reset)

def CheckLaunch():
    if not os.environ.get("bkey"):
        sys.exit()

def Clear():
    if platform_pc == "Windows":
        os.system("cls")
    elif platform_pc == "Linux":
        os.system("clear")
    elif platform_pc == "macOS":
        os.system("clear")

def Title(title):
    if platform_pc == "Windows":
        ctypes.windll.kernel32.SetConsoleTitleW(f"{name_tool} v{version_tool} - [{title}]")
    elif platform_pc == "Linux":
        sys.stdout.write(f"\x1b]2;{name_tool} v{version_tool} - [{title}]\x07")
    elif platform_pc == "macOS":
        sys.stdout.write(f"\x1b]2;{name_tool} v{version_tool} - [{title}]\x07")

def Reset():
    if platform_pc == "Windows":
        file = ['python', os.path.join(tool_path, 'Buildware.py'), '--no-anim']
        subprocess.run(file)
    elif platform_pc == "Linux":
        file = ['python3', os.path.join(tool_path, 'Buildware.py'), '--no-anim']
        subprocess.run(file)
    elif platform_pc == "macOS":
        file = ['python3', os.path.join(tool_path, 'Buildware.py'), '--no-anim']
        subprocess.run(file)

def StartProgram(program):
    programs_dir = os.path.join(tool_path, 'Programs')
    if platform_pc == "Windows":
        file = ['python', os.path.join(programs_dir, program)]
        subprocess.run(file, cwd=programs_dir)
    elif platform_pc == "Linux":
        file = ['python3', os.path.join(programs_dir, program)]
        subprocess.run(file, cwd=programs_dir)
    elif platform_pc == "macOS":
        file = ['python3', os.path.join(programs_dir, program)]
        subprocess.run(file, cwd=programs_dir)

def Scroll(text):
    for line in text.split("\n"):
        print(line)
        time.sleep(0.03)

def Continue():
    input(f"{INPUT} Press to continue {red}->{reset} ")

def Error(e):
    print(f"{ERROR} Error:{red} {e}", reset)
    Continue()
    sys.exit()

def ErrorFeature():
    print(f"{ERROR} This feature is not available!", reset)
    time.sleep(2)
    Reset()

def ErrorChoice():
    print(f"{ERROR} Invalid choice!", reset)
    time.sleep(2)
    Reset()

def ErrorId():
    print(f"{ERROR} Invalid Id!", reset)
    time.sleep(2)
    Reset()

def ErrorUrl():
    print(f"{ERROR} Invalid Url!", reset)
    time.sleep(2)
    Reset()

def ErrorToken():
    print(f"{ERROR} Invalid Token!", reset)
    time.sleep(2)
    Reset()

def ErrorNumber():
    print(f"{ERROR} Invalid Number!", reset)
    time.sleep(2)
    Reset()

def ErrorInput():
    print(f"{ERROR} Invalid Input!", reset)
    time.sleep(2)
    Reset()

def ErrorMode():
    print(f"{ERROR} Invalid Mode!", reset)
    time.sleep(2)
    Reset()

def ErrorWebhook():
    print(f"{ERROR} Invalid Webhook!", reset)
    time.sleep(2)
    Reset()

def ErrorBot():
    print(f"{ERROR} Invalid Bot Token!", reset)
    time.sleep(2)
    Reset()

def ErrorCookie():
    print(f"{ERROR} Invalid Roblox Cookie!", reset)
    time.sleep(2)
    Reset()

def MissingModule(e):
    print(f"{ERROR} Missing Module:{red} {e}", reset)
    Continue()
    Reset()

def BrowseFile(title="Select File", file_types=None):
    if file_types is None:
        file_types = [("All Files", "*.*")]
    root = tk.Tk()
    root.withdraw()
    try:
        root.iconbitmap(os.path.join(tool_path, 'Programs', 'Images', 'BuildwareIcon.ico'))
    except Exception:
        pass
    file_path = filedialog.askopenfilename(
        title=f"{name_tool} v{version_tool} - [{title}]",
        filetypes=file_types
    )
    root.destroy()
    return file_path

def BloodAnimation():
    cols = shutil.get_terminal_size().columns
    rows = shutil.get_terminal_size().lines - 2

    hide  = "\033[?25l"
    show  = "\033[?25h"
    clear = "\033[2J\033[H"

    num_cols = cols

    def BloodColor(intensity):
        if intensity > 0.85:
            return "\033[38;2;180;0;0m"
        elif intensity > 0.65:
            return "\033[38;2;140;0;0m"
        elif intensity > 0.45:
            return "\033[38;2;100;0;0m"
        elif intensity > 0.25:
            return "\033[38;2;60;0;0m"
        else:
            return "\033[38;2;30;0;0m"

    drop_chars  = "█▓▒░╽╿│┃|╎╏"
    head_chars  = "▼▽⬇╤╥"
    splat_chars = "╸╺╾╼─╌┄"

    drops = []
    for _ in range(num_cols):
        drops.append({
            "pos"    : random.uniform(-rows, 0),
            "speed"  : random.uniform(0.3, 1.2),
            "length" : random.randint(4, min(rows - 1, 18)),
            "active" : True,
            "drip"   : random.uniform(0.0, 1.0),
            "wobble" : random.uniform(0.0, 0.3),
        })

    grid   = [[" "] * num_cols for _ in range(rows)]
    colors = [[""]  * num_cols for _ in range(rows)]
    splats = {}

    def ClearGrid():
        for r in range(rows):
            for c in range(num_cols):
                grid[r][c]   = " "
                colors[r][c] = ""

    def UpdateDrops(exit_mode=False):
        all_gone = True

        for col, drop in enumerate(drops):
            if not drop["active"]:
                continue

            head   = int(drop["pos"])
            length = drop["length"]
            speed  = drop["speed"]

            for i in range(length + 1):
                r = head - i
                if 0 <= r < rows:
                    intensity = 1.0 - (i / length)
                    intensity = max(0.05, intensity + random.uniform(-0.1, 0.1))

                    if i == 0:
                        grid[r][col]   = random.choice(head_chars)
                        colors[r][col] = "\033[38;2;220;10;10m"
                    elif i == 1:
                        grid[r][col]   = random.choice(drop_chars[:3])
                        colors[r][col] = "\033[38;2;190;5;5m"
                    else:
                        grid[r][col]   = random.choice(drop_chars)
                        colors[r][col] = BloodColor(intensity)

            tail = head - length - 1
            if 0 <= tail < rows:
                grid[tail][col]   = " "
                colors[tail][col] = ""

            drop["pos"] += speed + random.uniform(-drop["wobble"], drop["wobble"])

            if drop["pos"] - length > rows:
                if exit_mode:
                    for r in range(rows):
                        grid[r][col]   = " "
                        colors[r][col] = ""
                    drop["active"] = False
                else:
                    for r in range(rows):
                        grid[r][col]   = " "
                        colors[r][col] = ""

                    if rows - 1 not in splats:
                        splats[col] = {
                            "char" : random.choice(splat_chars),
                            "color": "\033[38;2;80;0;0m",
                            "ttl"  : random.randint(8, 20),
                        }

                    drop["pos"]    = random.uniform(-rows * 0.6, 0)
                    drop["speed"]  = random.uniform(0.3, 1.2)
                    drop["length"] = random.randint(4, min(rows - 1, 18))
                    drop["drip"]   = random.uniform(0.0, 1.0)
                    drop["wobble"] = random.uniform(0.0, 0.3)
            else:
                if exit_mode:
                    all_gone = False

        dead_cols = [c for c, s in list(splats.items()) if s["ttl"] <= 0]
        for c in dead_cols:
            del splats[c]
            if 0 <= rows - 1 < rows:
                grid[rows - 1][c]   = " "
                colors[rows - 1][c] = ""

        for c, s in splats.items():
            if 0 <= rows - 1 < rows:
                grid[rows - 1][c]   = s["char"]
                colors[rows - 1][c] = s["color"]
            s["ttl"] -= 1

        return all_gone

    def Render():
        frame = clear
        for row in range(rows):
            line = ""
            for col in range(num_cols):
                c   = grid[row][col]
                clr = colors[row][col]
                line += (clr + c + "\033[0m") if (c != " " and clr) else " "
            frame += line + "\n"
        print(frame, end="", flush=True)

    def RenderBlank():
        print(clear + "\n" * rows, end="", flush=True)

    try:
        print(hide, end="", flush=True)

        RenderBlank()
        time.sleep(0.5)

        start = time.time()
        while time.time() - start < 2.5:
            ClearGrid()
            UpdateDrops(exit_mode=False)
            Render()
            time.sleep(0.04)

        for drop in drops:
            drop["speed"] = max(drop["speed"], 1.5)

        while True:
            ClearGrid()
            all_gone = UpdateDrops(exit_mode=True)
            Render()
            time.sleep(0.04)
            if all_gone:
                break

        RenderBlank()
        time.sleep(0.5)

    finally:
        print(show + clear, end="", flush=True)

def StarRequired(text):
    start_color = (255, 215, 0)
    end_color   = (184, 134, 11)
    num_steps   = 3
    colors      = []

    for i in range(num_steps):
        R = start_color[0] + (end_color[0] - start_color[0]) * i // (num_steps - 1)
        G = start_color[1] + (end_color[1] - start_color[1]) * i // (num_steps - 1)
        B = start_color[2] + (end_color[2] - start_color[2]) * i // (num_steps - 1)
        colors.append((R, G, B))

    colors += list(reversed(colors[:-1]))

    result      = []
    color_index = 0

    for char in text:
        if char == '\n':
            result.append('\033[0m\n')
        else:
            color = colors[color_index % len(colors)]
            result.append(ColorText(*color, char))
            color_index += 1

    result.append('\033[0m')
    return ''.join(result)

def Premium(text):
    start_color = (186, 85, 211)
    end_color   = (123, 31, 162)
    num_steps   = 3
    colors      = []

    for i in range(num_steps):
        R = start_color[0] + (end_color[0] - start_color[0]) * i // (num_steps - 1)
        G = start_color[1] + (end_color[1] - start_color[1]) * i // (num_steps - 1)
        B = start_color[2] + (end_color[2] - start_color[2]) * i // (num_steps - 1)
        colors.append((R, G, B))

    colors += list(reversed(colors[:-1]))

    result      = []
    color_index = 0

    for char in text:
        if char == '\n':
            result.append('\033[0m\n')
        else:
            color = colors[color_index % len(colors)]
            result.append(ColorText(*color, char))
            color_index += 1

    result.append('\033[0m')
    return ''.join(result)

def Gradient(text, include_zero=False):
    start_color = (223, 5, 5)
    end_color   = (121, 3, 3)
    num_steps   = 10
    colors      = []

    for i in range(num_steps):
        R = start_color[0] + (end_color[0] - start_color[0]) * i // (num_steps - 1)
        G = start_color[1] + (end_color[1] - start_color[1]) * i // (num_steps - 1)
        B = start_color[2] + (end_color[2] - start_color[2]) * i // (num_steps - 1)
        colors.append((R, G, B))

    colors += list(reversed(colors[:-1]))
    chars = '╖╜╙╓┴┼┘┤└┐▌▀()╚╗═╔╝─┬├┌└│]░▒░▒█▓▄'
    if include_zero:
        chars += '0'

    lines  = text.split('\n')
    result = []

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char in chars:
                color = colors[(i + j) % len(colors)]
                result.append(ColorText(*color, char))
            else:
                result.append(char)
        result.append('\033[0m\n')

    return ''.join(result)

def GradientBanner(text):
    return Gradient(text, include_zero=True)

def RandomUserAgents():
    file = os.path.join(tool_path, "Programs", "Extras", "UserAgents.txt")
    try:
        with open(file, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
        if lines:
            return random.choice(lines)
    except Exception:
        pass
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def CheckWebhook(webhook):
    try:
        response = requests.get(webhook, timeout=5)
        return response.status_code in (200, 204)
    except Exception:
        return None

def CheckToken(token):
    api     = "https://discord.com/api/v9/users/@me"
    headers = {"Authorization": token, "User-Agent": RandomUserAgents()}
    try:
        response = requests.get(api, headers=headers, timeout=5)
        return response.status_code == 200
    except Exception:
        return None

def SaveWebhook(webhook):
    if CheckWebhook(webhook) is True:
        data = LoadData()
        if webhook not in data.get("webhooks", []):
            data.setdefault("webhooks", []).append(webhook)
            SaveData(data)
        return True
    return False

def SaveToken(token):
    if CheckToken(token) is True:
        data = LoadData()
        if token not in data.get("tokens", []):
            data.setdefault("tokens", []).append(token)
            SaveData(data)
        return True
    return False

def CheckBot(bot_token):
    api     = "https://discord.com/api/v9/users/@me"
    headers = {"Authorization": f"Bot {bot_token}", "User-Agent": RandomUserAgents()}
    try:
        response = requests.get(api, headers=headers, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception:
        return None

def SaveBot(bot_token):
    result = CheckBot(bot_token)
    if result is True:
        data = LoadData()
        if bot_token not in data.get("bots", []):
            data.setdefault("bots", []).append(bot_token)
            SaveData(data)
        return True
    return False

def CheckCookie(cookie):
    try:
        session                        = requests.Session()
        session.cookies[".ROBLOSECURITY"] = cookie
        response                       = session.get("https://users.roblox.com/v1/users/authenticated", timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception:
        return None

def SaveCookie(cookie):
    result = CheckCookie(cookie)
    if result is True:
        data = LoadData()
        if cookie not in data.get("cookies", []):
            data.setdefault("cookies", []).append(cookie)
            SaveData(data)
        return True
    return False

def ChoiceWebhook():
    data      = LoadData()
    path_name = f'{red}"{white}Programs/Extras/Config.json{red}"{white}'

    webhooks_list = [w for w in data.get("webhooks", []) if w.strip()]

    webhooks       = {}
    valid_webhooks = {}

    for i, wh in enumerate(webhooks_list, 1):
        webhooks[i] = wh
        if CheckWebhook(wh):
            valid_webhooks[i] = wh

    if not webhooks:
        print(f"{INFO} No Webhook found in {path_name}!", reset)
        while True:
            new_webhook = input(f"{INPUT} Webhook Url {red}->{reset} ").strip()
            if CheckWebhook(new_webhook):
                data.setdefault("webhooks", []).append(new_webhook)
                SaveData(data)
                print(f"{SUCCESS} Webhook added to {path_name}.", reset)
                time.sleep(1)
                return new_webhook
            else:
                ErrorWebhook()

    if not valid_webhooks:
        print(f"{INFO} No valid Webhook found in {path_name}!", reset)
        while True:
            new_webhook = input(f"{INPUT} Webhook Url {red}->{reset} ").strip()
            if CheckWebhook(new_webhook):
                data.setdefault("webhooks", []).append(new_webhook)
                SaveData(data)
                print(f"{SUCCESS} Webhook added to {path_name}.", reset)
                time.sleep(1)
                return new_webhook
            else:
                ErrorWebhook()

    print()
    for num, wh in webhooks.items():
        token_webhook  = wh.split("/")[-1]
        masked_webhook = token_webhook[:30] + ".." if len(token_webhook) > 30 else token_webhook
        if num in valid_webhooks:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Valid{white}   | Webhook:{red} {masked_webhook}", reset)
        else:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Invalid{white} | Webhook:{red} {masked_webhook}", reset)

    print(f'\n{INFO} To add more Webhooks, open {path_name}.', reset)

    try:
        choice = int(input(f"{INPUT} Choice {red}->{reset} ").strip())
    except ValueError:
        ErrorChoice()

    if choice not in webhooks:
        ErrorChoice()

    if choice in valid_webhooks:
        return valid_webhooks[choice]
    else:
        ErrorWebhook()

def ChoiceToken():
    data      = LoadData()
    path_name = f'{red}"{white}Programs/Extras/Config.json{red}"{white}'

    tokens_list = [t for t in data.get("tokens", []) if t.strip()]

    tokens       = {}
    valid_tokens = {}

    for i, tok in enumerate(tokens_list, 1):
        tokens[i] = tok
        if CheckToken(tok):
            valid_tokens[i] = tok

    if not tokens:
        print(f"{INFO} No Token found in {path_name}!", reset)
        while True:
            new_token = input(f"{INPUT} Token {red}->{reset} ").strip()
            if CheckToken(new_token):
                data.setdefault("tokens", []).append(new_token)
                SaveData(data)
                print(f"{SUCCESS} Token added to {path_name}.", reset)
                time.sleep(1)
                return new_token
            else:
                ErrorToken()

    if not valid_tokens:
        print(f"{INFO} No valid Token found in {path_name}!", reset)
        while True:
            new_token = input(f"{INPUT} Token {red}->{reset} ").strip()
            if CheckToken(new_token):
                data.setdefault("tokens", []).append(new_token)
                SaveData(data)
                print(f"{SUCCESS} Token added to {path_name}.", reset)
                time.sleep(1)
                return new_token
            else:
                ErrorToken()

    print()
    for num, tok3n in tokens.items():
        masked_token = tok3n[:30] + ".." if len(tok3n) > 30 else tok3n
        if num in valid_tokens:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Valid{white}   | Token:{red} {masked_token}", reset)
        else:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Invalid{white} | Token:{red} {masked_token}", reset)

    print(f'\n{INFO} To add more Tokens, open {path_name}.', reset)

    try:
        choice = int(input(f"{INPUT} Choice {red}->{reset} ").strip())
    except ValueError:
        ErrorChoice()

    if choice not in tokens:
        ErrorChoice()

    if choice in valid_tokens:
        return valid_tokens[choice]
    else:
        ErrorToken()

def ChoiceMultiToken():
    data      = LoadData()
    path_name = f'{red}"{white}Programs/Extras/Config.json{red}"{white}'

    tokens_list = [t for t in data.get("tokens", []) if t.strip()]

    tokens       = {}
    valid_tokens = {}

    for i, tok in enumerate(tokens_list, 1):
        tokens[i] = tok
        if CheckToken(tok):
            valid_tokens[i] = tok

    if not tokens:
        print(f"{INFO} No Token found in {path_name}!", reset)
        print(f"{ERROR} Please add Tokens to {path_name}.", reset)
        time.sleep(2)
        Reset()

    if not valid_tokens:
        print(f"{INFO} No valid Token found in {path_name}!", reset)
        print(f"{ERROR} Please add valid Tokens to {path_name}.", reset)
        time.sleep(2)
        Reset()

    print()
    for num, tok3n in tokens.items():
        masked_token = tok3n[:30] + ".." if len(tok3n) > 30 else tok3n
        if num in valid_tokens:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Valid{white}   | Token:{red} {masked_token}", reset)
        else:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Invalid{white} | Token:{red} {masked_token}", reset)

    print(f'\n {INFO} To add more Tokens, open {path_name}.')

    while True:
        try:
            num_tokens = int(input(f"{INPUT} Number {red}->{reset} ").strip())
            if num_tokens <= 0:
                ErrorNumber()
            if num_tokens > len(valid_tokens):
                print(f"{ERROR} Not enough valid Tokens!", reset)
                time.sleep(2)
                Reset()
            break
        except ValueError:
            ErrorNumber()

    selected_tokens = []

    for i in range(num_tokens):
        while True:
            try:
                choice = int(input(f"{INPUT} Token {i + 1} {red}->{reset} ").strip())
                if choice not in tokens:
                    ErrorChoice()
                if choice not in valid_tokens:
                    ErrorToken()
                if valid_tokens[choice] not in selected_tokens:
                    selected_tokens.append(valid_tokens[choice])
                    break
                else:
                    print(f"{ERROR} Token already selected!", reset)
                    Continue()
                    Reset()
            except ValueError:
                ErrorNumber()

    return selected_tokens

def ChoiceMultiWebhook():
    data      = LoadData()
    path_name = f'{red}"{white}Programs/Extras/Config.json{red}"{white}'

    webhooks_list = [w for w in data.get("webhooks", []) if w.strip()]

    webhooks       = {}
    valid_webhooks = {}

    for i, wh in enumerate(webhooks_list, 1):
        webhooks[i] = wh
        if CheckWebhook(wh):
            valid_webhooks[i] = wh

    if not webhooks:
        print(f"{INFO} No Webhook found in {path_name}!", reset)
        print(f"{ERROR} Please add Webhooks to {path_name}.", reset)
        time.sleep(2)
        Reset()

    if not valid_webhooks:
        print(f"{INFO} No valid Webhook found in {path_name}!", reset)
        print(f"{ERROR} Please add valid Webhooks to {path_name}.", reset)
        time.sleep(2)
        Reset()

    print()
    for num, wh in webhooks.items():
        token_webhook  = wh.split("/")[-1]
        masked_webhook = token_webhook[:30] + ".." if len(token_webhook) > 30 else token_webhook
        if num in valid_webhooks:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Valid{white}   | Webhook:{red} {masked_webhook}", reset)
        else:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Invalid{white} | Webhook:{red} {masked_webhook}", reset)

    print(f'\n{INFO} To add more Webhooks, open {path_name}.')

    while True:
        try:
            num_webhooks = int(input(f"{INPUT} Number {red}->{reset} ").strip())
            if num_webhooks <= 0:
                ErrorNumber()
            if num_webhooks > len(valid_webhooks):
                print(f"{ERROR} Not enough valid Webhooks!", reset)
                time.sleep(2)
                Reset()
            break
        except ValueError:
            ErrorNumber()

    selected_webhooks = []

    for i in range(num_webhooks):
        while True:
            try:
                choice = int(input(f"{INPUT} Webhook {i + 1} {red}->{reset} ").strip())
                if choice not in webhooks:
                    ErrorChoice()
                if choice not in valid_webhooks:
                    ErrorWebhook()
                if valid_webhooks[choice] not in selected_webhooks:
                    selected_webhooks.append(valid_webhooks[choice])
                    break
                else:
                    print(f"{ERROR} Webhook already selected!", reset)
                    Continue()
                    Reset()
            except ValueError:
                ErrorNumber()

    return selected_webhooks

def ChoiceBot():
    data      = LoadData()
    path_name = f'{red}"{white}Programs/Extras/Config.json{red}"{white}'

    bots_list = [b for b in data.get("bots", []) if b.strip()]

    bots       = {}
    valid_bots = {}

    for i, bot in enumerate(bots_list, 1):
        bots[i] = bot
        if CheckBot(bot):
            valid_bots[i] = bot

    if not bots:
        print(f"{INFO} No Bot found in {path_name}!", reset)
        while True:
            new_bot = input(f"{INPUT} Bot Token {red}->{reset} ").strip()
            if CheckBot(new_bot):
                data.setdefault("bots", []).append(new_bot)
                SaveData(data)
                print(f"{SUCCESS} Bot added to {path_name}.", reset)
                time.sleep(1)
                return new_bot
            else:
                ErrorBot()

    if not valid_bots:
        print(f"{INFO} No valid Bot found in {path_name}!", reset)
        while True:
            new_bot = input(f"{INPUT} Bot Token {red}->{reset} ").strip()
            if CheckBot(new_bot):
                data.setdefault("bots", []).append(new_bot)
                SaveData(data)
                print(f"{SUCCESS} Bot added to {path_name}.", reset)
                time.sleep(1)
                return new_bot
            else:
                ErrorBot()

    print()
    for num, bot in bots.items():
        masked_bot = bot[:30] + ".." if len(bot) > 30 else bot
        if num in valid_bots:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Valid{white}   | Bot:{red} {masked_bot}", reset)
        else:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Invalid{white} | Bot:{red} {masked_bot}", reset)

    print(f'\n{INFO} To add more Bots, open {path_name}.', reset)

    try:
        choice = int(input(f"{INPUT} Choice {red}->{reset} ").strip())
    except ValueError:
        ErrorChoice()

    if choice not in bots:
        ErrorChoice()

    if choice in valid_bots:
        return valid_bots[choice]
    else:
        ErrorBot()

def ChoiceMultiBot():
    data      = LoadData()
    path_name = f'{red}"{white}Programs/Extras/Config.json{red}"{white}'

    bots_list = [b for b in data.get("bots", []) if b.strip()]

    bots       = {}
    valid_bots = {}

    for i, bot in enumerate(bots_list, 1):
        bots[i] = bot
        if CheckBot(bot):
            valid_bots[i] = bot

    if not bots:
        print(f"{INFO} No Bot found in {path_name}!", reset)
        print(f"{ERROR} Please add Bots to {path_name}.", reset)
        time.sleep(2)
        Reset()

    if not valid_bots:
        print(f"{INFO} No valid Bot found in {path_name}!", reset)
        print(f"{ERROR} Please add valid Bots to {path_name}.", reset)
        time.sleep(2)
        Reset()

    print()
    for num, bot in bots.items():
        masked_bot = bot[:30] + ".." if len(bot) > 30 else bot
        if num in valid_bots:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Valid{white}   | Bot:{red} {masked_bot}", reset)
        else:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Invalid{white} | Bot:{red} {masked_bot}", reset)

    print(f'\n{INFO} To add more Bots, open {path_name}.')

    while True:
        try:
            num_bots = int(input(f"{INPUT} Number {red}->{reset} ").strip())
            if num_bots <= 0:
                ErrorNumber()
            if num_bots > len(valid_bots):
                print(f"{ERROR} Not enough valid Bots!", reset)
                time.sleep(2)
                Reset()
            break
        except ValueError:
            ErrorNumber()

    selected_bots = []

    for i in range(num_bots):
        while True:
            try:
                choice = int(input(f"{INPUT} Bot {i + 1} {red}->{reset} ").strip())
                if choice not in bots:
                    ErrorChoice()
                if choice not in valid_bots:
                    print(f"{ERROR} Invalid Bot Token!", reset)
                    time.sleep(2)
                    Reset()
                if valid_bots[choice] not in selected_bots:
                    selected_bots.append(valid_bots[choice])
                    break
                else:
                    print(f"{ERROR} Bot already selected!", reset)
                    Continue()
                    Reset()
            except ValueError:
                ErrorNumber()

    return selected_bots

def ChoiceCookie():
    data      = LoadData()
    path_name = f'{red}"{white}Programs/Extras/Config.json{red}"{white}'

    cookies_list = [c for c in data.get("cookies", []) if c.strip()]

    cookies       = {}
    valid_cookies = {}

    for i, ck in enumerate(cookies_list, 1):
        cookies[i] = ck
        if CheckCookie(ck):
            valid_cookies[i] = ck

    if not cookies:
        print(f"{INFO} No Roblox Cookie found in {path_name}!", reset)
        while True:
            new_cookie = input(f"{INPUT} Roblox Cookie {red}->{reset} ").strip()
            if CheckCookie(new_cookie):
                data.setdefault("cookies", []).append(new_cookie)
                SaveData(data)
                print(f"{SUCCESS} Roblox Cookie added to {path_name}.", reset)
                time.sleep(1)
                return new_cookie
            else:
                ErrorCookie()

    if not valid_cookies:
        print(f"{INFO} No valid Roblox Cookie found in {path_name}!", reset)
        while True:
            new_cookie = input(f"{INPUT} Roblox Cookie {red}->{reset} ").strip()
            if CheckCookie(new_cookie):
                data.setdefault("cookies", []).append(new_cookie)
                SaveData(data)
                print(f"{SUCCESS} Roblox Cookie added to {path_name}.", reset)
                time.sleep(1)
                return new_cookie
            else:
                ErrorCookie()

    print()
    for num, ck in cookies.items():
        masked_cookie = ck[:30] + ".." if len(ck) > 30 else ck
        if num in valid_cookies:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Valid{white}   | Cookie:{red} {masked_cookie}", reset)
        else:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Invalid{white} | Cookie:{red} {masked_cookie}", reset)

    print(f'\n{INFO} To add more Roblox Cookies, open {path_name}.', reset)

    try:
        choice = int(input(f"{INPUT} Choice {red}->{reset} ").strip())
    except ValueError:
        ErrorChoice()

    if choice not in cookies:
        ErrorChoice()

    if choice in valid_cookies:
        return valid_cookies[choice]
    else:
        ErrorCookie()

def ChoiceMultiCookie():
    data      = LoadData()
    path_name = f'{red}"{white}Programs/Extras/Config.json{red}"{white}'

    cookies_list = [c for c in data.get("cookies", []) if c.strip()]

    cookies       = {}
    valid_cookies = {}

    for i, ck in enumerate(cookies_list, 1):
        cookies[i] = ck
        if CheckCookie(ck):
            valid_cookies[i] = ck

    if not cookies:
        print(f"{INFO} No Roblox Cookie found in {path_name}!", reset)
        print(f"{ERROR} Please add Roblox Cookies to {path_name}.", reset)
        time.sleep(2)
        Reset()

    if not valid_cookies:
        print(f"{INFO} No valid Roblox Cookie found in {path_name}!", reset)
        print(f"{ERROR} Please add valid Roblox Cookies to {path_name}.", reset)
        time.sleep(2)
        Reset()

    print()
    for num, ck in cookies.items():
        masked_cookie = ck[:30] + ".." if len(ck) > 30 else ck
        if num in valid_cookies:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Valid{white}   | Cookie:{red} {masked_cookie}", reset)
        else:
            print(f"{PREFIX}{num:02d}{SUFFIX} Status:{red} Invalid{white} | Cookie:{red} {masked_cookie}", reset)

    print(f'\n{INFO} To add more Roblox Cookies, open {path_name}.')

    while True:
        try:
            num_cookies = int(input(f"{INPUT} Number {red}->{reset} ").strip())
            if num_cookies <= 0:
                ErrorNumber()
            if num_cookies > len(valid_cookies):
                print(f"{ERROR} Not enough valid Roblox Cookies!", reset)
                time.sleep(2)
                Reset()
            break
        except ValueError:
            ErrorNumber()

    selected_cookies = []

    for i in range(num_cookies):
        while True:
            try:
                choice = int(input(f"{INPUT} Cookie {i + 1} {red}->{reset} ").strip())
                if choice not in cookies:
                    ErrorChoice()
                if choice not in valid_cookies:
                    print(f"{ERROR} Invalid Roblox Cookie!", reset)
                    time.sleep(2)
                    Reset()
                if valid_cookies[choice] not in selected_cookies:
                    selected_cookies.append(valid_cookies[choice])
                    break
                else:
                    print(f"{ERROR} Roblox Cookie already selected!", reset)
                    Continue()
                    Reset()
            except ValueError:
                ErrorNumber()

    return selected_cookies

CheckLaunch()

buildware_banner = f"""
                          ▄▄▄▄    █    ██  ██▓ ██▓    ▓█████▄  █     █░ ▄▄▄       ██▀███  ▓█████  
                         ▓█████▄  ██  ▓██▒▓██▒▓██▒    ▒██▀ ██▌▓█░ █ ░█░▒████▄    ▓██ ▒ ██▒▓█   ▀  
                         ▒██▒ ▄██▓██  ▒██░▒██▒▒██░    ░██   █▌▒█░ █ ░█ ▒██  ▀█▄  ▓██ ░▄█ ▒▒███   
                         ▒██░█▀  ▓▓█  ░██░░██░▒██░    ░▓█▄   ▌░█░ █ ░█ ░██▄▄▄▄██ ▒██▀▀█▄  ▒▓█  ▄  
                         ░▓█  ▀█▓▒▒█████▓ ░██░░██████▒░▒████▓ ░░██▒██▓  ▓█   ▓██▒░██▓ ▒██▒░▒████▒ 
                         ░▒▓███▀▒░▒▓▒ ▒ ▒ ░▓  ░ ▒░▓  ░ ▒▒▓  ▒ ░ ▓░▒ ▒   ▒▒   ▓▒█░░ ▒▓ ░▒▓░░░ ▒░ ░ 
                         ▒░▒   ░ ░░▒░ ░ ░  ▒ ░░ ░ ▒  ░ ░ ▒  ▒   ▒ ░ ░    ▒   ▒▒ ░  ░▒ ░ ▒░ ░ ░  ░ 
                          ░    ░  ░░░ ░ ░  ▒ ░  ░ ░    ░ ░  ░   ░   ░    ░   ▒     ░░   ░    ░    
                          ░         ░      ░      ░  ░   ░        ░          ░  ░   ░        ░  ░"""

feedback_banner = f"""
                                                                            0000         
                                                                          0000000000     
                                                                         000000000000    
                                                                        00000     0000   
                                                                       0000000    0000   
                                                                      000000000000000    
                                                                     0000   00000000     
                                                                    0000      00000      
                                 00000000000000000000000000000000000000      00000       
                               000000000000000000000000000000000000000      00000        
                               0000                              0000      00000         
                               0000                             0000      00000          
                               0000  00000000000000000000000   0000      00000           
                               0000  00000000000000000000000 00000      000000           
                               0000                          0000      0000000           
                               0000  00000000000000000000000 0000     00000000           
                               0000   0000000000000000000000 0000  000000 0000           
                               0000    00000000000000000000  00000000000  0000           
                               0000  00000000000000000000000 00000000     0000           
                               0000   000000000000000000000  00000        0000           
                               0000   000000000000000000000000000000000   0000           
                               0000  0000000000000000000000000000000000   0000           
                               0000                                       0000           
                               0000                                       0000           
                               0000                                       0000           
                               0000                                       0000           
                               0000000000    000000000000000000000000000000000           
                                 00000000  000000000000000000000000000000000             
                                     0000000000                                          
                                     00000000                                            
                                     0000000                                             
                                     00000                                               
                                      000"""

information_banner = f"""
                                                000000000000000000000                    
                                            00000000000000000000000000000                
                                         00000000000000000000000000000000000             
                                      0000000000000               0000000000000          
                                     0000000000                       00000000000        
                                   000000000                             000000000       
                                 000000000                                 000000000     
                                00000000                                     00000000    
                               0000000                                         0000000   
                              0000000                  0000000                  0000000  
                              000000                  000000000                  0000000 
                             000000                    0000000                    000000 
                            0000000                      000                      0000000
                            000000                        0                        000000
                            000000                     0000000                     000000
                            00000                      0000000                      00000
                            00000                      0000000                      00000
                            00000                      0000000                      00000
                            000000                     0000000                     000000
                            000000                     0000000                     000000
                            0000000                    0000000                    0000000
                             000000                    0000000                    000000 
                              000000                   0000000                   0000000 
                              0000000                  0000000                  0000000  
                               0000000                  00000                  0000000   
                                00000000                                     00000000    
                                 000000000                                 000000000     
                                   000000000                             000000000       
                                    00000000000                       00000000000        
                                      0000000000000               0000000000000          
                                         00000000000000000000000000000000000             
                                            00000000000000000000000000000                
                                                000000000000000000000"""

extras_banner = f"""
                                    0000000000000000                                     
                                 0000000000000000000000                                  
                                0000000000000000000000000                                
                               000000              000000000000000000000000000000000     
                               00000                0000000000000000000000000000000000   
                               00000                 000000                     000000   
                               00000                  000000                     000000  
                               00000                   00000000000000000000000000000000  
                               00000                    0000000000000000000000000000000  
                               00000                       0000000000000000000000000000  
                               00000                                             000000  
                               00000                                             000000  
                               00000                                             000000  
                               00000                                             000000  
                               00000                                             000000  
                               00000                                             000000  
                               00000                                             000000  
                               00000                                             000000  
                               00000                                             000000  
                               00000                                             000000  
                               00000                                             000000  
                               000000                                           000000   
                               0000000000000000000000000000000000000000000000000000000   
                                 000000000000000000000000000000000000000000000000000     
                                    000000000000000000000000000000000000000000000"""

network_banner = f"""                                                             
                                                 0000000000000000000                     
                                             0000000000000000000000000000                
                                          0000000000000000 0000000000000000              
                                       0000000000000000       0000000000000000           
                                     000000000  000000         000000   00000000         
                                    0000000     00000           00000     0000000        
                                  000000000000000000             000000000000000000      
                                 000000000000000000000000000000000000000000000000000     
                                000000    000000000000000000000000000000000    000000    
                               000000         0000000000000000000000000         000000   
                               00000         00000                 00000         00000   
                              000000         00000                 00000         000000  
                              00000          00000                 00000          00000  
                              00000          00000                 00000          000000 
                              0000000000000000000000000000000000000000000000000000000000 
                              0000000000000000000000000000000000000000000000000000000000 
                              0000000000000000000000000000000000000000000000000000000000 
                              00000          00000                 00000          000000 
                              00000          00000                 00000          00000  
                              000000         00000                 00000         000000  
                               00000         00000                 00000         00000   
                               000000         0000000000000000000000000         000000   
                                000000     0000000000000000000000000000000     000000    
                                 000000000000000000000000000000000000000000000000000     
                                  000000000000000000             000000000000000000      
                                    0000000     00000           00000     0000000        
                                     000000000  000000         000000   00000000         
                                       0000000000000000       0000000000000000           
                                         00000000000000000 00000000000000000             
                                            00000000000000000000000000000                
                                                 0000000000000000000"""

osint_banner = f"""
                                           000000000000000000                            
                                       00000000000000000000000000                        
                                    00000000   0000000000   0000000                      
                                  0000000 00000000000000000000 000000                    
                                 00000  00000000        00000000  00000                  
                                0000  000000      00000000  000000  0000                 
                               0000 00000          0000000000  0000  0000                
                              0000 0000                  000000 00000 0000               
                             0000 0000                      00000 0000 0000              
                            0000 0000                        00000 000 00000             
                            000 00000                         0000 0000 0000             
                            000 0000                                000 0000             
                            000 0000                           0000 000 0000             
                            000 0000                           000  000 0000             
                            000 0000                                000 0000             
                            000000000                              0000 0000             
                             000 0000                             0000 0000              
                             0000 00000                          0000  0000              
                              0000 00000                        00000 0000               
                               0000 000000                    00000  0000                
                                00000 0000000              0000000 0000000               
                                 000000 000000000000000000000000 00000000000             
                                   000000  00000000000000000  0000000   00000            
                                     00000000              0000000000   0000000          
                                        00000000000000000000000   000000000 00000        
                                             00000000000000         00000     00000      
                                                                     000000    000000    
                                                                       00000     00000   
                                                                         00000     00000 
                                                                           00000     0000
                                                                            000000    000
                                                                              00000000000
                                                                                00000000"""

utilities_banner = f"""
                                                    0000000000000                        
                                                   000000000000000                       
                                                   00000     000000                      
                                      00000000    00000       00000    00000000          
                                    0000000000000000000       0000000000000000000        
                                   0000000 00000000000         00000000000 0000000       
                                  000000     0000                   0000     0000000     
                                 00000                                         00000     
                                 000000                                       000000     
                                  0000000             000000000             0000000      
                                   000000         00000000000000000         000000       
                                   00000        000000000000000000000        00000       
                               000000000       0000000         0000000       000000000   
                             0000000000       000000             000000       0000000000 
                            0000000000       00000                 00000       0000000000
                            0000             00000                 00000             0000
                            0000             0000                   0000             0000
                            0000             0000                   0000             0000
                            0000000000       00000                 00000       0000000000
                             0000000000       00000               00000       0000000000 
                               000000000       0000000         0000000       000000000   
                                   00000        000000000000000000000        00000       
                                   000000         00000000000000000         000000       
                                  0000000             000000000             0000000      
                                 000000                                       000000     
                                 00000                                         00000     
                                 0000000     0000                   0000     0000000     
                                   0000000 00000000000         00000000000 0000000       
                                    0000000000000000000       0000000000000000000        
                                      00000000    00000       00000    00000000          
                                                   00000     000000                      
                                                   000000000000000                       
                                                    0000000000000"""

stealer_banner = f"""                                                             
                                              000                   000                  
                                          00000000000000     00000000000000              
                                         00000000000000000000000000000000000             
                                        0000           00000000          0000            
                                       0000                               0000           
                                       0000                               0000           
                                      0000                                 0000          
                                      0000                                 0000          
                                     0000                                   0000         
                                     0000                                   0000         
                                    0000                                     000         
                                    0000                                                 
                                  0000000000000000000000000000000000000000000000000      
                                000000000000000000000000000000000000000000000000000000   
                             0000000                                             0000000 
                            0000000000000000000000000000000000000000000000000000000000000
                            0000000000000000000000000000000000000000000000000000000000000
                                                             
                                                             
                                       000000000000               000000000000           
                                     0000000000000000   00000   0000000000000000         
                                    00000         000000000000000000        00000        
                                   0000            000000   000000            0000       
                                  0000              0000     0000              0000      
                                  0000              0000     0000              0000      
                                  0000              0000     0000              0000      
                                   0000            0000       0000            0000       
                                   00000          00000       00000          00000       
                                     0000000000000000           0000000000000000         
                                       000000000000               000000000000           
                                           0000                       0000"""

attacks_banner = f"""
                                                                             0           
                                                                           0000          
                                                                           0000    000   
                                                                           0000  00000   
                                                                 00         000 00000    
                                             000000000000      000000  00000             
                                        00000000000000000000000000000000000000000 0000000
                                     00000000            00000000   00000  0000   0000000
                                   000000                    000000   00000              
                                 000000                         00000  0000              
                                00000                             000000000              
                               0000                                0000000               
                              0000                                  0000                 
                             0000                                    0000                
                            0000                                      0000               
                            000                                        000               
                            000                                        0000              
                            000                                        0000              
                            000                                   000  0000              
                            000                                   000  000               
                            0000                                      0000               
                             000                                000   0000               
                             0000                              0000  0000                
                              0000                           00000  0000                 
                               00000                       000000  0000                  
                                00000                  00000000  00000                   
                                  000000          0000000000  000000                     
                                    0000000       000000   0000000                       
                                      00000000000000000000000000                         
                                         00000000000000000000                            
                                                000000"""

roblox_banner = f"""
                                              00000                                      
                                              0000000000                                 
                                             0000000000000000                            
                                            0000      00000000000                        
                                            0000            0000000000                   
                                           0000                  0000000000              
                                          00000                      00000000000         
                                          0000                            000000000      
                                         0000        0000                     00000      
                                        00000       0000000000                0000       
                                       00000        000000000000000          00000       
                                       0000        0000      0000000         0000        
                                      00000        0000         0000        0000         
                                     00000        0000         0000        00000         
                                     0000        0000         00000       00000          
                                    00000        0000000      0000        0000           
                                   00000          0000000000000000       00000           
                                   0000                0000000000       00000            
                                  00000                     0000        0000             
                                  000000000                            0000              
                                     0000000000                        0000              
                                          0000000000                  0000               
                                               0000000000             000                
                                                   000000000000      0000                
                                                        0000000000000000                 
                                                             0000000000                  
                                                                  00000"""

discord_banner = f"""
                                              000000             000000                  
                                         00000000000000000000000000000000000             
                                      000000000000000000000000000000000 0000000          
                                   000000 00000000                 00000000 000000       
                                   000 000000                           000000 0000      
                                  0000 000                                 000 0000      
                                 0000                                           0000     
                                0000                                             0000    
                                000                                               000    
                               0000                                               0000   
                               000              000               000              000   
                              0000           000000000         000000000           0000  
                              000           0000   0000       0000   0000           000  
                             0000           000     0000     0000     000           0000 
                             000            000     0000     0000     000            000 
                             000            0000   0000       0000   0000            000 
                            000              000000000         000000000              000
                            000                                                       000
                            000     00000                                   00000     000
                            000       000000                             000000       000
                             0000        0000000                     0000000        0000 
                               00000         000000000000000000000000000         000000  
                                 0000000      0000 000000000000000 0000      0000000     
                                    0000000000000                   0000000000000        
                                         0000000                     0000000"""