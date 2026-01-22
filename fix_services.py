"""
Исправление функции get_all_cached_products
"""
import re

with open('catalog/services.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Ищем функцию get_all_cached_products
pattern = r'(def get_all_cached_products\(\):.*?)(\n\s*def|\Z)'
match = re.search(pattern, content, re.DOTALL)

if match:
    func_text = match.group(1)
    print("Найдена функция get_all_cached_products")
    
    # Проверяем содержит ли она select_related('category')
    if "select_related('category')" in func_text:
        print("Исправляем select_related('category')...")
        
        # Заменяем на безопасную версию
        new_func_text = func_text.replace(
            ".select_related('category')", 
            ""
        )
        # Обновляем content
        content = content.replace(func_text, new_func_text)
        
        # Сохраняем исправленный файл
        with open('catalog/services.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Функция исправлена (удален select_related)")
    else:
        print("✅ select_related не найден, все OK")
else:
    print("❌ Функция get_all_cached_products не найдена")
