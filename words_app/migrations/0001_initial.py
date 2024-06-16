# Generated by Django 5.0.6 on 2024-06-08 22:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite_words', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('can_add_favourite_word', 'Can add a favourite word'), ('can_remove_favourite_word', 'Can remove a favourite word')],
            },
        ),
    ]
