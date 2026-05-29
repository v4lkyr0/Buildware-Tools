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
    import threading
    import time
except Exception as e:
    MissingModule(e)

Title("Proxy Scraper")

Scroll(GradientBanner(network_banner))

try:
    Scroll(f"""
 {PREFIX}01{SUFFIX} Http
 {PREFIX}02{SUFFIX} Https
 {PREFIX}03{SUFFIX} Socks4
 {PREFIX}04{SUFFIX} Socks5
 {PREFIX}05{SUFFIX} All
""")

    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    if choice not in ["1", "2", "3", "4", "5"]:
        ErrorChoice()

    try:
        check    = input(f"{INPUT} Check proxies? {YESORNO} {red}->{reset} ").strip().lower()
        do_check = check in ["y", "yes"]
    except Exception:
        do_check = False

    max_latency = 5000

    if do_check:
        try:
            lat_input = input(f"{INPUT} Max latency ms {red}({white}Default=5000{red}) ->{reset} ").strip()
            if lat_input:
                max_latency = int(lat_input)
                if max_latency < 1:
                    ErrorNumber()
        except ValueError:
            ErrorNumber()

    sources = {
        "http": [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
            "https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt",
            "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
            "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/Volodichev/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/RX4096/proxy-list/main/online/http.txt",
            "https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt",
            "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
            "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
            "https://raw.githubusercontent.com/yuceltoluyag/GoodProxy/main/raw.txt",
        ],
        "https": [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
            "https://raw.githubusercontent.com/Volodichev/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/RX4096/proxy-list/main/online/https.txt",
            "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTPS.txt",
            "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/https.txt",
            "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/https.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
        ],
        "socks4": [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
            "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS4.txt",
            "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt",
            "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/socks4.txt",
            "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks4_proxies.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
            "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
            "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt",
            "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
        ],
        "socks5": [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
            "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
            "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/socks5.txt",
            "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks5_proxies.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
            "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt",
            "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
            "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
            "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
            "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        ],
    }

    protocol_map = {
        "1": ["http"],
        "2": ["https"],
        "3": ["socks4"],
        "4": ["socks5"],
        "5": ["http", "https", "socks4", "socks5"],
    }

    selected_protocols = protocol_map[choice]

    print(f"{LOADING} Scraping proxies..", reset)

    proxies     = set()
    seen_hosts  = set()
    lock_scrape = threading.Lock()
    sem_scrape  = threading.Semaphore(20)

    def ScrapeSource(url, protocol):
        with sem_scrape:
            try:
                r = requests.get(url, timeout=10)
                if r.status_code != 200:
                    return
                for line in r.text.splitlines():
                    line  = line.strip()
                    parts = line.split(":")
                    if not line or len(parts) != 2:
                        continue
                    host = f"{parts[0]}:{parts[1]}"
                    with lock_scrape:
                        if host not in seen_hosts:
                            seen_hosts.add(host)
                            proxies.add(f"{protocol}://{host}")
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.ConnectionError:
                pass
            except Exception:
                pass

    scrape_threads = []
    for protocol in selected_protocols:
        for url in sources[protocol]:
            t = threading.Thread(target=ScrapeSource, args=(url, protocol), daemon=True)
            scrape_threads.append(t)
            t.start()

    for t in scrape_threads:
        t.join()

    if not proxies:
        print(f"{ERROR} No proxies found!", reset)
        Continue()
        Reset()

    proxies = list(proxies)
    print(f"{SUCCESS} Scraped:{red} {len(proxies)} unique proxies", reset)

    valid_proxies = []

    if do_check:
        print(f"{LOADING} Checking proxies {red}({white}max latency: {max_latency}ms{red}){white}..", reset)

        lock      = threading.Lock()
        semaphore = threading.Semaphore(50)

        def CheckProxy(proxy):
            with semaphore:
                try:
                    protocol = proxy.split("://")[0]
                    start    = time.time()
                    r        = requests.get(
                        "https://api.ipify.org?format=json",
                        proxies = {protocol: proxy},
                        timeout = max_latency / 1000
                    )
                    latency = round((time.time() - start) * 1000)
                    if r.status_code == 200 and latency <= max_latency:
                        ip = r.json().get("ip", "None")
                        with lock:
                            valid_proxies.append((proxy, latency))
                            print(f"{SUCCESS} Valid | {proxy:<52} | Ip:{red} {ip}{white} | Latency:{red} {latency}ms", reset)
                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.ProxyError:
                    pass
                except requests.exceptions.ConnectionError:
                    pass
                except Exception:
                    pass

        try:
            threads = [threading.Thread(target=CheckProxy, args=(p,), daemon=True) for p in proxies]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        except KeyboardInterrupt:
            pass

        valid_proxies.sort(key=lambda x: x[1])

        by_protocol = {}
        for proxy, latency in valid_proxies:
            proto = proxy.split("://")[0]
            by_protocol.setdefault(proto, []).append((proxy, latency))

        Scroll(f"\n{SUCCESS} Valid:{red} {len(valid_proxies)}", reset)

        for proto, items in by_protocol.items():
            print(f"{INFO} {proto.upper():<8}{red}:{white} {len(items)}", reset)

        proxies_to_save = [proxy for proxy, _ in valid_proxies]

    else:
        by_protocol = {}
        for proxy in proxies:
            proto = proxy.split("://")[0]
            by_protocol.setdefault(proto, []).append(proxy)

        proxies_to_save = proxies

    if not proxies_to_save:
        print(f"{ERROR} No proxies to save!", reset)
        Continue()
        Reset()

    output_dir = os.path.join(tool_path, "Programs", "Output", "ProxyScraper")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "proxies.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(proxies_to_save))

    if len(selected_protocols) > 1:
        for proto, items in by_protocol.items():
            proto_lines = [proxy for proxy, _ in items] if do_check else items
            proto_path  = os.path.join(output_dir, f"{proto}.txt")
            with open(proto_path, "w", encoding="utf-8") as f:
                f.write("\n".join(proto_lines))

    print(f"{SUCCESS} Saved:{red} {output_path}", reset)

    if platform_pc == "Windows":
        os.startfile(output_dir)
    else:
        subprocess.Popen(["xdg-open", output_dir])

    Continue()
    Reset()

except Exception as e:
    Error(e)