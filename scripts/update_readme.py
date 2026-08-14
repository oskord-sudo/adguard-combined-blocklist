#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path


def _meta_from_file(path: Path) -> tuple[str, str]:
    if not path.exists():
        return "неизвестно", "неизвестно"
    with open(path, "r", encoding="utf-8") as f:
        lines = []
        for _ in range(5):
            try:
                lines.append(next(f).strip())
            except StopIteration:
                break
    date_str = "неизвестно"
    count_str = "неизвестно"
    for line in lines:
        if "Сгенерировано:" in line:
            date_str = line.split("Сгенерировано:", 1)[1].strip()
        if "Количество записей:" in line:
            count_str = line.split("Количество записей:", 1)[1].strip()
    return date_str, count_str


def update_readme() -> None:
    readme_path = Path("README.md")
    combined_path = Path("combined.txt")
    dns_path = Path("combined-dns.txt")

    date_full, count_full = _meta_from_file(combined_path)
    date_dns, count_dns = _meta_from_file(dns_path)

    new_meta_block = f"""<!-- START_META -->
**🗓 Дата генерации:** {date_full}  
**📊 Полный список (`combined.txt`):** {count_full}  
**📊 DNS-список (`combined-dns.txt`):** {count_dns}
<!-- END_META -->"""

    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
    else:
        content = ""

    pattern = r"<!-- START_META -->.*?<!-- END_META -->"
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, new_meta_block, content, flags=re.DOTALL)
    else:
        # Если маркеров нет — вставляем после заголовка или в начало
        if content.startswith("#"):
            parts = content.split("\n", 1)
            if len(parts) == 2:
                new_content = parts[0] + "\n\n" + new_meta_block + "\n" + parts[1]
            else:
                new_content = content + "\n\n" + new_meta_block + "\n"
        else:
            new_content = new_meta_block + "\n\n" + content

    readme_path.write_text(new_content, encoding="utf-8")
    print(f"README.md обновлён: full={count_full}, dns={count_dns}")


if __name__ == "__main__":
    update_readme()
