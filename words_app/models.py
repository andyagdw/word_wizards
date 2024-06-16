"""
Defines the database models for the words app

It includes the 'FavouriteWord' model, which represents words that can
be marked as favourites by multiple users. The model includes fields for
the word, the users who favourited it, and the date it was added
"""
# words_app/models.py
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class FavouriteWord(models.Model):
    """
    Subclasses from 'django.db.models.Model'. It Represents a word that
    can be a favourite of multiple users
    """
    # Access favourite words associated with using user.favourite_words
    users = models.ManyToManyField(User, related_name='favourite_words')
    # Ensure word is unique
    word = models.CharField(max_length=100, unique=True)
    date_added = models.DateField(auto_now_add=True)

    # Permissions could be defined here within Meta class

    def __str__(self) -> str:
        """Returns a word"""
        return f'{self.word}'
