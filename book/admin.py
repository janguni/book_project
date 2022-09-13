from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportMixin
from .models import Genre, User, Book, WishBookList, Review

# Register your models here.

class BookAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['book_isbn',
                    'book_title', 
                    'book_author', 
                    'book_publisher', 
                    'book_date', 
                    'book_img_url',
                    'genre_name',
                    'book_plot']
UserAdmin.fieldsets += (("Custom fields",{"fields":("nickname","profile_pic","intro")}),)

admin.site.register(User,UserAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(WishBookList)
admin.site.register(Genre)
admin.site.register(Review)

