"""
Settings Models | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>  
Created: 11/5/2021  
Updated: 11/5/2021  

Settings data model.
"""
# Standard imports.
from dataclasses import dataclass
from datetime import datetime

# Internal imports.
from .base import Model


@dataclass
class User(Model):
    """The person performing the work."""
    _collection = 'users/%s'
    email: str = ''
    license_number: str = ''
    linked_in_url: str = ''
    name: str = ''
    phone_number: str = ''
    phone_number_formatted: str = ''
    signature_storage_ref: str = ''
    signed_in: bool = False
    signed_in_at: datetime = None
