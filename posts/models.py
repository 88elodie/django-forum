from django.db import models
from accounts.models import CustomUser
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50, validators = [
            MinLengthValidator(1, 'your title needs at least 1 character')
        ])
    body = models.TextField(max_length=5000,
        validators = [
            MinLengthValidator(5, 'your post needs at least 5 characters'),
            MaxLengthValidator(5000, 'your post can only have 5000 characters')
        ]
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class File(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.CharField(max_length=2048)
    upload_id = models.CharField(max_length=22)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.file