from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Product, Category
from .forms import ProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        # ЗАМЕНЯЕМ is_published=True на status='published'
        return queryset.filter(status='published').select_related('category', 'owner')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        # Показываем продукт даже если он не опубликован, 
        # но с проверкой прав
        return Product.objects.all()


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание нового продукта'
        return context
    
    def form_valid(self, form):
        # Автоматически назначаем владельца
        form.instance.owner = self.request.user
        messages.success(self.request, 'Продукт успешно создан!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    
    def test_func(self):
        # Проверяем: только владелец может редактировать
        product = self.get_object()
        return self.request.user == product.owner
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование продукта'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Продукт успешно обновлен!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    context_object_name = 'product'
    
    def test_func(self):
        product = self.get_object()
        user = self.request.user
        
        # Владелец может удалить
        if user == product.owner:
            return True
        
        # Модератор может удалить если у него есть право delete_product
        if user.has_perm('catalog.delete_product'):
            return True

        return False
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Продукт успешно удален!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('catalog:product_list')


# Новая функция для отмены публикации
@login_required
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Проверка прав: модератор ИЛИ владелец
    has_permission = (
        request.user.has_perm('catalog.can_unpublish_product') or 
        request.user == product.owner
    )
    
    if not has_permission:
        raise PermissionDenied("У вас нет прав для отмены публикации")
    
    # Отменяем публикацию (меняем статус на moderation)
    product.status = Product.Status.MODERATION
    product.save()
    messages.success(request, 'Публикация продукта отменена!')
    
    return redirect('catalog:product_detail', pk=pk)
