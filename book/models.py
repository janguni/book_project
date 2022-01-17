from distutils.command.upload import upload
from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_no_special_characters

# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        validators=[validate_no_special_characters],
        error_messages={'unique':'이미 사용중인 닉넥임입니다'},
    )
    profile_pic = models.ImageField(default="default_profile_pic.jpg",upload_to="profile_pics")
    intro = models.CharField(max_length=60,blank=True)
