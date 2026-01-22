"""
Инициализация базы данных: создание суперпользователя и тестовых данных
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 60)
print("ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ ДЛЯ ДЗ 18.x")
print("=" * 60)

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    # Создаем суперпользователя
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✅ Суперпользователь создан:")
        print("   Логин: admin")
        print("   Пароль: admin123")
        print("   Email: admin@example.com")
    else:
        print("✅ Суперпользователь 'admin' уже существует")
except Exception as e:
    print(f"❌ Ошибка создания суперпользователя: {e}")

# Создаем тестовые категории и продукты
try:
    from catalog.models import Category, Product
    
    print("\n📦 Создание тестовых данных...")
    
    # Создаем категории
    categories_data = [
        {"name": "Электроника", "description": "Техника и гаджеты"},
        {"name": "Одежда", "description": "Мужская и женская одежда"},
        {"name": "Книги", "description": "Художественная и учебная литература"},
        {"name": "Мебель", "description": "Домашняя и офисная мебель"},
        {"name": "Спорт", "description": "Спортивные товары и инвентарь"},
    ]
    
    categories = {}
    for cat_data in categories_data:
        cat, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={"description": cat_data["description"]}
        )
        categories[cat.name] = cat
        if created:
            print(f"   ✅ Создана категория: {cat.name}")
        else:
            print(f"   ✅ Категория уже существует: {cat.name}")
    
    # Создаем продукты
    products_data = [
        {"name": "Смартфон iPhone", "description": "Мощный смартфон", "price": 79999.99, "quantity": 15, "category": "Электроника"},
        {"name": "Ноутбук игровой", "description": "Игровой ноутбук", "price": 129999.99, "quantity": 8, "category": "Электроника"},
        {"name": "Наушники беспроводные", "description": "Bluetooth наушники", "price": 8999.99, "quantity": 30, "category": "Электроника"},
        {"name": "Футболка хлопковая", "description": "Хлопковая футболка", "price": 1999.99, "quantity": 50, "category": "Одежда"},
        {"name": "Джинсы классические", "description": "Классические джинсы", "price": 4999.99, "quantity": 25, "category": "Одежда"},
        {"name": "Куртка зимняя", "description": "Теплая зимняя куртка", "price": 12999.99, "quantity": 12, "category": "Одежда"},
        {"name": "Роман 'Война и мир'", "description": "Художественная литература", "price": 799.99, "quantity": 40, "category": "Книги"},
        {"name": "Учебник по Python", "description": "Учебное пособие", "price": 2499.99, "quantity": 20, "category": "Книги"},
        {"name": "Кресло офисное", "description": "Эргономичное офисное кресло", "price": 15999.99, "quantity": 10, "category": "Мебель"},
        {"name": "Фитбол", "description": "Гимнастический мяч", "price": 2999.99, "quantity": 35, "category": "Спорт"},
    ]

    for prod_data in products_data:
        prod, created = Product.objects.get_or_create(
            name=prod_data["name"],
            defaults={
                "description": prod_data["description"],
                "price": prod_data["price"],
                "quantity": prod_data["quantity"],
                "category": categories[prod_data["category"]]
            }
        )
        if created:
            print(f"   ✅ Создан продукт: {prod.name} ({prod_data['category']})")
        else:
            print(f"   ✅ Продукт уже существует: {prod.name}")
    
    print(f"\n📊 Итог:")
    print(f"   Категорий: {Category.objects.count()}")
    print(f"   Продуктов: {Product.objects.count()}")
    
except Exception as e:
    print(f"❌ Ошибка создания тестовых данных: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ ИНИЦИАЛИЗАЦИЯ ЗАВЕРШЕНА")
print("=" * 60)
print("\nДля запуска сервера выполните:")
print("python manage.py runserver")
print("\nДля входа в админку:")
print("Логин: admin")
print("Пароль: admin123")
print("URL: http://localhost:8000/admin/")
