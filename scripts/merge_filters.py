#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Список всех источников (полный, как у вас)
URLS = [
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_1.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_2.txt",
    "https://filters.adtidy.org/extension/chromium/filters/1.txt",
    "https://filters.adtidy.org/extension/chromium/filters/2.txt",
    "https://filters.adtidy.org/extension/chromium/filters/4.txt",
    "https://filters.adtidy.org/extension/chromium/filters/6.txt",
    "https://filters.adtidy.org/extension/chromium/filters/8.txt",
    "https://filters.adtidy.org/extension/chromium/filters/9.txt",
    "https://filters.adtidy.org/extension/chromium/filters/11.txt",
    "https://filters.adtidy.org/extension/chromium/filters/13.txt",
    "https://filters.adtidy.org/extension/chromium/filters/16.txt",
    "https://filters.adtidy.org/extension/chromium/filters/17.txt",
    "https://filters.adtidy.org/extension/chromium/filters/19.txt",
    "https://filters.adtidy.org/extension/chromium/filters/20.txt",
    "https://filters.adtidy.org/extension/chromium/filters/21.txt",
    "https://filters.adtidy.org/extension/chromium/filters/23.txt",
    "https://filters.adtidy.org/extension/chromium/filters/103.txt",
    "https://filters.adtidy.org/extension/chromium/filters/105.txt",
    "https://filters.adtidy.org/extension/chromium/filters/108.txt",
    "https://filters.adtidy.org/extension/chromium/filters/109.txt",
    "https://filters.adtidy.org/extension/chromium/filters/110.txt",
    "https://filters.adtidy.org/extension/chromium/filters/111.txt",
    "https://filters.adtidy.org/extension/chromium/filters/120.txt",
    "https://filters.adtidy.org/extension/chromium/filters/202.txt",
    "https://filters.adtidy.org/extension/chromium/filters/203.txt",
    "https://filters.adtidy.org/extension/chromium/filters/208.txt",
    "https://filters.adtidy.org/extension/chromium/filters/216.txt",
    "https://filters.adtidy.org/extension/chromium/filters/217.txt",
    "https://filters.adtidy.org/extension/chromium/filters/218.txt",
    "https://filters.adtidy.org/extension/chromium/filters/227.txt",
    "https://filters.adtidy.org/extension/chromium/filters/233.txt",
    "https://filters.adtidy.org/extension/chromium/filters/238.txt",
    "https://filters.adtidy.org/extension/chromium/filters/243.txt",
    "https://filters.adtidy.org/extension/chromium/filters/249.txt",
    "https://filters.adtidy.org/extension/chromium/filters/252.txt",
    "https://filters.adtidy.org/extension/chromium/filters/253.txt",
    "https://filters.adtidy.org/extension/chromium/filters/254.txt",
    "https://filters.adtidy.org/extension/chromium/filters/255.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/pro.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/pro.plus.txt",
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_20_Annoyances_MobileApp/filter.txt",
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_19_Annoyances_Popups/filter.txt",
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_1_Russian/filter.txt",
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_11_Mobile/filter.txt",
    "https://ublockorigin.github.io/uAssets/filters/filters.txt",
    "https://ublockorigin.github.io/uAssets/filters/badware.txt",
    "https://ublockorigin.github.io/uAssets/filters/privacy.txt",
    "https://ublockorigin.github.io/uAssets/filters/quick-fixes.txt",
    "https://ublockorigin.github.io/uAssets/filters/unbreak.txt",
    "https://ublockorigin.github.io/uAssets/thirdparties/easylist.txt",
    "https://ublockorigin.github.io/uAssets/thirdparties/easyprivacy.txt",
    "https://malware-filter.gitlab.io/urlhaus-filter/urlhaus-filter-ag-online.txt",
    "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=adblockplus&showintro=1&mimetype=plaintext",
    "https://easylist.to/easylistgermany/easylistgermany.txt",
    "https://cdn.jsdelivr.net/gh/dimisa-RUAdList/RUAdListCDN@main/lists/ruadlist.ubo.min.txt",
    "https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-adguard.txt",
    "https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdns.txt",
    "https://raw.githubusercontent.com/8680/GOODBYEADS/master/data/rules/dns.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/ultimate.txt",
]

def fetch_list(url):
    try:
        logging.info(f"Загрузка: {url}")
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        lines = resp.text.splitlines()
        # Удаляем пустые строки и комментарии (строки, начинающиеся с ! или #)
        # Но не удаляем правила, которые могут содержать ! или # внутри (например, в исключениях)
        filtered = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('!', '#')):
                filtered.append(line)
        logging.info(f"  Загружено строк: {len(filtered)}")
        return set(filtered)
    except Exception as e:
        logging.error(f"Ошибка при загрузке {url}: {e}")
        return set()

def build_combined():
    all_rules = set()
    for url in URLS:
        rules = fetch_list(url)
        all_rules.update(rules)
        logging.info(f"Всего уникальных правил на данный момент: {len(all_rules)}")

    sorted_rules = sorted(all_rules)  # сортировка для стабильности
    out_path = Path("combined.txt")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("! Объединённый список блокировки для AdGuard Home\n")
        f.write(f"! Сгенерировано: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"! Количество записей: {len(sorted_rules)}\n")
        f.write("\n".join(sorted_rules))
    
    logging.info(f"Файл {out_path} создан, записей: {len(sorted_rules)}")

if __name__ == "__main__":
    build_combined()
