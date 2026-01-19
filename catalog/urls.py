from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    category_products
)

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('category/<int:category_id>/products/', category_products, name='category_products'),
]
