# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

Title("Utility Text Converter")

try:
    Scroll(f"""
 {PREFIX}01{SUFFIX} Text to Binary
 {PREFIX}02{SUFFIX} Binary to Text
 {PREFIX}03{SUFFIX} Text to Hexadecimal
 {PREFIX}04{SUFFIX} Hexadecimal to Text
 {PREFIX}05{SUFFIX} Text to Decimal
 {PREFIX}06{SUFFIX} Decimal to Text
 {PREFIX}07{SUFFIX} Text to Morse Code
 {PREFIX}08{SUFFIX} Morse Code to Text
 {PREFIX}09{SUFFIX} Reverse Text
""")
    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    morse_code_map = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', ' ': '/', '.': '.-.-.-', ',': '--..--',
        '?': '..--..', '!': '-.-.--', '@': '.--.-.', '&': '.-...',
    }
    reverse_morse = {v: k for k, v in morse_code_map.items()}

    if choice == "1":
        text = input(f"{INPUT} Text {red}->{reset} ").strip()
        binary = ' '.join(format(ord(c), '08b') for c in text)
        print(f"\n {SUCCESS} Binary:{red} {binary}", reset)

    elif choice == "2":
        binary = input(f"{INPUT} Binary {red}->{reset} ").strip()
        try:
            text = ''.join(chr(int(b, 2)) for b in binary.split())
            print(f"\n {SUCCESS} Text:{red} {text}", reset)
        except:
            print(f"\n {ERROR} Invalid binary input!", reset)

    elif choice == "3":
        text = input(f"{INPUT} Text {red}->{reset} ").strip()
        hex_str = ' '.join(format(ord(c), '02x') for c in text)
        print(f"\n {SUCCESS} Hex:{red} {hex_str}", reset)

    elif choice == "4":
        hex_str = input(f"{INPUT} Hex {red}->{reset} ").strip()
        try:
            hex_clean = hex_str.replace(" ", "").replace("0x", "")
            text = bytes.fromhex(hex_clean).decode('utf-8')
            print(f"\n {SUCCESS} Text:{red} {text}", reset)
        except:
            print(f"\n {ERROR} Invalid hexadecimal input!", reset)

    elif choice == "5":
        text = input(f"{INPUT} Text {red}->{reset} ").strip()
        decimal = ' '.join(str(ord(c)) for c in text)
        print(f"\n {SUCCESS} Decimal:{red} {decimal}", reset)

    elif choice == "6":
        decimal = input(f"{INPUT} Decimal {red}->{reset} ").strip()
        try:
            text = ''.join(chr(int(d)) for d in decimal.split())
            print(f"\n {SUCCESS} Text:{red} {text}", reset)
        except:
            print(f"\n {ERROR} Invalid decimal input!", reset)

    elif choice == "7":
        text = input(f"{INPUT} Text {red}->{reset} ").strip().upper()
        morse = ' '.join(morse_code_map.get(c, c) for c in text)
        print(f"\n {SUCCESS} Morse:{red} {morse}", reset)

    elif choice == "8":
        morse = input(f"{INPUT} Morse Code {red}->{reset} ").strip()
        try:
            words = morse.split(' / ')
            text = ''
            for word in words:
                for letter in word.split():
                    text += reverse_morse.get(letter, '?')
                text += ' '
            print(f"\n {SUCCESS} Text:{red} {text.strip()}", reset)
        except:
            print(f"\n {ERROR} Invalid Morse code input!", reset)

    elif choice == "9":
        text = input(f"{INPUT} Text {red}->{reset} ").strip()
        print(f"\n {SUCCESS} Reversed:{red} {text[::-1]}", reset)

    else:
        ErrorChoice()

    print()
    Continue()
    Reset()

except Exception as e:
    Error(e)
