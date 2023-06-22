from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(("email address"), unique=True)

    def __str__(self):
        return self.username
    