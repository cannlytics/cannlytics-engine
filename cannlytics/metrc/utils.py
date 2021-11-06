"""
Metrc Utility Functions | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>
Created: 11/5/2021
Updated: 11/5/2021

This module contains common Metrc utility functions.
"""
# Standard imports.
from base64 import b64encode, decodebytes
from datetime import datetime, timedelta
from re import sub

# External imports.
from pandas import read_excel

# Internal imports.
from .constants import parameters


def camel_to_snake(s):
    """Turn a camel-case string to a snake-case string.
    Args:
        s (str): The string to convert to snake-case.
    Returns:
        (str): Returns the string in snake_case.
    """
    return sub(r'(?<!^)(?=[A-Z])', '_', s).lower()


def snake_to_camel(s):
    """Turn a snake-case string to a camel-case string.
    Args:
        s (str): The string to convert to camel-case.
    Returns:
        (str): Returns the string in CamelCase
    """
    return ''.join([*map(str.title, s.split('_'))])


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


def decode_pdf(data: str, destination: str):
    """Save an base-64 encoded string as a PDF.
    Args:
        data (str): Base-64 encoded string representing a PDF.
        destination (str): The destination for the PDF file.
    """
    bits = decodebytes(data)
    with open(destination, 'wb') as pdf:
        pdf.write(bits)


def encode_pdf(filename):
    """Open a PDF file in binary mode.
    Args:
        filename (str): The full file path of a PDF to encode.
    Returns:
        (str): A string encoded in base-64.
    """
    with open(filename, 'rb') as pdf:
        return b64encode(pdf.read())


def format_params(**kwargs):
    """Format Metrc request parameters.
    Returns:
        (dict): Returns the parameters as a dictionary.
    """
    params = {}
    for param in kwargs:
        if kwargs[param]:
            key = parameters[param]
            params[key] = kwargs[param]
    return params


def get_timestamp(past=0, future=0, tz='local'):
    """Get an ISO formatted timestamp.
    Args:
        past (int): Number of minutes in the past to get a timestamp.
        future (int): Number of minutes into the future to get a timestamp.

    # TODO: Set time in timezone of state (e.g. {'state': 'OK'} -> CDT)
    """
    now = datetime.now()
    now += timedelta(minutes=future)
    now -= timedelta(minutes=past)
    if tz is None:
        return now.isoformat()[:19]
    else:
        return now.isoformat()


def remove_dict_fields(d, fields):
    """Remove multiple keys from a dictionary.
    Args:
        d (dict): The dictionary to clean.
        fields (list): A list of keys (str) to remove.
    """
    for key in fields:
        if key in d:
            del d[key]
    return d


def remove_dict_nulls(d):
    """Return a shallow copy of a dictionary with all `None` values excluded.
    Args:
        d (dict): The dictionary to reduce.
    """
    return {k: v for k, v in d.items() if v is not None}


def update_context(context, function=snake_to_camel, **kwargs):
    """Update context with keyword arguments.
    Args:
        function (function): Function to apply to final dictionary keys.
    """
    entry = {}
    for key in kwargs:
        entry[key] = kwargs[key]
    data = {
        **clean_nested_dictionary(context, function),
        **clean_nested_dictionary(entry, function)
    }
    return data


def import_tags(file_path):
    """Import plant and package tags.
    Args:
        file_path (str): The file location of the tags.
    Returns:
        (dict): Returns the tags as a dictionary.
    """
    df = read_excel(file_path, sep=',')
    data = df.to_dict('records')
    return clean_dictionary(data)


# TODO: Data import
# 1. Create Plantings / Plantings from Plants / Plantings from Packages
# 2. Immature Plants Growth Phase
# 3. Record Immature Plants Waste
# 4. Immature Plants Packages
# 5. Destroy Immature Plants
# 6. Plants Location
# 7. Plants Growth Phase
# 8. Record Plants Waste
# 9. Manicure Plants
# 10.Harvest Plants
# 11.Destroy Plants
# 12.Packages from Harvest
# 13.Lab Results
# 14.Package Adjustment
# 15.Sales (new)
# 16.Sales (update)
# If uploading multiple types of CSV files, it is recommended that they be uploaded in the
# order listed above to avoid data collisions. For instance, if uploading a CSV to
# Manicure Plants and another to Destroy Plants and the same plant is included on both
# files, the manicure must be recorded prior to the destruction of the plant.
# Except for Lab Results, all CSV files are limited to 500 rows per file. When adding
# plants to the same harvest or manicure batch using multiple CSV files, it is
# recommended that they be uploaded one file at a time.
# Please reference the CA CSV Guide available under the Metrc Support menu for
# additional Data Import assistance.
