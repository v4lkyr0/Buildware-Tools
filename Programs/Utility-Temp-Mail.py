# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import random
    import string
    import time
except Exception as e:
    MissingModule(e)

Title("Utility Temp Mail")
Connection()

API_BASE = "https://api.mail.tm"

def get_domain():
    response = requests.get(f"{API_BASE}/domains", timeout=10)
    response.raise_for_status()
    domains = response.json().get("hydra:member", [])
    if not domains:
        return None
    return domains[0]["domain"]

def create_account(domain):
    user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    address = f"{user}@{domain}"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    response = requests.post(f"{API_BASE}/accounts", json={"address": address, "password": password}, timeout=10)
    if response.status_code != 201:
        return None, None, None
    return address, password, response.json().get("id")

def get_token(address, password):
    response = requests.post(f"{API_BASE}/token", json={"address": address, "password": password}, timeout=10)
    if response.status_code != 200:
        return None
    return response.json().get("token")

def get_messages(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE}/messages", headers=headers, timeout=10)
    if response.status_code != 200:
        return []
    return response.json().get("hydra:member", [])

def get_message_detail(token, msg_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE}/messages/{msg_id}", headers=headers, timeout=10)
    if response.status_code != 200:
        return None
    return response.json()

try:
    Scroll(f"""
 {PREFIX}01{SUFFIX} Generate New Temp Email
 {PREFIX}02{SUFFIX} Check Inbox (enter existing email)
""")
    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    if choice == "1":
        print(f"{LOADING} Generating Temporary Email..", reset)

        domain = get_domain()
        if not domain:
            print(f"{ERROR} Could not fetch available domain!", reset)
            Continue()
            Reset()

        address, password, account_id = create_account(domain)
        if not address:
            print(f"{ERROR} Could not create email account!", reset)
            Continue()
            Reset()

        token = get_token(address, password)
        if not token:
            print(f"{ERROR} Could not authenticate!", reset)
            Continue()
            Reset()

        Scroll(f"""
 {SUCCESS} Your temporary email:{red} {address}
 {SUCCESS} Password:{red} {password}""")

    elif choice == "2":
        email = input(f"{INPUT} Email Address {red}->{reset} ").strip()
        if not email or "@" not in email:
            ErrorInput()

        password = input(f"{INPUT} Password {red}->{reset} ").strip()
        if not password:
            ErrorInput()

        print(f"{LOADING} Authenticating..", reset)

        token = get_token(email, password)
        if not token:
            print(f"{ERROR} Authentication failed! Check email and password.", reset)
            Continue()
            Reset()

        print(f"{LOADING} Checking Inbox..", reset)

        messages = get_messages(token)
        output = ""

        if not messages:
            output += f" {INFO} Inbox is empty!{reset}\n"
        else:
            output += f" {INFO} Found {len(messages)} email(s)\n\n"

            for msg in messages:
                msg_id = msg.get("id")
                detail = get_message_detail(token, msg_id)
                if not detail:
                    continue

                sender = detail.get("from", {})
                sender_str = sender.get("address", "N/A") if isinstance(sender, dict) else str(sender)

                output += f" {SUCCESS} Email Received!{reset}\n"
                output += f" {INFO} From    :{red} {sender_str}{reset}\n"
                output += f" {INFO} Subject :{red} {detail.get('subject', 'N/A')}{reset}\n"
                output += f" {INFO} Date    :{red} {detail.get('createdAt', 'N/A')[:19].replace('T', ' ')}{reset}\n"

                body = detail.get("text", detail.get("intro", "N/A")) or "N/A"
                if len(body) > 500:
                    body = body[:500] + "..."
                output += f" {INFO} Body    :{red} {body}{reset}\n\n"

        Scroll(f"\n{output}")
    else:
        ErrorChoice()

    print()
    Continue()
    Reset()

except Exception as e:
    Error(e)
