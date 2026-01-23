import os

template_path = 'catalog/templates/catalog/category_products.html'
if os.path.exists(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Ищем упоминания 'product_list'...")
    
    # Заменяем все упоминания product_list
    if 'product_list' in content:
        print("✅ Найдены упоминания 'product_list'")
        
        # Заменяем все варианты
        import re
        
        # Вариант 1: {% url 'product_list' %}
        content = re.sub(
            r'\{%\s*url\s+[\'"]product_list[\'"]\s*%\}',
            '/',
            content
        )
        
        # Вариант 2: 'product_list' в строке
        content = content.replace("'product_list'", "'catalog:home'")
        content = content.replace('"product_list"', '"catalog:home"')
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Все упоминания 'product_list' заменены")
    else:
        print("✅ Упоминаний 'product_list' не найдено")
        
else:
    print("❌ Файл category_products.html не найден")
    # Создаем простой рабочий шаблон
    simple_category = '''
<!DOCTYPE html>
<html>
<head>
    <title>Товары категории</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h1>Товары категории</h1>
        
        {% if products %}
            <div class="alert alert-info">
                {% if cache_source == 'redis_cache' %}
                    ⚡ Данные загружены из кэша Redis
                {% else %}
                    📊 Данные загружены из базы данных
                {% endif %}
            </div>
            
            <a href="/" class="btn btn-secondary mb-3">← На главную</a>
            
            <div class="row">
                {% for product in products %}
                    <div class="col-md-4 mb-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">{{ product.name }}</h5>
                                <p class="card-text">{{ product.description|truncatechars:100 }}</p>
                                <p><strong>Цена:</strong> {{ product.price }} руб.</p>
                                <p><strong>Остаток:</strong> {{ product.quantity }} шт.</p>
                                <a href="/product/{{ product.id }}/" class="btn btn-primary">Подробнее</a>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="alert alert-warning">
                В этой категории нет товаров.
            </div>
            <a href="/" class="btn btn-secondary">← На главную</a>
        {% endif %}
    </div>
</body>
</html>'''
    os.makedirs('catalog/templates/catalog', exist_ok=True)
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(simple_category)
    
    print("✅ Создан простой category_products.html")
