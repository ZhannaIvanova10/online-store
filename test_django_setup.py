#!/usr/bin/env python3
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    print("✅ Django успешно настроен")
    
    from catalog.models import Product
    print("✅ Модель Product импортирована успешно")
    
    # Проверим метод short_description
    test_product = Product(
        name="Тестовый товар",
        description="Очень длинное описание тестового товара, которое должно быть обрезано на главной странице до 100 символов. Это важно для выполнения домашнего задания номер 4 по Django.",
        price=1000.00,
        stock=5
    )
    short_desc = test_product.short_description()
    print(f"✅ Метод short_description работает: {len(short_desc)} символов")
    print(f"   Оригинал: {len(test_product.description)} символов")
    print(f"   Обрезано: {short_desc}")
    
    if len(short_desc) <= 103:
        print("✅ Описание корректно обрезается до 100 символов")
    else:
        print("❌ Ошибка: описание не обрезается правильно")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
