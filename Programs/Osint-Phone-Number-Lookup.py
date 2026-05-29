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
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except Exception as e:
    MissingModule(e)

Title("Phone Number Lookup")

Scroll(GradientBanner(osint_banner))

try:
    phone = input(f"{INPUT} Phone Number {red}({white}+country code{red}) ->{reset} ").strip()

    if not phone:
        ErrorInput()

    print(f"{LOADING} Looking up..", reset)

    try:
        parsed = phonenumbers.parse(phone)
    except phonenumbers.NumberParseException as e:
        print(f"{ERROR} Invalid phone number format:{red} {e}", reset)
        Continue()
        Reset()

    if not phonenumbers.is_valid_number(parsed):
        print(f"{ERROR} Invalid phone number!", reset)
        Continue()
        Reset()

    try:
        country  = geocoder.description_for_number(parsed, "en") or "None"
        operator = carrier.name_for_number(parsed, "en")         or "None"
        zones    = timezone.time_zones_for_number(parsed)
        format1  = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        format2  = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        format3  = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        zones_str = ", ".join(zones) if zones else "None"

        number_type_map = {
            0 : "Fixed Line",
            1 : "Mobile",
            2 : "Fixed or Mobile",
            3 : "Toll Free",
            4 : "Premium Rate",
            5 : "Shared Cost",
            6 : "VoIP",
            7 : "Personal Number",
            8 : "Pager",
            9 : "UAN",
            10: "Unknown",
            27: "Emergency",
            28: "Voicemail",
        }
        number_type = number_type_map.get(phonenumbers.number_type(parsed), "None")

        e164_clean   = format3.lstrip("+")
        national_raw = format2.replace(" ", "").replace("-", "")

        osint_links = {
            "Truecaller"   : f"https://www.truecaller.com/search/us/{e164_clean}",
            "Sync.me"      : f"https://sync.me/search/?number={format3}",
            "SpyDialer"    : f"https://spydialer.com/default.aspx?phone={national_raw}",
            "CallerID Test": f"https://calleridtest.com/lookup?phone={e164_clean}",
            "Mr. Number"   : f"https://mrnumber.com/{e164_clean}",
            "WhoCallsMe"   : f"https://www.whocalledme.com/PhoneNumber/{national_raw}",
            "800notes"     : f"https://800notes.com/Phone.aspx/{national_raw}",
            "Tellows"      : f"https://www.tellows.com/num/{e164_clean}",
        }

        osint_block = "\n".join(f" {SUCCESS} {name:<13} :{red} {url}{white}" for name, url in osint_links.items())

        Scroll(f"""
 {SUCCESS} Number   :{red} {format1}{white}
 {SUCCESS} National :{red} {format2}{white}
 {SUCCESS} E164     :{red} {format3}{white}
 {SUCCESS} Country  :{red} {country}{white}
 {SUCCESS} Carrier  :{red} {operator}{white}
 {SUCCESS} Timezone :{red} {zones_str}{white}
 {SUCCESS} Type     :{red} {number_type}{white}
 {SUCCESS} Valid    :{red} {phonenumbers.is_valid_number(parsed)}{white}
 {SUCCESS} Possible :{red} {phonenumbers.is_possible_number(parsed)}{white}

{osint_block}
""")

    except Exception:
        print(f"{ERROR} Could not fetch phone information!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)