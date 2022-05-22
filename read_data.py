#from user.models import Users
import django
from django.core.management import call_command
import pandas as pd
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookproject.settings")
django.setup()
from book.models import Book


filename = 'book/static/bookList.xlsx'
df_excel=pd.read_excel(filename)
#file = open(r'C:\janguni\project\book_project\book\static\book/bookList.xlsx')

# Book객체에 데이터 넣기
for book in df_excel.iterrows():
    id=book[1][0]
    img=book[1][1]
    title=book[1][2]
    author=book[1][3]
    publisher=book[1][4]
    genre=book[1][5]
    print(id,img,title,author,publisher,genre)

    if type(id) is int:
        Book(id=id,img=img,title=title,author=author,publisher=publisher,genre=genre).save()
    else:
        continue