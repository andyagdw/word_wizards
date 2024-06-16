"""
Defines the form used for user registration

The 'RegisterForm' class encapsulates the fields required for a user to
register, including username, password, and password confirmation.
Each field is styled with Bootstrap classes for consistent UI design
"""
# authenticate/forms.py

from django import forms


class RegisterForm(forms.Form):
    """
    Inherits from Django's Form class. It is used for user registration
    """

    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Type username here'
                }
            )
        )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Type password here'
                }
            )
        )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Type password here again'
                }
            )
        )
