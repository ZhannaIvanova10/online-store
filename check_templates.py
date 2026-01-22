import os
import sys
from pathlib import Path

print("=== ПОИСК ССЫЛОК В ШАБЛОНАХ ===")

# Ищем все HTML файлы
html_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'product_update' in content:
                print(f"\nФайл: {html_file}")
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if 'product_update' in line:
                        print(f"  Строка {i}: {line.strip()[:100]}...")
    except:
        pass

print(f"\n=== Найдено HTML файлов: {len(html_files)} ===")
