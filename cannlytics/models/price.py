"""
Price Model | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>  
Created: 11/5/2021  
Updated: 11/5/2021  

Price data model.
"""
# Standard imports.
from dataclasses import dataclass
from datetime import datetime

# Internal imports.
from .base import Model


@dataclass
class Price(Model):
    """A price for an analysis or group of analyses."""
    _collection = 'organizations/%s/prices'
    public: bool = False
    price: float = 0
    currency: str = 'USD'
