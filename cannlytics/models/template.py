"""
Template Model | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>  
Created: 11/5/2021  
Updated: 11/5/2021  

Template data model.
"""
# Standard imports.
from dataclasses import dataclass
from datetime import datetime

# Internal imports.
from .base import Model


@dataclass
class Template(Model):
    """Templates for generating documents, such as invoices and
    certificates."""
    _collection = 'organizations/%s/transfers'
    status: str = ''
    storage_ref: str = ''
    version: str = ''
