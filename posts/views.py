from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post


@login_required(login_url='/users/login/')
def study_group_posts(request):
    user = request.user
    posts = Post.objects.filter(only_for_group=True, author__group=user.group)
    context = {
        'user': user,
        'posts': posts
    }
    return render(request, 'posts/study_group.html', context)


