from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    password2 = models.CharField(max_length=128)
    nickname = models.CharField(max_length=100)