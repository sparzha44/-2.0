from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from django.contrib.auth.models import User
from datetime import date

from django.shortcuts import render
from .models import Post

def index(request):
    keyword = request.GET.get('keyword', '')
    if keyword:
        # фильтр по наличию слова в тексте поста
        posts = Post.objects.filter(text__icontains=keyword).select_related('author', 'group')
    else:
        posts = Post.objects.all().select_related('author', 'group')
    context = {
        'posts': posts,
        'keyword': keyword,
    }
    return render(request, 'posts/index.html', context)

def group_posts(request, slug):
    """Страница с постами, отфильтрованными по группам"""
    # Функция get_object_or_404 получает по заданным критериям объект
    # из базы данных или возвращает сообщение об ошибке, если объект не найден.
    # В нашем случае в переменную group будут переданы объекты модели Group,
    # поле slug у которых соответствует значению slug в запросе
    group = get_object_or_404(Group, slug=slug)
    # Метод .filter позволяет ограничить поиск по критериям.
    # Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)

def search_posts(request):
    keyword = request.GET.get('keyword', '')
    results = []

    if keyword:
        # Получаем пользователя leo
        try:
            leo = User.objects.get(username='leo')
        except User.DoesNotExist:
            leo = None

        if leo:
            start_date = date(1854, 7, 7)
            end_date = date(1854, 7, 21)
            results = Post.objects.filter(
                author=leo,
                pub_date__range=(start_date, end_date),
                text__icontains=keyword
            )

    return render(request, 'posts/search_results.html', {'results': results, 'keyword': keyword})