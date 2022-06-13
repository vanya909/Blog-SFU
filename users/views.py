from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm
from .models import StudyGroup, Follow, User


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            try:
                user.group = StudyGroup.objects.filter(title=form.cleaned_data['group'].upper())[0]
                user.save()
                login(request, user)
                return redirect('index')
            except IndexError:
                form.add_error('group', 'Такой группы не найдено')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
        'studygroups': StudyGroup.objects.all()
    }
    return render(request, 'users/signup.html', context=context)


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    following = user.followers.filter(user=request.user.id).exists()
    followers_count = user.followers.count()
    posts_count = user.posts.count()
    context = {
        'following': following,
        'profile': user,
        'followers_count': followers_count,
        'posts_count': posts_count
    }
    return render(request, 'users/profile.html', context=context)


@login_required(login_url='/users/login')
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('profile', username=username)


@login_required(login_url='/users/login')
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    follower = Follow.objects.filter(user=request.user, author=author)
    if follower.exists():
        if author != request.user:
            follower.delete()
    return redirect('profile', username=username)
