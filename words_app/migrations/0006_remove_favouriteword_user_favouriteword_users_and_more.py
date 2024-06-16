# Generated by Django 5.0.6 on 2024-06-13 11:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words_app', '0005_alter_favouriteword_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favouriteword',
            name='user',
        ),
        migrations.AddField(
            model_name='favouriteword',
            name='users',
            field=models.ManyToManyField(related_name='favourite_words', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='favouriteword',
            name='word',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]