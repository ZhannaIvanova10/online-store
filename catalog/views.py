from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Product

# Кэшируем список товаров на 5 минут (300 секунд)
@method_decorator(cache_page(300), name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

# Кэшируем детали товара на 10 минут
@method_decorator(cache_page(600), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

# Не кэшируем формы создания/редактирования
class ProductCreateView(CreateView):
    model = Product
    template_name = 'catalog/product_form.html'
    fields = ['name', 'description', 'price']
    success_url = reverse_lazy('catalog:product_list')

def category_products(request, category_id):
    """
    Представление для отображения продуктов в категории.
    Использует низкоуровневое кэширование через сервисную функцию.
    """
    from .services import get_products_in_category
    
    products = get_products_in_category(category_id)
    
    # Определяем название категории
    category_name = f"Категория {category_id}"
    context = {
        'products': products,
        'category_id': category_id,
        'category_name': category_name
    }
    
    return render(request, 'catalog/category_products.html', context)

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'catalog/product_form.html'
    fields = ['name', 'description', 'price']
    success_url = reverse_lazy('catalog:product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .services import get_all_cached_products_safe as get_all_cached_products

@cache_page(60 * 5)  # Кешировать главную на 5 минут
def home(request):
    """
    Главная страница со списком всех продуктов
    Использует низкоуровневое кеширование через get_all_cached_products
    """
    products = get_all_cached_products()
    
    context = {
        'products': products,
        'title': '🏪 Онлайн-магазин - Главная страница',
        'category_name': 'Все категории',
        'cache_info': 'Используется двухуровневое кеширование: '
                     '1) cache_page для всей страницы (5 мин) '
                     '2) get_all_cached_products для данных (30 мин)'
    }
    
    return render(request, 'catalog/product_list.html', context)
