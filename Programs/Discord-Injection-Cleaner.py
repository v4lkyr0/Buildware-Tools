# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import os
    import shutil
    import psutil
    import ctypes
except Exception as e:
    MissingModule(e)

Title("Discord Injection Cleaner")
Connection()

if platform_pc != "Windows":
    print(f"{ERROR} This feature is only available on Windows!", reset)
    Continue()
    Reset()

PATHS = {
    'Discord': os.path.join(os.getenv('LOCALAPPDATA', ''), 'Discord'),
    'Discord PTB': os.path.join(os.getenv('LOCALAPPDATA', ''), 'DiscordPTB'),
    'Discord Canary': os.path.join(os.getenv('LOCALAPPDATA', ''), 'DiscordCanary'),
    'Discord Development': os.path.join(os.getenv('LOCALAPPDATA', ''), 'DiscordDevelopment'),
    'Lightcord': os.path.join(os.getenv('APPDATA', ''), 'Lightcord'),
    'Discord (Scoop)': os.path.join(os.getenv('USERPROFILE', ''), 'scoop', 'apps', 'discord', 'current'),
    'BetterDiscord': os.path.join(os.getenv('APPDATA', ''), 'BetterDiscord')
}

DISCORD_PROCESSES = ['Discord.exe', 'DiscordPTB.exe', 'DiscordCanary.exe', 'DiscordDevelopment.exe', 'Lightcord.exe']

def find_modules(base_path):
    modules = []
    try:
        for entry in sorted(os.listdir(base_path), reverse=True):
            if not entry.startswith('app'):
                continue
            app_path = os.path.join(base_path, entry)
            if not os.path.isdir(app_path):
                continue
            modules_dir = os.path.join(app_path, 'modules')
            if not os.path.exists(modules_dir):
                continue
            for mod in os.listdir(modules_dir):
                if mod.startswith('discord_desktop_core'):
                    core = os.path.join(modules_dir, mod, 'discord_desktop_core')
                    if os.path.exists(core):
                        modules.append(core)
    except Exception:
        pass
    return modules

def clean_module(module_path):
    index_file = os.path.join(module_path, 'index.js')
    backup_file = os.path.join(module_path, 'index.js.bak')
    if not os.path.exists(index_file):
        return 'missing'
    try:
        with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        if '_0xW' not in content:
            return 'clean'
        if os.path.exists(backup_file):
            shutil.copy2(backup_file, index_file)
            os.remove(backup_file)
            return 'restored'
        idx = content.find('module.exports')
        if idx != -1:
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content[idx:])
            return 'stripped'
        return 'invalid'
    except PermissionError:
        return 'permission'
    except Exception:
        return 'error'

def kill_discord():
    killed = []
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] in DISCORD_PROCESSES:
                proc.kill()
                killed.append(proc.info['name'].replace('.exe', ''))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return list(set(killed))

def restart_discord():
    started = []
    paths = {
        'Discord': os.path.join(os.getenv('LOCALAPPDATA', ''), 'Discord'),
        'DiscordPTB': os.path.join(os.getenv('LOCALAPPDATA', ''), 'DiscordPTB'),
        'DiscordCanary': os.path.join(os.getenv('LOCALAPPDATA', ''), 'DiscordCanary'),
        'DiscordDevelopment': os.path.join(os.getenv('LOCALAPPDATA', ''), 'DiscordDevelopment'),
    }
    for name, path in paths.items():
        exe = os.path.join(path, 'Update.exe')
        if os.path.exists(exe):
            try:
                ctypes.windll.shell32.ShellExecuteW(None, 'open', exe, f'--processStart {name}.exe', None, 0)
                started.append(name)
            except Exception:
                continue
    return started

def remove_persistence():
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE)
        try:
            winreg.QueryValueEx(key, 'DiscordUpdate')
            winreg.DeleteValue(key, 'DiscordUpdate')
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            winreg.CloseKey(key)
            return False
    except Exception:
        return False

try:
    print(f"{LOADING} Scanning for Discord injections..", reset)

    infected = []
    for name, path in PATHS.items():
        if not os.path.exists(path):
            continue
        modules = find_modules(path)
        for module in modules:
            index_file = os.path.join(module, 'index.js')
            if not os.path.exists(index_file):
                continue
            with open(index_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if '_0xW' in content:
                infected.append((name, module))

    if not infected:
        print(f"\n{SUCCESS} No injection found! Your Discord is clean.", reset)
        Continue()
        Reset()

    print(f"\n{INFO} Found injection in {red}{len(infected)}{reset} client(s):\n", reset)
    for name, path in infected:
        print(f"  {red}>{reset} {name}:{red} {path}{reset}")

    confirm = input(f"\n{INPUT} Remove all injections? {YESORNO} {red}->{reset} ").strip().lower()
    if confirm not in ["y", "yes"]:
        print(f"{INFO} Cancelled.", reset)
        Continue()
        Reset()

    print(f"\n{LOADING} Killing Discord processes..", reset)
    killed = kill_discord()
    if killed:
        print(f"{SUCCESS} Killed:{red} {', '.join(killed)}{reset}")
        import time
        time.sleep(2)

    cleaned = 0
    for name, module in infected:
        result = clean_module(module)
        if result == 'restored':
            print(f"{SUCCESS} {name}: Restored from backup", reset)
            cleaned += 1
        elif result == 'stripped':
            print(f"{SUCCESS} {name}: Injection stripped", reset)
            cleaned += 1
        elif result == 'permission':
            print(f"{ERROR} {name}: Permission denied", reset)
        elif result == 'error':
            print(f"{ERROR} {name}: Failed to clean", reset)

    print(f"\n{LOADING} Checking persistence (registry)..", reset)
    if remove_persistence():
        print(f"{SUCCESS} Registry startup entry removed!", reset)
    else:
        print(f"{INFO} No registry startup entry found.", reset)

    persist_file = os.path.join(os.getenv('APPDATA', ''), 'Microsoft', 'DiscordUpdate.exe')
    persist_pyw = os.path.join(os.getenv('APPDATA', ''), 'Microsoft', 'DiscordUpdate.pyw')
    persist_py = os.path.join(os.getenv('APPDATA', ''), 'Microsoft', 'DiscordUpdate.py')
    for pf in [persist_file, persist_pyw, persist_py]:
        if os.path.exists(pf):
            try:
                os.remove(pf)
                print(f"{SUCCESS} Removed persistence file:{red} {pf}{reset}")
            except Exception:
                print(f"{ERROR} Could not remove:{red} {pf}{reset}")

    if killed:
        print(f"\n{LOADING} Restarting Discord..", reset)
        started = restart_discord()
        if started:
            print(f"{SUCCESS} Restarted:{red} {', '.join(started)}{reset}")

    print(f"\n{SUCCESS} Cleaned {red}{cleaned}/{len(infected)}{reset} client(s). Your Discord is now clean!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)
