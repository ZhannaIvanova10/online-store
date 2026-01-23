import os
import re

template_path = 'catalog/templates/catalog/category_products.html'
if os.path.exists(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Найденные упоминания 'product_list':")
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if 'product_list' in line.lower():
            print(f"Строка {i}: {line.strip()}")
    
    # Заменяем ВСЕ упоминания product_list
    # Вариант 1: {% url 'catalog:product_list' %}
    content = re.sub(
        r'\{%\s*url\s+[\'"](catalog:)?product_list[\'"]\s*%\}',
        "{% url 'catalog:home' %}",
        content
    )
    # Вариант 2: {% url 'product_list' %}
    content = re.sub(
        r'\{%\s*url\s+[\'"]product_list[\'"]\s*%\}',
        "{% url 'catalog:home' %}",
        content
    )
    
    # Вариант 3: Просто текст
    content = content.replace("'catalog:product_list'", "'catalog:home'")
    content = content.replace('"catalog:product_list"', '"catalog:home"')
    content = content.replace("'product_list'", "'catalog:home'")
    content = content.replace('"product_list"', '"catalog:home"')
    
    # Также заменяем на простую ссылку /
    content = re.sub(
        r"href\s*=\s*['\"]{%\s*url\s+['\"][^'\"]+['\"]\s*%}['\"]",
        'href="/"',
        content
    )
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Все упоминания 'product_list' заменены на 'catalog:home'")
    
    # Создаем еще более простую версию на всякий случай
    simple_version = '''
<!DOCTYPE html>
<html>
<head>
    <title>Товары категории</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .cache-info {
            background-color: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .cache-redis {
            background-color: #e8f5e9;
            border-left: 4px solid #4CAF50;
        }
        .cache-db {
            background-color: #fff3e0;
            border-left: 4px solid #FF9800;
        }
    </style>
</head>
<body>
    <div class="container mt-4">
        <h1>Товары категории</h1>
        {% if products %}
            <div class="cache-info {% if cache_source == 'redis_cache' %}cache-redis{% else %}cache-db{% endif %}">
                {% if cache_source == 'redis_cache' %}
                    <h5>⚡ Данные загружены из кэша Redis</h5>
                    <p>Ключ кэша: <code>products_category_{{ category_id }}</code></p>
                {% else %}
                    <h5>📊 Данные загружены из базы данных</h5>
                    <p>Данные сохранены в Redis кэш на 5 минут</p>
                {% endif %}
            </div>
            
            <a href="/" class="btn btn-secondary mb-3">← На главную</a>
            
            <div class="row">
                {% for product in products %}
                    <div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title">{{ product.name }}</h5>
                                <p class="card-text">{{ product.description|truncatechars:100 }}</p>
                                <div class="mb-3">
                                    <span class="badge bg-success">💰 {{ product.price }} руб.</span>
                                    <span class="badge bg-primary">📦 {{ product.quantity }} шт.</span>
                                </div>
                                <a href="/product/{{ product.id }}/" class="btn btn-primary">Подробнее</a>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="alert alert-warning">
                <h4>В этой категории нет товаров</h4>
                <a href="/" class="btn btn-secondary">← На главную</a>
                <a href="/admin/catalog/product/add/" class="btn btn-success">Добавить товар</a>
            </div>
        {% endif %}
        <div class="mt-4">
            <div class="alert alert-info">
                <h5>📊 Информация о кешировании Redis:</h5>
                <p>При первом заходе на эту страницу данные загружаются из базы данных и сохраняются в Redis.</p>
                <p>При повторных заходах в течение 5 минут данные берутся из Redis кэша.</p>
                <p>Попробуйте обновить страницу (F5) несколько раз и посмотрите сообщения в консоли Django.</p>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    # Сохраняем простую версию как backup
    with open('catalog/templates/catalog/category_products_simple.html', 'w', encoding='utf-8') as f:
        f.write(simple_version)
    
    print("✅ Создана простая резервная версия шаблона")
    
else:
    print("❌ Файл category_products.html не найден")
    print("📝 Создаю новый...")
    
    os.makedirs('catalog/templates/catalog', exist_ok=True)
    simple_version = '''<!DOCTYPE html>
<html>
<head>
    <title>Товары категории</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h1>Товары категории {{ category_id }}</h1>
        <a href="/" class="btn btn-secondary mb-3">← На главную</a>
        
        {% if products %}
            <div class="row">
                {% for product in products %}
                    <div class="col-md-4 mb-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">{{ product.name }}</h5>
                                <p class="card-text">{{ product.description }}</p>
                                <p><strong>Цена:</strong> {{ product.price }} руб.</p>
                                <p><strong>Количество:</strong> {{ product.quantity }} шт.</p>
                                <a href="/product/{{ product.id }}/" class="btn btn-primary">Подробнее</a>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="alert alert-warning">
                Нет товаров в этой категории.
            </div>
        {% endif %}
    </div>
</body>
</html>'''
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(simple_version)
    
    print("✅ Создан новый category_products.html")
