from django.urls import path, include
from .views import PostsCreatorView, PostsSearchView

app_name = 'posts'

urlpatterns = [
    path(r'', PostsSearchView.as_view(), {'created': '0'}, name='posts_index'),
    path('create/', PostsCreatorView.as_view(), name='posts_create'),
]
