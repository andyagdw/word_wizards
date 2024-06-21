"""
Defines the URL patterns for the words app

It includes routes for various functionalities such as viewing the
index page, managing favourite words, upgrading user accounts, viewing
specific words, generating random words, accessing games, and viewing
user profiles
"""
# words_app/urls.py

from django.urls import path
from . import views

app_name = 'words_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('favourite_words/', views.favourite_words, name='favourite'),
    path('upgrade_account/', views.upgrade_account, name='upgrade_account'),
    path('view_word/<str:word>/', views.view_word, name='view_word'),
    path('random_word/', views.random_word, name='random_word'),
    path('games/', views.view_games, name='games'),
    path('profile/', views.user_profile, name='user_profile'),
    path('view_words/<str:querystring>/', views.view_words, name='view_words'),
]
