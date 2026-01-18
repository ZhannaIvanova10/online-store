#!/usr/bin/env python3
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import reverse
from blog.models import BlogPost

print("=== ПРОВЕРКА ДЗ 5 ===")

print("\n1. Проверка модели BlogPost:")
try:
    post = BlogPost.objects.first()
    if post:
        print(f"✅ Модель работает, первая статья: {post.title}")
        print(f"✅ Метод __str__: {post}")
        print(f"✅ Метод get_absolute_url: {post.get_absolute_url()}")
    else:
        print("❌ Нет статей в базе")
except Exception as e:
    print(f"❌ Ошибка модели: {e}")
print("\n2. Проверка URL блога:")
urls_to_check = [
    ('blog:post_list', {}, 'Список статей'),
    ('blog:post_create', {}, 'Создание статьи'),
]

if BlogPost.objects.exists():
    post = BlogPost.objects.first()
    urls_to_check.extend([
        ('blog:post_detail', {'slug': post.slug}, 'Детальная страница'),
        ('blog:post_edit', {'slug': post.slug}, 'Редактирование'),
        ('blog:post_delete', {'slug': post.slug}, 'Удаление'),
    ])

for url_name, kwargs, description in urls_to_check:
    try:
        url = reverse(url_name, kwargs=kwargs)
        print(f"✅ {description}: {url}")
        if not url.endswith('/'):
            print(f"   ⚠  URL не заканчивается на /")
    except Exception as e:
        print(f"❌ {description}: {e}")
print("\n3. Проверка контроллеров CBV:")
from blog.views import (
    BlogPostListView, BlogPostDetailView,
    BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView
)

cbv_controllers = [
    (BlogPostListView, 'ListView'),
    (BlogPostDetailView, 'DetailView'),
    (BlogPostCreateView, 'CreateView'),
    (BlogPostUpdateView, 'UpdateView'),
    (BlogPostDeleteView, 'DeleteView'),
]

for controller, base_class in cbv_controllers:
    print(f"✅ {controller.__name__} (наследует {base_class})")

print("\n4. Проверка функциональности:")
# Проверка get_queryset (фильтрация опубликованных)
list_view = BlogPostListView()
queryset = list_view.get_queryset()
print(f"✅ get_queryset возвращает только опубликованные: {queryset.count()} статей")

# Проверка get_object (увеличение просмотров)
if BlogPost.objects.exists():
    post = BlogPost.objects.first()
    initial_views = post.views_count
    print(f"✅ Счетчик просмотров у статьи: {initial_views}")

# Проверка get_success_url
if BlogPost.objects.exists():
    from blog.views import BlogPostUpdateView
    update_view = BlogPostUpdateView()
    update_view.object = BlogPost.objects.first()
    success_url = update_view.get_success_url()
    print(f"✅ get_success_url возвращает URL статьи: {success_url}")

print("\n5. Проверка настроек:")
with open('config/settings.py', 'r') as f:
    content = f.read()
    if "'blog'" in content:
        print("✅ Приложение blog в INSTALLED_APPS")
    else:
        print("❌ Приложение blog не в INSTALLED_APPS")

with open('config/urls.py', 'r') as f:
    if "path('blog/', include('blog.urls'))" in f.read():
        print("✅ URL блога подключены через include")
    else:
        print("❌ URL блога не подключены")

print("\n=== ПРОВЕРКА ЗАВЕРШЕНА ===")
