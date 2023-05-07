from django.db import models
from django.contrib.auth.models import AbstractUser


class StudyGroup(models.Model):
    title = models.CharField(
        verbose_name='название',
        max_length=120,
        unique=True
    )

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'

    def __str__(self):
        return self.title


class User(AbstractUser):
    group = models.ForeignKey(
        StudyGroup,
        related_name='users',
        verbose_name='Группа',
        null=True,
        on_delete=models.SET_NULL
    )
    first_name = models.CharField(max_length=120, verbose_name='Имя')
    second_name = models.CharField(max_length=120, verbose_name='Фамилия')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.username} --> {self.author.username}'
