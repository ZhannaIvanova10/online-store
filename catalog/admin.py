from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')  # Поля в списке
    list_filter = ('created_at',)                   # Фильтр по дате
    search_fields = ('name', 'description')         # Поиск по названию и описанию
    ordering = ('-created_at',)                     # Сортировка (новые сверху)
