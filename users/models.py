from django.db import models
from django.contrib.auth.models import AbstractUser


class Group(models.Model):
    title = models.CharField(verbose_name='название')
    slug = models.SlugField(unique=True, verbose_name='слаг')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class User(AbstractUser):
    image = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='аватарка'
    )
    group = models.ForeignKey(Group, related_name='users')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

