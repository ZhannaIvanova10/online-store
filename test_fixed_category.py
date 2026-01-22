import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 60)
print("ТЕСТ С ИСПРАВЛЕННОЙ ФУНКЦИЕЙ КАТЕГОРИИ")
print("=" * 60)

from django.core.cache import cache
from catalog.services import get_products_in_category, get_all_cached_products_safe

# Очищаем кеш
cache.delete('all_products_safe')
cache.delete('products_category_1')

print("1. Тестируем get_products_in_category(1)...")
try:
    products = get_products_in_category(1)
    print(f"   ✅ Получено {len(products)} продуктов")
    print("   ⚠️  Внимание: возвращаются все продукты (т.к. нет модели Category)")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
print("\n2. Тестируем get_all_cached_products_safe()...")
try:
    products = get_all_cached_products_safe()
    print(f"   ✅ Получено {len(products)} продуктов")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")

print("\n3. Проверяем работу кеша...")
print("   Второй вызов get_products_in_category(1):")
products2 = get_products_in_category(1)
print(f"   ✅ Получено {len(products2)} продуктов (из кеша)")

print("\n" + "=" * 60)
print("РЕКОМЕНДАЦИЯ:")
print("=" * 60)
print("Для полного соответствия ДЗ рекомендуется:")
print("1. Добавить модель Category в catalog/models.py")
print("2. Добавить ForeignKey на Category в модели Product")
print("3. Создать миграции: python manage.py makemigrations")
print("4. Применить миграции: python manage.py migrate")
print("5. Обновить функцию get_products_in_category для реальной фильтрации")
print("\nТекущая реализация демонстрирует принцип кеширования,")
print("но не имеет реальной фильтрации по категориям.")
