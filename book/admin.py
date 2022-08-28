from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
<<<<<<< HEAD
from .models import Book, User
=======
from import_export.admin import ImportExportMixin
from .models import Genre, User, Book, WishBookList, Review
>>>>>>> upstream/master
# Register your models here.

class BookAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['book_isbn','book_img_url',
    'book_title','book_author','book_publisher','genre_name']
UserAdmin.fieldsets += (("Custom fields",{"fields":("nickname","profile_pic","intro")}),)
<<<<<<< HEAD

admin.site.register(Book)
=======
admin.site.register(User,UserAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(WishBookList)
admin.site.register(Genre)
admin.site.register(Review)
>>>>>>> upstream/master
