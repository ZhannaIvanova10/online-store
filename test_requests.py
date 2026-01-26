import os
import sys
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('.')

django.setup()

from catalog.models import Product

client = Client()

# Получаем первый продукт
product = Product.objects.first()
if not product:
    print('Нет продуктов в базе!')
    sys.exit(1)
print(f'Тестируем с продуктом ID={product.id} ({product.name})')
print('=' * 50)

# Тест 1: Главная страница (кэшируется на 5 минут)
print('\\n1. Главная страница (первый запрос):')
response = client.get('/')
print(f'   Статус: {response.status_code}')
print(f'   Из кэша: {hasattr(response, "_from_cache")}')

# Тест 2: Страница продукта (кэшируется на 10 минут)
print('\\n2. Страница продукта (первый запрос):')
response = client.get(f'/product/{product.id}/')
print(f'   Статус: {response.status_code}')
print(f'   Из кэша: {hasattr(response, "_from_cache")}')

# Тест 3: Страница категории (низкоуровневое кэширование)
print('\\n3. Страница категории (первый запрос):')
response = client.get('/category/1/products/')
print(f'   Статус: {response.status_code}')

# Тест 4: Повторные запросы (должны быть быстрее)
print('\\n4. Повторные запросы (должны быть из кэша):')
import time

urls = ['/', f'/product/{product.id}/', '/category/1/products/']
for url in urls:
    start = time.time()
    response = client.get(url)
    elapsed = time.time() - start
    print(f'   {url}: {elapsed:.3f} сек')

# Проверяем Redis
print('\\n5. Проверка Redis:')
import redis
r = redis.Redis(host='localhost', port=6379, db=1)
keys = r.keys('*')
print(f'   Ключей в Redis: {len(keys)}')
for key in keys:
    ttl = r.ttl(key)
    print(f'   - {key.decode()}: TTL={ttl} сек')
