from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='post_list'),
    path('create/', views.BlogPostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/', views.BlogPostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/edit/', views.BlogPostUpdateView.as_view(), name='post_edit'),
    path('<slug:slug>/delete/', views.BlogPostDeleteView.as_view(), name='post_delete'),
]
