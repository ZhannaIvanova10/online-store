simple_template = '''<!DOCTYPE html>
<html>
<head>
    <title>Продукты категории</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h1>Продукты в категории</h1>
        
        {% if products %}
            <div class="alert alert-info">
                ⚡ Данные загружены из кеша Redis
            </div>
            
            <a href="/" class="btn btn-secondary mb-3">← Назад на главную</a>
            
            <div class="row">
                {% for product in products %}
                    <div class="col-md-4 mb-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">{{ product.name }}</h5>
                                <p class="card-text">{{ product.description|truncatewords:20 }}</p>
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
                В этой категории нет продуктов.
            </div>
            <a href="/" class="btn btn-secondary">← Назад на главную</a>
        {% endif %}
    </div>
</body>
</html>'''

with open('catalog/templates/catalog/category_products.html', 'w', encoding='utf-8') as f:
    f.write(simple_template)

print("✅ Создан простой работающий шаблон category_products.html")
