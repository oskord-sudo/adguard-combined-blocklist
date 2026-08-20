# Combined AdGuard Home Blocklist

<!-- START_META -->
**🗓 Дата генерации:** 2026-08-20 01:24:37  
**📊 Полный список (`combined.txt`):** 818970  
**📊 DNS-список (`combined-dns.txt`):** 608574
<!-- END_META -->

Автоматически собирает 50+ списков блокировки рекламы, трекеров и вредоносных сайтов и формирует **два** файла.

## 📥 Использование

### Для AdGuard Home (рекомендуется)

Только сетевые правила (без cosmetic / `$cookie` / `$csp` / scriptlet):

```text
https://raw.githubusercontent.com/oskord-sudo/adguard-combined-blocklist/main/combined-dns.txt
```

### Полный список (браузер + DNS)

Все типы правил, включая косметику и annoyances:

```text
https://raw.githubusercontent.com/oskord-sudo/adguard-combined-blocklist/main/combined.txt
```

## Что внутри

| Файл | Описание |
|------|----------|
| `combined.txt` | Полный merge всех источников, дедуп точных строк |
| `combined-dns.txt` | Только сетевые правила; языковые фильтры сохранены; дубли EasyList убраны |

### DNS-версия

- Оставляет языковые фильтры  
- Убирает дубли EasyList / EasyPrivacy / EasyList Germany (остаётся по одной полной копии)  
- Отфильтровывает cosmetic, `$cookie`, `$csp`, scriptlet  
- Оставляет правила вида `||domain^`, `@@||...`, hosts, простые домены  

## 🔄 Автообновление

Список обновляется каждые 12 часов (00:00 и 12:00 UTC) через GitHub Actions.
