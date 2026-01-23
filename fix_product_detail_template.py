import os

template_path = 'catalog/templates/catalog/product_detail.html'
if os.path.exists(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем на наличие 'product_list'
    if 'product_list' in content:
        print("✅ Найдены упоминания 'product_list' в product_detail.html")
        
        import re
        # Заменяем все варианты
        content = re.sub(
            r'\{%\s*url\s+[\'"]product_list[\'"]\s*%\}',
            "{% url 'catalog:home' %}",
            content
        )
        
        content = content.replace("'product_list'", "'catalog:home'")
        content = content.replace('"product_list"', '"catalog:home"')
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Исправления применены")
    else:
        print("✅ Упоминаний 'product_list' не найдено")
else:
    print("❌ Файл product_detail.html не найден")
