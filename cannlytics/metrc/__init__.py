"""
Cannlytics Metrc Client Initialization | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>
Created: 11/6/2021
Updated: 11/6/2021
"""
from .client import Client


def authorize(vendor_api_key, user_api_key, client_class=Client):
    """Authorize use of the Leaf Data Systems API
    using an API key and MME (licensee) code.

    This is a shortcut function which
    instantiates `client_class`.
    By default :class:`cannlytics.traceability.leaf.Client` is used.
    
    Returns: `client_class` instance.
    """
    return client_class(vendor_api_key, user_api_key)
