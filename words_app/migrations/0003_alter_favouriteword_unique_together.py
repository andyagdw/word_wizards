# Generated by Django 5.0.6 on 2024-06-08 23:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('words_app', '0002_alter_favouriteword_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favouriteword',
            unique_together={('user', 'word')},
        ),
    ]