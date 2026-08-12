#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path

def is_valid_domain(rule):
    """
    Проверяет, что правило выглядит как корректный домен с префиксом || и суффиксом ^
    Пример: ||example.com^
    """
    if not rule.startswith('||') or not rule.endswith('^'):
        return False
    domain = rule[2:-1]  # убираем || и ^
    # Домен должен содержать только буквы, цифры, точки и дефисы
    if not re.match(r'^[a-z0-9]([a-z0-9\-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9\-]*[a-z0-9])?)*$', domain):
        return False
    # Не должен быть IP-адресом
    if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain):
        return False
    return True

def validate():
    combined_path = Path("combined.txt")
    if not combined_path.exists():
        print("Файл combined.txt не найден")
        return

    suspicious = []
    with open(combined_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            # Пропускаем комментарии (начинаются с !)
            if line.startswith('!'):
                continue
            if not line:
                continue
            if not is_valid_domain(line):
                suspicious.append((line_num, line))

    if suspicious:
        print(f"Найдено {len(suspicious)} подозрительных записей:")
        for num, line in suspicious[:20]:  # покажем первые 20
            print(f"  Строка {num}: {line}")
        if len(suspicious) > 20:
            print(f"  ... и ещё {len(suspicious) - 20} записей.")
        # Сохраняем полный отчёт в файл
        report_path = Path("suspicious.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"Всего подозрительных записей: {len(suspicious)}\n\n")
            for num, line in suspicious:
                f.write(f"Строка {num}: {line}\n")
        print(f"Полный отчёт сохранён в {report_path}")
    else:
        print("Все записи выглядят корректно.")

if __name__ == "__main__":
    validate()
