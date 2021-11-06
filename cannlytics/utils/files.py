"""
File Utilities | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>
Created: 11/6/2021
Updated: 11/6/2021
"""
# Standard imports.
from base64 import b64encode, decodebytes


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
