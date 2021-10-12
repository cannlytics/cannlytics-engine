"""
Cannlytics Module | Cannlytics

This module contains the Cannlytics class,
the entry point into Cannlytics features and functionality.
"""
import logging
from typing import Dict, List, Optional, Type, Union

from enforce_typing import enforce_types

logger = logging.getLogger('cannlytics')


class Cannlytics:
    """An instance of this class is the entry point into Cannlytics."""

    @enforce_types
    def __init__(self) -> None:
        """Initialize Cannlytics class.
        Usage: Make a new Cannlytics instance
        `cannlytics = Cannlytics({...})`
        This class provides the main top-level functions in Cannlytics.
        """
        logger.debug('Cannlytics instance initialized.')
