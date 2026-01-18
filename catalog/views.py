from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from .models import Product

class HomeView(ListView):
    """Контроллер для главной страницы."""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        """Получаем все товары для главной страницы."""
        print("=== ДОМАШНЯЯ РАБОТА: HomeView вызван! ===")
        return Product.objects.all()

class ProductDetailView(DetailView):
    """Контроллер для страницы одного товара."""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ContactsView(TemplateView):
    """Контроллер для страницы контактов."""
    template_name = 'catalog/contacts.html'
    def post(self, request, *args, **kwargs):
        """Обработка POST запроса из формы контактов."""
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        print(f"Получено сообщение от {name} ({email}): {message}")
        messages.success(request, 'Сообщение успешно отправлено!')
        return render(request, self.template_name)
