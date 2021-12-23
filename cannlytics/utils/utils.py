"""
Utility Functions | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Authors: Keegan Skeate <keegan@cannlytics.com>
Created: 11/6/2021
Updated: 11/8/2021
License: <https://github.com/cannlytics/cannlytics-engine/blob/main/LICENSE>

Description: This module contains general cannabis analytics utility functions.
"""
# Standard imports.
from datetime import datetime, timedelta
from typing import Any, List, Optional
from zoneinfo import ZoneInfo
from re import sub, findall

# External imports.
from dateutil import parser

# Internal imports.
from .constants import state_time_zones


def camelcase(string: str) -> str:
    """Turn a given string to CamelCase.
    Args:
        string (str): A given string to turn to CamelCase.
    Returns:
        (str): A string in CamelCase.
    """
    key = ''.join(x for x in string.title() if not x.isspace())
    key = key.replace('_', '').replace('-', '')
    return key


def camel_to_snake(string: str) -> str:
    """Turn a camel-case string to a snake-case string.
    Args:
        string (str): The string to convert to snake-case.
    Returns:
        (str): Returns the string in snake_case.
    """
    return sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


def clean_column_names(data: Any, column: str) -> Any:
    """
    Args:
        data (DataFrame): A DataFrame with any column names.
        column (str): The column of the DataFrame to clean.
    Returns:
        (DataFrame): A DataFrame with snake_case column names.
    """
    data[column] = data[column].str.strip()
    data[column] = data[column].str.rstrip('.)]')
    data[column] = data[column].str.replace('%', 'percent', regex=True)
    data[column] = data[column].str.replace('#', 'number', regex=True)
    data[column] = data[column].str.replace('[/,]', '_', regex=True)
    data[column] = data[column].str.replace('[.,(,)]', '', regex=True)
    data[column] = data[column].str.replace("\'", '', regex=True)
    data[column] = data[column].str.replace("[[]", '_', regex=True)
    data[column] = data[column].str.replace(r"[]]", '', regex=True)
    data[column] = data[column].str.replace('β', 'beta', regex=True)
    data[column] = data[column].str.replace('Δ', 'delta', regex=True)
    data[column] = data[column].str.replace('δ', 'delta', regex=True)
    data[column] = data[column].str.replace('α', 'alpha', regex=True)
    data[column] = data[column].str.replace('__', '', regex=True)
    return data


def clean_dictionary(data: dict, function: function = camel_to_snake) -> dict:
    """Format dictionary keys with given function, snake case by default.
    Args:
        d (dict): A dictionary to clean.
        function (function): A function to apply to each key.
    Returns:
        (dict): Returns the input dictionary with a function applied to the keys.
    """
    return {function(k): v for k, v in data.items()}


def clean_nested_dictionary(data: dict, function: function = camel_to_snake) -> dict:
    """Format nested (at most 2 levels) dictionary keys with a given function,
    snake case by default.
    Args:
        d (dict): A dictionary to clean, allowing dictionaries as values.
        function (function): A function to apply to each key.
    Returns:
        (dict): Returns the input dictionary with cleaned keys.
    """
    clean = clean_dictionary(data, function)
    for k, v in clean.items():
        try:
            clean[k] = clean_dictionary(v, function)
        except AttributeError:
            pass
    return clean


def get_keywords(string: str) -> List[str]:
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


def get_timestamp(
        date: Optional[str] = None,
        past: Optional[int] = 0,
        future: Optional[int] = 0,
        zone: Optional[str] = 'utc'
) -> str:
    """Get an ISO formatted timestamp.
    Args:
        date (str): An optional date to pin the timestamp to a specific time.
        past (int): Number of minutes in the past to get a timestamp.
        future (int): Number of minutes into the future to get a timestamp.
        zone (str): A specific timezone or US state abbreviation, e.g. CA.
    Returns:
        (str): An ISO formatted date/time string in the specified time zone,
            UTC by default.
    """
    time_zone = state_time_zones.get(str(zone).upper(), zone)
    if date:
        now = parser.parse(date).replace(tzinfo=ZoneInfo(time_zone))
    elif time_zone is None:
        now = datetime.now()
    else:
        now = datetime.now(ZoneInfo(time_zone))
    now += timedelta(minutes=future)
    now -= timedelta(minutes=past)
    if time_zone is None:
        return now.isoformat()[:19]
    else:
        return now.isoformat()


def remove_dict_fields(data: dict, fields: List[str]) -> dict:
    """Remove multiple keys from a dictionary.
    Args:
        data (dict): The dictionary to clean.
        fields (list): A list of keys (str) to remove.
    Returns:
        (dict): Returns the dictionary with the keys removed.
    """
    for key in fields:
        if key in data:
            del data[key]
    return data


def remove_dict_nulls(data: dict) -> dict:
    """Return a shallow copy of a dictionary with all `None` values excluded.
    Args:
        data (dict): The dictionary to reduce.
    Returns:
        (dict): Returns the dictionary with the keys with
            null values removed.
    """
    return {k: v for k, v in data.items() if v is not None}


def snake_case(string: str) -> str:
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


def snake_to_camel(string: str) -> str:
    """Turn a snake-case string to a camel-case string.
    Args:
        string (str): The string to convert to camel-case.
    Returns:
        (str): Returns the string in CamelCase
    """
    return ''.join([*map(str.title, string.split('_'))])


def update_dict(context: dict, function: function = snake_to_camel, **kwargs) -> dict:
    """Update dictionary with keyword arguments.
    Args:
        context (dict): A dictionary of context to update.
        function (function): Function to apply to final dictionary keys.
        kwargs (*args): Key/value arguments to update in the dictionary.
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
