"""
PayPal Subscription Management
Copyright (c) 2021-2022 Cannlytics

Author: Keegan Skeate
Contact: <keegan@cannlytics.com>
Created: 11/29/2021
Updated: 1/10/2022
License: MIT License <https://opensource.org/licenses/MIT>
"""
# Standard imports.
from typing import List, Optional

# External imports.
import requests

# API defaults.
BASE = 'https://api-m.paypal.com'
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Accept-Language': 'en_US',
}


def cancel_paypal_subscription(
        access_token: str,
        subscription_id: str,
        reason: Optional[str] = 'No reason provided.',
        base: Optional[str] = 'https://api-m.paypal.com',
):
    """Cancel a PayPal subscription for an individual subscriber.
    Args:
        access_token (str): A required access token.
        subscription_id (str): A specific subscription ID.
        reason (str): The reason for cancellation.
        base (str): The base API URL, with the live URL as the default.
    Returns:
        (bool): An indicator if cancellation was successful.
    """
    url = f'{base}/v1/billing/subscriptions/{subscription_id}/cancel'
    authorization = {'Authorization': f'Bearer {access_token}'}
    headers = {**HEADERS, **authorization}
    data = {'reason': reason}
    response = requests.post(url, data=data, headers=headers)
    return response.status_code == 200


def get_paypal_access_token(
        client_id: str,
        secret: str,
        base: Optional[str] = 'https://api-m.paypal.com',
) -> str:
    """Get a PayPal access token.
    Args:
        client_id (str): Your PayPal client ID.
        secret (str): Your PayPal secret.
        base (str): The base API URL, with the live URL as the default.
    Returns:
        (str): The PayPal access token.
    """
    data = {'grant_type': 'client_credentials'}
    url = f'{base}/v1/oauth2/token'
    auth = (client_id, secret)
    response = requests.post(url, data=data, headers=HEADERS, auth=auth)
    body = response.json()
    return body['access_token']


def get_paypal_subscription_plans( #pylint: disable=too-many-arguments
        access_token: str,
        product_id: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        total_required: Optional[bool] = True,
        base: Optional[str] = 'https://api-m.paypal.com',
) -> List[dict]:
    """Get PayPal subscription plans.
    Args:
        access_token (str): A required access token.
        product_id (str): A specific subscription plan ID.
        page (int): The page at which to begin listing.
        page_size (int): The number of entries per page.
        total_required (bool): Whether or not to return the total.
        base (str): The base API URL,
            with the live URL as the default.
    Returns:
        (list): A list of PayPal subscriptions.    
    """
    url = f'{base}/v1/billing/plans'
    params = {
        'product_id': product_id,
        'page': page,
        'page_size': page_size,
        'total_required': total_required,
    }
    authorization = {'Authorization': f'Bearer {access_token}'}
    headers = {**HEADERS, **authorization}
    response = requests.get(url, params=params, headers=headers)
    body = response.json()
    return body['plans']
