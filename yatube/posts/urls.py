from django.urls import path
from . import views
from datetime import date
from django.contrib.auth.models import User
from .models import Post

app_name = 'posts'  # Добавляем namespace для приложения

urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('search/', views.search_posts, name='search'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
]