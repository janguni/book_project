# Generated by Django 4.0.4 on 2022-05-25 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_alter_user_nickname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_isbn', models.CharField(max_length=200)),
                ('book_img_url', models.URLField()),
                ('book_title', models.CharField(max_length=255)),
                ('book_author', models.CharField(max_length=100)),
                ('book_publisher', models.CharField(max_length=100)),
                ('genre_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'bookList.csv',
            },
        ),
    ]