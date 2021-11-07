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
from dotenv import dotenv_values
import logging
from os import environ
from typing import Dict, Optional
# from typing import List, Type, Union

# External imports.
from enforce_typing import enforce_types

# Internal imports.
# from .exceptions import CannlyticsError
from .firebase import initialize_firebase
from .metrc import initialize_metrc

logger = logging.getLogger('cannlytics')


class Cannlytics:
    """An instance of this class is the entry point into Cannlytics."""

    @enforce_types
    def __init__(self, config: Optional[Dict]) -> None:
        """Initialize Cannlytics class.

        Usage: Make a new Cannlytics instance

        `cannlytics = Cannlytics({...})`

        This class provides the main top-level functions in Cannlytics.
        """
        if isinstance(config, dict):
            config_dict = {}
            config = {**config_dict, **config}
        else:
            config = dotenv_values('./.env')
        self.config = config
        logger.debug('Cannlytics instance initialized.')

    def initialize_firebase(self, config=None):
        """Initialize a Firebase account for back-end, cloud services."""
        if config is None:
            config = self.config
        credentials = config['GOOGLE_APPLICATION_CREDENTIALS']
        environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials
        self.db = initialize_firebase()
        self.storage_bucket = config.get('FIREBASE_STORAGE_BUCKET')
        logger.debug('Firebase client initialized.')
    
    def initialize_traceability(self, config=None, primary_license=None, state=None):
        """Initialize the traceability client.
        Args:
            config (dict): The configuration for the traceability client.
            primary_license (str): A primary license to initialize the traceability client.
        """
        if config is None:
            config = self.config
        if state is None:
            state = config.get('METRC_STATE', 'ca')
        self.track = initialize_metrc(
            vendor_api_key=config['METRC_TEST_VENDOR_API_KEY'],
            user_api_key=config['METRC_TEST_USER_API_KEY'],
            primary_license=primary_license,
            state=state,
        )
        logger.debug('Traceability client initialized.')
