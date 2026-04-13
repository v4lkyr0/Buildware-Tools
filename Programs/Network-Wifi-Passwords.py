# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    import ctypes
    from ctypes import wintypes
    import xml.etree.ElementTree as ET
except Exception as e:
    MissingModule(e)

Title("Network Wifi Passwords")

WLAN_PROFILE_GET_PLAINTEXT_KEY = 4
ERROR_SUCCESS = 0

class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", ctypes.c_ulong),
        ("Data2", ctypes.c_ushort),
        ("Data3", ctypes.c_ushort),
        ("Data4", ctypes.c_ubyte * 8),
    ]

class WLAN_INTERFACE_INFO(ctypes.Structure):
    _fields_ = [
        ("InterfaceGuid", GUID),
        ("strInterfaceDescription", ctypes.c_wchar * 256),
        ("isState", ctypes.c_uint),
    ]

class WLAN_INTERFACE_INFO_LIST(ctypes.Structure):
    _fields_ = [
        ("dwNumberOfItems", ctypes.c_uint),
        ("dwIndex", ctypes.c_uint),
        ("InterfaceInfo", WLAN_INTERFACE_INFO * 1),
    ]

class WLAN_PROFILE_INFO(ctypes.Structure):
    _fields_ = [
        ("strProfileName", ctypes.c_wchar * 256),
        ("dwFlags", ctypes.c_uint),
    ]

class WLAN_PROFILE_INFO_LIST(ctypes.Structure):
    _fields_ = [
        ("dwNumberOfItems", ctypes.c_uint),
        ("dwIndex", ctypes.c_uint),
        ("ProfileInfo", WLAN_PROFILE_INFO * 1),
    ]

def get_wifi_profiles():
    profiles = []

    try:
        wlanapi = ctypes.windll.wlanapi
    except OSError:
        return profiles

    negotiated_version = ctypes.c_uint()
    client_handle = ctypes.c_void_p()

    ret = wlanapi.WlanOpenHandle(
        ctypes.c_uint(2), None,
        ctypes.byref(negotiated_version),
        ctypes.byref(client_handle)
    )
    if ret != ERROR_SUCCESS:
        return profiles

    interface_list_ptr = ctypes.c_void_p()
    ret = wlanapi.WlanEnumInterfaces(client_handle, None, ctypes.byref(interface_list_ptr))
    if ret != ERROR_SUCCESS:
        wlanapi.WlanCloseHandle(client_handle, None)
        return profiles

    interface_list = ctypes.cast(interface_list_ptr, ctypes.POINTER(WLAN_INTERFACE_INFO_LIST)).contents
    num_interfaces = interface_list.dwNumberOfItems

    for i in range(num_interfaces):
        iface = ctypes.cast(
            ctypes.addressof(interface_list.InterfaceInfo) + i * ctypes.sizeof(WLAN_INTERFACE_INFO),
            ctypes.POINTER(WLAN_INTERFACE_INFO)
        ).contents
        guid = iface.InterfaceGuid

        profile_list_ptr = ctypes.c_void_p()
        ret = wlanapi.WlanGetProfileList(client_handle, ctypes.byref(guid), None, ctypes.byref(profile_list_ptr))
        if ret != ERROR_SUCCESS:
            continue

        profile_list = ctypes.cast(profile_list_ptr, ctypes.POINTER(WLAN_PROFILE_INFO_LIST)).contents
        num_profiles = profile_list.dwNumberOfItems

        for j in range(num_profiles):
            prof = ctypes.cast(
                ctypes.addressof(profile_list.ProfileInfo) + j * ctypes.sizeof(WLAN_PROFILE_INFO),
                ctypes.POINTER(WLAN_PROFILE_INFO)
            ).contents
            profile_name = prof.strProfileName

            xml_data = ctypes.c_wchar_p()
            flags = ctypes.c_uint(WLAN_PROFILE_GET_PLAINTEXT_KEY)
            access = ctypes.c_uint()

            ret = wlanapi.WlanGetProfile(
                client_handle, ctypes.byref(guid), profile_name, None,
                ctypes.byref(xml_data), ctypes.byref(flags), ctypes.byref(access)
            )

            password = "N/A"
            auth = "N/A"
            cipher = "N/A"

            if ret == ERROR_SUCCESS and xml_data.value:
                xml_string = xml_data.value
                wlanapi.WlanFreeMemory(xml_data)

                try:
                    ns = {'ns': 'http://www.microsoft.com/networking/WLAN/profile/v1'}
                    root = ET.fromstring(xml_string)

                    key_elem = root.find('.//ns:keyMaterial', ns)
                    if key_elem is not None and key_elem.text:
                        password = key_elem.text

                    auth_elem = root.find('.//ns:authentication', ns)
                    if auth_elem is not None and auth_elem.text:
                        auth = auth_elem.text

                    enc_elem = root.find('.//ns:encryption', ns)
                    if enc_elem is not None and enc_elem.text:
                        cipher = enc_elem.text
                except:
                    pass

            profiles.append({
                'name': profile_name,
                'password': password,
                'auth': auth,
                'cipher': cipher
            })

        wlanapi.WlanFreeMemory(profile_list_ptr)

    wlanapi.WlanFreeMemory(interface_list_ptr)
    wlanapi.WlanCloseHandle(client_handle, None)

    return profiles

try:
    if platform_pc != "Windows":
        print(f"{ERROR} This feature is only available on Windows!", reset)
        Continue()
        Reset()

    print(f"{LOADING} Retrieving Saved Wifi Profiles..", reset)

    profiles = get_wifi_profiles()

    if not profiles:
        print(f"{ERROR} No saved Wifi profiles found!", reset)
        Continue()
        Reset()

    output = ""
    output += f"{INFO} Found {len(profiles)} saved Wifi Networks{reset}\n\n"

    found = 0
    for profile in profiles:
        name = profile['name']
        password = profile['password']
        auth = profile['auth']

        output += f"{SUCCESS} Network:{red} {name:20s}{white}| Password:{red} {password:20s}{white}| Auth:{red} {auth}{reset}\n"
        found += 1

    output += f"\n{INFO} Total retrieved:{red} {found}/{len(profiles)}{reset}\n"

    Scroll(f"\n{output}")

    Continue()
    Reset()

except Exception as e:
    Error(e)
