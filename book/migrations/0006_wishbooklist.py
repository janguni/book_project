# Generated by Django 4.0.4 on 2022-05-29 04:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishBookList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wish_book', to='book.book')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wish_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
