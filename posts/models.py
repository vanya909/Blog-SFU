from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='автор'
    )
    only_for_group = models.BooleanField(verbose_name='только для группы')
    title = models.CharField(max_length=120, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    update_date = models.DateTimeField(auto_now=True, db_index=True, verbose_name='дата обновления')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
