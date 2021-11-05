"""
Workflow Model | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>  
Created: 11/5/2021  
Updated: 11/5/2021  

Workflow data model.
"""
# Standard imports.
from dataclasses import dataclass

# Internal imports.
from .base import Model

@dataclass
class Workflow(Model):
    """An abstract series of actions performed on a set trigger."""
    _collection = 'organizations/%s/workflows'
