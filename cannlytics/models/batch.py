"""
Batch Model | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>  
Created: 11/5/2021  
Updated: 11/5/2021  

Batch data model.
"""
# Standard imports.
from dataclasses import dataclass

# Internal imports.
from .base import Model


@dataclass
class Batch(Model):
    """A group of samples. A batch does not depend on the client or the
    project of the sample."""
    _collection = 'organizations/%s/batches'
    status: str = ''
    sample_count: int = 0
