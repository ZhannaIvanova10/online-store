from django.db import models

class Product(models.Model):
    """Модель товара."""
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', blank=True, null=True)
    stock = models.IntegerField(default=0, verbose_name='Количество на складе')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name
    
    def short_description(self):
        """Возвращает описание, обрезанное до 100 символов."""
        if len(self.description) > 100:
            return self.description[:100] + "..."
        return self.description

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
