#!/usr/bin/env python
"""
Простой тест Django конфигурации
"""
import os
import sys

print("=== ТЕСТ DJANGO КОНФИГУРАЦИИ ===")

# Добавляем текущую директорию в путь
sys.path.append('.')

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    import django
    django.setup()
    print("✓ Django настроен")
    
    # Проверяем приложения
    from django.apps import apps
    print("\nЗарегистрированные приложения:")
    for app in apps.get_app_configs():
        print(f"  - {app.name}")
    
    # Проверяем модели
    print("\nМодели в catalog:")
    try:
        from catalog.models import Product
        print(f"  ✓ Product: {Product}")
        print(f"    Поля: {[f.name for f in Product._meta.get_fields() if not f.auto_created]}")
    except Exception as e:
        print(f"  ✗ Ошибка Product: {e}")
    # Проверяем URLs
    print("\nПроверка URLs:")
    try:
        from django.urls import reverse, resolve
        from catalog.urls import urlpatterns
        
        print(f"  ✓ Найдено {len(urlpatterns)} паттернов в catalog.urls")
        
        # Пробуем reverse
        try:
            url = reverse('catalog:product_list')
            print(f"  ✓ Reverse catalog:product_list: {url}")
        except Exception as e:
            print(f"  ✗ Reverse catalog:product_list: {e}")
            
        try:
            url = reverse('catalog:category_products', args=[1])
            print(f"  ✓ Reverse catalog:category_products: {url}")
        except Exception as e:
            print(f"  ✗ Reverse catalog:category_products: {e}")
            
    except Exception as e:
        print(f"  ✗ Ошибка URLs: {e}")
    
    # Проверяем кэширование
    print("\nПроверка кэширования:")
    try:
        from django.core.cache import cache
        from django.conf import settings
        
        print(f"  ✓ CACHE_ENABLED: {getattr(settings, 'CACHE_ENABLED', 'не найден')}")
        if hasattr(settings, 'CACHES'):
            backend = settings.CACHES.get('default', {}).get('BACKEND', 'не найден')
            print(f"  ✓ CACHE backend: {backend}")
            # Тест записи
            cache.set('django_test', 'работает', 30)
            value = cache.get('django_test')
            print(f"  ✓ Тест кэша: {value}")
        else:
            print("  ✗ CACHES не настроены")
            
    except Exception as e:
        print(f"  ✗ Ошибка кэширования: {e}")
        
except Exception as e:
    print(f"✗ Критическая ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n=== ТЕСТ ЗАВЕРШЕН ===")
