import os
import sys
import re

print("="*80)
print("ФИНАЛЬНАЯ ПРОВЕРКА ВСЕХ КРИТЕРИЕВ ДЗ 5 (ИСПРАВЛЕННАЯ)")
print("="*80)

def check_urls_file(filename):
    """Проверяет, что все URL в файле заканчиваются на /"""
    print(f"\n{filename}:")
    
    if not os.path.exists(filename):
        print(f"   ❌ Файл не существует")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ищем ВСЕ path() вызовы, включая те, что могут быть на нескольких строках
    # Более надежный regex
    path_pattern = r"path\s*\(\s*'([^']*)'"
    paths = re.findall(path_pattern, content)
    all_ok = True
    for path_url in paths:
        # Проверяем: пустой путь (для главной) или путь заканчивается на /
        if path_url == '' or path_url.endswith('/'):
            print(f"   ✅ path('{path_url}'")
        else:
            print(f"   ❌ path('{path_url}' - не заканчивается на /")
            all_ok = False
    
    return all_ok

# Проверяем URL
print("\n2. ПРОВЕРКА URL (все должны заканчиваться на /):")
blog_ok = check_urls_file('blog/urls.py')
catalog_ok = check_urls_file('catalog/urls.py')

print("\n" + "="*80)
print("ИТОГ ПРОВЕРКИ URL:")
print("="*80)
print(f"Blog URLs: {'✅ ВСЕ ОК' if blog_ok else '❌ ЕСТЬ ПРОБЛЕМЫ'}")
print(f"Catalog URLs: {'✅ ВСЕ ОК' if catalog_ok else '❌ ЕСТЬ ПРОБЛЕМЫ'}")
