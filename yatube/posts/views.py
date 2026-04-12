from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import date

from django.shortcuts import render
from .models import Post

def index(request):
    keyword = request.GET.get('keyword', '')
    if keyword:
        # фильтр по наличию слова в тексте поста
        post_list = Post.objects.filter(text__icontains=keyword).select_related('author', 'group').order_by('-pub_date')
    else:
        post_list = Post.objects.all().select_related('author', 'group').order_by('-pub_date')
    
    # Создаём паджинатор: показываем по 10 постов на странице
    paginator = Paginator(post_list, 10)
    
    # Из URL извлекаем номер запрошенной страницы
    page_number = request.GET.get('page')
    
    # Получаем набор постов для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'keyword': keyword,
    }
    return render(request, 'posts/index.html', context)

def group_posts(request, slug):
    """Страница с постами, отфильтрованными по группам"""
    group = get_object_or_404(Group, slug=slug)
    
    # Получаем все посты группы, отсортированные по дате (новые первыми)
    post_list = Post.objects.filter(group=group).order_by('-pub_date')
    
    # Создаём паджинатор: показываем по 10 постов на странице
    paginator = Paginator(post_list, 10)
    
    # Из URL извлекаем номер запрошенной страницы
    page_number = request.GET.get('page')
    
    # Получаем набор постов для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    
    context = {
        'group': group,
        'page_obj': page_obj,
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


# Пример защищённой функции: создание поста
# Декоратор @login_required работает как замыкание:
# он оборачивает функцию create_post() в проверку авторизации
@login_required(login_url='users:login')
def create_post(request):
    """
    Эта функция доступна только авторизованным пользователям.
    Если пользователь не авторизован, его перенаправит на login_url.
    
    Декоратор @login_required — это замыкание, которое:
    1. Проверяет request.user.is_authenticated
    2. Если False — перенаправляет на 'users:login'
    3. Если True — выполняет оригинальную функцию create_post()
    """
    if request.method == 'POST':
        # Обработка создания поста
        text = request.POST.get('text')
        group_id = request.POST.get('group')
        
        group = None
        if group_id:
            group = get_object_or_404(Group, id=group_id)
        
        post = Post.objects.create(
            author=request.user,
            text=text,
            group=group
        )
        return redirect('posts:index')
    
    groups = Group.objects.all()
    context = {'groups': groups}
    return render(request, 'posts/create_post.html', context)


# Пример другой защищённой функции: добавление комментария
@login_required(login_url='users:login')
def add_comment(request, post_id):
    """
    Добавление комментария доступно только авторизованным пользователям.
    """
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        # Здесь будет логика добавления комментария
        pass
    
    return redirect('posts:index')


def profile(request, username):
    """Страница профайла пользователя со всеми его постами"""
    author = get_object_or_404(User, username=username)
    
    # Получаем все посты автора, отсортированные по дате (новые первыми)
    post_list = Post.objects.filter(author=author).order_by('-pub_date')
    
    # Создаём паджинатор: показываем по 10 постов на странице
    paginator = Paginator(post_list, 10)
    
    # Из URL извлекаем номер запрошенной страницы
    page_number = request.GET.get('page')
    
    # Получаем набор постов для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    
    # Количество постов у автора
    post_count = post_list.count()
    
    context = {
        'author': author,
        'page_obj': page_obj,
        'post_count': post_count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Страница просмотра отдельного поста"""
    post = get_object_or_404(Post, id=post_id)
    
    # Количество постов у автора этого поста
    post_count = Post.objects.filter(author=post.author).count()
    
    context = {
        'post': post,
        'post_count': post_count,
    }
    return render(request, 'posts/post_detail.html', context)