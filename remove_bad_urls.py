import os
import re

def clean_template(filepath):
    print(f"\nОбработка: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Удаляем ВСЕ теги {% url ... %} с problem маршрутами
    bad_patterns = [
        r'\{%\s*url\s+[\'"][^\'"]*product_list[^\'"]*[\'"]\s*%\}',
        r'\{%\s*url\s+[\'"][^\'"]*product_delete[^\'"]*[\'"]\s*%\}',
        r'\{%\s*url\s+[\'"][^\'"]*product_edit[^\'"]*[\'"]\s*%\}',
        r'\{%\s*url\s+[\'"][^\'"]*product_update[^\'"]*[\'"]\s*%\}',
    ]
    
    for pattern in bad_patterns:
        matches = re.findall(pattern, content)
        if matches:
            print(f"  Найдены проблемные ссылки: {matches}")
    
    # Заменяем на простые ссылки
    content = re.sub(
        r'\{%\s*url\s+[\'"][^\'"]*product_list[^\'"]*[\'"]\s*%\}',
        '/',
        content
    )
    
    content = re.sub(
        r'\{%\s*url\s+[\'"][^\'"]*product_delete[^\'"]*[\'"]\s*%\}',
        '/',
        content
    )
    
    content = re.sub(
        r'\{%\s*url\s+[\'"][^\'"]*product_edit[^\'"]*[\'"]\s*%\}',
        '/',
        content
    )
    
    content = re.sub(
        r'\{%\s*url\s+[\'"][^\'"]*product_update[^\'"]*[\'"]\s*%\}',
        '/',
        content
    )
    # Также заменяем строковые упоминания
    content = re.sub(r"'product_list'", "'catalog:home'", content)
    content = re.sub(r'"product_list"', '"catalog:home"', content)
    content = re.sub(r"'product_delete'", "''", content)
    content = re.sub(r'"product_delete"', '""', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Исправлен")
        return True
    else:
        print(f"  ✅ Ошибок не найдено")
        return False

# Обрабатываем все HTML файлы
template_dir = 'catalog/templates'
if os.path.exists(template_dir):
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                clean_template(os.path.join(root, file))
else:
    print(f"❌ Директория {template_dir} не найдена")
