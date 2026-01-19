import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('.')

django.setup()

from catalog.models import Product

# Проверяем, есть ли уже продукты
count = Product.objects.count()
print(f'Сейчас продуктов в базе: {count}')

if count == 0:
    print('Создаем тестовые продукты...')
    
    products_data = [
        {'name': 'Ноутбук Dell XPS 13', 'description': 'Мощный ультрабук с экраном 13 дюймов', 'price': 999.99},
        {'name': 'iPhone 15 Pro', 'description': 'Флагманский смартфон Apple', 'price': 1299.99},
        {'name': 'Наушники Sony WH-1000XM5', 'description': 'Беспроводные наушники с шумоподавлением', 'price': 349.99},
        {'name': 'Фотокамера Canon EOS R6', 'description': 'Зеркальная камера для профессионалов', 'price': 2499.99},
        {'name': 'Планшет Samsung Galaxy Tab S9', 'description': 'Планшет с дисплеем AMOLED', 'price': 899.99},
        {'name': 'Умные часы Apple Watch Series 9', 'description': 'Смарт-часы с измерением ЭКГ', 'price': 399.99},
        {'name': 'Игровая консоль PlayStation 5', 'description': 'Новейшая игровая консоль от Sony', 'price': 499.99},
        {'name': 'Монитор Dell UltraSharp 4K', 'description': '32-дюймовый монитор 4K', 'price': 799.99},
        {'name': 'Клавиатура Logitech MX Keys', 'description': 'Беспроводная клавиатура для работы', 'price': 99.99},
        {'name': 'Мышь Razer DeathAdder V3', 'description': 'Игровая мышь с оптическим сенсором', 'price': 69.99},
    ]
    for data in products_data:
        product = Product.objects.create(**data)
        print(f'Создан: {product.name} (ID: {product.id})')
    
    print(f'\\nСоздано {len(products_data)} продуктов!')
else:
    print('Продукты уже существуют. Вот список:')
    for p in Product.objects.all():
        print(f'  ID: {p.id}, Название: {p.name}')
