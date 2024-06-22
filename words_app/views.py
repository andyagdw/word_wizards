"""
Defines the views for the words app

It includes functions to render the index page, manage favourite words,
handle account upgrades, view specific words, display random words,
access games, and view user profiles. Each view processes user requests
and interacts with the WordsAPI and the database as needed
"""
# words_app/views.py

from urllib.parse import unquote
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, get_object_or_404
from .utils import (process_word_data,
                    get_word_of_day,
                    fetch_word
                    )
from .forms import BasicSearchForm, AdvancedSearchForm
from .models import FavouriteWord
from . import constants


# Create your views here.
@login_required
def index(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    Fetches a random word from WordsAPI or retrieves it from cache if it
    was fetched within the last 24 hours

    It checks if the random word data is already in the cache and still
    valid. If valid, it uses the cached data. Otherwise, it fetches new
    data from WordsAPI and updates the cache

    Takes in a HttpRequest and renders the index template

    Parameters
    ----------
    request: HttpRequest
        Contains metadata about the request

    Returns
    ----------
    HttpResponse | HttpResponseRedirect
    """

    # Check if the User has provided an API key
    api_key = settings.WORDS_API_KEY
    if not api_key:
        context = {
            'error_message': "API key is not provided. Cannot make "
            " requests to WordsAPI."
        }
        return render(request, 'words_app/error.html', context=context)

    user = request.user
    user_group = user.groups.all()[0].name
    user_favourite_words = user.favourite_words.all()

    if request.method == 'POST':

        # Check if user wants to favourite a word
        if 'add' in request.POST:
            word = request.POST['add']
            # Get favourite word or create a new one if it doesn't exist
            favourite_word, _ = (
                FavouriteWord.objects.get_or_create(word=word)
                )
            user.favourite_words.add(favourite_word)
            return redirect('words_app:index')

        # Check if user wants to unfavourite a word
        elif 'remove' in request.POST:
            word = request.POST['remove']
            favourite_word = FavouriteWord.objects.get(word=word)
            user.favourite_words.remove(favourite_word)

            # Check if word is no longer favourited by any user
            # This keeps the database clean
            if not favourite_word.users.count():
                favourite_word.delete()
            return redirect('words_app:index')

    if request.method == 'GET':
        form_type = request.GET.get("form_type")

        # Check if user wants to view a word
        if form_type == 'basic_search':
            user_word = request.GET['search']
            return redirect('words_app:view_word', word=user_word)

        # Check if user wants to view multiple words
        elif form_type == 'advanced_search':
            advanced_search_form = AdvancedSearchForm(request.GET)
            if advanced_search_form.is_valid():
                letter_pattern = (
                    advanced_search_form.cleaned_data.
                    get('letter_pattern', '')
                    )
                letters_min = (
                    advanced_search_form.cleaned_data.
                    get('letters_min', '')
                    )
                letters_max = (
                    advanced_search_form.cleaned_data.
                    get('letters_max', '')
                    )
                letters = (
                    advanced_search_form.cleaned_data.
                    get('letters', '')
                    )
                syllables = (
                    advanced_search_form.cleaned_data.
                    get('syllables', '')
                    )
                syllables_min = (
                    advanced_search_form.cleaned_data.
                    get('syllables_min', '')
                    )
                syllables_max = (
                    advanced_search_form.cleaned_data.
                    get('syllables_max', '')
                    )
                frequency_min = (
                    advanced_search_form.cleaned_data.
                    get('frequency_min', '')
                    )
                frequency_max = (
                    advanced_search_form.cleaned_data.
                    get('frequency_max', '')
                    )

                querystring_dict = {
                    "letterPattern": letter_pattern,
                    "lettersmin": letters_min,
                    "lettersMax": letters_max,
                    "letters": letters,
                    "syllables": syllables,
                    "syllablesMin": syllables_min,
                    "syllablesMax": syllables_max,
                    "frequencymin": frequency_min,
                    "frequencymax": frequency_max,
                    "limit": (constants.NUM_OF_PRO_RESULTS if
                              user_group == 'Pro'
                              else constants.NUM_OF_PLUS_RESULTS
                              ),
                }

                # Encode dictionary into a string
                querystring = '&'.join(
                    [f"{key}={value}"
                     for key, value in querystring_dict.items()]
                    )

                return redirect("words_app:view_words",
                                querystring=querystring
                                )

        else:
            advanced_search_form = AdvancedSearchForm()

    form = BasicSearchForm()

    # Get word of the day data
    word_of_today_data = get_word_of_day()
    # Process the word data to extract required fields
    (usage_level,
     word,
     syllable_count,
     results_data) = process_word_data(word_of_today_data, user_group)

    # Check if word of today is in users favourites
    word_of_today_in_users_favourites = (
        bool(user_favourite_words.filter(word__contains=word))
    )

    # As it is the index, get only the first result
    results_data_list = (
        results_data[:1] if results_data is not None else None
        )
    results_data_obj = results_data_list

    context = {
        'number_of_syllables_str': 'Number of syllables:',
        'usage_level': usage_level,
        'word_of_today_data': word_of_today_data,
        'word_of_today_word': word,
        'word_of_today_syllable_count': syllable_count,
        'form': form,
        'results_data': results_data_obj,
        'user_favourite_words': word_of_today_in_users_favourites,
        'user_group': user_group,
        'advanced_search_form': advanced_search_form,
    }

    return render(request, 'words_app/index.html', context=context)


@login_required
def favourite_words(
        request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    Displays all the favourite words associated with a user

    Takes in a HttpRequest and renders the favourite template

    Parameters
    ----------
    request: HttpRequest
        Contains metadata about the request

    Returns
    ----------
    HttpResponse | HttpResponseRedirect
    """

    user = request.user
    user_group = user.groups.all()[0].name
    # 'favourite_words' comes from 'related_name' in the model
    user_favourite_words = user.favourite_words.all()

    if request.method == 'POST':
        word = request.POST['remove']
        favourite_word = get_object_or_404(FavouriteWord, word=word)
        user.favourite_words.remove(favourite_word)

        # Check if word is no longer favourited by any user
        if not favourite_word.users.count():
            favourite_word.delete()
        return redirect('words_app:favourite')

    context = {
        'user_group': user_group,
        'user_favourite_words': user_favourite_words,
    }

    return render(request, 'words_app/favourite.html', context=context)


@login_required
def upgrade_account(
        request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    Allows a user to upgrade or downgrade their account type
    
    Takes in a HttpRequest and renders the upgrade_account template

    Parameters
    ----------
    request: HttpRequest
        Contains metadata about the request

    Returns
    ----------
    HttpResponse | HttpResponseRedirect
    """

    user = request.user
    user_group = user.groups.all()[0].name
    upgrade_account_str = 'Account has been upgraded to '
    downgrade_account_str = 'Account has been downgraded to '

    if request.method == 'POST':

        user.groups.clear()  # Remove user from all groups

        if request.POST.get('upgrade_type') == 'starter_group':
            starter_group = Group.objects.get(name='Starter')
            user.groups.add(starter_group)
            new_group = user.groups.all()[0].name  # Get new group name
            messages.success(request,
                             f'{downgrade_account_str} {new_group}'
                             )
            return redirect('words_app:index')

        if request.POST.get('upgrade_type') == 'plus_group':
            plus_group = Group.objects.get(name='Plus')
            user.groups.add(plus_group)
            new_group = user.groups.all()[0].name
            if user_group == 'Starter':
                messages.success(request,
                                 f'{upgrade_account_str} {new_group}'
                                 )
            elif user_group == 'Pro':
                messages.success(request,
                                 f'{downgrade_account_str} {new_group}'
                                 )
            return redirect('words_app:index')

        if request.POST.get('upgrade_type') == 'pro_group':
            pro_group = Group.objects.get(name='Pro')
            user.groups.add(pro_group)
            new_group = user.groups.all()[0].name
            messages.success(request,
                             f'{upgrade_account_str} {new_group}'
                             )
            return redirect('words_app:index')

    context = {
        'user_group': user_group,
        'num_of_plus_results': constants.NUM_OF_PLUS_RESULTS,
        'num_of_pro_results': constants.NUM_OF_PRO_RESULTS,
    }

    return render(request,
                  'words_app/upgrade_account.html',
                  context=context
                  )


@login_required
def view_word(request: HttpRequest,
              word: str) -> HttpResponse | HttpResponseRedirect:
    """
    Displays a word that the user has requested to view

    Takes in a HttpRequest and a word and then renders
    the view_word template

    Parameters
    ----------
    request: HttpRequest
        Contains metadata about the request
    word: str
        A word that the user has requested to view

    Returns
    ----------
    HttpResponse | HttpResponseRedirect
    """

    # Decode the word if it was URL-encoded
    # See 'view_words' template
    decoded_word = unquote(word)
    get_word = fetch_word(word=decoded_word, get_random_word=False)
    user = request.user
    user_group = user.groups.all()[0].name
    # Check if word is in users favourite words
    word_in_user_favourites = (
        user.favourite_words.filter(word=decoded_word).exists()
        )

    if request.method == 'POST':
        # Check user action - if they want to add or remove a word
        if 'add' in request.POST:
            # Grab value from input type hidden in HTML template
            value = request.POST['add']
            # Get favourite word or create a new one if it doesn't exist
            favourite_word, _ = (
                FavouriteWord.objects.get_or_create(word=value)
                )
            user.favourite_words.add(favourite_word)
            return redirect('words_app:view_word', word=value)
        elif 'remove' in request.POST:
            value = request.POST['remove']
            favourite_word = FavouriteWord.objects.get(word=value)
            user.favourite_words.remove(favourite_word)
            # Check if word is no longer favourited by any user
            if not favourite_word.users.count():
                favourite_word.delete()
            return redirect('words_app:view_word', word=value)

    if request.method == 'GET':

        if 'search' in request.GET:
            user_word = request.GET['search']
            return redirect('words_app:view_word', word=user_word)

    form = BasicSearchForm()

    # Process the word data to extract required fields
    (usage_level,
     word,
     syllable_count,
     results_data) = process_word_data(get_word, user_group)

    # Display the 'upgrade_account' container if there are results
    results_data_first_result = (
        results_data[:1][0]
        if results_data and 'partOfSpeech' in results_data[:1][0]
        else None
        )

    context = {
        'number_of_syllables_str': 'Number of syllables:',
        'usage_level': usage_level,
        'word_data': get_word,
        'users_word': word,
        'syllable_count': syllable_count,
        'user_group': user_group,
        'results_data': results_data,
        'word_in_user_favourites': word_in_user_favourites,
        'results_data_first_result': results_data_first_result,
        'form': form,
    }

    return render(request, 'words_app/view_word.html', context=context)


@login_required
def random_word(request: HttpRequest
                ) -> HttpResponse | HttpResponseRedirect:
    """
    Displays a random word

    Takes in a HttpRequest and renders the view_word template

    Parameters
    ----------
    request: HttpRequest
        Contains metadata about the request

    Returns
    ----------
    HttpResponse | HttpResponseRedirect
    """

    user = request.user
    user_group = user.groups.all()[0].name

    get_random_word = fetch_word()

    if request.method == 'POST':
        if 'add' in request.POST:
            value = request.POST['add']
            # Get favourite word or create a new one if it doesn't exist
            favourite_word, _ = (
                FavouriteWord.objects.get_or_create(word=value)
                )
            user.favourite_words.add(favourite_word)
            return redirect('words_app:random_word')
        elif 'remove' in request.POST:
            value = request.POST['remove']
            favourite_word = FavouriteWord.objects.get(word=value)
            user.favourite_words.remove(favourite_word)
            # Check if word is no longer favourited by any user
            if not favourite_word.users.count():
                favourite_word.delete()
            return redirect('words_app:random_word')

    (usage_level,
     word,
     syllable_count,
     results_data) = process_word_data(get_random_word, user_group)

    # Display the 'upgrade_account' container if there are results
    results_data_first_result = (
        results_data[:1][0]
        if results_data and 'partOfSpeech' in results_data[:1][0]
        else None
        )

    context = {
        'number_of_syllables_str': 'Number of syllables:',
        'usage_level': usage_level,
        'word_data': get_random_word,
        'users_word': word,
        'syllable_count': syllable_count,
        'results_data': results_data,
        'user_group': user_group,
        'results_data_first_result': results_data_first_result,
    }

    return render(request, 'words_app/view_word.html', context=context)


@login_required
def view_games(request: HttpRequest) -> HttpResponse:
    """
    Displays the games section (available only for 'Pro' account type)

    Takes in a HttpRequest and renders the games template

    Parameters
    ----------
    request: HttpRequest
        Contains metadata about the request

    Returns
    ----------
    HttpResponse

    """

    user = request.user
    user_group = user.groups.all()[0].name

    context = {
        'user_group': user_group,
    }

    return render(request, 'words_app/games.html', context=context)


@login_required
def user_profile(request: HttpRequest) -> HttpResponse:
    """
    Displays the user profile section

    Takes in a HttpRequest and renders the user_profile template

    Parameters
    ----------
    request: HttpRequest
        Contains metadata about the request

    Returns
    ----------
    HttpResponse

    """

    user = request.user
    user_group = user.groups.all()[0].name

    context = {
        'user_group': user_group,
    }

    return render(request, 'words_app/user_profile.html', context=context)


@login_required
def view_words(request, querystring: str) -> HttpResponse:
    """
    Displays words based on what the user has requested

    Takes in a HttpRequest and renders the view_words template

    Parameters
    ----------
    request: HttpRequest
        Contains metadata about the request
    querystring: str
        A querystring dictionary converted into a string. This is the
        data that was sent to the server

    Returns
    ----------
    HttpResponse

    """

    user = request.user
    user_group = user.groups.all()[0].name

    # Decode the dictionary
    querystring_dict = dict(
        map(lambda s: s.split('='), unquote(querystring).split('&'))
        )

    get_data = fetch_word(get_random_word=False,
                          querystring=querystring_dict)

    # Check if there is data
    if not get_data or 'results' not in get_data:
        num_of_results = None
        data = None
    else:
        num_of_results = get_data['results']['total']
        results_list = get_data['results']['data']
        # Set how many words should be in a column
        chunk_size = 25
        data = (
            [results_list[i:i+chunk_size]
             for i in range(0, len(results_list), chunk_size)]
            )
    context = {
        'num_of_results': num_of_results,
        'querystring': querystring_dict,
        'user_group': user_group,
        'num_of_plus_results': constants.NUM_OF_PLUS_RESULTS,
        'num_of_pro_results': constants.NUM_OF_PRO_RESULTS,
        'data': data,
    }

    return render(request, 'words_app/view_words.html', context=context)
