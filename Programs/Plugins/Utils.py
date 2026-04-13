# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from .Config import *

try:
    from colorama import Fore
    import ctypes
    import json
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
    print('Required Python modules for Buildware-Tools are not installed. Please run "Setup.py" to install them.')
    input(f"Error: {e}")

username_webhook = "Buildware-Tools"
avatar_webhook = "https://i.imgur.com/7Gu71Gc.png"
color_embed = 0x880000

red = Fore.RED
white = Fore.WHITE
green = Fore.GREEN
reset = Fore.RESET
blue = Fore.BLUE
yellow = Fore.YELLOW

PREFIX = f"{red}[{white}"
SUFFIX = f"{red}]{white}"
PREFIX1 = f"{red}{{{white}"
SUFFIX1 = f"{red}}}{white}"
SUFFIXP = f"{red}}}{yellow}"

YESORNO = f"{red}({white}y/n{red}){white}"
INPUT = f"{PREFIX}>{SUFFIX}"
INFO = f"{PREFIX}?{SUFFIX}"
ERROR = f"{PREFIX}x{SUFFIX}"
SUCCESS = f"{PREFIX}+{SUFFIX}"
LOADING = f"{PREFIX}~{SUFFIX}"

tool_path = os.path.dirname(os.path.abspath(__file__)).split("Programs\\")[0].split("Programs/")[0].strip()

try:
    username_pc = os.getlogin()
except:
    username_pc = "user"

try:
    if sys.platform.startswith("win"):
        platform_pc = "Windows"
    elif sys.platform.startswith("linux"):
        platform_pc = "Linux"
    else:
        platform_pc = "Unknown"
except:
    platform_pc = "None"

def Connection():
    try:
        requests.get("https://www.google.com", timeout=5)
    except:
        print(f"{ERROR} An internet connection is required to use this feature!", reset)
        Continue()

data_file = os.path.join(tool_path, "Programs", "Extras", "Config.json")
github_repo_owner = "v4lkyr0"
github_repo_name = "Buildware-Tools"

def load_data():
    if os.path.exists(data_file):
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"webhooks": [], "tokens": [], "bots": [], "cookies": [], "github_star": "", "page": 1}

def save_data(data):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def decode_pat(data):
    import base64
    return base64.b64decode(data.encode()).decode()

def encode_pat(pat):
    import base64
    return base64.b64encode(pat.encode()).decode()

def CheckGithubStar():
    if os.environ.get("BUILDWARE_STAR_VERIFIED") == "1":
        return True

    data = load_data()
    cached_pat = data.get("github_star", "")

    if cached_pat:
        try:
            pat = decode_pat(cached_pat)
            headers = {"Authorization": f"token {pat}", "Accept": "application/vnd.github.v3+json"}
            print(f"\n{LOADING} Verifying..", reset)
            r = requests.get("https://api.github.com/user", headers=headers, timeout=10)
            if r.status_code == 200:
                username = r.json().get("login", "")
                if _is_stargazer(username.lower(), headers):
                    print(f"{SUCCESS} Verified as:{red} {username}{reset}", reset)
                    os.environ["BUILDWARE_STAR_VERIFIED"] = "1"
                    time.sleep(1)
                    return True
                else:
                    print(f"{ERROR} {red}{username}{reset} has removed the star from the repository!", reset)
                    print(f"{INFO} Please star {red}{github_url}{reset} and try again.", reset)
            else:
                print(f"{ERROR} Verification failed!", reset)
            data["github_star"] = ""
            save_data(data)
        except:
            print(f"{ERROR} Verification failed!", reset)
            data["github_star"] = ""
            save_data(data)

    print(f"\n{INFO} This feature requires you to star the GitHub repository.", reset)
    print(f"{INFO} {red}{github_url}{reset}", reset)
    print(f"\n{INFO} You need a GitHub Personal Access Token to verify your identity.", reset)
    print(f"{INFO} Create one at:{red} https://github.com/settings/tokens{reset}", reset)
    print(f"{INFO} No scopes/permissions needed, just generate and paste it.\n", reset)

    pat = input(f"{INPUT} GitHub Token {red}->{reset} ").strip()
    if not pat:
        print(f"{ERROR} No token provided!", reset)
        time.sleep(2)
        sys.exit()

    print(f"{LOADING} Authenticating..", reset)
    try:
        headers = {"Authorization": f"token {pat}", "Accept": "application/vnd.github.v3+json"}
        r = requests.get("https://api.github.com/user", headers=headers, timeout=10)
        if r.status_code != 200:
            print(f"{ERROR} Invalid GitHub token!", reset)
            time.sleep(2)
            sys.exit()

        username = r.json().get("login", "Unknown")
        print(f"{SUCCESS} Authenticated as:{red} {username}{reset}", reset)

        print(f"{LOADING} Checking star..", reset)
        if _is_stargazer(username.lower(), headers):
            data = load_data()
            data["github_star"] = encode_pat(pat)
            save_data(data)
            print(f"{SUCCESS} Star verified!", reset)
            os.environ["BUILDWARE_STAR_VERIFIED"] = "1"
            time.sleep(1)
            return True
        else:
            print(f"{ERROR} {red}{username}{reset} has not starred the repository!", reset)
            print(f"{INFO} Please star {red}{github_url}{reset} and try again.", reset)
            time.sleep(3)
            sys.exit()
    except:
        print(f"{ERROR} Could not verify. Check your connection.", reset)
        time.sleep(2)
        sys.exit()

def _is_stargazer(username, headers):
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

def Update():
    url = f"https://api.github.com/repos/v4lkyr0/Buildware-Tools/releases/latest"
    try:
        response = requests.get(url)
        response.raise_for_status()
        github_version = response.json()['tag_name']
    except:
        return ""
    
    if version_tool != github_version:
        print(f"{INFO} New version available! {version_tool} {red}->{white} {github_version} {red}|{white} Link:{red} {github_url}/releases/latest", reset)
    
    return ""

def Clear():
    if platform_pc == "Windows":
        os.system("cls")
    elif platform_pc == "Linux":
        os.system("clear")

def Title(title):
    if platform_pc == "Windows":
        ctypes.windll.kernel32.SetConsoleTitleW(f"{name_tool} {version_tool} - [{title}]")
    elif platform_pc == "Linux":
        sys.stdout.write(f"\x1b]2;{name_tool} {version_tool} - [{title}]\x07")

def Reset():
    if platform_pc == "Windows":
        file = ['python', os.path.join(tool_path, 'Buildware.py')]
        subprocess.run(file)
    elif platform_pc == "Linux":
        file = ['python3', os.path.join(tool_path, 'Buildware.py')]
        subprocess.run(file)

def StartProgram(program):
    if platform_pc == "Windows":
        file = ['python', os.path.join(tool_path, 'Programs', program)]
        subprocess.run(file)
    elif platform_pc == "Linux":
        file = ['python3', os.path.join(tool_path, 'Programs', program)]
        subprocess.run(file)

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

def Gradient(text):
    start_color = (223, 5, 5)
    end_color   = (121, 3, 3)
    num_steps   = 18
    colors      = []
    
    for i in range(num_steps):
        R = start_color[0] + (end_color[0] - start_color[0]) * i // (num_steps - 1)
        G = start_color[1] + (end_color[1] - start_color[1]) * i // (num_steps - 1)
        B = start_color[2] + (end_color[2] - start_color[2]) * i // (num_steps - 1)
        colors.append((R, G, B))

    colors += list(reversed(colors[:-1]))
    chars = '╖╜╙╓┴┼┘┤└┐▌▀()╚╗═╔╝─┬├┌└│]░▒░▒█▓▄'

    def ColorText(R, G, B, Char):
        return f"\033[38;2;{R};{G};{B}m{Char}"

    lines = text.split('\n')
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

def RandomUserAgents():
    file = os.path.join(tool_path, 'Programs', 'Extras', 'UserAgents.txt')

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if lines:
        user_agent = random.choice(lines).strip()
    else:
        user_agent = "Mozilla/5.0 (Linux; Android 4.4.4; Nexus 7 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36"
    
    return user_agent

def CheckWebhook(webhook):
    try:
        response = requests.get(webhook, timeout=5)
        if response.status_code in [200, 204]:
            return True
        else:
            return False
    except:
        return None
    
def CheckToken(token):
    api = "https://discord.com/api/v9/users/@me"
    headers = {"Authorization": token, "User-Agent": RandomUserAgents()}
    try:
        response = requests.get(api, headers=headers, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return None
    
def SaveWebhook(webhook):
    result = CheckWebhook(webhook)
    if result is True:
        data = load_data()
        if webhook not in data.get("webhooks", []):
            data.setdefault("webhooks", []).append(webhook)
            save_data(data)
        return True
    return False

def SaveToken(token):
    result = CheckToken(token)
    if result is True:
        data = load_data()
        if token not in data.get("tokens", []):
            data.setdefault("tokens", []).append(token)
            save_data(data)
        return True
    return False

def CheckBot(bot_token):
    api = "https://discord.com/api/v9/users/@me"
    headers = {"Authorization": f"Bot {bot_token}", "User-Agent": RandomUserAgents()}
    try:
        response = requests.get(api, headers=headers, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return None

def SaveBot(bot_token):
    result = CheckBot(bot_token)
    if result is True:
        data = load_data()
        if bot_token not in data.get("bots", []):
            data.setdefault("bots", []).append(bot_token)
            save_data(data)
        return True
    return False

def CheckCookie(cookie):
    try:
        session = requests.Session()
        session.cookies[".ROBLOSECURITY"] = cookie
        response = session.get("https://users.roblox.com/v1/users/authenticated", timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return None

def SaveCookie(cookie):
    result = CheckCookie(cookie)
    if result is True:
        data = load_data()
        if cookie not in data.get("cookies", []):
            data.setdefault("cookies", []).append(cookie)
            save_data(data)
        return True
    return False

def ChoiceWebhook():
    data = load_data()
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
                save_data(data)
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
                save_data(data)
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
    data = load_data()
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
                save_data(data)
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
                save_data(data)
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
    data = load_data()
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
    data = load_data()
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
    data = load_data()
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
                save_data(data)
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
                save_data(data)
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
    data = load_data()
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
    data = load_data()
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
                save_data(data)
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
                save_data(data)
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
    data = load_data()
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