import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import Category, Product

print("🔍 Проверяем базу данных...")

# Создаем категорию если нет
category, created = Category.objects.get_or_create(
    id=1,
    defaults={
        'name': 'Электроника',
        'description': 'Товары электроники'
    }
)
if created:
    print(f"✅ Создана категория: {category.name} (ID: {category.id})")
else:
    print(f"✅ Категория уже существует: {category.name}")
# Создаем товар с ID=1 если нет
try:
    product = Product.objects.get(id=1)
    print(f"✅ Товар уже существует: {product.name} (ID: {product.id})")
except Product.DoesNotExist:
    product = Product.objects.create(
        id=1,
        category=category,
        name='Смартфон Samsung Galaxy S23',
        description='Флагманский смартфон Samsung с камерой 200 МП',
        price=89990.00,
        quantity=15
    )
    print(f"✅ Создан товар: {product.name} (ID: {product.id})")

# Создаем еще несколько товаров для категории
for i in range(2, 6):
    try:
        Product.objects.get(id=i)
    except Product.DoesNotExist:
        Product.objects.create(
            id=i,
            category=category,
            name=f'Товар {i}',
            description=f'Описание товара {i}',
            price=1000 * i,
            quantity=10 * i
        )
        print(f"✅ Создан товар: Товар {i} (ID: {i})")

print(f"\\n📊 Статистика:")
print(f"   Категорий: {Category.objects.count()}")
print(f"   Товаров: {Product.objects.count()}")
print(f"   Товаров в категории 1: {Product.objects.filter(category_id=1).count()}")

print("\\n🌐 Тестовые URL:")
print("   http://localhost:8000/ - Главная")
print("   http://localhost:8000/product/1/ - Смартфон Samsung")
print("   http://localhost:8000/category/1/products/ - Все товары электроники")
