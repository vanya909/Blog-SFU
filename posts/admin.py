from django.contrib import admin
from .models import Post, Comment, Like, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "only_for_group", "description")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "pub_date")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "user", "__str__")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
