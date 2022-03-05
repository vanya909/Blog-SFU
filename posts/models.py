from django.db import models
from django.contrib.auth import get_user_model

from users.models import Group


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL, related_name='posts')
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    descriptions = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return self.title
