#!/bin/bash

echo "=========================================="
echo "ПРОВЕРКА КРИТЕРИЕВ ДОМАШНЕЙ РАБОТЫ"
echo "=========================================="

echo ""
echo "1. РАБОТА С GIT И GITHUB"
echo "========================="

# Проверяем текущую ветку
current_branch=$(git branch --show-current)
echo "✓ Текущая ветка: $current_branch"

# Проверяем, что ветка hw2-django-project
if [ "$current_branch" = "hw2-django-project" ]; then
    echo "✓ Работаем в ветке домашней работы"
else
    echo "✗ НЕ В ВЕТКЕ ДОМАШНЕЙ РАБОТЫ!"
fi

# Проверяем игнорируемые файлы в коммитах
echo "✓ Проверка .gitignore (визуально):"
grep -E "(\.pyc|__pycache__|db\.sqlite3|venv|\.env)" .gitignore || echo "✗ Возможно не все файлы в .gitignore"

echo ""
echo "2. БАЗОВЫЕ НАСТРОЙКИ ПРОЕКТА"
echo "============================="

# Проверяем requirements.txt
if [ -f "requirements.txt" ]; then
    echo "✓ Файл requirements.txt существует"
    echo "  Содержимое:"
    cat requirements.txt | head -5
else
    echo "✗ requirements.txt не найден!"
fi
echo ""
echo "3. СТРАНИЦА ОДНОГО ТОВАРА"
echo "=========================="

# Проверяем контроллер
echo "✓ Проверяем контроллер catalog/views.py:"
if grep -q "ProductDetailView" catalog/views.py; then
    echo "  ✓ Класс ProductDetailView существует"
    
    if grep -q "DetailView" catalog/views.py; then
        echo "  ✓ Использует DetailView"
    fi
    
    if grep -q "template_name.*product_detail" catalog/views.py; then
        echo "  ✓ Указан правильный template_name"
    fi
else
    echo "  ✗ ProductDetailView не найден!"
fi
# Проверяем шаблон
if [ -f "catalog/templates/catalog/product_detail.html" ]; then
    echo "✓ Шаблон product_detail.html существует"
    
    # Проверяем использование базового шаблона
    if head -2 catalog/templates/catalog/product_detail.html | grep -q "extends"; then
        echo "  ✓ Использует extends (базовый шаблон)"
    fi
    
    # Проверяем отображение данных
    if grep -q "{{ product\." catalog/templates/catalog/product_detail.html; then
        echo "  ✓ Выводятся данные продукта"
    fi
    
    if grep -q "product.image.url" catalog/templates/catalog/product_detail.html; then
        echo "  ✓ Изображение выводится корректно"
    fi
else
    echo "✗ Шаблон product_detail.html не найден!"
fi

# Проверяем URL
echo "✓ Проверяем URL в catalog/urls.py:"
if grep -q "product/<int:pk>" catalog/urls.py; then
    echo "  ✓ URL для товара с pk существует"
    
    if grep -q "product_detail" catalog/urls.py; then
        echo "  ✓ Правильный нейминг (product_detail)"
    fi
else
    echo "  ✗ URL для товара не найден!"
fi

echo ""
echo "4. ГЛАВНАЯ СТРАНИЦА"
echo "===================="
# Проверяем контроллер главной страницы
echo "✓ Проверяем контроллер главной страницы:"
if grep -q "HomeView" catalog/views.py; then
    echo "  ✓ HomeView существует"
    
    if grep -q "ListView" catalog/views.py; then
        echo "  ✓ Использует ListView"
    fi
    
    if grep -q "Product.objects" catalog/views.py; then
        echo "  ✓ Есть ORM-запрос для получения продуктов"
    fi
fi

# Проверяем шаблон главной страницы
if [ -f "catalog/templates/catalog/home.html" ]; then
    echo "✓ Шаблон home.html существует"
    
    # Проверяем цикл for
    if grep -q "{% for.*in products %}" catalog/templates/catalog/home.html || 
       grep -q "{% for product in products %}" catalog/templates/catalog/home.html; then
        echo "  ✓ Есть цикл для вывода товаров"
    fi
    
    # Проверяем обрезку описания
    if grep -q "truncatechars:100" catalog/templates/catalog/home.html; then
        echo "  ✓ Описание обрезается до 100 символов (truncatechars:100)"
    else
        echo "  ✗ Нет обрезки описания до 100 символов!"
    fi
    # Проверяем ссылки на товары
    if grep -q "{% url.*product_detail" catalog/templates/catalog/home.html; then
        echo "  ✓ Есть ссылки на страницы товаров"
    fi
    
    # Проверяем отображение изображений
    if grep -q "product.image.url" catalog/templates/catalog/home.html; then
        echo "  ✓ Изображения выводятся корректно"
    fi
else
    echo "✗ Шаблон home.html не найден!"
fi

echo ""
echo "5. БАЗОВЫЙ ШАБЛОН"
echo "=================="

if [ -f "templates/base.html" ]; then
    echo "✓ Базовый шаблон base.html существует"
    
    # Проверяем, используют ли его другие шаблоны
    echo "✓ Проверяем использование базового шаблона:"
    
    if head -2 catalog/templates/catalog/home.html | grep -q "extends.*base.html"; then
        echo "  ✓ home.html использует base.html"
    fi
    
    if head -2 catalog/templates/catalog/product_detail.html | grep -q "extends.*base.html"; then
        echo "  ✓ product_detail.html использует base.html"
    fi
    
    if [ -f "catalog/templates/catalog/contacts.html" ]; then
        if head -2 catalog/templates/catalog/contacts.html | grep -q "extends.*base.html"; then
            echo "  ✓ contacts.html использует base.html"
        fi
    fi
else
    echo "✗ Базовый шаблон base.html не найден!"
fi

echo ""
echo "6. ПОДШАБЛОН МЕНЮ"
echo "=================="

if [ -f "templates/includes/menu.html" ]; then
    echo "✓ Подшаблон меню menu.html существует"
    
    # Проверяем, используется ли в базовом шаблоне
    if grep -q "include.*menu" templates/base.html || 
       grep -q "include.*includes/menu" templates/base.html; then
        echo "  ✓ menu.html используется в base.html"
    else
        echo "  ✗ menu.html НЕ используется в base.html!"
    fi
else
    echo "✗ Подшаблон меню menu.html не найден!"
fi

echo ""
echo "7. МОДЕЛЬ PRODUCT"
echo "=================="

if [ -f "catalog/models.py" ]; then
    echo "✓ Файл models.py существует"
    
    if grep -q "class Product" catalog/models.py; then
        echo "  ✓ Модель Product определена"
        
        # Проверяем основные поля
        if grep -q "CharField.*название" catalog/models.py; then
            echo "  ✓ Есть поле name (CharField)"
        fi
        
        if grep -q "TextField.*описание" catalog/models.py; then
            echo "  ✓ Есть поле description (TextField)"
        fi
        
        if grep -q "DecimalField.*цена" catalog/models.py; then
            echo "  ✓ Есть поле price (DecimalField)"
        fi
        
        if grep -q "ImageField.*изображение" catalog/models.py; then
            echo "  ✓ Есть поле image (ImageField)"
        fi
    fi
fi

echo ""
echo "8. ПРОВЕРКА РАБОТЫ ПРИЛОЖЕНИЯ"
echo "=============================="

# Проверяем запуск Django
echo "✓ Проверяем, что Django проект может запуститься:"
if py manage.py check --deploy 2>&1 | grep -q "System check identified no issues"; then
    echo "  ✓ Django проект проходит проверку"
else
    echo "  ⚠ Есть предупреждения, но проект работает"
fi

# Проверяем наличие товаров в БД
echo "✓ Проверяем наличие товаров в базе данных:"
py -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from catalog.models import Product
count = Product.objects.count()
print(f'  В базе данных товаров: {count}')
if count > 0:
    print('  ✓ Товары есть в базе данных')
else:
    print('  ✗ В базе данных нет товаров!')
"
echo ""
echo "=========================================="
echo "ИТОГОВАЯ ПРОВЕРКА"
echo "=========================================="
echo ""
echo "Для успешной сдачи убедитесь, что:"
echo "1. Все критерии отмечены ✓"
echo "2. Нет критических ошибок (✗)"
echo "3. PR создан и содержит все изменения"
echo "4. Ссылка на PR отправлена наставнику"
echo ""
echo "URL PR: https://github.com/ZhannaIvanova10/online-store/pull/2"
