from django import forms
from django.contrib import admin
from django.forms import fields
from .models import Post

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'slug', 'user')