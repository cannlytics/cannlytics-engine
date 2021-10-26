"""
Test Data Market

Authors: Keegan Skeate <keegan@cannlytics.com>
Created: 10/11/2021
Updated: 10/16/2021
"""
# Standard imports.
import os
import sys
import yaml

# Internal imports.
sys.path.append('../../')
from cannlytics.data import market # pylint: disable=import-error
from cannlytics.firebase import (
    initialize_firebase,
    update_document,
)

SELLER_KEY = 'CANNLYTICS_PRIVATE_KEY'
BUYER_KEY = 'TEST_PRIVATE_KEY2'


def test_publish_data(dataset):
    """Publish a dataset on the data market."""

    # Initialize Ocean market.
    ocean = market.initialize_market('../../env.yaml')
    config = None
    with open('../../env.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    # Mint a test OCEAN.
    from ocean_lib.ocean.mint_fake_ocean import mint_fake_OCEAN
    os.environ['FACTORY_DEPLOYER_PRIVATE_KEY'] = config['FACTORY_DEPLOYER_PRIVATE_KEY']
    mint_fake_OCEAN(ocean.config)

    # Publish a dataset.
    data_token, asset = market.publish_data(
        ocean,
        config.get(SELLER_KEY),
        dataset['files'],
        dataset['datatoken_name'],
        dataset['datatoken_symbol'],
        dataset['author'],
        dataset['license'],
    )
    
    # Upload the datatoken and asset information.
    initialize_firebase()
    ref = f'public/market/datasets/{asset.did}'
    update_document(ref, dataset)
    
    return data_token, asset

def test_sell_data(data_token):
    """Sell a dataset on the data market."""

    # Initialize Ocean market.
    ocean = market.initialize_market()

    # Sell a dataset.
    market.sell_data(
        ocean,
        os.environ(SELLER_KEY),
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
        os.environ(SELLER_KEY)
    )
    market.buy_data(
        ocean,
        os.environ(BUYER_KEY),
        data_token.address,
        seller_wallet,
        min_amount=2,
        max_amount=5,
    )

    # Download a dataset.
    market.download_data(
        ocean,
        os.environ(BUYER_KEY),
        asset.did
    )

if __name__ == '__main__':
    
    dataset = {
        'sample_file': '',
        'terms': '',
        'price_usd': 3867,
        'datatoken_symbol': 'TD-1',
        'published_at': '2021-10-25',
        'description': 'This is the first test data!',
        'access_type': 'download',
        'file': '',
        'image_url': '',
        'did': '123',
        'author': 'KLS',
        'published_by': 'KLS',
        'datatoken_name': 'test-data',
        'timeout': 0,
        'price_eth': 1,
        'tags': ['test'],
        'title': 'Test Dataset',
        'license': 'CC0: Public Domain',
        'files': [
            {
                "index": 0,
                "contentType": "text/text",
                "url": "https://raw.githubusercontent.com/trentmc/branin/main/branin.arff"
            }
        ]
    }

    # Test publishing a dataset.
    data_token, asset = test_publish_data(dataset)

    # Test selling a dataset.
    # test_sell_data(data_token)

    # Test buying a dataset.
    # test_buy_data(data_token, asset)
