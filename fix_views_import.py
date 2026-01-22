import re

with open('catalog/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Заменяем импорт старой функции на новую
if 'from .services import get_all_cached_products' in content:
    content = content.replace(
        'from .services import get_all_cached_products',
        'from .services import get_all_cached_products_safe as get_all_cached_products'
    )
    print("✅ Импорт обновлен: get_all_cached_products_safe as get_all_cached_products")
else:
    # Проверяем есть ли импорт в другом формате
    if 'import get_all_cached_products' in content:
        # Найдем и заменим строку импорта
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'get_all_cached_products' in line and 'import' in line:
                if 'from .services import' in line:
                    lines[i] = 'from .services import get_all_cached_products_safe as get_all_cached_products'
                elif 'import' in line:
                    # Просто добавляем новую строку
                    lines[i] = 'from .services import get_all_cached_products_safe as get_all_cached_products'
                print(f"✅ Строка {i+1} обновлена")
                break
        content = '\n'.join(lines)
    else:
        print("⚠️  Импорт get_all_cached_products не найден, добавляем...")
        # Добавляем импорт после других импортов
        import_match = re.search(r'^(from .*?\n|import .*?\n)+', content, re.MULTILINE)
        if import_match:
            imports_end = import_match.end()
            content = content[:imports_end] + 'from .services import get_all_cached_products_safe as get_all_cached_products\n' + content[imports_end:]
            print("✅ Импорт добавлен")

# Сохраняем исправленный файл
with open('catalog/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ views.py обновлен")
