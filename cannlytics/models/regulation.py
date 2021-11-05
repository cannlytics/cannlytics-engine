"""
Regulation Model | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>  
Created: 11/5/2021  
Updated: 11/5/2021  

Regulation data model.
"""
# Standard imports.
from dataclasses import dataclass

# Internal imports.
from .base import Model

@dataclass
class Regulation(Model):
    """."""
    _collection = 'regulations'
