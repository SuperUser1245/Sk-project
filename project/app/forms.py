from django import forms
from .models import Post, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
