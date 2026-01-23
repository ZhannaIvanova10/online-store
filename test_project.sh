#!/bin/bash

echo "🧪 Тестирование проекта ДЗ 18.x"
echo "================================"

# Проверка Redis
echo "1. Проверка Redis:"
if redis-cli ping &> /dev/null; then
    echo "   ✅ Redis работает"
else
    echo "   ❌ Redis не запущен"
    echo "   Запустите командой: redis-server"
    exit 1
fi

# Проверка зависимостей
echo -e "\n2. Проверка зависимостей:"
if [ -f "requirements.txt" ]; then
    echo "   ✅ requirements.txt существует"
    echo "   Содержимое:"
    cat requirements.txt
else
    echo "   ❌ requirements.txt не найден"
fi
# Проверка настроек Django
echo -e "\n3. Проверка настроек Django:"
if [ -f "config/settings.py" ]; then
    echo "   ✅ settings.py существует"
    echo "   Настройки Redis:"
    grep -A10 "CACHES = {" config/settings.py | head -12
else
    echo "   ❌ settings.py не найден"
fi

# Быстрая проверка Python
echo -e "\n4. Быстрая проверка Python:"
py -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    import django
    django.setup()
    print('   ✅ Django настроен')
    
    from django.core.cache import cache
    cache.set('test_dz_18', 'works', 5)
    result = cache.get('test_dz_18')
    if result == 'works':
        print('   ✅ Redis кеширование работает')
    else:
        print('   ❌ Redis кеширование не работает')
        
    from catalog.models import Product, Category
    products_count = Product.objects.count()
    categories_count = Category.objects.count()
    print(f'   ✅ Модели загружены: {products_count} продуктов, {categories_count} категорий')
    # Проверка сервисных функций
    from catalog.services import get_all_cached_products_safe
    products = get_all_cached_products_safe()
    print(f'   ✅ Сервисные функции работают: получено {len(products)} продуктов')
    
except Exception as e:
    print(f'   ❌ Ошибка: {e}')
"
echo -e "\n================================"
echo "Тестирование завершено!"
echo "Проект готов к проверке! 🚀"
