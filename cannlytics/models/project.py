"""
Project Model | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>  
Created: 11/5/2021  
Updated: 11/5/2021  

Project data model.
"""
# Standard imports.
from dataclasses import dataclass
from datetime import datetime

# Internal imports.
from .base import Model


@dataclass
class Project(Model):
    """A group of samples for a specific client."""
    _collection = 'organizations/%s/projects'
    status: str = ''
    sample_count: int = 0
