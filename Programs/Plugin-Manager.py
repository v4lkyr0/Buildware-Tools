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
    import io
    import sys
    import json
    import time
    import os
    import webbrowser
    import shutil
    import zipfile
    import subprocess
    import requests
except Exception as e:
    MissingModule(e)

Title("Plugin Manager")

plugins_dir     = os.path.join(tool_path, "Programs", "Plugins")
required_files  = ["plugin.json", "main.py"]
required_fields = ["name", "author", "category", "version"]

def GetPlugins():
    plugins = []
    if not os.path.exists(plugins_dir):
        return plugins
    for folder in sorted(os.listdir(plugins_dir)):
        folder_path = os.path.join(plugins_dir, folder)
        if not os.path.isdir(folder_path):
            continue
        if folder == "__pycache__":
            continue
        json_path = os.path.join(folder_path, "plugin.json")
        if not os.path.exists(json_path):
            continue
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            plugins.append((folder, data))
        except Exception:
            continue
    return plugins

def ParseGithubUrl(url):
    try:
        url   = url.strip().rstrip("/")
        parts = url.replace("https://github.com/", "").split("/")
        if len(parts) >= 2:
            return parts[0], parts[1]
    except Exception:
        pass
    return None, None

def CheckBuildwareTag(owner, repo):
    try:
        headers  = {"Accept": "application/vnd.github.mercy-preview+json"}
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/topics",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            topics = response.json().get("names", [])
            return "buildware-plugin" in topics
    except Exception:
        pass
    return False

def GetRemoteVersion(owner, repo):
    try:
        for branch in ["main", "master"]:
            r = requests.get(
                f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/plugin.json",
                timeout=10
            )
            if r.status_code == 200:
                data = r.json()
                return data.get("version", None)
    except Exception:
        pass
    return None

def CheckCompatibility(plugin_data):
    required = plugin_data.get("buildware", None)
    if not required:
        return True
    try:
        current  = tuple(int(x) for x in version_tool.split("."))
        required = tuple(int(x) for x in str(required).split("."))
        return current >= required
    except Exception:
        return True

def ValidatePlugin(folder_path):
    for f in required_files:
        if not os.path.exists(os.path.join(folder_path, f)):
            print(f"{ERROR} Missing required file:{red} {f}", reset)
            return None

    json_path = os.path.join(folder_path, "plugin.json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        print(f"{ERROR} plugin.json is invalid or corrupted!", reset)
        return None

    for field in required_fields:
        if not data.get(field):
            print(f"{ERROR} Missing required field in plugin.json:{red} {field}", reset)
            return None

    return data

def InstallRequirements(plugin_data):
    requires = plugin_data.get("requires", [])
    if not requires:
        return True
    print(f"{LOADING} Installing dependencies..", reset)
    for package in requires:
        try:
            r = subprocess.run(
                [sys.executable, "-m", "pip", "install", package, "-q"],
                timeout=30
            )
            if r.returncode == 0:
                print(f"{SUCCESS} {package} installed!", reset)
            else:
                print(f"{ERROR} Failed to install {package}!", reset)
                return False
        except Exception as e:
            print(f"{ERROR} Error:{red} {e}", reset)
            return False
    return True

def DownloadZip(owner, repo):
    for branch in ["main", "master"]:
        try:
            r = requests.get(
                f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip",
                timeout=15
            )
            if r.status_code == 200:
                return r
        except Exception:
            pass
    return None

def ExtractPlugin(response, dest):
    tmp_path = os.path.join(plugins_dir, "_tmp")
    try:
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall(tmp_path)

        extracted = None
        for item in os.listdir(tmp_path):
            if os.path.isdir(os.path.join(tmp_path, item)):
                extracted = item
                break

        if not extracted:
            print(f"{ERROR} Could not find extracted content!", reset)
            shutil.rmtree(tmp_path, ignore_errors=True)
            return None

        plugin_root = os.path.join(tmp_path, extracted)
        plugin_data = ValidatePlugin(plugin_root)

        if not plugin_data:
            shutil.rmtree(tmp_path, ignore_errors=True)
            return None

        if os.path.exists(dest):
            shutil.rmtree(dest, ignore_errors=True)

        shutil.copytree(plugin_root, dest)
        shutil.rmtree(tmp_path, ignore_errors=True)
        return plugin_data

    except Exception as e:
        shutil.rmtree(tmp_path, ignore_errors=True)
        print(f"{ERROR} Extraction failed:{red} {e}", reset)
        return None

def InstallPlugin(url):
    owner, repo = ParseGithubUrl(url)

    if not owner or not repo:
        print(f"{ERROR} Invalid GitHub Url!", reset)
        time.sleep(2)
        Reset()

    print(f"{LOADING} Checking repository tag..", reset)

    if not CheckBuildwareTag(owner, repo):
        print(f"{ERROR} This repository does not have the buildware-plugin tag!", reset)
        time.sleep(2)
        Reset()

    print(f"{SUCCESS} Tag verified!", reset)
    print(f"{LOADING} Downloading plugin..", reset)

    response = DownloadZip(owner, repo)
    if not response:
        print(f"{ERROR} Could not download the repository!", reset)
        time.sleep(2)
        Reset()

    print(f"{LOADING} Validating plugin..", reset)

    tmp_dest    = os.path.join(plugins_dir, "_installing")
    plugin_data = ExtractPlugin(response, tmp_dest)

    if not plugin_data:
        shutil.rmtree(tmp_dest, ignore_errors=True)
        time.sleep(2)
        Reset()

    if not CheckCompatibility(plugin_data):
        required = plugin_data.get("buildware", "?")
        print(f"{ERROR} This plugin requires Buildware-Tools v{required} or higher!", reset)
        print(f"{INFO} Your current version is v{version_tool}.", reset)
        shutil.rmtree(tmp_dest, ignore_errors=True)
        time.sleep(2)
        Reset()

    plugin_name = plugin_data["name"].replace(" ", "-")
    final_dest  = os.path.join(plugins_dir, plugin_name)

    if os.path.exists(final_dest):
        print(f"{ERROR} Plugin {plugin_name} is already installed!", reset)
        shutil.rmtree(tmp_dest, ignore_errors=True)
        time.sleep(2)
        Reset()

    os.rename(tmp_dest, final_dest)

    if not InstallRequirements(plugin_data):
        print(f"{ERROR} Failed to install dependencies!", reset)
        time.sleep(2)
        Reset()

    print(f"{SUCCESS} Plugin{red} {plugin_data['name']}{white} v{plugin_data['version']} by{red} {plugin_data['author']}{white} installed!", reset)

    Continue()
    Reset()

def UpdatePlugin(folder, data):
    github = data.get("github", "")

    if not github:
        print(f"{ERROR} No github field found in plugin.json!", reset)
        time.sleep(2)
        Reset()

    owner, repo = ParseGithubUrl(github)

    if not owner or not repo:
        print(f"{ERROR} Invalid GitHub Url in plugin.json!", reset)
        time.sleep(2)
        Reset()

    print(f"{LOADING} Downloading update..", reset)

    response = DownloadZip(owner, repo)
    if not response:
        print(f"{ERROR} Could not download update!", reset)
        time.sleep(2)
        Reset()

    print(f"{LOADING} Validating update..", reset)

    dest        = os.path.join(plugins_dir, folder)
    plugin_data = ExtractPlugin(response, dest)

    if not plugin_data:
        Continue()
        Reset()

    if not CheckCompatibility(plugin_data):
        required = plugin_data.get("buildware", "?")
        print(f"{ERROR} This update requires Buildware-Tools v{required} or higher!", reset)
        print(f"{INFO} Your current version is v{version_tool}.", reset)
        time.sleep(2)
        Reset()

    if not InstallRequirements(plugin_data):
        print(f"{ERROR} Failed to install dependencies!", reset)
        time.sleep(2)
        Reset()

    print(f"{SUCCESS} Plugin {plugin_data['name']} updated to v{plugin_data['version']}!", reset)

    Continue()
    Reset()

try:
    Scroll(f"""
 {PREFIX}01{SUFFIX} Install Plugin
 {PREFIX}02{SUFFIX} Manage Plugins
""")

    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    if choice == "1":
        print(f"{INFO} Paste the GitHub repository link of the plugin.", reset)
        print(f"{INFO} The repository must have the buildware-plugin tag.\n", reset)

        open_link = input(f"{INPUT} Open the plugin list on GitHub? {YESORNO} {red}->{reset} ").strip().lower()
        if open_link in ["y", "yes"]:
            webbrowser.open("https://github.com/topics/buildware-plugin")

        print()
        url = input(f"{INPUT} GitHub Url {red}->{reset} ").strip()

        if not url.startswith("https://github.com/"):
            print(f"{ERROR} Invalid GitHub Url!", reset)
            time.sleep(2)
            Reset()

        InstallPlugin(url)

    elif choice == "2":
        plugins = GetPlugins()

        if not plugins:
            print(f"{INFO} No plugins installed!", reset)
            time.sleep(2)
            Reset()

        print()
        for i, (folder, data) in enumerate(plugins, 1):
            cfg        = LoadData()
            visible    = cfg.get("plugins_visible", [])
            is_visible = folder in visible
            status     = "Shown" if is_visible else "Hidden"

            github = data.get("github", "")
            update = ""
            if github:
                owner, repo = ParseGithubUrl(github)
                if owner and repo:
                    remote = GetRemoteVersion(owner, repo)
                    if remote and remote != data.get("version", ""):
                        update = f" [Update: v{remote}]"

            print(f" {PREFIX}{str(i).zfill(2)}{SUFFIX} Name:{red} {data['name']} v{data['version']}{white} | Category:{red} {data['category']}{white} | By:{red} {data['author']}{white} | Status:{red} {status}{white}{update}", reset)

        choice_2 = input(f"\n{INPUT} Choice {red}->{reset} ").strip()

        try:
            idx = int(choice_2) - 1
            if idx < 0 or idx >= len(plugins):
                ErrorChoice()
        except Exception:
            ErrorChoice()

        folder, data = plugins[idx]

        cfg        = LoadData()
        visible    = cfg.get("plugins_visible", [])
        is_visible = folder in visible
        status     = "Shown" if is_visible else "Hidden"

        Scroll(f"""
 {PREFIX}01{SUFFIX} Show / Hide {red}({white}{status}{red}){white}
 {PREFIX}02{SUFFIX} Run
 {PREFIX}03{SUFFIX} Update
 {PREFIX}04{SUFFIX} Uninstall
""")

        action = input(f"{INPUT} Action {red}->{reset} ").strip().lstrip("0")

        if action == "1":
            cfg     = LoadData()
            visible = cfg.get("plugins_visible", [])
            if folder in visible:
                visible.remove(folder)
                print(f"{SUCCESS} Plugin {data['name']}{white} is now Hidden from the menu!", reset)
            else:
                visible.append(folder)
                print(f"{SUCCESS} Plugin {data['name']}{white} is now Shown in the menu!", reset)
            cfg["plugins_visible"] = visible
            SaveData(cfg)

        elif action == "2":
            StartProgram(os.path.join("Plugins", folder, "main.py"))

        elif action == "3":
            UpdatePlugin(folder, data)

        elif action == "4":
            confirm = input(f"{INPUT} Uninstall {data['name']}{white}? {YESORNO} {red}->{reset} ").strip().lower()
            if confirm in ["y", "yes"]:
                cfg     = LoadData()
                visible = cfg.get("plugins_visible", [])
                if folder in visible:
                    visible.remove(folder)
                cfg["plugins_visible"] = visible
                SaveData(cfg)
                shutil.rmtree(os.path.join(plugins_dir, folder), ignore_errors=True)
                print(f"{SUCCESS} Plugin {data['name']}{white} uninstalled!", reset)
            else:
                print(f"{INFO} Cancelled.", reset)

        else:
            ErrorChoice()

    else:
        ErrorChoice()

    Continue()
    Reset()

except Exception as e:
    Error(e)