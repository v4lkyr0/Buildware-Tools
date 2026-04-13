# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import os
    import subprocess
except Exception as e:
    MissingModule(e)

Title("Extras Files")

try:
    extras_path = os.path.join(tool_path, "Programs", "Extras")
    
    Scroll(f"""
 {PREFIX}01{SUFFIX} Data File
 {PREFIX}02{SUFFIX} Extras Folder
""")
    
    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")
    
    if choice == "1":
        file_path = os.path.join(extras_path, "Config.json")
        file_name = "Config.json"
        print(f"{INFO} Contains webhooks, tokens, bots, and settings", reset)
    elif choice == "2":
        file_path = extras_path
        file_name = "Extras"
    else:
        ErrorChoice()
    
    print(f"{LOADING} Opening File..", reset)

    try:
        if platform_pc == "Windows":
            os.startfile(file_path)
        else:
            subprocess.Popen(['xdg-open', file_path])
        print(f"{SUCCESS} {file_name} opened!", reset)
    except:
        print(f"{ERROR} Error while trying to open {file_name}!", reset)
        print(f"{INFO} Path:{red} {file_path}", reset)

    print()
    
    Continue()
    Reset()

except Exception as e:
    Error(e)