import os

views_path = 'catalog/views.py'
if os.path.exists(views_path):
    print("✅ views.py существует")
    
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем ключевые элементы
    checks = [
        ('def home(', 'Функция home'),
        ('@cache_page', 'Кеширование product_detail'),
        ('def product_detail(', 'Функция product_detail'),
        ('def category_products(', 'Функция category_products'),
        ('cache_source', 'cache_source в category_products'),
        ('logger.info', 'Логирование'),
    ]
    
    print("\n🔍 Проверка views.py:")
    all_ok = True
    for pattern, desc in checks:
        if pattern in content:
            print(f"  ✅ {desc}")
        else:
            print(f"  ❌ {desc} - ОТСУТСТВУЕТ!")
            all_ok = False
    if all_ok:
        print("\n✅ views.py в порядке")
    else:
        print("\n⚠️  Пересоздаю views.py...")
        
        # Создаем правильную версию
        correct_views = '''from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import Product, Category
import logging

logger = logging.getLogger(__name__)

def home(request):
    """Главная страница со всеми товарами"""
    products = Product.objects.all().select_related('category')
    context = {'products': products}
    return render(request, 'catalog/home.html', context)

@cache_page(60 * 15)  # Кеширование на 15 минут
def product_detail(request, product_id):
    """Детальная страница товара"""
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)

def category_products(request, category_id):
    """Товары определенной категории с Redis-кешированием"""
    cache_key = f'products_category_{category_id}'
    
    # Пытаемся получить данные из кэша
    cached_data = cache.get(cache_key)

    if cached_data is None:
        # Если нет в кэше, загружаем из БД
        products = Product.objects.filter(category_id=category_id).select_related('category')
        products_list = list(products)
        
        # Сохраняем в Redis на 5 минут
        cache.set(cache_key, products_list, timeout=60 * 5)
        logger.info(f'Данные загружены из БД и сохранены в кэш с ключом: {cache_key}')
        cache_source = 'database'
    else:
        # Данные из кэша
        products = cached_data
        logger.info(f'Данные получены из кэша с ключом: {cache_key}')
        cache_source = 'redis_cache'
    
    context = {
        'products': products,
        'category_id': category_id,
        'cache_source': cache_source
    }
    return render(request, 'catalog/category_products.html', context)
'''
        
        with open(views_path, 'w', encoding='utf-8') as f:
            f.write(correct_views)
        
        print("✅ views.py пересоздан")
        
else:
    print("❌ views.py не найден, создаю...")
    
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(correct_views)
    
    print("✅ views.py создан")
