from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator

User = settings.AUTH_USER_MODEL

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(("email address"), unique=True)

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, blank=True)
    about = models.CharField(max_length=200, blank=True)
    profile_picture = models.CharField(max_length=2048, blank=True)
    
    