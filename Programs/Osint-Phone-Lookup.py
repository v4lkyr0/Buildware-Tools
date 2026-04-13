# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import re
except Exception as e:
    MissingModule(e)

Title("Osint Phone Lookup")

country_codes = {
    "+1": "United States / Canada", "+7": "Russia / Kazakhstan", "+20": "Egypt",
    "+27": "South Africa", "+30": "Greece", "+31": "Netherlands", "+32": "Belgium",
    "+33": "France", "+34": "Spain", "+36": "Hungary", "+39": "Italy", "+40": "Romania",
    "+41": "Switzerland", "+43": "Austria", "+44": "United Kingdom", "+45": "Denmark",
    "+46": "Sweden", "+47": "Norway", "+48": "Poland", "+49": "Germany", "+51": "Peru",
    "+52": "Mexico", "+53": "Cuba", "+54": "Argentina", "+55": "Brazil", "+56": "Chile",
    "+57": "Colombia", "+58": "Venezuela", "+60": "Malaysia", "+61": "Australia",
    "+62": "Indonesia", "+63": "Philippines", "+64": "New Zealand", "+65": "Singapore",
    "+66": "Thailand", "+81": "Japan", "+82": "South Korea", "+84": "Vietnam",
    "+86": "China", "+90": "Turkey", "+91": "India", "+92": "Pakistan",
    "+93": "Afghanistan", "+94": "Sri Lanka", "+95": "Myanmar", "+98": "Iran",
    "+212": "Morocco", "+213": "Algeria", "+216": "Tunisia", "+218": "Libya",
    "+220": "Gambia", "+221": "Senegal", "+234": "Nigeria", "+254": "Kenya",
    "+255": "Tanzania", "+256": "Uganda", "+260": "Zambia", "+261": "Madagascar",
    "+263": "Zimbabwe", "+351": "Portugal", "+352": "Luxembourg", "+353": "Ireland",
    "+354": "Iceland", "+355": "Albania", "+358": "Finland", "+359": "Bulgaria",
    "+370": "Lithuania", "+371": "Latvia", "+372": "Estonia", "+373": "Moldova",
    "+374": "Armenia", "+375": "Belarus", "+380": "Ukraine", "+381": "Serbia",
    "+385": "Croatia", "+386": "Slovenia", "+387": "Bosnia", "+420": "Czech Republic",
    "+421": "Slovakia", "+852": "Hong Kong", "+853": "Macau", "+855": "Cambodia",
    "+856": "Laos", "+880": "Bangladesh", "+886": "Taiwan", "+960": "Maldives",
    "+961": "Lebanon", "+962": "Jordan", "+963": "Syria", "+964": "Iraq",
    "+965": "Kuwait", "+966": "Saudi Arabia", "+967": "Yemen", "+968": "Oman",
    "+971": "United Arab Emirates", "+972": "Israel", "+973": "Bahrain", "+974": "Qatar",
    "+975": "Bhutan", "+976": "Mongolia", "+977": "Nepal", "+992": "Tajikistan",
    "+993": "Turkmenistan", "+994": "Azerbaijan", "+995": "Georgia", "+996": "Kyrgyzstan",
    "+998": "Uzbekistan",
}

try:
    phone = input(f"{INPUT} Phone Number {red}->{reset} ").strip()
    if not phone:
        ErrorInput()

    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    if not cleaned.startswith('+'):
        cleaned = '+' + cleaned

    if not re.match(r'^\+\d{7,15}$', cleaned):
        print(f"{ERROR} Invalid phone number format!", reset)
        Continue()
        Reset()

    print(f"{LOADING} Analyzing Phone Number..", reset)

    country = "Unknown"
    matched_code = "Unknown"
    for length in [4, 3, 2]:
        prefix = cleaned[:length]
        if prefix in country_codes:
            country = country_codes[prefix]
            matched_code = prefix
            break

    local_number = cleaned[len(matched_code):] if matched_code != "Unknown" else cleaned[1:]
    num_length = len(local_number)

    if num_length >= 9:
        number_type = "Mobile / Landline"
    elif num_length >= 7:
        number_type = "Landline / Short"
    else:
        number_type = "Short / Special"

    Scroll(f"""
 {INFO} Raw Input                :{red} {phone}
 {INFO} Cleaned Format           :{red} {cleaned}
 {INFO} Country Code             :{red} {matched_code}
 {INFO} Country                  :{red} {country}
 {INFO} Local Number             :{red} {local_number}
 {INFO} Number Length            :{red} {num_length} digits
 {INFO} Possible Type            :{red} {number_type}
 {INFO} International Format     :{red} {matched_code} {local_number}
""")

    Continue()
    Reset()

except Exception as e:
    Error(e)
