import os
import sys

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    import django
    django.setup()
    
    from django.urls import reverse, NoReverseMatch
    import catalog.views
    
    # Проверяем, что функции существуют
    print("🔍 Проверка функций в views.py:")
    print("=" * 40)
    
    required_functions = ['home', 'product_detail', 'category_products']
    for func in required_functions:
        if hasattr(catalog.views, func):
            print(f"✅ Функция {func}() существует")
        else:
            print(f"❌ Функция {func}() отсутствует")
    print("\n🔗 Проверка маршрутов:")
    print("=" * 40)
    
    test_cases = [
        ('catalog:home', [], 'Главная страница'),
        ('catalog:product_detail', [1], 'Страница товара #1'),
        ('catalog:category_products', [1], 'Товары категории #1'),
    ]
    
    all_ok = True
    for name, args, description in test_cases:
        try:
            url = reverse(name, args=args)
            print(f"✅ {description:25} -> {url}")
        except NoReverseMatch as e:
            print(f"❌ {description:25} -> Ошибка: {e}")
            all_ok = False
    
    print("=" * 40)
    
    if all_ok:
        print("\n🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
        print("\n🌐 ДОСТУПНЫЕ ССЫЛКИ:")
        print("   1. http://localhost:8000/                    - Главная страница")
        print("   2. http://localhost:8000/product/1/          - Товар #1")
        print("   3. http://localhost:8000/category/1/products/ - Категория #1")
        print("   4. http://localhost:8000/admin/              - Админ панель")
        
        print("\n⚡ ПРОВЕРКА КЕШИРОВАНИЯ:")
        print("   • Обновите страницу товара 2-3 раза и проверьте заголовки")
        print("   • Перейдите на страницу категории, затем обновите её")
        print("   • В консоли Django увидите сообщения о кешировании")
    else:
        print("\n⚠️  Требуется дополнительная настройка")
        
except Exception as e:
    print(f"💥 Критическая ошибка: {e}")
    print("\n🔄 Возможно, нужно выполнить миграции:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
