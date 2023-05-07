from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
from django.core.cache import cache

from posts.models import Post
from posts.views import get_objects_on_page


def index_view(request):
    search_request = request.GET.get('search')

    if search_request:
        complex_filter = Q(description__icontains=search_request) \
            | Q(author__username__icontains=search_request)
        if request.user.is_anonymous:
            complex_filter &= Q(only_for_group=False)
        else:
            complex_filter &= Q(only_for_group=False) | Q(author__group=request.user.group)
        relevant_posts = Post.objects.filter(complex_filter)
        page_title = 'Поиск'
    else:
        relevant_posts = cache.get('index_page')
        if relevant_posts is None:
            relevant_posts = Post.objects.filter(only_for_group=False)
            cache.set('index_page', relevant_posts, timeout=0)
        page_title = 'Домашняя страница'

    posts = get_objects_on_page(
        request=request,
        all_objects_list=relevant_posts,
        page_capacity=settings.MAX_POSTS_PER_PAGE
    )

    return render(
        request,
        'pages/index.html',
        context={
            'posts': posts,
            'page_title': page_title,
            'search_request': search_request
        }
    )
