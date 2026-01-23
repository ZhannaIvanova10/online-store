2. Установите зависимости:
bash
py -m pip install -r requirements.txt
3. Примените миграции (если нужно):
bash
py manage.py migrate
4. Создайте тестовые данные:
bash
py manage.py shell -c "
from catalog.models import Category, Product
import random

# Создаем категории
categories = []
for i in range(3):
    cat = Category.objects.create(
        name=f'Категория {i+1}',
        description=f'Описание категории {i+1}'
    )
    categories.append(cat)

# Создаем продукты
for i in range(10):
    Product.objects.create(
        name=f'Продукт {i+1}',
        description=f'Описание продукта {i+1}',
        price=random.uniform(100, 1000),
        quantity=random.randint(1, 50),
        category=random.choice(categories) if categories else None
    )

print(f'Создано: {Category.objects.count()} категорий, {Product.objects.count()} продуктов')
"
5. Запустите сервер:
bash
py manage.py runserver
6. Проверьте эндпоинты:
Главная страница: http://localhost:8000/

Страница продукта: http://localhost:8000/product/1/

Продукты категории: http://localhost:8000/category/1/products/

Критерии для проверки:
✅ Должно работать:
Redis подключение и кеширование

Страница продукта кешируется (время загрузки уменьшается при повторных запросах)

Сервисная функция get_products_in_category() возвращает продукты

Низкоуровневое кеширование работает (проверьте логи в консоли)

🔍 Что проверить в коде:
catalog/services.py - функции кеширования

catalog/views.py - декораторы cache_page

config/settings.py - настройки CACHES

requirements.txt - зависимости
🧪 Автоматическая проверка:
Запустите скрипт проверки:

bash
./test_project.sh
📞 Контакты для вопросов:
Студент: Zhanna Ivanova

Проект: ДЗ 18.x - Кеширование с Redis

Ветка: homework-caching-redis

Количество коммитов: 4
