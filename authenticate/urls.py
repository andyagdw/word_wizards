"""
Defines the URL patterns for the authenticate app

It includes routes for user login, registration, and logout, integrating
Django's built-in authentication views for logging in. The URL patterns
are configured to use custom templates and view functions for handling
these authentication processes
"""
# authenticate/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'authenticate'  # Set application namespace
urlpatterns = [
    path('login/',
         # Change default template name
         (auth_views.LoginView.
          as_view(template_name='authenticate/login.html')),
         name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
]
