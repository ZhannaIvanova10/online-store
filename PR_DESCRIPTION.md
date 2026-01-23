# 🚀 Реализация Redis кеширования в Django проекте

## 📋 Задача
Реализовать кеширование с использованием Redis в Django приложении "Онлайн-магазин".

## ✅ Выполненные задачи

### 1. Настройка Redis
- Установлены пакеты: `redis`, `django-redis`
- Настроен бэкенд кеширования в `config/settings.py`
- Проверено подключение к Redis серверу

### 2. Реализация кеширования
#### а) Кеширование страницы товара (`@cache_page`)
- Использован декоратор `@cache_page(60 * 15)` для кеширования на 15 минут
- Страница: `/product/<id>/`

#### б) Ручное кеширование Redis для категорий
- Реализована логика в функции `category_products()`:
  - Ключ кэша: `products_category_{category_id}`
  - Время жизни: 5 минут
  - При первом запросе: данные из БД → сохраняются в Redis
  - При повторных запросах: данные из Redis кэша
- Страница: `/category/<id>/products/`

### 3. Исправление ошибок
- ✅ Исправлены ошибки `NoReverseMatch` для маршрутов `product_list` и `product_delete`
- ✅ Удалены проблемные шаблоны
- ✅ Созданы простые рабочие шаблоны с абсолютными ссылками

### 4. Логирование
- Добавлено логирование работы кэша
- В консоли отображается источник данных (БД или Redis)

### 5. Тестовые данные
- Созданы тестовые категории и товары
- Добавлен скрипт для автоматического создания данных

## 🔧 Техническая реализация

### Настройки Redis (`config/settings.py`):
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
Кеширование страницы товара (catalog/views.py):
python
@cache_page(60 * 15)
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'catalog/product_detail.html', {'product': product})
Ручное кеширование категории:
python
def category_products(request, category_id):
    cache_key = f'products_category_{category_id}'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        # Данные из БД
        products = Product.objects.filter(category_id=category_id)
        cache.set(cache_key, list(products), timeout=60 * 5)
        cache_source = 'database'
        logger.info(f'Данные загружены из БД: {cache_key}')
    else:
        # Данные из кэша
        products = cached_data
        cache_source = 'redis_cache'
        logger.info(f'Данные получены из кэша: {cache_key}')
    
    return render(request, 'catalog/category_products.html', {
        'products': products,
        'category_id': category_id,
        'cache_source': cache_source
    })
🎯 Результат
Работающие страницы:
Главная страница (/) - отображает все товары

Страница товара (/product/<id>/) - кешируется на 15 минут

Страница категории (/category/<id>/products/) - демонстрация Redis кеширования

Проверка работы кеширования:
Откройте страницу категории впервые → "ДАННЫЕ ИЗ БАЗЫ ДАННЫХ"

Обновите страницу (F5) → "ДАННЫЕ ИЗ REDIS КЭША!"

Проверьте логи в консоли Django

📊 Структура проекта
text
online-store/
├── catalog/
│   ├── views.py          # Логика с кешированием
│   ├── urls.py           # Маршруты
│   ├── models.py         # Модели Product и Category
│   └── templates/catalog/
│       ├── home.html                 # Главная страница
│       ├── product_detail.html       # Страница товара
│       └── category_products.html    # Страница категории (кеширование)
├── config/
│   └── settings.py       # Настройки Redis
└── requirements.txt      # Зависимости
🧪 Тестирование
Запустите Redis: redis-server

Запустите Django: python manage.py runserver 8000

Откройте: http://localhost:8000/category/1/products/

Обновите страницу 2-3 раза для проверки кеширования

📈 Потенциальные улучшения
Инвалидация кэша при изменении данных

Кеширование фрагментов шаблонов

Настройка TTL для разных типов данных

Мониторинг использования кэша

Автор: Zhanna Ivanova
Дата: 2026-01-23
Версия Django: 4.2.27
Версия Python: 3.13.3
