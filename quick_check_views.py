import os

views_path = 'catalog/views.py'
if os.path.exists(views_path):
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем ключевые элементы
    required = [
        ('def category_products(', 'Функция category_products'),
        ('cache_source', 'Переменная cache_source'),
        ('cache.get', 'Чтение из кэша'),
        ('cache.set', 'Запись в кэш'),
        ('logger.info', 'Логирование'),
    ]
    
    print("Проверка views.py:")
    all_ok = True
    for pattern, desc in required:
        if pattern in content:
            print(f"  ✅ {desc}")
        else:
            print(f"  ❌ {desc}")
            all_ok = False
    
    if all_ok:
        print("✅ views.py в порядке")
    else:
        print("⚠️  Нужны исправления в views.py")
else:
    print("❌ views.py не найден")
