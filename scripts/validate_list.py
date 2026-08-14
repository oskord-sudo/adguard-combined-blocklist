#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Проверяет combined-dns.txt: ищет строки, которые не похожи на сетевые правила.
Полный combined.txt намеренно содержит cosmetic/cookie/csp — его не валидируем строго.
"""

import re
from pathlib import Path


def is_network_looking(rule: str) -> bool:
    if not rule or rule.startswith("!"):
        return True  # комментарии ок
    if rule.startswith("##") or rule.startswith("#@#") or rule.startswith("#?#") or rule.startswith("#$#"):
        return False
    if "+js(" in rule or "scriptlet" in rule.lower():
        return False
    if re.search(r"\$(?:cookie|csp)(?:=|,|$)", rule, re.I):
        return False
    if re.match(r"^(0\.0\.0\.0|127\.0\.0\.1|::)\s+\S+", rule):
        return True
    if rule.startswith("||") or rule.startswith("@@") or rule.startswith("/"):
        return True
    if re.match(
        r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9\-]*[a-z0-9])?)+$",
        rule,
        re.I,
    ):
        return True
    return False


def validate() -> None:
    dns_path = Path("combined-dns.txt")
    if not dns_path.exists():
        print("Файл combined-dns.txt не найден")
        return

    suspicious = []
    with open(dns_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("!"):
                continue
            if not is_network_looking(line):
                suspicious.append((line_num, line))

    if suspicious:
        print(f"Найдено {len(suspicious)} подозрительных записей в combined-dns.txt:")
        for num, line in suspicious[:20]:
            print(f"  Строка {num}: {line[:120]}")
        if len(suspicious) > 20:
            print(f"  ... и ещё {len(suspicious) - 20} записей.")
        report_path = Path("suspicious.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"Всего подозрительных записей в combined-dns.txt: {len(suspicious)}\n\n")
            for num, line in suspicious:
                f.write(f"Строка {num}: {line}\n")
        print(f"Полный отчёт: {report_path}")
    else:
        print("combined-dns.txt: все записи выглядят как сетевые правила.")
        Path("suspicious.txt").write_text(
            "Подозрительных записей нет.\n", encoding="utf-8"
        )


if __name__ == "__main__":
    validate()
