"""
Test Data Market

Authors: Keegan Skeate <keegan@cannlytics.com>
Created: 10/11/2021
Updated: 10/11/2021
"""
# Standard imports.
import os
import sys

# Internal imports.
sys.path.append('../..')
from cannlytics.data import market # pylint: disable=import-error


def test_publish_data():
    """Publish a dataset on the data market."""

    # Initialize Ocean market.
    ocean = market.initialize_market()

    # Publish a dataset.
    files = [
        {
            "index": 0,
            "contentType": "text/text",
            "url": "https://raw.githubusercontent.com/trentmc/branin/main/branin.arff"
        }
    ]
    data_token, asset = market.publish_data(
        ocean,
        os.environ('TEST_PRIVATE_KEY1'),
        files,
        'DataToken1',
        'DT1',
        'KLS',
        data_license='CC0: Public Domain',
    )
    return data_token, asset

def test_sell_data(data_token):
    """Sell a dataset on the data market."""

    # Initialize Ocean market.
    ocean = market.initialize_market()

    # Sell a dataset.
    market.sell_data(
        ocean,
        os.environ('TEST_PRIVATE_KEY1'),
        data_token,
        100,
        fixed_price=True,
    )

def test_buy_data(data_token, asset):
    """Buy a dataset on the data market."""

    # Initialize Ocean market.
    ocean = market.initialize_market()

    # Buy a dataset.
    seller_wallet = market.get_wallet(
        ocean,
        os.environ('TEST_PRIVATE_KEY1')
    )
    market.buy_data(
        ocean,
        os.environ('TEST_PRIVATE_KEY2'),
        data_token.address,
        seller_wallet,
        min_amount=2,
        max_amount=5,
    )

    # Download a dataset.
    market.download_data(
        ocean,
        os.environ('TEST_PRIVATE_KEY2'),
        asset.did
    )

if __name__ == '__main__':

    # Test publishing a dataset.
    data_token, asset = test_publish_data()

    # Test selling a dataset.
    test_sell_data(data_token)

    # Test buying a dataset.
    test_buy_data(data_token, asset)
