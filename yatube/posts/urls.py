from django.urls import path
from . import views
from datetime import date
from django.contrib.auth.models import User
from .models import Post

# Получаем пользователя leo
leo = User.objects.get(username='leo')

# Определяем диапазон дат
start_date = date(1854, 7, 7)
end_date = date(1854, 7, 21)

# Выполняем запрос
posts_with_keyword = Post.objects.filter(
    author=leo,
    pub_date__range=(start_date, end_date),
    text__icontains='утро'
)

# Для проверки можно вывести SQL-запрос
print(posts_with_keyword.query)

app_name = 'posts'  # Добавляем namespace для приложения

urlpatterns = [
    path('', views.index, name='index'),  # Добавляем name
    path('group/<slug:slug>/', views.group_posts, name='group_list'),  # Добавляем name
    path('search/', views.search_posts, name='search'),
]