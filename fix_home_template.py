import os

template_path = 'catalog/templates/catalog/home.html'
if os.path.exists(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Исходный код содержащий ошибку:")
    print("-" * 50)
    
    # Находим строку с ошибкой
    import re
    error_pattern = r"{%\s*url\s+['\"]catalog:category_products['\"]\s+product\.category\.id\s*%}"
    match = re.search(error_pattern, content)
    
    if match:
        print(f"Найдена ошибка: {match.group(0)}")
        
        # Исправляем - убираем пробелы вокруг аргумента
        fixed = re.sub(
            r"{%\s*url\s+['\"]catalog:category_products['\"]\s+product\.category\.id\s*%}",
            "{% url 'catalog:category_products' product.category.id %}",
            content
        )
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(fixed)
        print("✅ Шаблон home.html исправлен")
    else:
        print("Ищем другие возможные ошибки...")
        
        # Проверяем другие варианты
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'category_products' in line and 'url' in line:
                print(f"Строка {i+1}: {line}")
        
        # Просто заменяем все возможные проблемные варианты
        fixed = content
        
        # Исправляем {% url 'catalog:category_products' product.category.id %}
        fixed = re.sub(
            r"{%\s*url\s+['\"]catalog:category_products['\"]\s*product\.category\.id\s*%}",
            "{% url 'catalog:category_products' product.category.id %}",
            fixed
        )
        
        # Исправляем {% url 'catalog:category_products' product.category.id %}
        fixed = re.sub(
            r"{%\s*url\s+['\"]category_products['\"]\s*product\.category\.id\s*%}",
            "{% url 'catalog:category_products' product.category.id %}",
            fixed
        )
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(fixed)
        
        print("✅ Применены исправления к home.html")
        
else:
    print("❌ Файл home.html не найден")
    
    # Создаем простой рабочий шаблон
    simple_home = '''
<!DOCTYPE html>
<html>
<head>
    <title>Главная страница</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h1>Товары</h1>
        
        {% if products %}
            <div class="row">
                {% for product in products %}
                    <div class="col-md-4 mb-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">{{ product.name }}</h5>
                                <p class="card-text">{{ product.description|truncatechars:100 }}</p>
                                <p><strong>Цена:</strong> {{ product.price }} руб.</p>
                                <p><strong>Остаток:</strong> {{ product.quantity }} шт.</p>
                                <p><strong>Категория:</strong> {{ product.category.name }}</p>
                                <div class="d-grid gap-2">
                                    <a href="/product/{{ product.id }}/" class="btn btn-primary">
                                        Подробнее
                                    </a>
                                    <a href="/category/{{ product.category.id }}/products/" class="btn btn-info">
                                        Все товары категории
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="alert alert-warning">
                Товаров нет. Добавьте через админку.
            </div>
            <a href="/admin/" class="btn btn-warning">Админка</a>
        {% endif %}
    </div>
</body>
</html>'''
    
    os.makedirs('catalog/templates/catalog', exist_ok=True)
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(simple_home)
    
    print("✅ Создан простой home.html")
