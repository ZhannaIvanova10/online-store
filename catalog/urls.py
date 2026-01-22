from django.urls import path
from . import views
from .views import category_products

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', category_products, name='category_products'),
]
