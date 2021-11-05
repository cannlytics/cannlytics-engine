"""
Calculation Model | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>  
Created: 11/5/2021  
Updated: 11/5/2021  

Calculation data model.
"""
# Standard imports.
from dataclasses import dataclass

# Internal imports.
from .base import Model


@dataclass
class Calculation(Model):
    """A calculation is applied to measurements to determine final
    results, such as applying dilution factor, etc."""
    _collection = 'organizations/%s/calculations'
    formula: str = ''
