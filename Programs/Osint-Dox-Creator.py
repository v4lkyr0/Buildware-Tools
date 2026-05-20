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
    import requests
    import os
    from datetime import datetime
except Exception as e:
    MissingModule(e)

Title("Dox Creator")

Scroll(GradientBanner(osint_banner))

def Ask(label):
    return input(f"{INPUT} {label} {red}->{reset} ").strip() or "None"

def LookupIp(ip):
    try:
        r = requests.get(
            f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,hosting,query",
            timeout=10
        )
        data = r.json()
        if data.get("status") == "success":
            return data
    except Exception:
        pass
    return {}

def LookupPhone(phone):
    try:
        import phonenumbers
        from phonenumbers import geocoder, carrier, timezone as tz
        parsed   = phonenumbers.parse(phone)
        if phonenumbers.is_valid_number(parsed):
            return {
                "country" : geocoder.description_for_number(parsed, "en") or "None",
                "carrier" : carrier.name_for_number(parsed, "en") or "None",
                "timezone": ", ".join(tz.time_zones_for_number(parsed)) or "None",
                "format"  : phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            }
    except Exception:
        pass
    return {}

try:
    print(f"{INFO} Press {red}Enter{white} to skip a field.\n", reset)

    print(f"{INFO} Generated", reset)
    created_by    = Ask("Created By")


    print(f"{INFO} Identity", reset)
    first_name    = Ask("First Name")
    last_name     = Ask("Last Name")
    username      = Ask("Username")
    date_of_birth = Ask("Date of Birth")
    age           = Ask("Age")
    gender        = Ask("Gender")
    nationality   = Ask("Nationality")
    ethnicity     = Ask("Ethnicity")
    religion      = Ask("Religion")
    face_photo    = Ask("Face Photo Url")
    other_photos  = Ask("Other Photos Urls")

    print(f"\n{INFO} Location", reset)
    ip = Ask("Public Ip")

    geo = {}
    if ip != "None":
        pass
        geo = LookupIp(ip)
        if geo:
            pass

    country       = geo.get("country",    None) or Ask("Country")
    region        = geo.get("regionName", None) or Ask("Region / State")
    city          = geo.get("city",       None) or Ask("City")
    zip_code      = geo.get("zip",        None) or Ask("Zip Code")
    latitude      = geo.get("lat",        None) or Ask("Latitude")
    longitude     = geo.get("lon",        None) or Ask("Longitude")
    timezone      = geo.get("timezone",   None) or Ask("Timezone")
    isp           = geo.get("isp",        None) or Ask("ISP")
    org           = geo.get("org",        None) or Ask("Organization")
    asn           = geo.get("as",         None) or Ask("ASN")
    hostname      = geo.get("reverse",    None) or Ask("Hostname")
    is_proxy      = str(geo.get("proxy",  "")) or Ask("Proxy/VPN")
    is_mobile     = str(geo.get("mobile", "")) or Ask("Mobile")
    address       = Ask("Full Address")
    home_address  = Ask("Home Address")
    work_address  = Ask("Work Address")
    coordinates   = f"{latitude}, {longitude}" if latitude != "None" and longitude != "None" else "None"
    maps_url      = f"https://www.google.com/maps?q={latitude},{longitude}" if latitude != "None" and longitude != "None" else "None"

    print(f"\n{INFO} Contact", reset)
    email         = Ask("Email")
    email2        = Ask("Email 2")
    phone         = Ask("Phone Number")

    phone_info = {}
    if phone != "None":
        pass
        phone_info = LookupPhone(phone)
        if phone_info:
            pass

    phone2        = Ask("Phone Number 2")
    phone_country = phone_info.get("country",  "None")
    phone_carrier = phone_info.get("carrier",  "None")
    phone_tz      = phone_info.get("timezone", "None")
    phone_format  = phone_info.get("format",   phone)

    print(f"\n{INFO} Social Media", reset)
    discord       = Ask("Discord")
    discord_id    = Ask("Discord Id")
    instagram     = Ask("Instagram")
    twitter       = Ask("Twitter / X")
    tiktok        = Ask("TikTok")
    facebook      = Ask("Facebook")
    snapchat      = Ask("Snapchat")
    telegram      = Ask("Telegram")
    youtube       = Ask("YouTube")
    twitch        = Ask("Twitch")
    github        = Ask("GitHub")
    steam         = Ask("Steam")
    steam_id      = Ask("Steam Id")
    reddit        = Ask("Reddit")
    linkedin      = Ask("LinkedIn")
    pinterest     = Ask("Pinterest")
    roblox        = Ask("Roblox")
    roblox_id     = Ask("Roblox Id")
    minecraft     = Ask("Minecraft")
    psn           = Ask("PSN")
    xbox          = Ask("Xbox")

    print(f"\n{INFO} Device", reset)
    os_info       = Ask("Operating System")
    browser_info  = Ask("Browser")
    mac_address   = Ask("Mac Address")
    device_model  = Ask("Device Model")
    screen_res    = Ask("Screen Resolution")
    language      = Ask("Language")
    user_agent    = Ask("User Agent")

    print(f"\n{INFO} Family", reset)
    mother        = Ask("Mother's Name")
    mother_phone  = Ask("Mother's Phone")
    father        = Ask("Father's Name")
    father_phone  = Ask("Father's Phone")
    siblings      = Ask("Siblings")
    partner       = Ask("Partner / Spouse")
    partner_phone = Ask("Partner's Phone")
    children      = Ask("Children")
    relationship  = Ask("Relationship Status")

    print(f"\n{INFO} Work & Education", reset)
    job           = Ask("Job / Occupation")
    company       = Ask("Company")
    company_addr  = Ask("Company Address")
    work_email    = Ask("Work Email")
    work_phone    = Ask("Work Phone")
    school        = Ask("School / University")
    degree        = Ask("Degree")
    student_id    = Ask("Student Id")

    print(f"\n{INFO} Financial", reset)
    bank          = Ask("Bank")
    crypto_wallet = Ask("Crypto Wallet")
    paypal        = Ask("PayPal")

    print(f"\n{INFO} Notes", reset)
    notes         = Ask("Notes")
    source        = Ask("Source / How obtained")

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    dox = f"""
⠀⣿⠲⠤⣀⡀
⠀⣸⡏⠀⠀⠀⠉⠳⢄⡀
⠀⣿⠀⠀⠀⠀⠀⠀⠀⠉⠲⣄
⢰⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠲⣄⠀⠀⠀⡰⠋⢙⣿⣦⡀⠀⠀⠀⠀⠀          ██████╗  ██████╗ ██╗  ██╗
⠸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣙⣦⣮⣤⡀⣸⣿⣿⣿⣆⠀⠀⠀⠀          ██╔══██╗██╔═══██╗╚██╗██╔╝
⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⠀⣿⢟⣫⠟⠋⠀⠀⠀⠀          ██║  ██║██║   ██║ ╚███╔╝
⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣷⣷⣿⡁⠀⠀⠀⠀⠀⠀          ██║  ██║██║   ██║ ██╔██╗
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢸⣿⣿⣧⣿⣿⣆⠙⢆⡀⠀⠀⠀⠀          ██████╔╝╚██████╔╝██╔╝ ██╗
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⣤⣿⣿⣿⡟⠹⣿⣿⣿⣿⣷⡀⠀⠀          ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣧⣴⣿⣿⣿⣿⠏⢧
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠈⢳⡀           ██████╗██████╗ ███████╗ █████╗ ████████╗ ██████╗ ██████╗
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡏⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⢳          ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀          ██║     ██████╔╝█████╗  ███████║   ██║   ██║   ██║██████╔╝
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠸⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀          ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██║   ██║██╔══██╗
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀          ╚██████╗██║  ██║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇⢠⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀           ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⢸⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣼⢸⣿⣿⣿⣿⣿⣿⣿⣿                 - Template By {name_tool} | {github_url}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⡄
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇
⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠛⠻⠿⣿⣿⣿⡿⠿⠿⠿⠿⠿⢿⣿⣿⠏

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

╓─────────────────────────────────────╖
              Generated               
╙─────────────────────────────────────╜
 - Created At     : {created_at}
 - Created By     : {created_by}

╓─────────────────────────────────────╖
               Identity
╙─────────────────────────────────────╜
 - Full Name      : {first_name} {last_name}
 - Username       : {username}
 - Date of Birth  : {date_of_birth}
 - Age            : {age}
 - Gender         : {gender}
 - Nationality    : {nationality}
 - Ethnicity      : {ethnicity}
 - Religion       : {religion}
 - Face Photo     : {face_photo}
 - Other Photos   : {other_photos}

╓─────────────────────────────────────╖
               Location
╙─────────────────────────────────────╜
 - Public Ip      : {ip}
 - Hostname       : {hostname}
 - ISP            : {isp}
 - Organization   : {org}
 - ASN            : {asn}
 - Proxy / VPN    : {is_proxy}
 - Mobile         : {is_mobile}
 - Country        : {country}
 - Region         : {region}
 - City           : {city}
 - Zip Code       : {zip_code}
 - Address        : {address}
 - Home Address   : {home_address}
 - Work Address   : {work_address}
 - Coordinates    : {coordinates}
 - Google Maps    : {maps_url}
 - Timezone       : {timezone}

╓─────────────────────────────────────╖
               Contact               
╙─────────────────────────────────────╜
 - Email          : {email}
 - Email 2        : {email2}
 - Phone          : {phone_format}
 - Phone Country  : {phone_country}
 - Phone Carrier  : {phone_carrier}
 - Phone Timezone : {phone_tz}
 - Phone 2        : {phone2}

╓─────────────────────────────────────╖
             Social Media             
╙─────────────────────────────────────╜
 - Discord        : {discord}
 - Discord Id     : {discord_id}
 - Instagram      : {instagram}
 - Twitter / X    : {twitter}
 - TikTok         : {tiktok}
 - Facebook       : {facebook}
 - Snapchat       : {snapchat}
 - Telegram       : {telegram}
 - YouTube        : {youtube}
 - Twitch         : {twitch}
 - GitHub         : {github}
 - Steam          : {steam}
 - Steam Id       : {steam_id}
 - Reddit         : {reddit}
 - LinkedIn       : {linkedin}
 - Pinterest      : {pinterest}
 - Roblox         : {roblox}
 - Roblox Id      : {roblox_id}
 - Minecraft      : {minecraft}
 - PSN            : {psn}
 - Xbox           : {xbox}

╓─────────────────────────────────────╖
                Device                
╙─────────────────────────────────────╜
 - OS             : {os_info}
 - Browser        : {browser_info}
 - Mac Address    : {mac_address}
 - Device Model   : {device_model}
 - Screen Res     : {screen_res}
 - Language       : {language}
 - User Agent     : {user_agent}

╓─────────────────────────────────────╖
                Family                
╙─────────────────────────────────────╜
 - Mother         : {mother}
 - Mother Phone   : {mother_phone}
 - Father         : {father}
 - Father Phone   : {father_phone}
 - Siblings       : {siblings}
 - Partner        : {partner}
 - Partner Phone  : {partner_phone}
 - Children       : {children}
 - Relationship   : {relationship}

╓─────────────────────────────────────╖
           Work & Education            
╙─────────────────────────────────────╜
 - Job            : {job}
 - Company        : {company}
 - Company Addr   : {company_addr}
 - Work Email     : {work_email}
 - Work Phone     : {work_phone}
 - School         : {school}
 - Degree         : {degree}
 - Student Id     : {student_id}

╓─────────────────────────────────────╖
              Financial               
╙─────────────────────────────────────╜
 - Bank           : {bank}
 - Crypto Wallet  : {crypto_wallet}
 - PayPal         : {paypal}

╓─────────────────────────────────────╖
                Notes                
╙─────────────────────────────────────╜
 - Notes          : {notes}
 - Source         : {source}

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────"""

    print(f"{LOADING} Generating..", reset)

    timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
    name        = f"{first_name}".replace(" ", "_") if first_name != "None" else "Unknown"
    filename    = f"Dox_{name}.txt"
    output_dir  = os.path.join(tool_path, "Programs", "Output", "DoxCreator")
    output_path = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(dox)

    print(f"{SUCCESS} Saved:{red} {filename}", reset)

    if platform_pc == "Windows":
        os.startfile(output_dir)
    else:
        subprocess.Popen(["xdg-open", output_dir])

    Continue()
    Reset()

except Exception as e:
    Error(e)