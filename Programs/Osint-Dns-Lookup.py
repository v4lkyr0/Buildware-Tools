# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import socket
    import requests
except Exception as e:
    MissingModule(e)

Title("Osint Dns Lookup")
Connection()

try:
    domain = input(f"{INPUT} Domain {red}->{reset} ").strip().lower()
    if not domain:
        ErrorInput()

    domain = domain.replace("http://", "").replace("https://", "").split("/")[0]

    print(f"{LOADING} Resolving Dns Records..", reset)

    output = ""

    output += f" {INFO} A Records:\n"
    try:
        results = socket.getaddrinfo(domain, None, socket.AF_INET)
        ips = list(set(r[4][0] for r in results))
        for ip in ips:
            output += f" {SUCCESS} {red}{ip}{reset}\n"
    except:
        output += f" {ERROR} No A records found!{reset}\n"

    output += f"\n {INFO} AAAA Records:\n"
    try:
        results = socket.getaddrinfo(domain, None, socket.AF_INET6)
        ips = list(set(r[4][0] for r in results))
        for ip in ips:
            output += f" {SUCCESS} {red}{ip}{reset}\n"
    except:
        output += f" {ERROR} No AAAA records found!{reset}\n"

    output += f"\n {INFO} Host Information:\n"
    try:
        hostname, aliases, addresses = socket.gethostbyname_ex(domain)
        output += f" {SUCCESS} Hostname    :{red} {hostname}{reset}\n"
        if aliases:
            for alias in aliases:
                output += f" {SUCCESS} Alias       :{red} {alias}{reset}\n"
        for addr in addresses:
            output += f" {SUCCESS} Address     :{red} {addr}{reset}\n"
    except:
        output += f" {ERROR} Could not resolve host!{reset}\n"

    output += f"\n {INFO} Reverse Dns:\n"
    try:
        primary_ip = socket.gethostbyname(domain)
        reverse = socket.gethostbyaddr(primary_ip)
        output += f" {SUCCESS} {red}{primary_ip} -> {reverse[0]}{reset}\n"
    except:
        output += f" {ERROR} No reverse Dns found!{reset}\n"

    output += f"\n {INFO} MX Records:\n"
    try:
        r = requests.get(f"https://cloudflare-dns.com/dns-query?name={domain}&type=MX",
                         headers={"Accept": "application/dns-json", "User-Agent": RandomUserAgents()}, timeout=10)
        data = r.json()
        answers = data.get("Answer", [])
        mx_found = [a for a in answers if a.get("type") == 15]
        if mx_found:
            for mx in mx_found:
                output += f" {SUCCESS} {red}{mx.get('data', 'N/A')}{reset}\n"
        else:
            output += f" {ERROR} No MX records found!{reset}\n"
    except:
        output += f" {ERROR} Could not query MX records!{reset}\n"

    output += f"\n {INFO} TXT Records:\n"
    try:
        r = requests.get(f"https://cloudflare-dns.com/dns-query?name={domain}&type=TXT",
                         headers={"Accept": "application/dns-json", "User-Agent": RandomUserAgents()}, timeout=10)
        data = r.json()
        answers = data.get("Answer", [])
        txt_found = [a for a in answers if a.get("type") == 16]
        if txt_found:
            for txt in txt_found:
                output += f" {SUCCESS} {red}{txt.get('data', 'N/A')}{reset}\n"
        else:
            output += f" {ERROR} No TXT records found!{reset}\n"
    except:
        output += f" {ERROR} Could not query TXT records!{reset}\n"

    output += f"\n {INFO} NS Records:\n"
    try:
        r = requests.get(f"https://cloudflare-dns.com/dns-query?name={domain}&type=NS",
                         headers={"Accept": "application/dns-json", "User-Agent": RandomUserAgents()}, timeout=10)
        data = r.json()
        answers = data.get("Answer", [])
        ns_found = [a for a in answers if a.get("type") == 2]
        if ns_found:
            for ns in ns_found:
                output += f" {SUCCESS} {red}{ns.get('data', 'N/A')}{reset}\n"
        else:
            output += f" {ERROR} No NS records found!{reset}\n"
    except:
        output += f" {ERROR} Could not query NS records!{reset}\n"

    Scroll(f"\n{output}")

    Continue()
    Reset()

except Exception as e:
    Error(e)
