from django.db import models
from django.contrib.auth import get_user_model

from users.models import Group


class Post(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='группа'
    )
    title = models.CharField(max_length=120, verbose_name='название')
    descriptions = models.TextField(verbose_name='описание')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    update_date = models.DateTimeField(auto_now=True, db_index=True, verbose_name='дата обновления')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title
