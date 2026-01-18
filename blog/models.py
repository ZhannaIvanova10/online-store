from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    """Модель блоговой записи."""
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
        help_text='Введите заголовок статьи (макс. 200 символов)'
    )
    
    content = models.TextField(
        verbose_name='Содержимое',
        help_text='Введите текст статьи'
    )
    
    preview = models.ImageField(
        upload_to='blog/previews/',
        verbose_name='Превью (изображение)',
        blank=True,
        null=True,
        help_text='Загрузите изображение для превью статьи'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Признак публикации',
        help_text='Опубликовать статью?'
    )
    
    views_count = models.IntegerField(
        default=0,
        verbose_name='Количество просмотров',
        editable=False
    )
    
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL-адрес',
        help_text='Уникальная часть URL для статьи (латинские буквы, цифры, дефисы)'
    )
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """Возвращает URL для детального просмотра статьи."""
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        """Увеличивает счетчик просмотров на 1."""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'
        ordering = ['-created_at']
