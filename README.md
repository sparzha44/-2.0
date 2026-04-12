# Yatube - Социальная сеть блогеров

## Основная информация

Добро пожаловать в Yatube — платформу, созданную специально для блогеров и контент-мейкеров! Здесь ты можешь делиться своими постами, фото, историями и находить единомышленников.

### Что ты найдешь на Yatube:
- Публикация и просмотр постов
- Темы (группы) по интересам
- Личные блоги и истории
- Возможность набирать подписчиков и развивать свой бренд
- Обсуждения и комментарии
- Поиск по постам
- Постраничное навигация
- Система авторизации

### Почему выбирают Yatube:
- Удобный интерфейс
- Продвинутые инструменты для блогеров
- Сообщество единомышленников
- Безопасность и конфиденциальность

---

# Декораторы, Замыкания и @login_required в Yatube

## Как работает @login_required

Декоратор `@login_required` — это практическое применение концепции **замыканий**.

### Под капотом (упрощённо)

Когда вы пишете:

```python
@login_required(login_url='users:login')
def create_post(request):
    # код функции
    pass
```

Django создаёт замыкание по следующей схеме:

```python
def login_required(login_url):
    """Это обёртка - функция, которая возвращает функцию"""
    def decorator(view_func):
        """Это сам декоратор"""
        def wrapper(request, *args, **kwargs):
            """Это замыкание - оно "помнит" view_func и login_url"""
            
            # Проверка авторизации
            if not request.user.is_authenticated:
                # Перенаправление на страницу входа
                return redirect(login_url)
            
            # Если авторизован - выполняем оригинальную функцию
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator
```

### Области видимости в этом коде

1. **Глобальная область** — `login_required` видна везде
2. **Область login_required** — переменная `login_url` ("users:login")
3. **Область decorator** — переменная `view_func` (функция create_post)
4. **Область wrapper (замыкание)** — вложенная функция помнит и `view_func`, и `login_url`

### Пример замыкания из курса применён здесь

Помните пример с `speech()`?

```python
def speech(text, volume):
    def whisper():
        return f'{text.lower()}...'
    
    def scream():
        return f'{text.upper()}!!!11'
    
    if volume < 50:
        return whisper
    return scream

easy_closure = speech('Замыкание - это просто', 99)
print(easy_closure())  # ЗАМЫКАНИЕ - ЭТО ПРОСТО!!!11
```

Точно так же работает `@login_required`:
- Функция `login_required()` — это "фабрика"
- Она создаёт функции-обёртки, которые "помнят" исходную view-функцию
- Каждая защищённая функция получает свою уникальную обёртку

### Что изменилось в Yatube

Добавлены защищённые функции в `posts/views.py`:

```python
@login_required(login_url='users:login')
def create_post(request):
    # Доступна только авторизованным пользователям
    # Неавторизованные → redirect на 'users:login'
    pass

@login_required(login_url='users:login')
def add_comment(request, post_id):
    # Доступна только авторизованным пользователям
    pass
```

### Как Django использует замыкания

Когда вы обращаетесь к `http://127.0.0.1:8000/create/`:

1. Django вызывает `wrapper()` (функцию-обёртку)
2. `wrapper()` проверяет `request.user.is_authenticated`
3. Благодаря **замыканию**, `wrapper()` помнит исходную функцию `create_post`
4. Если пользователь авторизован → выполняется `create_post(request)`
5. Если нет → выполняется `redirect(login_url)`

### Контекст замыкания (enclosing scope)

В каждом замыкании сохраняется свой контекст:

```python
@login_required(login_url='users:login')
def create_post(request):
    pass

@login_required(login_url='users:profile')
def edit_post(request, post_id):
    pass
```

Каждая функция-обёртка "помнит" свой `login_url`, даже хотя `login_required()` давно закончила работу.

### Вложенные функции и области видимости

```python
@login_required(login_url='users:login')
def create_post(request):
    if request.method == 'POST':
        # локальная область видимости create_post
        text = request.POST.get('text')
        group_id = request.POST.get('group')
        
        group = None
        if group_id:  # вложенная область видимости
            group = get_object_or_404(Group, id=group_id)
        
        # group видна везде внутри create_post
        post = Post.objects.create(...)
        return redirect('posts:index')
```

Переменная `group` (локальная) — видна только внутри функции `create_post()`.
Переменная `Group` (глобальная) — импортирована и видна везде в модуле.

### Практическое применение

✅ Функции, которые должны быть защищены:
- `create_post()` — создание поста
- `add_comment()` — добавление комментария
- Редактирование своих постов
- Удаление своих постов

❌ Функции, которые НЕ защищены:
- `index()` — главная страница (видна всем)
- `group_posts()` — список постов группы (видна всем)
- `search_posts()` — поиск (видна всем)

Попробуйте обратиться к `/create/` без авторизации — вы будете перенаправлены на `/auth/login/`!

---

# Контекст-процессоры в Yatube

## Что произошло

В проекте Yatube создано приложение `core` с контекст-процессором `year`, который автоматически добавляет текущий год во все шаблоны проекта.

## Структура

```
yatube/
├── core/
│   ├── __init__.py
│   ├── apps.py
│   └── context_processors/
│       ├── __init__.py
│       └── year.py          # Наш контекст-процессор
├── posts/
├── users/
├── templates/
│   └── includes/
│       └── footer.html      # Использует {{ year }}
└── yatube/
    └── settings.py          # Зарегистрирован контекст-процессор
```

## Как это работает

### 1. Функция контекст-процессора

```python
# core/context_processors/year.py

def year(request):
    """
    Контекст-процессор — это просто функция, которая:
    1. Принимает на вход request
    2. Возвращает словарь с переменными для шаблонов
    """
    return {
        'year': datetime.now().year
    }
```

### 2. Регистрация в settings.py

```python
# yatube/settings.py

TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'core.context_processors.year.year',  # ← Вот наш
        ],
    },
}]
```

### 3. Использование в шаблонах

```html
<!-- templates/includes/footer.html -->
<footer>
  <p>© {{ year }} Copyright Yatube</p>    
</footer>
```

## Жизненный цикл контекст-процессора

```
Запрос к странице
        ↓
Django загружает шаблон
        ↓
Django вызывает ВСЕ контекст-процессоры из списка
        ↓
Каждый контекст-процессор возвращает словарь
        ↓
Все словари объединяются в один контекст
        ↓
Шаблон рендерится с этим контекстом
        ↓
{{ year }} доступна везде
```

## Почему это полезно

### ❌ Без контекст-процессора

```python
# views.py
def my_view(request):
    context = {
        'year': datetime.now().year,  # Повторяем в каждой view
    }
    return render(request, 'template.html', context)

def another_view(request):
    context = {
        'year': datetime.now().year,  # Повторяем опять...
    }
    return render(request, 'template.html', context)

# Ужасный паттерн DRY violation!
```

### ✅ С контекст-процессором

```python
# views.py - чистый код, без дублирования!
def my_view(request):
    return render(request, 'template.html')

def another_view(request):
    return render(request, 'template.html')

# {{ year }} доступна везде благодаря контекст-процессору
```

## Когда контекст-процессор вызывается?

Контекст-процессор вызывается **при каждом запросе**, перед рендерингом шаблона.

```
GET /posts/
    ↓
Django обрабатывает запрос
    ↓
Вызывает view-функцию
    ↓
View возвращает render(request, 'template.html', context)
    ↓
Django вызывает year() контекст-процессор
    ↓
year() возвращает {'year': 2026}
    ↓
Объединённый контекст: {**context, 'year': 2026}
    ↓
Шаблон рендерится с этим контекстом
```

## Примеры использования контекст-процессоров

### Пример 1: Глобальные настройки

```python
# core/context_processors/settings.py

def site_name(request):
    """Название сайта во всех шаблонах"""
    return {
        'site_name': 'Yatube',
        'site_email': 'info@yatube.ru',
    }
```

### Пример 2: Информация о версии

```python
# core/context_processors/version.py

def version(request):
    """Версия проекта"""
    return {
        'version': '1.0.0',
    }
```

### Пример 3: Информация о пользователе (уже встроена в Django)

```python
# django.contrib.auth.context_processors.auth

def auth(request):
    """Добавляет user в контекст"""
    return {
        'user': request.user,
    }
```

Благодаря этому в шаблонах доступны:
- `{{ user.username }}` — имя пользователя
- `{{ user.is_authenticated }}` — авторизован ли
- `{{ user.email }}` — email

## Лучшие практики

✅ **Делайте:**
- Один контекст-процессор — одна задача
- Давайте уникальные имена переменным
- Встраивайте контекст-процессоры в приложения (как мы с core)
- Документируйте, что возвращает каждый процессор

❌ **Не делайте:**
- Не создавайте один большой контекст-процессор
- Не вызывайте тяжёлые операции (БД запросы, файловые операции)
- Не используйте простые имена ('data', 'info', 'value')

## Использование в нашем проекте

Сейчас в шаблонах доступна переменная `{{ year }}` везде:

```html
<!-- Any template -->
© {{ year }} Copyright Yatube

<!-- Например в footer.html -->
<footer>
  <p>© {{ year }} Copyright <span style="color:red">Ya</span>tube</p>    
</footer>
```

При открытии любой страницы на сайте будет выведен текущий год из `datetime.now().year`.

---

# Паджинатор (Постраничное разбиение) в Yatube

## Что было сделано

Реализовано постраничное разбиение контента на главной странице и в группах. Теперь вместо того чтобы показывать все посты разом, сайт показывает их по 10 на странице с навигацией.

## Структура

```
templates/
├── posts/
│   ├── index.html
│   ├── group_list.html
│   └── includes/
│       └── paginator.html      ← Паджинатор (общий для всех списков)
posts/
└── views.py                    ← Обновлены functions с Paginator
```

## Как это работает

### 1. View-функция с Paginator

```python
# posts/views.py

from django.core.paginator import Paginator

def index(request):
    # Получаем все посты, отсортированные по дате
    post_list = Post.objects.all().order_by('-pub_date')
    
    # Создаём объект Paginator: показываем по 10 постов на странице
    paginator = Paginator(post_list, 10)
    
    # Из URL извлекаем номер запрошенной страницы (?page=2)
    page_number = request.GET.get('page')
    
    # Получаем объект Page с постами для запрошенной страницы
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'posts/index.html', context)
```

### 2. Что содержит page_obj

Объект `page_obj` — это экземпляр класса `Page`, который содержит:

```python
# Объект страницы
page_obj                           # <Page 2 of 5>

# Список объектов на текущей странице
page_obj.object_list              # [Post 11, Post 12, ..., Post 20]
# или используем for в шаблоне:
{% for post in page_obj %} ... {% endfor %}

# Удобно для шаблонов
page_obj.number                   # 2 (текущая страница)
page_obj.has_previous()           # True (есть предыдущая страница)
page_obj.has_next()               # True (есть следующая страница)
page_obj.previous_page_number()   # 1
page_obj.next_page_number()       # 3

# Полная информация о паджинаторе
page_obj.paginator.count          # 47 (всего постов)
page_obj.paginator.num_pages      # 5 (страниц всего)
page_obj.paginator.per_page       # 10 (постов на странице)
page_obj.paginator.page_range     # range(1, 6) - для цикла
```

### 3. HTML-шаблон (index.html)

```html
{% extends 'base.html' %}

{% block content %}
  <h1>Последние обновления на сайте</h1>
  
  <!-- Цикл по постам на текущей странице -->
  {% for post in page_obj %}
    <article>{{ post.text }}</article>
  {% empty %}
    <p>Нет постов.</p>
  {% endfor %}

  <!-- Включаем виджет паджинатора -->
  {% include 'posts/includes/paginator.html' %}
{% endblock %}
```

### 4. Паджинатор (paginator.html)

```html
{% if page_obj.has_other_pages %}
<nav class="pagination">
  <ul class="pagination">
    
    <!-- Кнопка "Первая" и "Предыдущая" -->
    {% if page_obj.has_previous %}
      <li><a href="?page=1">Первая</a></li>
      <li><a href="?page={{ page_obj.previous_page_number }}">Предыдущая</a></li>
    {% endif %}
    
    <!-- Номера страниц -->
    {% for i in page_obj.paginator.page_range %}
        {% if page_obj.number == i %}
          <li class="active">{{ i }}</li>
        {% else %}
          <li><a href="?page={{ i }}">{{ i }}</a></li>
        {% endif %}
    {% endfor %}
    
    <!-- Кнопка "Следующая" и "Последняя" -->
    {% if page_obj.has_next %}
      <li><a href="?page={{ page_obj.next_page_number }}">Следующая</a></li>
      <li><a href="?page={{ page_obj.paginator.num_pages }}">Последняя</a></li>
    {% endif %}
    
  </ul>
</nav>
{% endif %}
```

## Жизненный цикл паджинации

### Пример: Доступ к /posts/?page=2

```
1. Запрос к /posts/?page=2
        ↓
2. Django вызывает index(request)
        ↓
3. request.GET.get('page')  →  '2'
        ↓
4. paginator.get_page('2')  →  <Page 2 of 5>
        ↓
5. page_obj содержит посты 11-20
   page_obj.number = 2
   page_obj.has_previous() = True
   page_obj.has_next() = True
        ↓
6. Шаблон рендерится с page_obj
        ↓
7. {% for post in page_obj %} — итерирует посты 11-20
        ↓
8. paginator.html отображает:
   [Первая] [← Предыдущая] [1] [2*] [3] [4] [5] [Следующая →] [Последняя]
        ↓
9. Браузер показывает страницу 2
```

## URL параметры

Паджинатор использует GET-параметр `page`:

```
/                              # page=None → первая страница
/?page=1                       # Первая страница
/?page=2                       # Вторая страница
/group/cats/                   # Первая страница группы cats
/group/cats/?page=3            # Третья страница группы cats
/?keyword=python&page=2        # Вторая страница результатов поиска по "python"
```

## Изменения в представлениях

### До использования Paginator

```python
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)[:10]  # Жёсткий лимит 10
    
    context = {
        'group': group,
        'posts': posts,  # Список постов
    }
    return render(request, 'posts/group_list.html', context)
```

### После использования Paginator

```python
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by('-pub_date')
    
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'group': group,
        'page_obj': page_obj,  # Объект Page
    }
    return render(request, 'posts/group_list.html', context)
```

## Изменения в шаблонах

### До использования Paginator

```html
<!-- group_list.html -->
{% for post in posts %}  <!-- posts — это список -->
  <article>{{ post.text }}</article>
{% endfor %}
```

### После использования Paginator

```html
<!-- group_list.html -->
{% for post in page_obj %}  <!-- page_obj — это Page объект -->
  <article>{{ post.text }}</article>
{% endfor %}

<!-- Добавляем навигацию паджинатора -->
{% include 'posts/includes/paginator.html' %}
```

## Обработка граничных случаев

### Страница не существует

Если пользователь обратится к несуществующей странице (`?page=999`), `get_page()` вернёт последнюю страницу:

```python
paginator = Paginator([1, 2, 3], 1)  # 3 объекта, по 1 на странице
paginator.get_page(999)  # Вернёт последнюю страницу (3-я)
```

### Неверный параметр

Если `page` — не число:

```python
request.GET.get('page')  →  'abc'
paginator.get_page('abc')  # Вернёт первую страницу (1-я)
```

## Пример с поиском

Наш паджинатор работает и с поиском благодаря сохранению параметра:

```html
<!-- paginator.html, кнопка "Следующая" -->
<a href="?page={{ page_obj.next_page_number }}">Следующая</a>
<!-- Если был поиск: ?keyword=python&page=1
     Кликнуть по "Следующая" сохранит keyword и перейдёт на page=2 -->
```

Однако текущая версия paginator.html не сохраняет дополнительные параметры автоматически. Для полноты, можно обновить:

```html
<!-- Вариант с сохранением параметров -->
<a href="?keyword={{ keyword }}&page={{ page_obj.next_page_number }}">
  Следующая
</a>
```

## Интересные методы Paginator

```python
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

paginator = Paginator(Post.objects.all(), 10)

# Получить конкретную страницу (может выбросить исключение)
try:
    page = paginator.page(2)
except PageNotAnInteger:
    page = paginator.page(1)
except EmptyPage:
    page = paginator.page(paginator.num_pages)

# Получить страницу безопасно (рекомендуется)
page = paginator.get_page(2)  # Вернёт первую при ошибке
```

## Производительность

**Важно:** Пока список постов полностью загружается в память Python, паджинатор затем отбирает нужную часть. Для больших объёмов данных лучше использовать OFFSET/LIMIT на уровне базы данных или django-rest-framework.

```python
# Неоптимально для 1,000,000 постов
post_list = Post.objects.all()  # ← Загружает ВСЕ в память
paginator = Paginator(post_list, 10)

# Оптимально (но требует настройки)
# Использовать QuerySet напрямую или limit_offset_pagination
```

---

# Выделение найденных слов в поиске (Highlight)

## Выполняемый функционал

Реализована функция выделения найденного в поиске слова. Кастомный фильтр Django находит и подсвечивает совпадения в текстах постов.

## Структура

```
core/
├── templatetags/              ← Папка с кастомными фильтрами
│   ├── __init__.py
│   └── highlight.py           ← Фильтр для выделения текста
├── context_processors/
├── models.py
└── apps.py

templates/
└── posts/
    └── index.html             ← Обновлён для использования фильтра
```

## Как это работает

### 1. Кастомный фильтр Django

В Django можно создавать свои фильтры через `templatetags`. Фильтр — это функция, которая преобразует значение переменной в шаблоне.

```python
# core/templatetags/highlight.py

from django import template
import re

register = template.Library()

@register.filter
def highlight(text, keyword):
    """
    Преобразует текст, выделяя найденные слова жёлтым.
    
    Пример в шаблоне:
    {{ post.text|highlight:keyword }}
    """
    if not keyword or not text:
        return text
    
    # Регулярное выражение для поиска слова (без учёта регистра)
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    
    # Заменяем найденное слово на версию с HTML тегом <mark>
    highlighted = pattern.sub(
        lambda m: f'<mark style="background-color: yellow;">{m.group()}</mark>',
        text
    )
    
    return highlighted
```

### 2. Использование фильтра в шаблоне

```html
<!-- templates/posts/index.html -->

{% load highlight %}  {# Загружаем кастомный фильтр #}

{% for post in page_obj %}
  <!-- Применяем фильтр к тексту поста -->
  <p>{{ post.text|highlight:keyword|safe }}</p>
{% endfor %}
```

## Жизненный цикл выделения

### Пример: Поиск по слову "python"

```
1. Пользователь вводит "python" в поиск
        ↓
2. GET запрос: /?keyword=python&page=1
        ↓
3. Django вызывает index(request)
        ↓
4. view находит посты с "python":
   context = {
       'page_obj': page_obj,
       'keyword': 'python',  ← Передаём в шаблон
   }
        ↓
5. В шаблоне: {% load highlight %}
        ↓
6. {{ post.text|highlight:keyword|safe }}
        ↓
7. Фильтр highlight() ищет все "python" (без учёта регистра)
        ↓
8. Заменяет каждое на:
   <mark style="background-color: yellow;">python</mark>
        ↓
9. |safe разрешает рендерить HTML (не экранирует)
        ↓
10. Браузер отображает: "я люблю PYTHON"
                              ^^^^^^ жёлтый фон
```

## Как работают фильтры Django

### Базовый синтаксис

```django
{{ value|filter }}              {# Простой фильтр #}
{{ value|filter:argument }}     {# С аргументом #}
{{ value|filter1|filter2 }}     {# Цепочка фильтров #}
{{ value|filter:arg|safe }}     {# С safe #}
```

### Примеры встроенных фильтров

```django
{{ post.text|truncatewords:10 }}     {# Первые 10 слов #}
{{ post.pub_date|date:"d E Y" }}     {# Формат даты #}
{{ "hello"|upper }}                  {# Прописные буквы #}
{{ post.text|highlight:keyword|safe }} {# Наш фильтр #}
```

## Регулярные выражения в фильтре

```python
import re

# re.escape() - экранирует специальные символы
# Если пользователь ищет "(test)", то:
re.escape("(test)")  # → r"\(test\)"

# re.IGNORECASE - поиск без учёта регистра
# Ищет: Python, python, PYTHON, PyThOn
pattern = re.compile(r"python", re.IGNORECASE)

# lambda функция с pattern.sub()
pattern.sub(lambda m: f'<mark>{m.group()}</mark>', text)
# Заменяет каждое найденное совпадение (m.group()) на версию с <mark>
```

## Безопасность и |safe фильтр

### Зачем нужен |safe?

По умолчанию Django экранирует HTML в шаблонах для безопасности:

```
Без |safe:
{{ text }}  где text="Hello <script>alert('xss')</script>"
Вывод: Hello &lt;script&gt;alert('xss')&lt;/script&gt;

С |safe:
{{ text|safe }}
Вывод: Hello <script>alert('xss')</script>  ← ОПАСНО!
```

### Почему в нашем случае это безопасно?

1. **Мы контролируем содержимое тега**: Мы сами добавляем `<mark>`, не пользователь
2. **Текст поста экранирован**: В БД хранится исходный текст, не HTML
3. **keyword экранирован**: Используем `re.escape(keyword)` перед поиском

```python
# Даже если пользователь ищет "<script>", наш фильтр безопасен
keyword = "<script>"
re.escape(keyword)  # → r"\<script\>"
# Поиск будет за литеральный текст "<script>", а не за HTML
```

## Расширение функционала

### Вариант 1: Другой цвет выделения

```python
def highlight(text, keyword, color='yellow'):
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.sub(
        lambda m: f'<mark style="background-color: {color};">{m.group()}</mark>',
        text
    )
```

В шаблоне:
```django
{{ post.text|highlight:keyword:'red'|safe }}
```

### Вариант 2: CSS класс вместо inline стилей

```python
def highlight(text, keyword):
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.sub(
        lambda m: f'<mark class="search-highlight">{m.group()}</mark>',
        text
    )
```

### Вариант 3: Множественные слова

```python
def highlight_multiple(text, keywords_str):
    """Выделяет несколько слов (разделены запятыми)"""
    keywords = [k.strip() for k in keywords_str.split(',')]
    
    for keyword in keywords:
        if keyword:
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            text = pattern.sub(
                lambda m: f'<mark>{m.group()}</mark>',
                text
            )
    return text
```

## Производительность

**Важно:** Фильтр вызывается для каждого поста на странице. Если на странице 10 постов и текст каждого 10KB, то фильтр будет обрабатывать 100KB текста.

Для оптимизации можно:
1. Кешировать результаты выделения
2. Использовать полнотекстовый поиск БД (PostgreSQL, ElasticSearch)
3. Выделять только первые N символов текста

---

## Установка и использование

### Требования
- Python 3.9+
- Django 4.2
- SQLite3

### Как запустить

```bash
cd yatube
python manage.py migrate
python manage.py runserver
```

Сайт будет доступен по адресу: http://127.0.0.1:8000/

## Основные URL маршруты

- `/` — главная страница с постами
- `/group/<slug>/` — посты группы
- `/auth/login/` — вход
- `/auth/logout/` — выход
- `/auth/signup/` — регистрация
- `/auth/password_change/` — смена пароля
- `/auth/password_reset/` — восстановление пароля

## Функциональность

✅ Авторизация пользователей  
✅ Публикация постов (для авторизованных)  
✅ Группы (категории) постов  
✅ Поиск по постам  
✅ Постраничная навигация (10 постов на странице)  
✅ Адаптивный дизайн (Bootstrap)  
✅ Автоматический год в footer (контекст-процессор)  

---

**Присоединяйся и стань частью увлекательного мира блогинга на Yatube!**