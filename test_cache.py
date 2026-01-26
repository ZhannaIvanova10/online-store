#!/usr/bin/env python
"""
Тестирование работы кэширования Redis
"""
import os
import sys
import django
import time
# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.cache import cache
from catalog.models import Product

def test_redis_connection():
    """Тестирует подключение к Redis"""
    print("=== ТЕСТ ПОДКЛЮЧЕНИЯ К REDIS ===")
    
    try:
        # Пробуем записать и прочитать тестовое значение
        cache.set('test_key', 'test_value', 30)
        value = cache.get('test_key')
        
        if value == 'test_value':
            print("✅ Redis подключен и работает!")
            print(f"   Получено значение: {value}")
            
            # Тестируем производительность
            start = time.time()
            for i in range(100):
                cache.set(f'key_{i}', f'value_{i}', 10)
            set_time = time.time() - start
            
            start = time.time()
            for i in range(100):
                cache.get(f'key_{i}')
            get_time = time.time() - start
            print(f"   Время записи 100 ключей: {set_time:.4f}с")
            print(f"   Время чтения 100 ключей: {get_time:.4f}с")
            return True
        else:
            print("❌ Redis не вернул ожидаемое значение")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения к Redis: {e}")
        print("\nСОВЕТЫ ПО РЕШЕНИЮ:")
        print("1. Убедитесь, что Redis запущен на localhost:6379")
        print("2. Для Windows скачайте: https://github.com/microsoftarchive/redis/releases")
        print("3. Или используйте Docker: docker run -d -p 6379:6379 redis")
        return False

def test_product_caching():
    """Тестирует кэширование товаров"""
    print("\n=== ТЕСТ КЭШИРОВАНИЯ ТОВАРОВ ===")
    
    # Получаем первый товар
    product = Product.objects.first()
    if not product:
        print("❌ Нет товаров в базе для тестирования")
        return
    
    print(f"Тестируем товар: {product.name}")
    
    # Измеряем время без кэша
    print("\n1. Запрос БЕЗ кэша:")
    start = time.time()
    for _ in range(10):
        Product.objects.get(id=product.id)
    db_time = time.time() - start
    print(f"   Время 10 запросов к БД: {db_time:.4f}с")
    print(f"   Среднее время: {db_time/10:.4f}с")
    # Теперь с кэшем (имитируем)
    print("\n2. Запрос С кэшем (имитация):")
    
    # Сохраняем в кэш
    cache_key = f'product_{product.id}_detail'
    cache.set(cache_key, {
        'name': product.name,
        'description': product.description,
        'price': float(product.price)
    }, 300)
    
    start = time.time()
    for _ in range(10):
        cached_data = cache.get(cache_key)
    cache_time = time.time() - start
    
    print(f"   Время 10 запросов к кэшу: {cache_time:.4f}с")
    print(f"   Среднее время: {cache_time/10:.4f}с")
    print(f"   Ускорение: {db_time/cache_time:.1f}x")
    
    if cached_data:
        print(f"   Данные из кэша: {cached_data['name']}")

def clear_all_cache():
    """Очищает весь кэш"""
    print("\n=== ОЧИСТКА КЭША ===")
    cache.clear()
    print("✅ Весь кэш очищен")

if __name__ == '__main__':
    print("ДОМАШНЯЯ РАБОТА: КЭШИРОВАНИЕ С REDIS")
    print("=" * 50)

    if test_redis_connection():
        test_product_caching()
        clear_all_cache()
        
        print("\n✅ Все тесты завершены!")
        print("\nДЛЯ ДАЛЬНЕЙШЕЙ РАБОТЫ:")
        print("1. Запустите Redis сервер")
        print("2. Запустите Django: py manage.py runserver")
        print("3. Откройте http://127.0.0.1:8000/")
        print("4. Первая загрузка будет медленнее (кэш пуст)")
        print("5. Повторная загрузка будет быстрее (данные из кэша)")
    else:
        print("\n⚠️  Redis не подключен, используем локальный кэш")
        print("Замените в settings.py CACHES на LocMemCache для тестирования")
