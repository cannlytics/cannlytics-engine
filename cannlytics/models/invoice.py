"""
Batch Model | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>  
Created: 11/5/2021  
Updated: 11/5/2021  

Batch data model.
"""
# Standard imports.
from dataclasses import dataclass, field
from typing import List

# Internal imports.
from .base import Model


@dataclass
class Invoice(Model):
    """Invoices are incoming or outgoing bills that you want to manage
    in the Cannlytics platform."""
    _collection = 'organizations/%s/invoices'
    analyses: List = field(default_factory=list)
