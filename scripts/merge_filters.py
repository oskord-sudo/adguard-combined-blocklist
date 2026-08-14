#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Собирает два списка:
  - combined.txt      — полный (все типы правил)
  - combined-dns.txt  — только сетевые правила для AdGuard Home
"""

import re
import requests
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ============================================================
# Все источники (без урезания) + AdGuard Russian (uBlock path)
# ============================================================
URLS = [
    # Hostlists / DNS
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_1.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_2.txt",

    # AdGuard filters
    "https://filters.adtidy.org/extension/chromium/filters/1.txt",   # Russian (chromium)
    "https://filters.adtidy.org/extension/ublock/filters/1.txt",     # Russian (uBlock) — добавлено
    "https://filters.adtidy.org/extension/chromium/filters/2.txt",   # Base
    "https://filters.adtidy.org/extension/chromium/filters/4.txt",   # Social
    "https://filters.adtidy.org/extension/chromium/filters/6.txt",   # German
    "https://filters.adtidy.org/extension/chromium/filters/8.txt",   # Dutch
    "https://filters.adtidy.org/extension/chromium/filters/9.txt",   # Spanish/Portuguese
    "https://filters.adtidy.org/extension/chromium/filters/11.txt",  # Mobile Ads
    "https://filters.adtidy.org/extension/chromium/filters/13.txt",  # Turkish
    "https://filters.adtidy.org/extension/chromium/filters/16.txt",  # French
    "https://filters.adtidy.org/extension/chromium/filters/17.txt",  # URL Tracking
    "https://filters.adtidy.org/extension/chromium/filters/19.txt",  # Cookie Notices
    "https://filters.adtidy.org/extension/chromium/filters/20.txt",  # Popups
    "https://filters.adtidy.org/extension/chromium/filters/21.txt",  # Mobile App Banners
    "https://filters.adtidy.org/extension/chromium/filters/23.txt",  # Other Annoyances
    "https://filters.adtidy.org/extension/chromium/filters/103.txt", # EasyList (AdGuard)
    "https://filters.adtidy.org/extension/chromium/filters/105.txt", # EasyList Germany (AdGuard)
    "https://filters.adtidy.org/extension/chromium/filters/108.txt", # EasyList Italy
    "https://filters.adtidy.org/extension/chromium/filters/109.txt", # EasyList Lithuania
    "https://filters.adtidy.org/extension/chromium/filters/110.txt", # Latvian
    "https://filters.adtidy.org/extension/chromium/filters/111.txt", # Liste AR
    "https://filters.adtidy.org/extension/chromium/filters/120.txt", # Chinese
    "https://filters.adtidy.org/extension/chromium/filters/202.txt", # EasyPrivacy (AdGuard)
    "https://filters.adtidy.org/extension/chromium/filters/203.txt", # Fanboy's Annoyances
    "https://filters.adtidy.org/extension/chromium/filters/208.txt", # Online Malicious
    "https://filters.adtidy.org/extension/chromium/filters/216.txt", # RU AdList: Counters
    "https://filters.adtidy.org/extension/chromium/filters/217.txt", # ABPVN
    "https://filters.adtidy.org/extension/chromium/filters/218.txt", # Polish
    "https://filters.adtidy.org/extension/chromium/filters/227.txt", # List-KR
    "https://filters.adtidy.org/extension/chromium/filters/233.txt", # EasyList Cookie
    "https://filters.adtidy.org/extension/chromium/filters/238.txt", # Swedish
    "https://filters.adtidy.org/extension/chromium/filters/243.txt", # EasyList Polish
    "https://filters.adtidy.org/extension/chromium/filters/249.txt", # Nordic
    "https://filters.adtidy.org/extension/chromium/filters/252.txt", # Legitimate URL Shortener
    "https://filters.adtidy.org/extension/chromium/filters/253.txt", # Serbo-Croatian
    "https://filters.adtidy.org/extension/chromium/filters/254.txt", # Indian
    "https://filters.adtidy.org/extension/chromium/filters/255.txt", # Macedonian

    # HaGeZi
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/pro.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/pro.plus.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/ultimate.txt",

    # Прочие AdGuard registry
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_20_Annoyances_MobileApp/filter.txt",
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_19_Annoyances_Popups/filter.txt",
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_1_Russian/filter.txt",
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_11_Mobile/filter.txt",

    # uBlock
    "https://ublockorigin.github.io/uAssets/filters/filters.txt",
    "https://ublockorigin.github.io/uAssets/filters/badware.txt",
    "https://ublockorigin.github.io/uAssets/filters/privacy.txt",
    "https://ublockorigin.github.io/uAssets/filters/quick-fixes.txt",
    "https://ublockorigin.github.io/uAssets/filters/unbreak.txt",
    "https://ublockorigin.github.io/uAssets/thirdparties/easylist.txt",
    "https://ublockorigin.github.io/uAssets/thirdparties/easyprivacy.txt",

    # Остальное
    "https://malware-filter.gitlab.io/urlhaus-filter/urlhaus-filter-ag-online.txt",
    "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=adblockplus&showintro=1&mimetype=plaintext",
    "https://easylist.to/easylistgermany/easylistgermany.txt",
    "https://cdn.jsdelivr.net/gh/dimisa-RUAdList/RUAdListCDN@main/lists/ruadlist.ubo.min.txt",
    "https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-adguard.txt",
    "https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdns.txt",
    "https://raw.githubusercontent.com/8680/GOODBYEADS/master/data/rules/dns.txt",
]

# Дубли EasyList / EasyPrivacy / Germany — в DNS-версии пропускаем (оставляем uBO + easylist.to)
EASYLIST_DUPLICATE_URLS = {
    "https://filters.adtidy.org/extension/chromium/filters/103.txt",  # EasyList (AdGuard)
    "https://filters.adtidy.org/extension/chromium/filters/202.txt",  # EasyPrivacy (AdGuard)
    "https://filters.adtidy.org/extension/chromium/filters/105.txt",  # EasyList Germany (AdGuard)
}

COSMETIC_RE = re.compile(r"^#{1,2}|^#@#|^#\?#|^#\$#")
SCRIPTLET_RE = re.compile(r"\+js\(|scriptlet", re.I)
COOKIE_CSP_RE = re.compile(r"\$(?:cookie|csp)(?:=|,|$)", re.I)


def fetch_list(url: str) -> set:
    try:
        logging.info("Загрузка: %s", url)
        resp = requests.get(url, timeout=90)
        resp.raise_for_status()
        result = set()
        for line in resp.text.splitlines():
            line = line.strip()
            if not line:
                continue
            # Комментарии фильтров
            if line.startswith("!"):
                continue
            # Обычные #-комментарии hosts, но не cosmetic (## / #@# / #?# / #$#)
            if line.startswith("#") and not (
                line.startswith("##")
                or line.startswith("#@#")
                or line.startswith("#?#")
                or line.startswith("#$#")
            ):
                continue
            result.add(line)
        logging.info("  Загружено правил: %s", len(result))
        return result
    except Exception as e:
        logging.error("Ошибка %s: %s", url, e)
        return set()


def is_network_rule(rule: str) -> bool:
    """Правила, полезные для AdGuard Home (DNS / сеть)."""
    if not rule or rule.startswith("!"):
        return False

    if COSMETIC_RE.search(rule):
        return False
    if SCRIPTLET_RE.search(rule):
        return False
    if COOKIE_CSP_RE.search(rule):
        return False

    # hosts-формат
    if re.match(r"^(0\.0\.0\.0|127\.0\.0\.1|::)\s+\S+", rule):
        return True

    # простой домен
    if re.match(
        r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9\-]*[a-z0-9])?)+$",
        rule,
        re.I,
    ):
        return True

    # Adblock network / exception / regex
    if rule.startswith("||") or rule.startswith("@@") or rule.startswith("/"):
        return True

    return False


def write_list(path: Path, rules: set, title: str) -> None:
    sorted_rules = sorted(rules)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"! {title}\n")
        f.write(f"! Сгенерировано: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"! Количество записей: {len(sorted_rules)}\n")
        f.write("\n".join(sorted_rules))
        f.write("\n")
    logging.info("Создан %s — %s записей", path, len(sorted_rules))


def build() -> None:
    full_rules: set = set()
    dns_rules: set = set()

    for url in URLS:
        rules = fetch_list(url)
        full_rules.update(rules)

        if url in EASYLIST_DUPLICATE_URLS:
            logging.info("  [DNS] пропуск дубля EasyList: %s", url)
            continue

        for r in rules:
            if is_network_rule(r):
                dns_rules.add(r)

        logging.info("  Full: %s | DNS: %s", len(full_rules), len(dns_rules))

    write_list(
        Path("combined.txt"),
        full_rules,
        "Объединённый ПОЛНЫЙ список (браузер + DNS, все типы правил)",
    )
    write_list(
        Path("combined-dns.txt"),
        dns_rules,
        "Объединённый DNS-список для AdGuard Home (только сетевые правила)",
    )


if __name__ == "__main__":
    build()
