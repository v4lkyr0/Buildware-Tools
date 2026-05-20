# Plugin Development Guide:
#
# This file is the entry point of your plugin.
# Replace this comment with your actual code.
# -------------------------------------------------------
# Repository setup:
#
# Your repository must have the GitHub topic "buildware-plugin"
# set, otherwise Buildware-Tools will refuse to install it.
# You can add it in: Repository > Settings > Topics.
# -------------------------------------------------------
# Required files:
#
# Your repository must contain these two files:
# - plugin.json  : plugin metadata
# - main.py      : your plugin code (this file)
# -------------------------------------------------------
# plugin.json fields:
#
# Every field is required unless marked as optional.
#
# - name      : display name shown in the Buildware menu
# - author    : your GitHub username
# - category  : OSINT / Network / Utilities / Roblox / Discord
# - version   : plugin version, e.g. "1.0"
# - github    : full repository URL, used by the update system
# - buildware : minimum Buildware-Tools version required (optional)
#               e.g. "2.8" — leave out if no requirement
# - requires  : list of pip packages to auto-install (optional)
#               e.g. ["requests", "bs4"]
# -------------------------------------------------------
# Coding your plugin:
#
# Import the following at the top of your main.py:
#
#   from Core.Utils import *
#   from Core.Config import *
#
# All available functions and variables are inside Core/Utils.py.
# Read it before you start — everything you need is in there.
# -------------------------------------------------------
# Sharing your plugin:
#
# Push your repository to GitHub and share the link.
# Users can install it directly from Buildware-Tools via:
# Plugin Manager > Install Plugin > paste your GitHub URL.

import sys, os, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from Core.Utils import *
from Core.Config import *

Title("Example Plugin")
Scroll(GradientBanner(utilities_banner))

try:
    Scroll(f"""
 {INFO} This is the Example Plugin of Buildware-Tools.
 {INFO} Want to create your own? Read main.py.
    """)

    main_dir = os.path.join(tool_path, "Programs", "Plugins", "Example Plugin")
    if platform_pc == "Windows":
        os.startfile(main_dir)
    elif platform_pc == "Linux":
        subprocess.Popen(["xdg-open", main_dir])

    Continue()
    Reset()
except Exception as e:
    Error(e)