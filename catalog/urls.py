from django.urls import path
from . import views

app_name = 'catalog'  # Пространство имен для маршрутов

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/products/', views.category_products, name='category_products'),
]
