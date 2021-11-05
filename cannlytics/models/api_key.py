"""
Analyte Model | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>  
Created: 11/5/2021  
Updated: 11/5/2021  

Analyte data model.
"""
# Standard imports.
from dataclasses import dataclass
from datetime import datetime, timedelta

# Internal imports.
from .base import Model

@dataclass
class APIKey(Model):
    """A representation of an API key HMAC data."""
    _collection = 'admin/api/api_key_hmacs'
    expiration_at: datetime = datetime.now() + timedelta(365)
    name: str = ''
    # permissions: field(default_factory=list) = []
    uid: str = ''
    user_email: str = ''
    user_name: str = ''
