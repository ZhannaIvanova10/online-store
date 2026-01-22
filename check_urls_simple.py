from django.urls import reverse, resolve
from django.test import RequestFactory

# Проверяем основные URL
url_patterns = [
    ('catalog:product_list', [], 'Список продуктов'),
    ('catalog:product_create', [], 'Создание продукта'),
    ('catalog:product_detail', [1], 'Детали продукта (ID=1)'),
    ('catalog:product_edit', [1], 'Редактирование продукта (ID=1)'),
    ('catalog:product_delete', [1], 'Удаление продукта (ID=1)'),
    ('catalog:unpublish_product', [1], 'Отмена публикации (ID=1)'),
]

print("Проверка URL:")
print("="*60)

for url_name, args, description in url_patterns:
    try:
        url = reverse(url_name, args=args)
        print(f"✅ {description}")
        print(f"   Имя: {url_name}")
        print(f"   URL: {url}")
        print()
    except Exception as e:
        print(f"❌ Ошибка: {description}")
        print(f"   Имя: {url_name}")
        print(f"   Ошибка: {e}")
        print()

print("="*60)
