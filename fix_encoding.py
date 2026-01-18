#!/usr/bin/env python3
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from blog.models import BlogPost

# Обновим статьи с правильной кодировкой
articles_data = [
    {
        'title': 'Как выбрать игровой ноутбук',
        'slug': 'how-to-choose-gaming-laptop',
        'content': '''Полное руководство по выбору игрового ноутбука. Рассмотрим процессоры, видеокарты, оперативную память и другие важные компоненты.''',
        'is_published': True,
        'views_count': 150,
    },
    {
        'title': 'Топ смартфонов 2024',
        'slug': 'top-smartphones-2024',
        'content': '''Обзор лучших смартфонов 2024 года. iPhone 15 Pro, Samsung Galaxy S24, Google Pixel 8 и другие.''',
        'is_published': True,
        'views_count': 90,
    },
    {
        'title': 'Будущее беспроводных наушников',
        'slug': 'future-wireless-headphones',
        'content': '''Тенденции развития беспроводных наушников в 2025 году. ИИ-шумоподавление, биометрические датчики и другие технологии.''',
        'is_published': True,
        'views_count': 45,
    },
]

# Обновим или создадим статьи
for data in articles_data:
    post, created = BlogPost.objects.update_or_create(
        slug=data['slug'],
        defaults=data
    )
    if created:
        print(f"Создана статья: {data['title']}")
    else:
        print(f"Обновлена статья: {data['title']}")

print(f"\nВсего статей: {BlogPost.objects.count()}")
print(f"Опубликовано: {BlogPost.objects.filter(is_published=True).count()}")
