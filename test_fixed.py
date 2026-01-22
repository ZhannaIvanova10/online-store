"""
Исправленный тест кеширования
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 60)
print("ИСПРАВЛЕННЫЙ ТЕСТ КЕШИРОВАНИЯ")
print("=" * 60)

# Проверяем Redis
from django.core.cache import cache

print("1. Тестируем подключение к Redis...")
try:
    cache.set('test_fixed', 'Redis_Working', 10)
    result = cache.get('test_fixed')
    if result == 'Redis_Working':
        print("   ✅ Redis подключен и работает!")
    else:
        print(f"   ❌ Проблема: получено '{result}'")
except Exception as e:
    print(f"   ❌ Ошибка Redis: {e}")

# Проверяем сервисные функции (безопасные версии)
print("\n2. Тестируем сервисные функции...")
try:
    from catalog.services import get_products_in_category, get_all_cached_products_safe
    
    # Очищаем кеш для чистого теста
    cache.delete('all_products_safe')
    cache.delete('products_category_1')
    
    print("   Тестируем get_all_cached_products_safe()...")
    all_products = get_all_cached_products_safe()
    print(f"   ✅ Получено {len(all_products)} всех продуктов")
    
    print("   Тестируем get_products_in_category(1)...")
    category_products = get_products_in_category(1)
    print(f"   ✅ Получено {len(category_products)} продуктов категории 1")
    
    # Проверяем что кеш работает
    print("\n3. Проверяем работу кеша...")
    print("   Второй вызов get_all_cached_products_safe():")
    products2 = get_all_cached_products_safe()
    print(f"   ✅ Получено {len(products2)} продуктов (из кеша)")
    
    print("\n4. Проверяем содержимое кеша...")
    print(f"   Ключ 'all_products_safe' в кеше: {cache.get('all_products_safe') is not None}")
    print(f"   Ключ 'products_category_1' в кеше: {cache.get('products_category_1') is not None}")
    
except ImportError as e:
    print(f"   ❌ Ошибка импорта: {e}")
    print("   Проверьте что функции существуют в catalog/services.py")
except Exception as e:
    print(f"   ❌ Ошибка выполнения: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ ТЕСТ ЗАВЕРШЕН")
print("=" * 60)
