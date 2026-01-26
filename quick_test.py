import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    django.setup()
    print("✅ Django успешно настроен")
    
    # Проверяем модели
    from catalog.models import Category, Product
    print(f"✅ Модели загружены: Category={Category}, Product={Product}")
    
    # Проверяем количество записей
    print(f"   Категорий в БД: {Category.objects.count()}")
    print(f"   Продуктов в БД: {Product.objects.count()}")
    
    # Проверяем Redis
    from django.core.cache import cache
    cache.set('quick_test', 'works', 5)
    result = cache.get('quick_test')
    print(f"✅ Redis: {'РАБОТАЕТ' if result == 'works' else 'НЕ РАБОТАЕТ'}")
    
    # Проверяем сервисные функции
    from catalog.services import get_products_in_category, get_all_cached_products_safe
    print(f"✅ Сервисные функции загружены")
    # Быстрый тест функций
    try:
        products = get_all_cached_products_safe()
        print(f"✅ get_all_cached_products_safe() вернул {len(products)} продуктов")
    except Exception as e:
        print(f"❌ get_all_cached_products_safe() ошибка: {e}")
    
    print("\n🎉 Проект в основном работает!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
