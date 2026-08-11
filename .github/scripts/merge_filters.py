#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        lines = set(resp.text.splitlines())
        logging.info(f"  Загружено строк: {len(lines)}")
        return lines
    except Exception as e:
        logging.error(f"Ошибка при загрузке {url}: {e}")
        return set()

def normalize_domain(line: str):
    line = line.strip()
    if not line:
        return None
    if '#' in line:
        line = line.split('#', 1)[0]
    if '!' in line:
        line = line.split('!', 1)[0]
    line = line.strip()
    if not line:
        return None
    if line.startswith('@@'):
        return None
    if '$' in line:
        line = line.split('$', 1)[0]
    host_match = re.match(r'^(\d+\.\d+\.\d+\.\d+|0\.0\.0\.0|127\.0\.0\.1)\s+(\S+)', line)
    if host_match:
        domain = host_match.group(2).strip()
        if domain and '.' in domain:
            return domain.lower()
    if line.startswith('||'):
        domain = line[2:]
        domain = re.split(r'[\^/$]', domain)[0]
        if domain and '.' in domain and not domain.startswith('*'):
            return domain.lower()
    if '.' in line and not any(c in line for c in ['/', ':', '?', '&', '=', ' ', '\t']):
        if not re.match(r'^\d+\.\d+\.\d+\.\d+$', line):
            return line.lower()
    return None

def build_combined():
    all_domains = set()
    for url in URLS:
        raw_lines = fetch_list(url)
        for line in raw_lines:
            domain = normalize_domain(line)
            if domain:
                all_domains.add(domain)
        logging.info(f"Всего уникальных доменов: {len(all_domains)}")
    sorted_domains = sorted(all_domains)
    formatted = [f"||{d}^" for d in sorted_domains]
    out_path = Path("combined.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(formatted))
    logging.info(f"Файл {out_path} создан, записей: {len(formatted)}")

if __name__ == "__main__":
    build_combined()
