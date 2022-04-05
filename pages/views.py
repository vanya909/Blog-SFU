from django.shortcuts import render
from django.conf import settings

from posts.models import Post
from posts.views import get_objects_on_page


def index_view(request):
    posts = get_objects_on_page(
        request=request,
        all_objects_list=Post.objects.filter(only_for_group=False),
        page_capacity=settings.MAX_POSTS_PER_PAGE
    )
    return render(request, 'pages/index.html', context={'posts': posts})
