from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    # Добавьте другие URL-адреса по мере необходимости
]
