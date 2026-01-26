import os
import time
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import Product

client = Client()

# Получаем первый продукт
product = Product.objects.first()
if not product:
    print("Сначала запустите: py create_test_data.py")
    exit()

print(f"🔍 Тестируем кэширование для продукта ID={product.id}")
print("=" * 60)

# Тест 1: Первый запрос (должен быть из БД)
print("\n1. Первый запрос страницы продукта:")
start = time.time()
response = client.get(f'/product/{product.id}/')
elapsed = time.time() - start
print(f"   Время: {elapsed:.3f} сек")
print(f"   Статус: {response.status_code}")
# Тест 2: Второй запрос (должен быть из кэша, быстрее)
print("\n2. Второй запрос (должен быть из кэша):")
start = time.time()
response = client.get(f'/product/{product.id}/')
elapsed = time.time() - start
print(f"   Время: {elapsed:.3f} сек")
print(f"   Статус: {response.status_code}")

# Тест 3: Категория с низкоуровневым кэшированием
print("\n3. Тест категории (низкоуровневое кэширование):")
print("   Первый запрос:")
start = time.time()
response = client.get(f'/category/{product.id}/products/')
elapsed = time.time() - start
print(f"     Время: {elapsed:.3f} сек")

print("   Второй запрос (из кэша):")
start = time.time()
response = client.get(f'/category/{product.id}/products/')
elapsed = time.time() - start
print(f"     Время: {elapsed:.3f} сек")

# Проверяем Redis
print("\n4. Проверка Redis кэша:")
import redis
r = redis.Redis(host='localhost', port=6379, db=1)
keys = r.keys('*')
print(f"   Ключей в Redis: {len(keys)}")
for key in keys[:5]:  # Покажем первые 5 ключей
    key_str = key.decode('utf-8')
    ttl = r.ttl(key)
    print(f"   - {key_str[:50]}... (TTL: {ttl} сек)")

print("\n" + "=" * 60)
print("✅ Если второй запрос быстрее первого - кэширование работает!")
print(f"📊 Открой в браузере: http://localhost:8000/product/{product.id}/")
