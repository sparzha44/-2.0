from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        blank=True,  # Может быть пустым в формах
        null=True,   # Может быть NULL в базе данных
        related_name='posts'  # Позволит из группы получать все посты группы
    )

    def __str__(self):
        # выводим текст поста
        return self.text

class Group(models.Model):
    title = models.CharField(max_length=200)  # Название группы
    slug = models.SlugField(unique=True)      # Уникальный адрес для URL
    description = models.TextField()           # Описание группы

    def __str__(self):
        # При печати объекта Group будет выводиться его название
        return self.title