from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=10000)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=128, db_index=True, null=True)

    def __str__(self):
        return '%s' % (self.title)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Post,self).save(*args,**kwargs)