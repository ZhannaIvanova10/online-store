#!/bin/bash

echo "🚀 Быстрый запуск проекта ДЗ 18.x"
echo "================================="

# Проверка Redis
echo "1. Проверка Redis..."
if redis-cli ping &> /dev/null; then
    echo "   ✅ Redis работает"
else
    echo "   ⚠️  Redis не запущен"
    echo "   Запустите Redis в отдельном терминале:"
    echo "   redis-server"
    read -p "Нажмите Enter после запуска Redis..."
fi

# Установка зависимостей
echo -e "\n2. Установка зависимостей..."
py -m pip install -r requirements.txt

# Применение миграций
echo -e "\n3. Применение миграций..."
py manage.py migrate

# Создание тестовых данных
echo -e "\n4. Создание тестовых данных..."
py manage.py shell -c "
from catalog.models import Category, Product
import random
# Проверяем, есть ли уже данные
if Category.objects.count() == 0:
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
            price=round(random.uniform(100, 1000), 2),
            quantity=random.randint(1, 50),
            category=random.choice(categories)
        )
    print('✅ Созданы тестовые данные')
else:
    print('✅ Данные уже существуют')
print(f'📊 Статистика: {Category.objects.count()} категорий, {Product.objects.count()} продуктов')
"
# Запуск сервера
echo -e "\n5. Запуск сервера Django..."
echo "================================="
echo "🌐 Сервер запущен по адресу: http://localhost:8000/"
echo ""
echo "📱 Доступные страницы:"
echo "   • Главная: http://localhost:8000/"
echo "   • Продукт #1: http://localhost:8000/product/1/"
echo "   • Категория #1: http://localhost:8000/category/1/products/"
echo ""
echo "🔧 Для остановки сервера нажмите Ctrl+C"
echo "================================="

py manage.py runserver
