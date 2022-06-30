from django.db import models
from django.contrib.auth import get_user_model


class Tag(models.Model):
    title = models.CharField(
        verbose_name='название',
        max_length=120,
        unique=True
    )


class Post(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='автор'
    )
    only_for_group = models.BooleanField(verbose_name='только для группы')
    description = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    update_date = models.DateTimeField(auto_now=True, db_index=True, verbose_name='дата обновления')
    tags = models.ManyToManyField(Tag, related_name='posts')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        return f"{self.description} - {self.author}"


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', verbose_name='Комментарий', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.post}, {self.author} - {self.text[:60]} ({self.pub_date.strftime("%Y-%m-%d %H:%M:%S")})'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='likes')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return f"{self.user} - {self.post}"
