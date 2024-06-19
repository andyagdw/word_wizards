"""
Defines the view functions for user authentication operations

It includes views for user registration and logout. The registration
view handles user creation, form validation, and user authentication,
while the logout view manages user sign-out
"""
# authenticate/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.contrib.auth.models import User, Group
from .forms import RegisterForm


def register_user(
        request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    Displays a register form

    Takes in a HttpRequest and renders the register template

    Parameters
    ----------
    request: HttpRequest
        Contains metadata about the request

    Returns
    ----------
    HttpResponse | HttpResponseRedirect
    """

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                new_user = User()
                new_user.username = form.cleaned_data['username']
                new_user.set_password(password)
                new_user.save()
                group = Group.objects.get(name='Starter')
                new_user.groups.add(group)
                login(request, new_user)
                return redirect('words_app:index')

    form = RegisterForm()

    context = {
        'form': form,
    }

    return render(request, 'authenticate/register.html', context=context)


def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    """
    Logs out a user and redirects them back to login page

    Takes in a HttpRequest and returns a HttpResponseRedirect

    Parameters
    ----------
    request: HttpRequest
        Contains metadata about the request

    Returns
    ----------
    HttpResponseRedirect

    """
    logout(request)
    return redirect('authenticate:login')
