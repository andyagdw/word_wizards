"""
Defines the form used for searching words within the website

The 'SearchForm' class encapsulates a single field for entering search
queries. The form is styled with a Bootstrap class to ensure a
consistent and user-friendly interface
"""

from django import forms


class SearchForm(forms.Form):
    """
    Inherits from Django's Form class. It is used for searching a
    word
    """
    search = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control search-input',
                'placeholder': 'Search a word...'
                }
            )
        )
