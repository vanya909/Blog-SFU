from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.conf import settings

from .models import Post
from .forms import PostCreationForm, CommentCreationForm


def post_detail_view(request, pk):
    post = Post.objects.get(pk=pk)
    if post.only_for_group and post.author != request.user:
        return HttpResponseNotFound()
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': post.comments.all()})


@login_required(login_url='/users/login/')
def study_group_posts_view(request):
    user = request.user

    posts = get_objects_on_page(
        request=request,
        all_objects_list=Post.objects.filter(only_for_group=True, author__group=user.group),
        page_capacity=settings.MAX_POSTS_PER_PAGE
    )

    context = {
        'user': user,
        'posts': posts,
    }
    return render(request, 'posts/study_group.html', context)


@login_required(login_url='/users/login/')
def subscriptions_posts_view(request):
    user = request.user
    posts_ids = [post.id for subscription in user.following.all() for post in subscription.author.posts.all()]

    posts = get_objects_on_page(
        request=request,
        all_objects_list=Post.objects.filter(id__in=posts_ids).order_by('-pub_date'),
        page_capacity=settings.MAX_POSTS_PER_PAGE
    )

    context = {
        'user': user,
        'posts': posts,
    }
    return render(request, 'posts/subscriptions_posts.html', context)


@login_required(login_url='/users/login/')
def post_create_view(request):
    form = PostCreationForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.title = request.user.username
        post.save()
        return redirect('index')
    form = PostCreationForm()
    context = {'form': form}
    return render(request, 'posts/post_create.html', context)


@login_required(login_url='/users/login/')
def post_edit_view(request, post_pk):
    post = get_object_or_404(Post, id=post_pk)
    if post.author != request.user:
        return redirect(
            'post_detail',
            pk=post_pk
        )
    form = PostCreationForm(
        request.POST or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect(
            'post_detail',
            pk=post_pk
        )
    context = {
        'author': post.author,
        'post': post,
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)


@login_required(login_url='/users/login/')
def post_delete_view(request, post_pk):
    post = get_object_or_404(Post, id=post_pk)
    if post.author != request.user:
        return HttpResponseNotFound()
    if request.method == 'POST':
        post.delete()
        return redirect('/')
    return render(request, 'posts/post_delete.html', {'pk': post_pk})


@login_required(login_url='/users/login/')
def comment_create_view(request, post_pk):
    if request.method == 'POST':
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = get_object_or_404(Post, pk=post_pk)
            comment.save()
            return redirect('post_detail', pk=post_pk)
    form = CommentCreationForm()
    context = {'form': form}
    return render(request, 'posts/comment_create.html', context)


def get_objects_on_page(request, all_objects_list, page_capacity):
    paginator = Paginator(all_objects_list, page_capacity)
    return paginator.get_page(request.GET.get('page'))
