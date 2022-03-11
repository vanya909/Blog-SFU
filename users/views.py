from django.shortcuts import render, redirect

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
                return redirect('index')
            except IndexError:
                form.add_error('group', 'Такой группы не найдено')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', context={'form': form})
