import re

with open('catalog/templates/catalog/product_list.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Исправляем все ссылки на использование namespace catalog:
content = re.sub(r"{% url 'product_create' %}", "{% url 'catalog:product_create' %}", content)
content = re.sub(r"{% url 'product_detail'", "{% url 'catalog:product_detail'", content)
content = re.sub(r"{% url 'product_update'", "{% url 'catalog:product_update'", content)
content = re.sub(r"{% url 'product_delete'", "{% url 'catalog:product_delete'", content)
content = re.sub(r"{% url 'home' %}", "{% url 'catalog:home' %}", content)

with open('catalog/templates/catalog/product_list.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Шаблон исправлен: все ссылки используют namespace catalog:")
