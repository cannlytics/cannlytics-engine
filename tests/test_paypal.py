"""
PayPal Management Test
Copyright (c) 2021-2022 Cannlytics

Author: Keegan Skeate
Contact: <keegan@cannlytics.com>
Created: 1/21/2022
Updated: 1/21/2022
License: MIT License <https://opensource.org/licenses/MIT>
"""
# Standard imports.
import os
import sys

# External imports.
from dotenv import dotenv_values

# Internal imports.
sys.path.append('../')
from cannlytics import paypal

# Get credentials.
try:
    config = dotenv_values('../.env')
    credentials = config['GOOGLE_APPLICATION_CREDENTIALS']
except KeyError:
    config = dotenv_values('.env')
    credentials = config['GOOGLE_APPLICATION_CREDENTIALS']

# Set Google application credentials.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials


def test_get_paypal_access_token():
    """Test getting a PayPal access token."""
    paypal_client_id = config['PAYPAL_CLIENT_ID']
    paypal_secret = config['PAYPAL_SECRET']
    paypal_access_token = paypal.get_paypal_access_token(paypal_client_id, paypal_secret)
    assert paypal_access_token is not None
    return paypal_access_token


def test_get_paypal_subscription_plans():
    """Test getting all PayPal subscriptions."""
    paypal_access_token = test_get_paypal_access_token()
    plans = paypal.get_paypal_subscription_plans(paypal_access_token)
    assert isinstance(plans, list)
    return plans


def test_cancel_paypal_subscription():
    """Test canceling a PayPal access token."""
    paypal_access_token = test_get_paypal_access_token()
    paypal.cancel_paypal_subscription(
        paypal_access_token,
        '<individual-subscription-id>',
        reason='Need to save funds.'
    )


def test_get_paypal_products():
    """Test getting PayPal products."""
    paypal_access_token = test_get_paypal_access_token()
    products = paypal.get_paypal_products(paypal_access_token)
    assert isinstance(products, list)
    return products


def test_get_paypal_product():
    """Test getting a PayPal product."""
    paypal_access_token = test_get_paypal_access_token()
    product = paypal.get_paypal_products(
        paypal_access_token,
        product_id='cannlytics-enterprise-subscription'
    )
    assert isinstance(product, dict)
    return product


# TODO: Run test.
def test_create_paypal_product():
    """Test getting a PayPal product."""
    paypal_access_token = test_get_paypal_access_token()
    product = paypal.create_paypal_product(
        paypal_access_token,
        name='ProductName',
        description='A new product!',
        product_id='product-id',
        product_type='DIGITAL',
        category='OTHER',
        image_url='',
        home_url='https://cannlytics.com',
    )
    assert isinstance(product, dict)
    return product


# TODO: Run test.
def test_update_paypal_product():
    """Test getting a PayPal product."""
    paypal_access_token = test_get_paypal_access_token()
    paypal.update_paypal_product(
        paypal_access_token,
        product_id='product-id',
        field='description',
        value='The best product.',
    )
