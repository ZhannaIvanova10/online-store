#!/usr/bin/env python
import requests
import sys

BASE_URL = 'http://127.0.0.1:8000'

urls_to_check = [
    ('/', 'Главная страница'),
    ('/admin/', 'Админ-панель'),
    ('/accounts/login/', 'Страница входа'),
    ('/product/create/', 'Создание товара'),
    ('/users/profile/', 'Профиль (требует входа)'),
]

print("=== ПРОВЕРКА ДОСТУПНОСТИ URL ===")

for url, description in urls_to_check:
    try:
        response = requests.get(BASE_URL + url, timeout=2)
        status = "✓" if response.status_code < 400 else "✗"
        print(f"{status} {description}: {response.status_code} ({url})")
    except Exception as e:
        print(f"✗ {description}: Ошибка ({e})")

print("\\n=== ИНСТРУКЦИЯ ===")
print("1. Админка: http://127.0.0.1:8000/admin/")
print("2. Логин: admin / ваш_пароль")
print("3. После входа можно открыть профиль")
