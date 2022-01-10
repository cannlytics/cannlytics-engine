"""
Regulation Model | Cannlytics
Copyright (c) 2021-2022 Cannlytics and Cannlytics Contributors

Authors: Keegan Skeate <keegan@cannlytics.com>
Created: 11/5/2021
Updated: 11/5/2021
License: <https://github.com/cannlytics/cannlytics-engine/blob/main/LICENSE>

Description: Regulation data model.
"""
# Standard imports.
from dataclasses import dataclass

# Internal imports.
from .base import Model

@dataclass
class Regulation(Model):
    """."""
    _collection = 'regulations'
