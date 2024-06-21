"""
Defines the forms used for searching words within the website

The 'BasicSearchForm' class encapsulates a single field for entering
search queries. The 'AdvancedSearchForm' class
provides additional fields for more specific search parameters.
"""
# words_app/forms.py

from django import forms
from django.core.exceptions import ValidationError


def validate_frequency(value) -> None:
    """
    Validate that the input is a float within the range 1.74 to 8.03

    Parameters
    ----------
    value: str
        The value to validate

    Raises
    ----------
    ValidationError
        If the value is not a valid float or is out of the specified
        range
    """

    try:
        value = float(value)
    except ValueError as e:
        raise ValidationError('Enter a valid number') from e

    if not 1.74 <= value <= 8.03:
        raise ValidationError(
            """Please ensure that the value is between 1.74 and 8.03"""
            )


def validate_input_is_int(value):
    """
    Validate that the input value is an integer

    Parameters
    ----------
    value: str
        The value to validate

    Raises
    ----------
    ValidationError
        If the value is not a valid integer
    """

    try:
        int(value)
    except ValueError as e:
        raise ValidationError('Enter a valid number') from e


class BasicSearchForm(forms.Form):
    """
    Inherits from Django's Form class. It contains a single field for
    entering a search query
    """

    search = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control search-input',
                'placeholder': 'Search a word...'
                }
            )
        )


class AdvancedSearchForm(forms.Form):
    """
    Inherits from Django's Form class. It allows users to specify
    additional search parameters such as letter patterns, letter counts,
    syllable counts, and frequency scores
    """

    letter_pattern = forms.CharField(
        max_length=50,
        help_text="""
        Find words whose letters match the pattern. For example,
        Use '^a' to find words beginning with an 'a'. Alternatively, use
        'a$' to find words ending with an 'a'.
        Omit the signs if you would like to find words that just
        contain an 'a'.
        """,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
            )
        )
    letters_min = forms.CharField(
        required=False,
        max_length=2,
        label="Minimum number of letters",
        validators=[validate_input_is_int],
        help_text='The minimum number of letters the word must have.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
            )
        )
    letters_max = forms.CharField(
        required=False,
        max_length=2,
        label="Maximum number of letters",
        validators=[validate_input_is_int],
        help_text="The maximum number of letters the word can have.",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
            )
        )
    letters = forms.CharField(
        required=False,
        max_length=2,
        validators=[validate_input_is_int],
        help_text="The number of letters the word must have.",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
            )
        )
    syllables = forms.CharField(
        required=False,
        max_length=2,
        validators=[validate_input_is_int],
        help_text="The number of syllables the word must have.",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
            )
        )
    syllables_min = forms.CharField(
        required=False,
        max_length=2,
        label="Minimum number of syllables",
        validators=[validate_input_is_int],
        help_text="The minimum number of syllables the word can have.",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
            )
        )
    syllables_max = forms.CharField(
        required=False,
        max_length=2,
        label="Maximum number of syllables",
        validators=[validate_input_is_int],
        help_text="The maximum number of syllables the word can have.",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
            )
    )
    frequency_min = forms.CharField(
        required=False,
        max_length=4,
        label="Minimum frequency score",
        validators=[validate_frequency],
        help_text="""
        The minimum frequency score of words to return.
        You can use this to limit your search to words that people are
        familiar with (like "go", with a frequency of 6.98).
        The range is from 1.74 - 8.03.
        """,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
            )
    )
    frequency_max = forms.CharField(
        required=False,
        max_length=4,
        label="Maximum frequency score",
        validators=[validate_frequency],
        help_text="""
        The maximum frequency score of words to return.
        You can use this to limit your search to words that aren't seen
        as frequently (like "zygote", with a frequency of 2.55).
        The range is from 1.74 - 8.03.
        """,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                }
            )
    )
