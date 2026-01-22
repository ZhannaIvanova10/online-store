"""
Исправление фильтрации по категории
"""
import re

with open('catalog/services.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Ищем функцию get_products_in_category
pattern = r'def get_products_in_category\(category_id\):(.*?)(?=\n\s*def|\Z)'
match = re.search(pattern, content, re.DOTALL)

if match:
    func_text = match.group(0)
    print("Найдена функция get_products_in_category")
    
    # Проверяем что фильтр использует правильное имя поля
    if "filter(category_id=category_id)" in func_text:
        print("✅ Фильтр использует category_id - правильно")
    elif "filter(category=category_id)" in func_text:
        print("⚠️  Фильтр использует category, меняем на category_id...")
        content = content.replace("filter(category=category_id)", "filter(category_id=category_id)")

        with open('catalog/services.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Фильтр исправлен")
    else:
        print("❌ Не могу найти фильтр в функции")
        
        # Покажем функцию для диагностики
        print("\nТекст функции:")
        print(func_text[:500])
else:
    print("❌ Функция get_products_in_category не найдена")
