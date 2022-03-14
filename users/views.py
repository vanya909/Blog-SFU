from django.shortcuts import render, redirect
from django.contrib.auth import login

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