# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import socket
except Exception as e:
    MissingModule(e)

Title("Network Reverse Dns")
Connection()

try:
    ip = input(f"{INPUT} Ip Address {red}->{reset} ").strip()
    if not ip:
        ErrorInput()

    print(f"{LOADING} Performing Reverse Dns Lookup..", reset)

    try:
        hostname, aliases, addresses = socket.gethostbyaddr(ip)

        Scroll(f"""
 {INFO} Ip Address               :{red} {ip}
 {INFO} Hostname                 :{red} {hostname}
 {INFO} Aliases                  :{red} {', '.join(aliases) if aliases else 'None'}
 {INFO} Addresses                :{red} {', '.join(addresses) if addresses else 'None'}
""")

    except socket.herror:
        print(f" {ERROR} No Reverse Dns Record found!", reset)
    except socket.gaierror:
        print(f" {ERROR} Invalid Ip Address format!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)
