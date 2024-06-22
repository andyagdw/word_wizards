"""
Defines the form used for user registration

The 'RegisterForm' class encapsulates the fields required for a user to
register, including username, password, and password confirmation.
Each field is styled with Bootstrap classes for consistent UI design
"""
# authenticate/forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


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

    def clean(self):
        """
        Overrides the default clean method in Django's 'forms.Form'
        class to add custom validation logic

        This ensures that the form becomes invalid, granting access to
        form errors, which could be displayed to the user
        """

        # Call 'forms.Form' clean method to retrieve the cleaned data
        cleaned_data = super().clean()

        # Retrieve cleaned_data information
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Check if username already exists. Username must be unique
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")

        # Check if password and confirm_password are valid
        if password and confirm_password and password != confirm_password:
            # Raise a validation error if the passwords do not match
            raise ValidationError("Passwords do not match. Try again")

        # Return the cleaned data
        return cleaned_data
