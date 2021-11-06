"""
Cannlytics Module | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>
Created: 11/5/2021
Updated: 11/6/2021

This module contains the Cannlytics class,
the entry point into Cannlytics features and functionality.
"""
# Standard imports.
import logging
from typing import Dict, List, Optional, Type, Union

# External imports.
from enforce_typing import enforce_types

# Internal imports.
from .exceptions import CannlyticsError

logger = logging.getLogger('cannlytics')


class Cannlytics:
    """An instance of this class is the entry point into Cannlytics."""

    @enforce_types
    def __init__(self, config: Dict) -> None:
        """Initialize Cannlytics class.

        Usage: Make a new Cannlytics instance

        `cannlytics = Cannlytics({...})`

        This class provides the main top-level functions in Cannlytics.
        """
        # logger.debug('Cannlytics instance initialized.')

        if isinstance(config, dict):
            config_dict = {}
            config = {**config_dict, **config}
        self.config = config

    def initialize_traceability(self, config, license_number):
        """Initialize the traceability client.
        Args:
            config (dict): The configuration for the traceability client.
            license_number (str): A primary license to initialize the traceability client.
        """

        # TODO: Initialize a Metrc traceability client.
        self.track = {}

    def initialize_firebase(self):
        """Initialize a Firebase account for back-end, cloud services."""
        self.db = {}
        self.storage = {}  
