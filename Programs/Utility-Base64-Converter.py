# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import base64
    import tkinter as tk
    from tkinter import filedialog
except Exception as e:
    MissingModule(e)

def BrowseFile(title_text="Select File", file_types=None):
    if file_types is None:
        file_types = [("All Files", "*.*")]
    root = tk.Tk()
    root.withdraw()
    try:
        root.iconbitmap(os.path.join(tool_path, 'Programs', 'Images', 'BuildwareIcon.ico'))
    except:
        pass
    file_path = filedialog.askopenfilename(title=f"{name_tool} {version_tool} - {title_text}", filetypes=file_types)
    root.destroy()
    return file_path

Title("Utility Base64 Converter")

try:
    Scroll(f"""
 {PREFIX}01{SUFFIX} Encode Text to Base64
 {PREFIX}02{SUFFIX} Decode Base64 to Text
 {PREFIX}03{SUFFIX} Encode File to Base64
 {PREFIX}04{SUFFIX} Decode Base64 to File
""")
    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    if choice == "1":
        text = input(f"{INPUT} Text {red}->{reset} ").strip()
        if not text:
            ErrorInput()
        encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        print(f"\n {SUCCESS} Encoded:{red} {encoded}", reset)

    elif choice == "2":
        b64 = input(f"{INPUT} Base64 {red}->{reset} ").strip()
        if not b64:
            ErrorInput()
        try:
            decoded = base64.b64decode(b64).decode('utf-8')
            print(f"\n {SUCCESS} Decoded:{red} {decoded}", reset)
        except Exception:
            print(f"\n {ERROR} Invalid Base64 string!", reset)

    elif choice == "3":
        filepath = BrowseFile("Encode File to Base64")
        if not filepath:
            print(f"{ERROR} No file selected!", reset)
            Continue()
            Reset()
        print(f"{INPUT} File Path {red}->{reset} {filepath}")
        if not os.path.isfile(filepath):
            print(f"{ERROR} File not found!", reset)
            Continue()
            Reset()
        with open(filepath, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        output_dir = os.path.join(tool_path, "Programs", "Output", "Base64Converter")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, os.path.basename(filepath) + ".b64")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(encoded)
        print(f"\n {SUCCESS} File encoded and saved to:{red} {output_path}", reset)
        print(f" {INFO} Size :{red} {len(encoded)} characters", reset)
        if platform_pc == "Windows":
            os.startfile(output_dir)
        else:
            subprocess.Popen(['xdg-open', output_dir])

    elif choice == "4":
        filepath = BrowseFile("Decode Base64 to File", [("Base64 Files", "*.b64"), ("Text Files", "*.txt"), ("All Files", "*.*")])
        if not filepath:
            print(f"{ERROR} No file selected!", reset)
            Continue()
            Reset()
        print(f"{INPUT} Base64 File Path {red}->{reset} {filepath}")
        if not os.path.isfile(filepath):
            print(f"{ERROR} File not found!", reset)
            Continue()
            Reset()
        with open(filepath, 'r', encoding='utf-8') as f:
            b64_content = f.read().strip()
        try:
            decoded = base64.b64decode(b64_content)
            output_dir = os.path.join(tool_path, "Programs", "Output", "Base64Converter")
            os.makedirs(output_dir, exist_ok=True)
            basename = os.path.basename(filepath)
            out_name = basename.replace(".b64", ".decoded") if basename.endswith(".b64") else basename + ".decoded"
            output_path = os.path.join(output_dir, out_name)
            with open(output_path, 'wb') as f:
                f.write(decoded)
            print(f"\n {SUCCESS} File decoded and saved to:{red} {output_path}", reset)
            print(f" {INFO} Size :{red} {len(decoded)} bytes", reset)
            if platform_pc == "Windows":
                os.startfile(output_dir)
            else:
                subprocess.Popen(['xdg-open', output_dir])
        except Exception:
            print(f"\n {ERROR} Invalid Base64 content in file!", reset)
    else:
        ErrorChoice()

    print()
    Continue()
    Reset()

except Exception as e:
    Error(e)
