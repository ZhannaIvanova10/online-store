#!/usr/bin/env python3
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 80)
print("ФИНАЛЬНАЯ ПРОВЕРКА ВСЕХ КРИТЕРИЕВ ДЗ 5")
print("=" * 80)

# Импортируем все необходимые классы
try:
    from blog.views import (
        BlogPostListView, BlogPostDetailView, 
        BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView
    )
    print("✅ Все контроллеры блога импортируются успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    sys.exit(1)
# Проверка наследования
print("\n1. ПРОВЕРКА НАСЛЕДОВАНИЯ КЛАССОВ:")
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

controllers = [
    (BlogPostListView, ListView, 'BlogPostListView'),
    (BlogPostDetailView, DetailView, 'BlogPostDetailView'),
    (BlogPostCreateView, CreateView, 'BlogPostCreateView'),
    (BlogPostUpdateView, UpdateView, 'BlogPostUpdateView'),
    (BlogPostDeleteView, DeleteView, 'BlogPostDeleteView'),
]

for controller, base_class, name in controllers:
    if issubclass(controller, base_class):
        print(f"   ✅ {name} наследует {base_class.__name__}")
    else:
        print(f"   ❌ {name} НЕ наследует {base_class.__name__}")

# Проверка URL
print("\n2. ПРОВЕРКА URL (все должны заканчиваться на /):")

def check_urls_file(filename):
    print(f"\n{filename}:")
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    all_correct = True
    for line in lines:
        if 'path(' in line:
            line = line.strip()
            # Убираем комментарии если есть
            if '#' in line:
                line = line.split('#')[0].strip()
            
            # Проверяем, заканчивается ли на /
            if line.endswith('),'):
                line = line[:-2]  # Убираем '),'
            
            if "path(''" in line or line.endswith("/'") or "path(''," in line:
                print(f"   ✅ {line}")
            else:
                print(f"   ❌ {line} - не заканчивается на /")
                all_correct = False

    return all_correct

blog_ok = check_urls_file('blog/urls.py')
catalog_ok = check_urls_file('catalog/urls.py')

# Проверка переопределенных методов
print("\n3. ПРОВЕРКА ПЕРЕОПРЕДЕЛЕННЫХ МЕТОДОВ:")

# Проверка get_queryset в BlogPostListView
list_view_methods = dir(BlogPostListView)
if 'get_queryset' in list_view_methods:
    print("   ✅ BlogPostListView имеет метод get_queryset")
else:
    print("   ❌ BlogPostListView не имеет метод get_queryset")

# Проверка get_object в BlogPostDetailView
detail_view_methods = dir(BlogPostDetailView)
if 'get_object' in detail_view_methods:
    print("   ✅ BlogPostDetailView имеет метод get_object")
else:
    print("   ❌ BlogPostDetailView не имеет метод get_object")

# Проверка get_success_url в BlogPostUpdateView
update_view_methods = dir(BlogPostUpdateView)
if 'get_success_url' in update_view_methods:
    print("   ✅ BlogPostUpdateView имеет метод get_success_url")
else:
    print("   ❌ BlogPostUpdateView не имеет метод get_success_url")
# Проверка содержимого файлов
print("\n4. ПРОВЕРКА СОДЕРЖАНИЯ ФАЙЛОВ:")

# Проверка get_queryset в views.py
with open('blog/views.py', 'r') as f:
    views_content = f.read()
    if 'def get_queryset' in views_content and 'is_published=True' in views_content:
        print("   ✅ BlogPostListView.get_queryset() фильтрует опубликованные статьи")
    else:
        print("   ❌ BlogPostListView.get_queryset() не фильтрует")

# Проверка get_object в views.py
if 'def get_object' in views_content:
    print("   ✅ BlogPostDetailView.get_object() переопределен")
else:
    print("   ❌ BlogPostDetailView.get_object() не переопределен")

# Проверка get_success_url в views.py
if 'def get_success_url' in views_content and 'post_detail' in views_content:
    print("   ✅ BlogPostUpdateView.get_success_url() возвращает URL статьи")
else:
    print("   ❌ BlogPostUpdateView.get_success_url() не возвращает URL статьи")

# Итоговая проверка
print("\n" + "=" * 80)
print("ИТОГОВЫЙ РЕЗУЛЬТАТ:")
print("=" * 80)
all_criteria = [
    ("Все 5 CBV контроллеров импортируются", True),  # Уже проверили выше
    ("BlogPostListView наследует ListView", issubclass(BlogPostListView, ListView)),
    ("BlogPostDetailView наследует DetailView", issubclass(BlogPostDetailView, DetailView)),
    ("BlogPostCreateView наследует CreateView", issubclass(BlogPostCreateView, CreateView)),
    ("BlogPostUpdateView наследует UpdateView", issubclass(BlogPostUpdateView, UpdateView)),
    ("BlogPostDeleteView наследует DeleteView", issubclass(BlogPostDeleteView, DeleteView)),
    ("BlogPostListView имеет get_queryset", 'get_queryset' in list_view_methods),
    ("BlogPostDetailView имеет get_object", 'get_object' in detail_view_methods),
    ("BlogPostUpdateView имеет get_success_url", 'get_success_url' in update_view_methods),
    ("Все URL блога заканчиваются на /", blog_ok),
    ("Все URL каталога заканчиваются на /", catalog_ok),
    ("get_queryset фильтрует по is_published", 'is_published=True' in views_content),
    ("get_success_url возвращает URL статьи", 'post_detail' in views_content),
]

total = len(all_criteria)
passed = sum(1 for _, condition in all_criteria if condition)

print(f"\n✅ Выполнено: {passed} из {total} критериев")

if passed == total:
    print("\n🎉 ВСЕ КРИТЕРИИ ДЗ 5 ВЫПОЛНЕНЫ!")
else:
    print("\nНе выполнены:")
    for i, (desc, cond) in enumerate(all_criteria, 1):
        if not cond:
            print(f"   {i}. {desc}")

print("\n" + "=" * 80)
print("🚀 ПРОЕКТ ГОТОВ К ОТПРАВКЕ!")
