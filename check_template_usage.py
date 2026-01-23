import os

# Проверяем содержимое нашего основного шаблона
main_template = 'catalog/templates/catalog/category_products.html'
if os.path.exists(main_template):
    print("📄 СОДЕРЖИМОЕ ОСНОВНОГО ШАБЛОНА category_products.html:")
    print("=" * 60)
    
    with open(main_template, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Показываем первые 20 строк
    lines = content.split('\n')[:20]
    for i, line in enumerate(lines, 1):
        print(f"{i:3}: {line}")
    
    print("=" * 60)
    
    # Проверяем на наличие проблем
    if 'product_list' in content:
        print("🚨 ОШИБКА: В основном шаблоне все еще есть 'product_list'!")
        print("Исправляю...")
        # Заменяем простым способом
        content = content.replace("'product_list'", "'catalog:home'")
        content = content.replace('"product_list"', '"catalog:home"')
        content = content.replace('{% url "product_list" %}', '/')
        content = content.replace("{% url 'product_list' %}", '/')
        
        with open(main_template, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Исправлено")
    else:
        print("✅ В основном шаблоне нет 'product_list'")
    
    # Проверяем другие проблемные ссылки
    problematic = ['product_delete', 'product_edit', 'product_update', 'product_create']
    for problem in problematic:
        if problem in content:
            print(f"⚠️  Найден '{problem}' в шаблоне")
            
            # Заменяем на безопасные значения
            content = content.replace(f"'catalog:{problem}'", "''")
            content = content.replace(f'"catalog:{problem}"', '""')
            # Исправляем синтаксис для тегов url
            content = content.replace('{% url "catalog:' + problem + '" %}', '/')
            content = content.replace("{% url 'catalog:" + problem + "' %}", '/')
            
            with open(main_template, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ '{problem}' заменен")
else:
    print("❌ Основной шаблон не найден")
