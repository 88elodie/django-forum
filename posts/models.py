from django.db import models
from accounts.models import CustomUser
from django.conf import settings

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)