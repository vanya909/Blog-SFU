from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound

from .models import Post
from .forms import PostCreationForm


def post_detail_view(request, pk):
    post = Post.objects.get(pk=pk)
    if post.only_for_group and post.author != request.user:
        return HttpResponseNotFound()
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': post.comments.all()})


@login_required(login_url='/users/login/')
def study_group_posts_view(request):
    user = request.user
    posts = Post.objects.filter(only_for_group=True, author__group=user.group)
    context = {
        'user': user,
        'posts': posts,
    }
    return render(request, 'posts/study_group.html', context)


@login_required(login_url='/users/login/')
def subscriptions_posts_view(request):
    user = request.user
    posts_ids = [post.id for subscription in user.following.all() for post in subscription.author.posts.all()]
    posts = Post.objects.filter(id__in=posts_ids).order_by('-pub_date')
    context = {
        'user': user,
        'posts': posts,
    }
    return render(request, 'posts/subscriptions_posts.html', context)


@login_required(login_url='/users/login/')
def create_post(request):
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
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect(
            'post_detail',
            pk=post_id
        )
    form = PostCreationForm(
        request.POST or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect(
            'post_detail',
            pk=post_id
        )
    context = {
        'author': post.author,
        'post': post,
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)
