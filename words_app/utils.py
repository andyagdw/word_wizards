"""
Contains utility functions for the words app

It includes functions to fetch words from the WordsAPI, validate cache
timestamps, get the word of the day, process word data results based
on user groups, and extract and organise word data for display
"""
# words_app/utils.py

import datetime
import requests
import pytz
from django.conf import settings
from django.core.cache import cache


def fetch_word(word: str = None, get_random_word: bool = True) -> dict:
    """
    Fetches a word from WordsAPI and returns the results of this as a
    dictionary

    Parameters
    ----------
    word: str
        A word that the user wants to lookup
    get_random_word: bool
        Whether the user wants to view a random word or a specific word

    Returns
    ----------
    Dictionary

    """

    # The request should wait a maximum of 5 seconds for a response
    timeout = 8
    url = "https://wordsapiv1.p.rapidapi.com/words/"

    headers = {
        "x-rapidapi-key": settings.WORDS_API_KEY,
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com"
    }

    if get_random_word:
        querystring = {"random": "true"}
        response = requests.get(url,
                                headers=headers,
                                params=querystring,
                                timeout=timeout)
        if response.status_code == 200:  # Check if call was a success
            return response.json()
        return {}

    else:
        # Add word to end of url
        word_url = f'{url}{word}'
        response = requests.get(word_url,
                                headers=headers,
                                timeout=timeout
                                )
        if response.status_code == 200:
            return response.json()
        return {}


def is_cache_valid(timestamp: str) -> bool:
    """
    Checks if the cached timestamp is still within the valid period
    (less than a day old)

    Parameters
    ----------
    timestamp: str
        The timestamp string in '%Y-%m-%d %H:%M:%S' format

    Returns
    ----------
    Boolean
    """

    last_updated = (
        datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        )

    return (
        datetime.datetime.now() -
        last_updated < datetime.timedelta(days=1)
        )


def seconds_until_midnight_uk() -> int:
    """
    Calculates the number of seconds until midnight UK time

    Parameters
    ----------
    None

    Returns
    ----------
    Int
    """
    now_utc = datetime.datetime.now(pytz.utc)
    uk_timezone = pytz.timezone('Europe/London')
    now_uk = now_utc.astimezone(uk_timezone)
    midnight_uk = (
        (now_uk + datetime.timedelta(days=1)).
        replace(hour=0, minute=0, second=0, microsecond=0)
        )

    return int((midnight_uk - now_uk).total_seconds())


def get_word_of_day() -> dict:
    """
    Helper function to get the word of the day data, either from cache
    or WordsAPI. It returns the data of this as a dictionary

    Parameters
    ----------
    None

    Returns
    ----------
    Dictionary
    """

    # For storing the random word data and its timestamp
    cache_key = 'api_data_random_word'
    cache_timestamp_key = 'api_data_timestamp_random_word'
    # Retrieve cached data and timestamp
    cached_data = cache.get(cache_key)
    cached_timestamp = cache.get(cache_timestamp_key)

    if (cached_data
            and cached_timestamp
            and is_cache_valid(cached_timestamp)):
        return cached_data
    else:  # If not, fetch new data and update cache
        word_of_today_data = fetch_word()
        if word_of_today_data:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            timeout = seconds_until_midnight_uk()
            cache.set(cache_key, word_of_today_data, timeout=timeout)
            (cache.set(
                cache_timestamp_key,
                now,
                timeout=timeout))
            return word_of_today_data

    return {}


def process_word_data_results(group_name: str,
                              word_data: dict) -> None | list:
    """
    Extracts the required data from the word_data key 'results'
    and stores them in a list

    Parameters
    ----------
    group_name: str
        Represents the users group name (i.e., Starter, Plus, or Pro)

    word_data: dict
        Contains all the information about the word, if the WordsAPI
        call was successful

    Returns
    ----------
    None or a list
    """

    # Check if the WordsAPI call was successful and 'results' key exists
    if not word_data or 'results' not in word_data:
        return None

    # Represents the number of results a group can see
    group_max = None
    results_list = []

    if group_name == 'Starter':
        group_max = 1
    elif group_name == 'Plus':
        group_max = 2
    elif group_name == 'Pro':
        # Those with a pro account can view all results
        group_max = len(word_data['results'])

    for result in word_data['results'][:group_max]:
        # Check if keys exist in results
        definition = result.get('definition', None)
        part_of_speech = result.get('partOfSpeech', None)
        synonyms = result.get('synonyms', None)
        antonyms = result.get('antonyms', None)
        examples = result.get('examples', None)

        results_list.append(
            {
               'definition': definition,
               'partOfSpeech': part_of_speech,
               'synonyms': synonyms,
               'antonyms': antonyms,
               'examples': examples,
            }
        )

    return results_list


def process_word_data(word_data: dict, group_name: str) -> list:
    """
    Helper function to process the word data and extract required fields
    . It then returns the results of this as a list

    Parameters
    ----------
    word_data: dict
        Contains all the information about the word, if the WordsAPI
        call was successful
    group_name: str
        Represents the users group name (i.e., Starter, Plus, or Pro)

    Returns
    ----------
    List
    """

    results_data = process_word_data_results(group_name, word_data)

    # Check if WordsAPI call was successful
    if not word_data:
        word = frequency = syllable_count = usage_level = None

        return [
            usage_level,
            word,
            syllable_count,
            results_data
            ]

    word = (
        word_data['word']
        if 'word' in word_data
        else ''
        )

    # 'frequency' - How many times the word is used in everday life
    if 'frequency' in word_data:
        frequency = word_data['frequency']
        usage_level = (
            "Rarely Used" if frequency <= 3 else
            ("Commonly Used" if 3 < frequency < 5 else
                ("Widely Used" if frequency > 5 else ""))
            )
    else:
        usage_level = ''

    if ('syllables' in word_data) and ('count' in word_data['syllables']):
        syllable_count = word_data['syllables']['count']
    else:
        syllable_count = 0

    return [
        usage_level,
        word,
        syllable_count,
        results_data
        ]
