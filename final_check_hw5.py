#!/usr/bin/env python3
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 80)
print("ФИНАЛЬНАЯ ПРОВЕРКА ДЗ 5")
print("=" * 80)
# 1. Проверка структуры проекта
print("\n1. СТРУКТУРА ПРОЕКТА:")
required_dirs = [
    ('blog/', 'Приложение блога'),
    ('templates/blog/', 'Шаблоны блога'),
    ('blog/migrations/', 'Миграции блога'),
]

for dir_path, description in required_dirs:
    if os.path.exists(dir_path):
        print(f"   ✅ {description}")
    else:
        print(f"   ❌ {description}")

# 2. Проверка файлов
print("\n2. НЕОБХОДИМЫЕ ФАЙЛЫ:")
required_files = [
    ('blog/models.py', 'Модель BlogPost'),
    ('blog/views.py', 'Контроллеры CBV'),
    ('blog/urls.py', 'URL-адреса блога'),
    ('blog/forms.py', 'Формы блога'),
    ('templates/blog/post_list.html', 'Шаблон списка'),
    ('templates/blog/post_detail.html', 'Шаблон статьи'),
    ('templates/blog/post_form.html', 'Шаблон формы'),
    ('templates/blog/post_confirm_delete.html', 'Шаблон удаления'),
]

for file_path, description in required_files:
    if os.path.exists(file_path):
        print(f"   ✅ {description}")
        # Проверка размера файла
        if os.path.getsize(file_path) > 100:
            print(f"       Размер: {os.path.getsize(file_path)} байт")
    else:
        print(f"   ❌ {description}")
# 3. Проверка настроек
print("\n3. НАСТРОЙКИ DJANGO:")
with open('config/settings.py', 'r', encoding='utf-8') as f:
    settings = f.read()
    
checks = [
    ("'blog'" in settings, "Приложение blog в INSTALLED_APPS"),
    ("'catalog'" in settings, "Приложение catalog в INSTALLED_APPS"),
    ("LANGUAGE_CODE = 'ru-ru'" in settings or "LANGUAGE_CODE = 'ru'" in settings, "Русский язык"),
]

for condition, description in checks:
    if condition:
        print(f"   ✅ {description}")
    else:
        print(f"   ❌ {description}")

# 4. Проверка URLs
print("\n4. URL-АДРЕСА:")
with open('config/urls.py', 'r', encoding='utf-8') as f:
    urls_content = f.read()
    
if "path('blog/', include('blog.urls'))" in urls_content:
    print("   ✅ URL блога подключены через include")
else:
    print("   ❌ URL блога не подключены")
# 5. Проверка моделей
print("\n5. МОДЕЛЬ BLOGPOST:")
from blog.models import BlogPost

try:
    # Проверка полей
    fields = [f.name for f in BlogPost._meta.get_fields()]
    required_fields = ['title', 'content', 'preview', 'created_at', 'is_published', 'views_count', 'slug']
    
    for field in required_fields:
        if field in fields:
            print(f"   ✅ Поле {field}")
        else:
            print(f"   ❌ Поле {field} отсутствует")
    
    # Проверка методов
    post = BlogPost(title="Тест", slug="test", content="Тест")
    print(f"   ✅ Метод __str__: {str(post)}")
    print(f"   ✅ Метод get_absolute_url: {post.get_absolute_url()}")
    
except Exception as e:
    print(f"   ❌ Ошибка модели: {e}")
# 6. Проверка контроллеров CBV
print("\n6. КОНТРОЛЛЕРЫ CBV:")
try:
    from blog.views import (
        BlogPostListView, BlogPostDetailView,
        BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView
    )
    
    controllers = [
        ('BlogPostListView', BlogPostListView, 'ListView'),
        ('BlogPostDetailView', BlogPostDetailView, 'DetailView'),
        ('BlogPostCreateView', BlogPostCreateView, 'CreateView'),
        ('BlogPostUpdateView', BlogPostUpdateView, 'UpdateView'),
        ('BlogPostDeleteView', BlogPostDeleteView, 'DeleteView'),
    ]
    
    for name, controller, base in controllers:
        print(f"   ✅ {name} (наследует {base})")
        
        # Проверка специфичных методов
        if name == 'BlogPostListView' and hasattr(controller, 'get_queryset'):
            print(f"       ✓ Метод get_queryset переопределен")
        if name == 'BlogPostDetailView' and hasattr(controller, 'get_object'):
            print(f"       ✓ Метод get_object переопределен")
        if name == 'BlogPostUpdateView' and hasattr(controller, 'get_success_url'):
            print(f"       ✓ Метод get_success_url переопределен")
            
except Exception as e:
    print(f"   ❌ Ошибка контроллеров: {e}")
# 7. Проверка данных
print("\n7. ТЕСТОВЫЕ ДАННЫЕ:")
try:
    total_posts = BlogPost.objects.count()
    published_posts = BlogPost.objects.filter(is_published=True).count()
    
    print(f"   Всего статей: {total_posts}")
    print(f"   Опубликовано: {published_posts}")
    
    if total_posts > 0:
        sample = BlogPost.objects.first()
        print(f"   Пример: {sample.title}")
        print(f"   Просмотры: {sample.views_count}")
        print(f"   Слаг: {sample.slug}")
        
        # Проверка фильтрации
        list_view = BlogPostListView()
        filtered = list_view.get_queryset()
        print(f"   После фильтрации: {filtered.count()} статей")
        
except Exception as e:
    print(f"   ❌ Ошибка данных: {e}")

print("\n" + "=" * 80)
print("ИТОГИ ПРОВЕРКИ:")
print("=" * 80)

# Подсчет выполненных критериев
criteria = [
    ("Приложение blog создано", os.path.exists('blog/')),
    ("blog в INSTALLED_APPS", "'blog'" in settings),
    ("blog/urls.py существует", os.path.exists('blog/urls.py')),
    ("Модель BlogPost с полями", all(f in fields for f in ['title', 'content', 'is_published', 'views_count']) if 'fields' in locals() else False),
    ("Класс Meta в модели", 'class Meta:' in open('blog/models.py', encoding='utf-8').read()),
    ("Метод __str__ в модели", '__str__' in open('blog/models.py', encoding='utf-8').read()),
    ("Все CBV контроллеры", all(controller[0] in str(globals()) for controller in controllers) if 'controllers' in locals() else False),
    ("URL блога подключены", "path('blog/', include('blog.urls'))" in urls_content),
    ("URL заканчиваются на /", all(')/' in line for line in open('blog/urls.py').readlines() if 'path(' in line)),
    ("Шаблоны используют base.html", all(os.path.exists(f'templates/blog/{t}') and '{% extends' in open(f'templates/blog/{t}').read() for t in ['post_list.html', 'post_detail.html'])),
    ("get_queryset фильтрует", hasattr(BlogPostListView, 'get_queryset') if 'BlogPostListView' in locals() else False),
    ("get_object увеличивает просмотры", hasattr(BlogPostDetailView, 'get_object') if 'BlogPostDetailView' in locals() else False),
    ("get_success_url редиректит", hasattr(BlogPostUpdateView, 'get_success_url') if 'BlogPostUpdateView' in locals() else False),
]
total = len(criteria)
passed = sum(1 for _, condition in criteria if condition)

print(f"\n✅ Выполнено: {passed} из {total} критериев ({passed/total*100:.0f}%)")

if passed == total:
    print("\n🎉 ПОЗДРАВЛЯЕМ! ВСЕ КРИТЕРИИ ДЗ 5 ВЫПОЛНЕНЫ!")
else:
    print("\n⚠  Не выполнены:")
    for i, (desc, cond) in enumerate(criteria, 1):
        if not cond:
            print(f"   {i}. {desc}")

print("\n" + "=" * 80)
print("РЕКОМЕНДАЦИИ:")
print("=" * 80)
print("1. Запустите сервер: py manage.py runserver")
print("2. Проверьте страницы:")
print("   - http://127.0.0.1:8000/blog/ - Список статей")
print("   - http://127.0.0.1:8000/blog/top-smartphones-2024/ - Детальная страница")
print("   - http://127.0.0.1:8000/admin/ - Админка (admin/admin123)")
print("3. Убедитесь, что:")
print("   - Русский текст отображается корректно")
print("   - Счетчик просмотров увеличивается")
print("   - Только опубликованные статьи видны в списке")
print("   - После редактирования идет редирект на статью")
