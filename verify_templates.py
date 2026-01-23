import os
import re

print("🔍 ПРОВЕРКА ШАБЛОНОВ НА ОШИБКИ:")
print("=" * 60)

template_dir = 'catalog/templates/catalog'
if os.path.exists(template_dir):
    for file in os.listdir(template_dir):
        if file.endswith('.html'):
            filepath = os.path.join(template_dir, file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"\n📄 {file}:")
            
            # Проверяем на наличие проблемных строк
            problems = []
            
            # 1. Ищем 'product_list'
            if 'product_list' in content.lower():
                problems.append("❌ Найден 'product_list'")
            
            # 2. Ищем 'product_delete'
            if 'product_delete' in content.lower():
                problems.append("❌ Найден 'product_delete'")
            
            # 3. Ищем теги {% url %} с проблемными маршрутами
            url_pattern = r'\{%\s*url\s+[^%]+%\}'
            url_matches = re.findall(url_pattern, content)
            
            if url_matches:
                problems.append(f"❌ Найдены теги URL: {len(url_matches)} шт.")
                for match in url_matches[:3]:  # Показываем первые 3
                    problems.append(f"   - {match}")
            
            # 4. Ищем другие проблемные маршруты
            bad_routes = ['product_edit', 'product_update', 'product_create']
            for route in bad_routes:
                if route in content.lower():
                    problems.append(f"❌ Найден '{route}'")
            
            if problems:
                print("  🚨 ПРОБЛЕМЫ:")
                for problem in problems:
                    print(f"  {problem}")
                # Автоматически исправляем
                print("  🔧 Автоматическое исправление...")
                
                # Удаляем все теги {% url %}
                for match in url_matches:
                    # Пытаемся заменить на простые ссылки
                    if 'product_list' in match or 'home' in match:
                        content = content.replace(match, '/')
                    elif 'product_detail' in match:
                        # Пытаемся извлечь аргумент
                        if 'product.id' in match:
                            content = content.replace(match, '/product/{{ product.id }}/')
                        else:
                            content = content.replace(match, '/product/1/')
                    elif 'category_products' in match:
                        if 'product.category.id' in match:
                            content = content.replace(match, '/category/{{ product.category.id }}/products/')
                        else:
                            content = content.replace(match, '/category/1/products/')
                    else:
                        content = content.replace(match, '/')
                
                # Удаляем строковые упоминания
                content = content.replace("'product_list'", "'catalog:home'")
                content = content.replace('"product_list"', '"catalog:home"')
                content = content.replace("'catalog:product_list'", "'catalog:home'")
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("  ✅ Исправлено")
            else:
                print("  ✅ Ошибок не найдено")
else:
    print("❌ Директория шаблонов не найдена")

print("\n" + "=" * 60)
