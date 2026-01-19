from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL', blank=True)
    description = models.TextField(verbose_name='Описание')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
class Product(models.Model):
    # Статусы публикации
    class Status(models.TextChoices):
        MODERATION = 'moderation', 'На модерации'
        PUBLISHED = 'published', 'Опубликован'
        ARCHIVED = 'archived', 'В архиве'
    
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(
        upload_to='products/',
        verbose_name='Изображение',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='products'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    # Заменяем is_published на status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.MODERATION,
        verbose_name='Статус публикации'
    )
    
    # Новое поле: владелец
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Владелец',
        related_name='products'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']
        # Кастомные разрешения
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]
