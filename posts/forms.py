from django import forms
from .models import Post, Comment


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('description', 'only_for_group')


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
