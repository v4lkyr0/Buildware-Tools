# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

Title("Tool Information")

try:
    Scroll(f"""
 {INFO} Tool Name :{red} {name_tool}
 {INFO} Version   :{red} {version_tool}
 {INFO} Type      :{red} {type_tool}
 {INFO} Author    :{red} {author_tool}
 {INFO} GitHub    :{red} {github_url}
 {INFO} Guns.lol  :{red} {gunslol_url}
 {INFO} License   :{red} {license} ({license_url})
""")
    Continue()
    Reset()

except Exception as e:
    Error(e)