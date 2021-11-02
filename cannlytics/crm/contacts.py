"""
Contact Relationship Management | Cannlytics Module
Copyright (c) 2021 Cannlytics

Authors: Keegan Skeate <contact@cannlytics.com>  
Created: 11/2/2021  
Updated: 11/2/2021  

This module contains Cannlytics contact features and functionality.
"""
from typing import Dict

from enforce_typing import enforce_types


class Contact:
    """An instance of this class is the entry point into Cannlytics."""

    @enforce_types
    def __init__(self, config: Dict) -> None:
        """Initialize Cannlytics contact class.

        Usage: Make a new Cannlytics contact instance

        `contact = Contact({...})`

        This class provides the main top-level functions for contacts.
        """
        # logger.debug('Cannlytics instance initialized.')

        if isinstance(config, dict):
            config_dict = {}
            config = {**config_dict, **config}
        self.config = config
