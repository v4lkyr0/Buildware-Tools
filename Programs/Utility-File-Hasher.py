# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import hashlib
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

Title("Utility File Hasher")

try:
    Scroll(f"""
 {PREFIX}01{SUFFIX} Hash a File
 {PREFIX}02{SUFFIX} Compare Two Files
 {PREFIX}03{SUFFIX} Verify File Against Hash
""")
    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    def hash_file(filepath, algorithm="sha256"):
        h = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()

    if choice == "1":
        filepath = BrowseFile("Hash a File")
        if not filepath:
            print(f"{ERROR} No file selected!", reset)
            Continue()
            Reset()
        print(f"{INPUT} File Path {red}->{reset} {filepath}")
        if not os.path.isfile(filepath):
            print(f"{ERROR} File not found!", reset)
            Continue()
            Reset()

        size = os.path.getsize(filepath)
        print(f"\n {INFO} File :{red} {os.path.basename(filepath)}", reset)
        print(f" {INFO} Size :{red} {size:,} bytes", reset)

        for algo in ["md5", "sha1", "sha256", "sha512"]:
            h = hash_file(filepath, algo)
            print(f" {SUCCESS} {algo.upper():8s}:{red} {h}", reset)

    elif choice == "2":
        file1 = BrowseFile("Select File 1")
        if not file1:
            print(f"{ERROR} No file selected!", reset)
            Continue()
            Reset()
        print(f"{INPUT} File 1 {red}->{reset} {file1}")
        file2 = BrowseFile("Select File 2")
        if not file2:
            print(f"{ERROR} No file selected!", reset)
            Continue()
            Reset()
        print(f"{INPUT} File 2 {red}->{reset} {file2}")

        if not os.path.isfile(file1) or not os.path.isfile(file2):
            print(f"{ERROR} One or both files not found!", reset)
            Continue()
            Reset()

        print(f"{LOADING} Comparing Files..", reset)

        hash1 = hash_file(file1)
        hash2 = hash_file(file2)

        print(f" {INFO} File 1 :{red} {os.path.basename(file1)}", reset)
        print(f" {INFO} SHA256 :{red} {hash1}", reset)
        print(f" {INFO} File 2 :{red} {os.path.basename(file2)}", reset)
        print(f" {INFO} SHA256 :{red} {hash2}", reset)

        if hash1 == hash2:
            print(f" {SUCCESS} Files are identical!", reset)
        else:
            print(f" {ERROR} Files are different!", reset)

    elif choice == "3":
        filepath = BrowseFile("Verify File Against Hash")
        if not filepath:
            print(f"{ERROR} No file selected!", reset)
            Continue()
            Reset()
        print(f"{INPUT} File Path {red}->{reset} {filepath}")
        expected = input(f"{INPUT} Expected Hash {red}->{reset} ").strip().lower()

        if not os.path.isfile(filepath):
            print(f"{ERROR} File not found!", reset)
            Continue()
            Reset()

        hash_len = len(expected)
        if hash_len == 32:
            algo = "md5"
        elif hash_len == 40:
            algo = "sha1"
        elif hash_len == 64:
            algo = "sha256"
        elif hash_len == 128:
            algo = "sha512"
        else:
            algo = "sha256"

        actual = hash_file(filepath, algo)

        print(f"\n {INFO} Algorithm :{red} {algo.upper()}", reset)
        print(f" {INFO} Expected  :{red} {expected}", reset)
        print(f" {INFO} Actual    :{red} {actual}", reset)

        if actual == expected:
            print(f" {SUCCESS} Hash matches!", reset)
        else:
            print(f" {ERROR} Hash mismatch!", reset)

    else:
        ErrorChoice()

    print()
    Continue()
    Reset()

except Exception as e:
    Error(e)
