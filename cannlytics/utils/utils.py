"""
Utility Functions | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>
Created: 11/6/2021
Updated: 11/6/2021

This module contains general cannabis analytics utility functions.
"""
# Standard imports.
from datetime import datetime, timedelta
from re import sub, findall


def camelcase(string):
    """Turn a given string to CamelCase.
    Args:
        string (str): A given string to turn to CamelCase.
    Returns:
        (str): A string in CamelCase.
    """
    key = ''.join(x for x in string.title() if not x.isspace())
    key = key.replace('_', '').replace('-', '')
    return key


def camel_to_snake(s):
    """Turn a camel-case string to a snake-case string.
    Args:
        s (str): The string to convert to snake-case.
    Returns:
        (str): Returns the string in snake_case.
    """
    return sub(r'(?<!^)(?=[A-Z])', '_', s).lower()


def clean_dictionary(d, function=camel_to_snake):
    """Format dictionary keys with given function, snake case by default.
    Args:
        d (dict): A dictionary to clean.
        function (function): A function to apply to each key.
    Returns:
        (dict): Returns the input dictionary with a function applied to the keys.
    """
    return {function(k): v for k, v in d.items()}


def clean_nested_dictionary(d, function=camel_to_snake):
    """Format nested (at most 2 levels) dictionary keys with a given function,
    snake case by default.
    Args:
        d (dict): A dictionary to clean, allowing dictionaries as values.
        function (function): A function to apply to each key.
    Returns:
        (dict): Returns the input dictionary with cleaned keys.
    """
    clean = clean_dictionary(d, function)
    for k, v in clean.items():
        try:
            clean[k] = clean_dictionary(v, function)
        except AttributeError:
            pass
    return clean


def get_keywords(string):
    """Get keywords for a given string.
    Args:
        string (str): A string to get keywords for.
    Returns:
        (list): A list of keywords.
    """
    keywords = string.lower().split(' ')
    keywords = [x.strip() for x in keywords if x]
    keywords = list(set(keywords))
    return keywords


def get_timestamp(past=0, future=0, time_zone='local'):
    """Get an ISO formatted timestamp.
    Args:
        past (int): Number of minutes in the past to get a timestamp.
        future (int): Number of minutes into the future to get a timestamp.
        time_zone (str): UNIMPLEMENTED Set a given timezone.
    Returns:
        (str): An ISO formatted date/time string.
    """
    now = datetime.now()
    now += timedelta(minutes=future)
    now -= timedelta(minutes=past)
    if time_zone is None:
        return now.isoformat()[:19]
    else:
        return now.isoformat()


def remove_dict_fields(d, fields):
    """Remove multiple keys from a dictionary.
    Args:
        d (dict): The dictionary to clean.
        fields (list): A list of keys (str) to remove.
    Returns:
        (dict): Returns the dictionary with the keys removed.
    """
    for key in fields:
        if key in d:
            del d[key]
    return d


def remove_dict_nulls(d):
    """Return a shallow copy of a dictionary with all `None` values excluded.
    Args:
        d (dict): The dictionary to reduce.
    Returns:
        (dict): Returns the dictionary with the keys with
            null values removed.
    """
    return {k: v for k, v in d.items() if v is not None}


def snake_case(string):
    """Turn a given string to snake case.
    Handles CamelCase, replaces known special characters with
    preferred namespaces, replaces spaces with underscores,
    and removes all other nuisance characters.
    Args:
        string (str): The string to turn to snake case.
    Returns:
        (str): A snake case string.
    """
    key = string.replace(' ', '_')
    key = key.replace('&', 'and')
    key = key.replace('%', 'percent')
    key = key.replace('#', 'number')
    key = key.replace('$', 'dollars')
    key = key.replace('/', '_')
    key = key.replace(r'\\', '_')
    key = sub('[!@#$%^&*()[]{};:,./<>?\|`~-=+]', ' ', key)
    keys = findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', key)
    return '_'.join(map(str.lower, keys))


def snake_to_camel(s):
    """Turn a snake-case string to a camel-case string.
    Args:
        s (str): The string to convert to camel-case.
    Returns:
        (str): Returns the string in CamelCase
    """
    return ''.join([*map(str.title, s.split('_'))])


def update_dict(context, function=snake_to_camel, **kwargs):
    """Update dictionary with keyword arguments.
    Args:
        function (function): Function to apply to final dictionary keys.
    Returns:
        (dict): Returns the dictionary with updated keys.
    """
    entry = {}
    for key in kwargs:
        entry[key] = kwargs[key]
    data = {
        **clean_nested_dictionary(context, function),
        **clean_nested_dictionary(entry, function)
    }
    return data
