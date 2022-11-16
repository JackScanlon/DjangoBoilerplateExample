from django.contrib import admin
from .forms import PostCreationForm
from .models import Post

@admin.register(Post)
class PostChangeForm(admin.ModelAdmin):
    list_display = ['title', 'content', 'slug', 'user', 'created_at']
    list_filter = ['title', 'content', 'slug', 'user', 'created_at']
    search_fields = ['title', 'content', 'user']
    form = PostCreationForm
    model = Post