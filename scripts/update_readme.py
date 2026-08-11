#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path
from datetime import datetime

def update_readme():
    readme_path = Path("README.md")
    combined_path = Path("combined.txt")
    
    if not combined_path.exists():
        print("Файл combined.txt не найден, пропускаем обновление README")
        return
    
    # Читаем первые 3 строки из combined.txt
    with open(combined_path, "r", encoding="utf-8") as f:
        lines = [next(f).strip() for _ in range(3)]
    
    # Извлекаем дату и количество записей
    date_line = lines[1] if len(lines) > 1 else "! Сгенерировано: неизвестно"
    count_line = lines[2] if len(lines) > 2 else "! Количество записей: неизвестно"
    
    date_str = date_line.replace("! Сгенерировано: ", "").strip()
    count_str = count_line.replace("! Количество записей: ", "").strip()
    
    # Формируем новый блок для вставки
    new_meta_block = f"""<!-- START_META -->
**🗓 Дата генерации:** {date_str}  
**📊 Количество записей:** {count_str}
<!-- END_META -->"""
    
    # Читаем текущий README.md
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = ""
    
    # Заменяем блок между маркерами или создаём новый
    pattern = r"<!-- START_META -->.*?<!-- END_META -->"
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, new_meta_block, content, flags=re.DOTALL)
    else:
        # Если маркеров нет, добавляем блок в начало
        new_content = new_meta_block + "\n\n" + content
    
    # Записываем обновлённый README.md
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"README.md обновлён: {date_str}, {count_str}")

if __name__ == "__main__":
    update_readme()
