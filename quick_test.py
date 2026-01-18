#!/usr/bin/env python3
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

print("=== БЫСТРАЯ ПРОВЕРКА ПРОЕКТА ===")

try:
    django.setup()
    
    from django.test import Client
    from catalog.models import Product
    
    client = Client()
    
    print("\n1. Проверка базы данных:")
    product_count = Product.objects.count()
    print(f"   Товаров в базе: {product_count}")
    
    if product_count > 0:
        product = Product.objects.first()
        print(f"   Первый товар: {product.name}")
        print(f"   Описание: {len(product.description)} символов")
        print(f"   Short description: {len(product.short_description())} символов")
    
    print("\n2. Проверка страниц (HTTP статусы):")
    pages = [
        ("/", "Главная страница"),
        ("/contacts/", "Страница контактов"),
        ("/admin/", "Админ-панель"),
    ]
    
    for url, name in pages:
        response = client.get(url)
        print(f"   {name}: {response.status_code}")
    
    if product_count > 0:
        response = client.get(f'/product/{product.id}/')
        print(f"   Страница товара: {response.status_code}")
    
    print("\n3. Проверка шаблонов:")
    templates = [
        'templates/base.html',
        'templates/includes/menu.html',
        'templates/catalog/home.html',
        'templates/catalog/product_detail.html',
        'templates/catalog/contacts.html',
    ]
    
    for template in templates:
        if os.path.exists(template):
            print(f"   ✓ {template}")
        else:
            print(f"   ✗ {template} (не найден)")
    print("\n4. Проверка метода short_description:")
    if product_count > 0:
        for product in Product.objects.all()[:2]:
            short = product.short_description()
            if len(short) <= 103:
                print(f"   ✓ {product.name}: {len(short)} символов")
            else:
                print(f"   ✗ {product.name}: {len(short)} символов (должно быть ≤ 103)")
    
    print("\n=== ПРОВЕРКА ЗАВЕРШЕНА ===")
    print("\nЗапустите сервер: py manage.py runserver")
    print("Откройте: http://127.0.0.1:8000/")
    
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
