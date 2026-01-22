"""
Сервисные функции для работы с продуктами.
"""
from django.core.cache import cache
from .models import Product


def get_products_in_category(category_id):
    """
    Возвращает список продуктов в указанной категории с использованием кэширования.
    
    Args:
        category_id: ID категории
    
    Returns:
        QuerySet продуктов в категории
    """
    cache_key = f'products_category_{category_id}'
    products = cache.get(cache_key)
    
    if products is None:
        # Пытаемся найти продукты по категории
        # Проверяем различные варианты названия поля
        if hasattr(Product, 'category'):
            # Если есть поле category
            products = list(Product.objects.filter(category_id=category_id))
        elif hasattr(Product, 'categories'):
            # Если есть поле categories (ManyToMany)
            products = list(Product.objects.filter(categories__id=category_id))
        else:
            # Если нет категории, возвращаем все продукты
            # (для демонстрации работы кэширования)
            print(f"Внимание: поле 'category' не найдено в модели Product")
            products = list(Product.objects.all()[:10])
        
        # Кэшируем на 15 минут
        cache.set(cache_key, products, 60 * 15)
        print(f"Данные загружены из БД и закэшированы с ключом: {cache_key}")
    else:
        print(f"Данные получены из кэша с ключом: {cache_key}")
    
    return products

def get_all_cached_products():
    """
    Низкоуровневое кеширование списка всех продуктов
    ДЗ 18.x - Задание 4
    
    Возвращает:
        list: Список всех продуктов с информацией о категориях
    """
    from django.core.cache import cache
    from django.conf import settings
    from .models import Product
    
    if not getattr(settings, 'CACHE_ENABLED', True):
        # Если кеширование отключено, возвращаем напрямую
        return list(Product.objects.all())
    
    cache_key = 'all_products'
    
    # Пытаемся получить из кеша
    products = cache.get(cache_key)
    
    if products is None:
        # Если в кеше нет, загружаем из БД
        products = list(Product.objects.all())
        
        # Сохраняем в кеш на 30 минут
        cache.set(cache_key, products, timeout=60 * 30)
        print(f"[CACHE] 📦 Все продукты загружены из БД и сохранены в кеш (ключ: {cache_key})")
    else:
        print(f"[CACHE] ⚡ Все продукты загружены из кеша Redis (ключ: {cache_key})")
    
    return products


def clear_all_product_caches():
    """
    Очистка всех кешей продуктов
    """
    from django.core.cache import cache
    
    # Удаляем кеш всех продуктов
    cache.delete('all_products')
    
    # Удаляем все кеши категорий
    from django_redis import get_redis_connection
    redis_conn = get_redis_connection("default")
    
    # Ищем ключи категорий
    category_keys = redis_conn.keys('products_category_*')
    if category_keys:
        redis_conn.delete(*category_keys)
        print(f"[CACHE] 🧹 Очищено {len(category_keys)} ключей категорий")
    
    print("[CACHE] ✅ Все кеши продуктов очищены")

def get_all_cached_products_safe():
    """
    Безопасная версия функции get_all_cached_products
    без использования select_related
    """
    from django.core.cache import cache
    from django.conf import settings
    from .models import Product
    
    if not getattr(settings, 'CACHE_ENABLED', True):
        # Если кеширование отключено, возвращаем напрямую
        return list(Product.objects.all())
    
    cache_key = 'all_products_safe'
    
    # Пытаемся получить из кеша
    products = cache.get(cache_key)
    
    if products is None:
        # Если в кеше нет, загружаем из БД без select_related
        products = list(Product.objects.all())
        
        # Сохраняем в кеш на 30 минут
        cache.set(cache_key, products, timeout=60 * 30)
        
        print(f"[CACHE] 📦 Все продукты загружены из БД (без select_related)")
    else:
        print(f"[CACHE] ⚡ Все продукты загружены из кеша Redis")
    
    return products
