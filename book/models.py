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
        error_messages={'unique':'이미 사용중인 닉넥임입니다'},
        verbose_name="별명",
    )

    email = models.CharField(max_length = 128, verbose_name="이메일")
    password = models.CharField(max_length = 65, verbose_name = "비밀번호")
    profile_pic = models.ImageField(default="default_profile_pic.jpg",upload_to="profile_pics")
    intro = models.CharField(max_length=60,blank=True)


    def __str__(self):
        return self.username

    

class Book(models.Model):
    book_isbn = models.CharField(max_length=200)
    book_img_url = models.URLField()
    book_title = models.CharField(max_length=255)
    book_author = models.CharField(max_length=100)
    book_publisher = models.CharField(max_length=100)
    genre_name = models.CharField(max_length=50)


    class Meta:
        db_table = 'bookList.csv'

    def get_absolute_url(self):
        return f'/book/{self.book_isbn}/'

class WishBookList(models.Model):
    user_id= models.ForeignKey(
        "User", related_name="wish_user", on_delete=models.CASCADE, null=True)
    book_id= models.ForeignKey(
        "Book", related_name="wish_book", on_delete=models.CASCADE, null=True)
    #count = models.PositiveIntegerField()

    def __str__(self):
        return f'[{self.pk}] {self.user_id} like {self.book_id}'
    
    
