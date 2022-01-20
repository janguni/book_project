from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.CharField(max_length = 128, verbose_name="이메일")
    password = models.CharField(max_length = 65, verbose_name = "비밀번호")
    nickname = models.CharField(max_length=100, verbose_name="별명")

    def __str__(self):
        return self.username