from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm
from .models import StudyGroup


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


@login_required(login_url='users/login')
def profile_view(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    return render(request, 'users/profile.html', context={'user': user})
