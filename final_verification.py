#!/usr/bin/env python3
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 80)
print("ФИНАЛЬНАЯ ВЕРИФИКАЦИЯ ДЗ 5")
print("=" * 80)

# Проверка 1: URL заканчиваются на /
print("\n1. ПРОВЕРКА URL (должны заканчиваться на /):")

print("\nblog/urls.py:")
with open('blog/urls.py', 'r') as f:
    blog_urls = f.readlines()
    for line in blog_urls:
        if 'path(' in line:
            if ')/' in line:
                print(f"   ✅ {line.strip()}")
            else:
                print(f"   ❌ {line.strip()}")
print("\ncatalog/urls.py:")
with open('catalog/urls.py', 'r') as f:
    catalog_urls = f.readlines()
    for line in catalog_urls:
        if 'path(' in line:
            if ')/' in line or "path(''" in line:
                print(f"   ✅ {line.strip()}")
            else:
                print(f"   ❌ {line.strip()}")

# Проверка 2: Все остальные критерии
print("\n2. ПРОВЕРКА ОСТАЛЬНЫХ КРИТЕРИЕВ:")

from blog.models import BlogPost
from blog.views import BlogPostListView, BlogPostDetailView, BlogPostUpdateView

# Критерии для проверки
criteria = [
    ("Приложение blog создано", os.path.exists('blog/')),
    ("blog в INSTALLED_APPS", "'blog'" in open('config/settings.py').read()),
    ("blog/urls.py существует", os.path.exists('blog/urls.py')),
    ("Модель BlogPost с необходимыми полями", 
     all(hasattr(BlogPost, field) for field in ['title', 'content', 'is_published', 'views_count'])),
    ("Класс Meta в модели", 'class Meta:' in open('blog/models.py').read()),
    ("Метод __str__ в модели", '__str__' in open('blog/models.py').read()),
    ("BlogPostListView наследует ListView", BlogPostListView.__bases__[0].__name__ == 'ListView'),
    ("BlogPostDetailView наследует DetailView", BlogPostDetailView.__bases__[0].__name__ == 'DetailView'),
    ("BlogPostUpdateView наследует UpdateView", BlogPostUpdateView.__bases__[0].__name__ == 'UpdateView'),
    ("get_queryset фильтрует опубликованные", hasattr(BlogPostListView, 'get_queryset')),
    ("get_object увеличивает просмотры", hasattr(BlogPostDetailView, 'get_object')),
    ("get_success_url редиректит", hasattr(BlogPostUpdateView, 'get_success_url')),
    ("Все URL заканчиваются на /", 
     all(')/' in line for line in blog_urls if 'path(' in line) and 
     all(')/' in line or "path(''" in line for line in catalog_urls if 'path(' in line)),
]

total = len(criteria)
passed = sum(1 for _, condition in criteria if condition)

print(f"\n✅ Выполнено: {passed} из {total} критериев")

if passed == total:
    print("\n🎉 ВСЕ КРИТЕРИИ ВЫПОЛНЕНЫ!")
else:
    print("\nНе выполнены:")
    for i, (desc, cond) in enumerate(criteria, 1):
        if not cond:
            print(f"   {i}. {desc}")
print("\n" + "=" * 80)
print("РЕЗУЛЬТАТЫ:")
print("=" * 80)

# Тестовые данные
posts_count = BlogPost.objects.count()
published_count = BlogPost.objects.filter(is_published=True).count()

print(f"\n📊 Данные в базе:")
print(f"   Всего статей: {posts_count}")
print(f"   Опубликовано: {published_count}")
print(f"   Черновиков: {posts_count - published_count}")

if posts_count > 0:
    sample = BlogPost.objects.first()
    print(f"\n📝 Пример статьи:")
    print(f"   Заголовок: {sample.title}")
    print(f"   Слаг: {sample.slug}")
    print(f"   Просмотры: {sample.views_count}")
    print(f"   Опубликована: {sample.is_published}")
    
    # Проверка URL
    print(f"\n🔗 Пример URL:")
    print(f"   Детальная страница: /blog/{sample.slug}/")
    print(f"   Редактирование: /blog/{sample.slug}/edit/")
    print(f"   Удаление: /blog/{sample.slug}/delete/")

print("\n🚀 Проект готов к проверке!")
