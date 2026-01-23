import os

views_path = 'catalog/views.py'
if os.path.exists(views_path):
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Проверка views.py:")
    print("-" * 40)
    
    # Проверяем наличие cache_source в category_products
    if 'cache_source' in content:
        print("✅ cache_source используется в функции category_products")
    else:
        print("❌ cache_source не используется, исправляю...")
        
        # Находим функцию category_products
        import re
        pattern = r'def category_products\([^)]+\):[^}]+return render\([^)]+\)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            func_text = match.group(0)
            
            # Заменяем возврат с context
            if 'context' in func_text:
                # Если используется context, добавляем cache_source
                new_func_text = func_text.replace(
                    "'cache_source': cache_source",
                    "'cache_source': cache_source"  # Уже есть
                )
            else:
                # Если нет context, создаем его
                new_func_text = func_text.replace(
                    'return render(request, \'catalog/category_products.html\'',
                    'return render(request, \'catalog/category_products.html\', {\'products\': products, \'category_id\': category_id, \'cache_source\': cache_source})'
                )
            
            content = content.replace(func_text, new_func_text)
            
            with open(views_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Функция category_products обновлена")
        else:
            print("⚠️  Не могу найти функцию category_products")
    
    # Проверяем импорты
    if 'from django.views.decorators.cache import cache_page' in content:
        print("✅ cache_page импортирован")
    else:
        print("❌ cache_page не импортирован, добавляю...")
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'from django.shortcuts import' in line:
                lines[i] = 'from django.shortcuts import render, get_object_or_404\nfrom django.views.decorators.cache import cache_page'
                break
        
        content = '\n'.join(lines)
        with open(views_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Импорты обновлены")
    
    print("-" * 40)
    print("✅ views.py проверен и исправлен")
else:
    print("❌ Файл views.py не найден")
    print("📝 Создаю базовый views.py...")
    
    base_views = '''from django.shortcuts import render, get_object_or_404
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
        products_list = list(products)  # Конвертируем QuerySet в список
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

    os.makedirs('catalog', exist_ok=True)
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(base_views)
    
    print("✅ Создан views.py с базовыми функциями")
