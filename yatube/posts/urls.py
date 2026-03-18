from django.urls import path
from . import views

app_name = 'posts'  # Добавляем namespace для приложения

urlpatterns = [
    path('', views.index, name='index'),  # Добавляем name
    path('group/<slug:slug>/', views.group_posts, name='group_list'),  # Добавляем name
]