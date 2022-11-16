from django.contrib import admin
from django.urls import path, include
from .views import CeleryTasks

urlpatterns = [
    path('', include('apps.pages.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('posts/', include('apps.posts.urls')),
    path('admin/', admin.site.urls),

    # Test tasks for celery
    path('tasks/', CeleryTasks.as_view(), name='tasks'),
    path('tasks/test-celery', CeleryTasks.run_test_task, name='run_test_task')
]
