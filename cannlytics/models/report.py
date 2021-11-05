"""
Report Model | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>  
Created: 11/5/2021  
Updated: 11/5/2021  

Report data model.
"""
# Standard imports.
from dataclasses import dataclass
from datetime import datetime

# Internal imports.
from .base import Model

@dataclass
class Report(Model):
    """."""
    _collection = 'organizations/%s/reports'
