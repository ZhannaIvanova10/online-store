"""
Утилиты для работы с кэшированием в приложении catalog
"""
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
import time

def get_product_cache_key(product_id):
    """Генерирует ключ кэша для товара"""
    return f'product_{product_id}_detail'

def get_products_list_cache_key(page=1):
    """Генерирует ключ кэша для списка товаров"""
    return f'products_list_page_{page}'

def clear_product_caches(product_id=None):
    """Очищает кэши связанные с товарами"""
    if product_id:
        # Удаляем кэш конкретного товара
        cache.delete(get_product_cache_key(product_id))
    
    # Удаляем кэш всех страниц списка товаров
    for i in range(1, 6):  # Предполагаем не более 5 страниц
        cache.delete(get_products_list_cache_key(i))
    
    # Удаляем общий кэш
    cache.delete_pattern('product_*')
    cache.delete_pattern('products_*')
    return True
@receiver(post_save, sender=Product)
def clear_cache_on_product_save(sender, instance, **kwargs):
    """Очищает кэш при сохранении товара"""
    clear_product_caches(instance.id)
    print(f"Кэш очищен после сохранения товара: {instance.name}")

@receiver(post_delete, sender=Product)
def clear_cache_on_product_delete(sender, instance, **kwargs):
    """Очищает кэш при удалении товара"""
    clear_product_caches(instance.id)
    print(f"Кэш очищен после удаления товара: {instance.name}")

# Функция для тестирования производительности
def benchmark_view(view_func, *args, **kwargs):
    """Измеряет время выполнения view-функции"""
    start_time = time.time()
    result = view_func(*args, **kwargs)
    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"Время выполнения: {execution_time:.4f} секунд")
    
    # Проверяем, был ли ответ взят из кэша
    if hasattr(result, 'from_cache'):
        print(f"Результат из кэша: {result.from_cache}")
    
    return result
