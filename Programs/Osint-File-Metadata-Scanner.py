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
    import os
    import struct
    import zipfile
    import xml.etree.ElementTree as ET
    from datetime import datetime
except Exception as e:
    MissingModule(e)

Title("File Metadata Scanner")

Scroll(GradientBanner(osint_banner))

def FormatSize(size):
    if size >= 1024 * 1024:
        return f"{round(size / 1024 / 1024, 2)} MB"
    return f"{round(size / 1024, 2)} KB"

def FormatDate(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "None"

def ScanImage(filepath):
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS

        img      = Image.open(filepath)
        exif_raw = img._getexif()

        print(f"\n {INFO} Image", reset)
        print(f" {SUCCESS} Format     :{red} {img.format or 'None'}", reset)
        print(f" {SUCCESS} Mode       :{red} {img.mode or 'None'}", reset)
        print(f" {SUCCESS} Dimensions :{red} {img.size[0]}x{img.size[1]}", reset)

        if not exif_raw:
            return

        exif_data = {}
        for tag, value in exif_raw.items():
            decoded = TAGS.get(tag, tag)
            if decoded != "MakerNote":
                exif_data[decoded] = value

        priority = [
            "Make", "Model", "Software", "DateTime", "DateTimeOriginal",
            "DateTimeDigitized", "Artist", "Copyright", "HostComputer",
            "ExposureTime", "FNumber", "ISOSpeedRatings", "FocalLength",
            "Flash", "WhiteBalance", "Orientation",
        ]

        print(f"\n {INFO} Exif", reset)
        for tag in priority:
            if tag in exif_data:
                print(f" {SUCCESS} {tag:<20} :{red} {exif_data[tag]}", reset)

        gps_info = {}
        for tag, value in exif_raw.items():
            if TAGS.get(tag) == "GPSInfo":
                for t, v in value.items():
                    gps_info[GPSTAGS.get(t, t)] = v

        if gps_info:
            try:
                def ToDeg(val):
                    d, m, s = val
                    return float(d) + float(m) / 60 + float(s) / 3600

                lat = ToDeg(gps_info["GPSLatitude"])
                lon = ToDeg(gps_info["GPSLongitude"])
                if gps_info.get("GPSLatitudeRef")  == "S": lat = -lat
                if gps_info.get("GPSLongitudeRef") == "W": lon = -lon
                lat = round(lat, 6)
                lon = round(lon, 6)

                print(f"\n {INFO} GPS", reset)
                print(f" {SUCCESS} Latitude    :{red} {lat}", reset)
                print(f" {SUCCESS} Longitude   :{red} {lon}", reset)
                print(f" {SUCCESS} Google Maps :{red} https://www.google.com/maps?q={lat},{lon}", reset)
            except Exception:
                pass

    except ImportError:
        print(f"{ERROR} Pillow is required for image scanning!", reset)
    except Exception:
        pass

def ScanPdf(filepath):
    try:
        with open(filepath, "rb") as f:
            content = f.read().decode("latin-1", errors="ignore")

        print(f"\n {INFO} PDF", reset)

        fields = {
            "Title"   : "/Title",
            "Author"  : "/Author",
            "Creator" : "/Creator",
            "Producer": "/Producer",
            "Subject" : "/Subject",
            "Keywords": "/Keywords",
        }

        for label, key in fields.items():
            if key in content:
                try:
                    idx   = content.index(key) + len(key)
                    chunk = content[idx:idx+200].strip()
                    if chunk.startswith("("):
                        value = chunk[1:chunk.index(")")].strip()
                        if value:
                            print(f" {SUCCESS} {label:<12} :{red} {value}", reset)
                except Exception:
                    pass

        dates = ["CreationDate", "ModDate"]
        for d in dates:
            if d in content:
                try:
                    idx   = content.index(d) + len(d)
                    chunk = content[idx:idx+50].strip()
                    if "D:" in chunk:
                        raw = chunk[chunk.index("D:")+2:chunk.index("D:")+16]
                        print(f" {SUCCESS} {d:<12} :{red} {raw}", reset)
                except Exception:
                    pass

    except Exception:
        pass

def ScanDocx(filepath):
    try:
        if not zipfile.is_zipfile(filepath):
            return

        with zipfile.ZipFile(filepath, "r") as z:
            if "docProps/core.xml" in z.namelist():
                with z.open("docProps/core.xml") as f:
                    tree = ET.parse(f)
                    root = tree.getroot()

                ns = {
                    "dc"     : "http://purl.org/dc/elements/1.1/",
                    "cp"     : "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
                    "dcterms": "http://purl.org/dc/terms/",
                }

                print(f"\n {INFO} Document", reset)

                fields = {
                    "Title"          : "dc:title",
                    "Subject"        : "dc:subject",
                    "Creator"        : "dc:creator",
                    "Keywords"       : "cp:keywords",
                    "Description"    : "dc:description",
                    "Last Modified By": "cp:lastModifiedBy",
                    "Revision"       : "cp:revision",
                    "Created"        : "dcterms:created",
                    "Modified"       : "dcterms:modified",
                }

                for label, tag in fields.items():
                    prefix, name = tag.split(":")
                    el = root.find(f"{{{ns[prefix]}}}{name}")
                    if el is not None and el.text:
                        print(f" {SUCCESS} {label:<20} :{red} {el.text}", reset)

            if "docProps/app.xml" in z.namelist():
                with z.open("docProps/app.xml") as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    ns   = "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"

                    app_fields = ["Application", "Company", "AppVersion", "Pages", "Words", "Characters"]
                    for field in app_fields:
                        el = root.find(f"{{{ns}}}{field}")
                        if el is not None and el.text:
                            print(f" {SUCCESS} {field:<20} :{red} {el.text}", reset)

    except Exception:
        pass

def ScanMp3(filepath):
    try:
        with open(filepath, "rb") as f:
            data = f.read(10)

        if data[:3] != b"ID3":
            return

        print(f"\n {INFO} Audio", reset)

        with open(filepath, "rb") as f:
            content = f.read(10000).decode("latin-1", errors="ignore")

        tags = {
            "TIT2": "Title",
            "TPE1": "Artist",
            "TALB": "Album",
            "TYER": "Year",
            "TCON": "Genre",
            "TCOM": "Composer",
            "TCOP": "Copyright",
            "TENC": "Encoder",
            "TSSE": "Software",
        }

        for tag, label in tags.items():
            if tag in content:
                try:
                    idx   = content.index(tag) + 10
                    value = content[idx:idx+100].split("\x00")[0].strip()
                    if value and value.isprintable():
                        print(f" {SUCCESS} {label:<12} :{red} {value}", reset)
                except Exception:
                    pass

    except Exception:
        pass

try:
    filepath = BrowseFile("Select File", [
        ("All supported files", "*.jpg;*.jpeg;*.png;*.tiff;*.bmp;*.webp;*.pdf;*.docx;*.xlsx;*.pptx;*.mp3"),
        ("Images",              "*.jpg;*.jpeg;*.png;*.tiff;*.bmp;*.webp"),
        ("Documents",           "*.pdf;*.docx;*.xlsx;*.pptx"),
        ("Audio",               "*.mp3"),
        ("All Files",           "*.*"),
    ])

    if not filepath:
        print(f"{ERROR} No file selected!", reset)
        Continue()
        Reset()

    if not os.path.exists(filepath):
        print(f"{ERROR} File not found!", reset)
        Continue()
        Reset()

    filename = os.path.basename(filepath)
    ext      = os.path.splitext(filepath)[1].lower()
    size     = os.path.getsize(filepath)

    Scroll(f""" {SUCCESS} Name      :{red} {filename}{white}
 {SUCCESS} Size      :{red} {FormatSize(size)}{white}
 {SUCCESS} Extension :{red} {ext}{white}
 {SUCCESS} Created   :{red} {FormatDate(os.path.getctime(filepath))}{white}
 {SUCCESS} Modified  :{red} {FormatDate(os.path.getmtime(filepath))}{white}
 {SUCCESS} Accessed  :{red} {FormatDate(os.path.getatime(filepath))}{white}""")

    if ext in [".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".webp"]:
        ScanImage(filepath)
    elif ext == ".pdf":
        ScanPdf(filepath)
    elif ext in [".docx", ".xlsx", ".pptx"]:
        ScanDocx(filepath)
    elif ext == ".mp3":
        ScanMp3(filepath)
    else:
        print(f"{INFO} No specific metadata extractor for this file type.", reset)

    print()
    Continue()
    Reset()

except Exception as e:
    Error(e)