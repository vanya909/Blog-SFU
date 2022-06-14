from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.conf import settings

from .models import Post, Comment, Like
from .forms import PostCreationForm, CommentCreationForm
from users.models import User


def get_objects_on_page(request, all_objects_list, page_capacity):
    paginator = Paginator(all_objects_list, page_capacity)
    return paginator.get_page(request.GET.get('page'))


def post_detail_view(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.only_for_group and post.author.group != request.user.group:
        return HttpResponseNotFound()
    comments = post.comments.all()
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'posts/post_templates/post_detail.html', context)


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

    authors = [sub.author for sub in user.following.all()]

    posts = get_objects_on_page(
        request=request,
        all_objects_list=Post.objects.filter(author__in=authors).filter(only_for_group=False).order_by('-pub_date'),
        page_capacity=settings.MAX_POSTS_PER_PAGE
    )

    context = {
        'user': user,
        'posts': posts,
        'authors': authors,
    }
    return render(request, 'posts/subscriptions_posts.html', context)


@login_required(login_url='/users/login/')
def subscriptions_user_posts_view(request, username):
    author = get_object_or_404(User, username=username)

    authors = [sub.author for sub in request.user.following.all()]

    posts = get_objects_on_page(
        request=request,
        all_objects_list=author.posts.all().filter(only_for_group=False).order_by('-pub_date'),
        page_capacity=settings.MAX_POSTS_PER_PAGE
    )

    context = {
        'author': author,
        'posts': posts,
        'authors': authors,
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
        post.save()
        return redirect('index')
    form = PostCreationForm()
    context = {'form': form}
    return render(request, 'posts/post_templates/post_create.html', context)


@login_required(login_url='/users/login/')
def post_edit_view(request, post_pk):
    post = get_object_or_404(Post, id=post_pk)
    if post.author != request.user:
        return redirect(
            'post_detail',
            post_pk=post_pk
        )
    form = PostCreationForm(
        request.POST or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect(
            'post_detail',
            post_pk=post_pk
        )
    context = {
        'author': post.author,
        'post': post,
        'form': form,
    }
    return render(request, 'posts/post_templates/post_create.html', context)


@login_required(login_url='/users/login/')
def post_delete_view(request, post_pk):
    post = get_object_or_404(Post, id=post_pk)
    if post.author != request.user:
        return HttpResponseNotFound()
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    context = {
        'pk': post_pk
    }
    return render(request, 'posts/post_templates/post_delete.html', context)


@login_required(login_url='/users/login/')
def comment_create_view(request, post_pk):
    if request.method == 'POST':
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = get_object_or_404(Post, pk=post_pk)
            comment.save()
            return redirect('post_detail', post_pk=post_pk)
    form = CommentCreationForm()
    context = {'form': form}
    return render(request, 'posts/comment_templates/comment_create.html', context)


@login_required(login_url='/users/login/')
def comment_edit_view(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user != comment.author:
        return HttpResponseNotFound()
    if request.method == 'POST':
        form = CommentCreationForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_pk=post_pk)
    return render(request, 'posts/comment_templates/comment_edit.html')


@login_required(login_url='/users/login/')
def comment_delete_view(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user != comment.author:
        return HttpResponseNotFound()
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', post_pk=post_pk)
    return render(request, 'posts/comment_templates/comment_delete.html')


@login_required(login_url='/users/login/')
def like_view(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if not Like.objects.filter(user=request.user, post=post).exists():
        Like.objects.create(user=request.user, post=post)
    else:
        Like.objects.filter(user=request.user, post=post).delete()

    return redirect(request.META.get('HTTP_REFERER'))


def page_not_found(request, exception):
    return render(
        request,
        'posts/errors_pages/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(
        request,
        'posts/errors_pages/500.html',
        status=500
    )

