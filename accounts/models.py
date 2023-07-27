from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator
from posts.models import Post, Comment

User = settings.AUTH_USER_MODEL

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(("email address"), unique=True)

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, blank=True)
    about = models.TextField(max_length=200, blank=True, validators=[
        MaxLengthValidator(200, 'your about can only have 200 characters')
    ])
    profile_picture = models.CharField(max_length=2048, blank=True)
    get_comment_alerts = models.BooleanField(default=True)

class Alert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alerts_received')
    alerter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alerts_sent')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    