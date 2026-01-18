from blog.models import BlogPost
# Удалим старые данные
BlogPost.objects.all().delete()
# Создадим тестовые статьи
articles = [
    {
        'title': 'Как выбрать игровой ноутбук',
        'slug': 'how-to-choose-gaming-laptop',
        'content': 'Полное руководство по выбору игрового ноутбука...',
        'is_published': True,
        'views_count': 150,
    },
    {
        'title': 'Топ смартфонов 2024',
        'slug': 'top-smartphones-2024',
        'content': 'Обзор лучших смартфонов года...',
        'is_published': True,
        'views_count': 89,
    },
    {
        'title': 'Черновик статьи',
        'slug': 'draft-article',
        'content': 'Это черновик статьи...',
        'is_published': False,
        'views_count': 3,
    },
]

for data in articles:
    BlogPost.objects.create(**data)
    print(f"Создана статья: {data['title']}")

print(f"Всего статей: {BlogPost.objects.count()}")
print(f"Опубликовано: {BlogPost.objects.filter(is_published=True).count()}")
