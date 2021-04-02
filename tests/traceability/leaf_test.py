"""
Leaf Integration Test | Cannlytics

Author: Keegan Skeate
Created: Thu Mar 18 16:08:18 2021

License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Description:

    Perform required tests for Leaf Data Systems integration.
    The validation process requires completion of at least
    1 example of each API call listed in the Worksheet,
    and provide the Global ID and timestamp for each call.
    The MJ Freeway engineering team will pull logs and
    review the calls identified in the worksheet for
    successful completion:

        • Do the calls contain the required data?
        • Did the calls return errors?
        • Did the integrator use an excessive number of
        calls to complete the action?
    

Resources:

"""
import os
from dotenv import load_dotenv
from datetime import datetime

# DEV:
import leaf


def add_leaf_api_key(name, key, mme_code, owner):
    """Adds a Leaf Data Systems API key to the database.
    Args:
        name (str): 
        key (str): 
        mme_code (str):
        owner (str):
    """
    return NotImplementedError()



if __name__ == '__main__':
    
    # Record all requests made to the traceability system!
    now = datetime.now()
    current_time = now.isoformat()
    current_date = now.strftime('%m/%d/%Y')

    print('--------------------------------------------')
    print('Performing Leaf Data Systems Validation Test')
    print(current_time)
    print('--------------------------------------------')

    # Initialize the Leaf Data Systems traceability system API.
    load_dotenv()
    api_key = os.getenv('LEAF_TEST_API_KEY')
    mme_code = os.getenv('LEAF_TEST_PRODUCER_MME_CODE')
    traceability = leaf.authorize(api_key=api_key, mme_code=mme_code)

    # Create users for your facilities.
    # Requires the use of a Global ID for a licensee.
    # Get users for each facility.
    # Endpoint: '/user'
    # users = traceability.get_users()

    # Create an area.
    areas = [
        # {
        #     'name': 'Seed Vault',
        #     'type': 'non-quarantine',
        #     'external_id': 'area-1'
        # },
        {
            'name': 'Waste Room',
            'type': 'quarantine',
            'external_id': 'area-2'
        },
        # {
        #     'name': 'Drying Room',
        #     'type': 'quarantine',
        #     'external_id': 'area-3'
        # },
    ]
    areas = traceability.create_areas(areas)
    areas = traceability.get_areas()

    # Create a strain.
    # strains = [{'name': 'Gorilla Glue'}]
    # strains = traceability.create_strains(strains)

    # Create plant batches.
    # Requires the previous creation of strain and area.
    # Endpoint: '/batches'
    # batches = [{
    #     'type': 'propagation material',
    #     'origin': 'seed',
    #     'global_area_id': areas[0]['global_id'],
    #     'global_strain_id': strains[0]['global_id'],
    #     'num_plants': '33'
    # }]
    # batches = traceability.create_batches(batches)
    batches = traceability.get_batches()

    # Create a plant and add it to a batch.
    # Requires the previous creation of strain, area, and batch.
    # Endpoint: '/plants'
    plants =  [{
        'origin': 'seed',
        'stage': 'growing',
        'global_batch_id': batches[0]['global_id'],
        'plant_created_at': current_date,
    }]
    plants = traceability.create_plants(plants)
    
    # Create a partial disposal from a batch.
    # Requires the previous creation of inventory lot, batch, or plant.
    # Endpoint: '/disposals'
    disposed_at = now.strftime('%m/%d/%Y %h:%m')
    disposals = [{
        'external_id': 'disposal-1',
        'reason': 'unhealthy',
        'disposal_at': '06/07/2016 12:34pm',
        'qty': '13',
        'uom': 'ea',
        'source': 'batch',
        'global_batch_id': batches[0]['global_id'],
        'global_area_id': areas[1]['global_id'], # Area for waste.
        'global_plant_id': plants[0]['global_id'],
        'global_inventory_id': ''
    }]
    disposals = traceability.create_disposals(disposals)
    
    # https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
    
    # Create harvest batches.
    # Requires the previous creation of batch of plants.
    # Endpoint: '/plants/harvest_plants'
    # harvested_at = now.strftime('%m/%d/%Y %h:%m')
    harvested_at = now.isoformat()
    harvest = traceability.harvest_plants(
        area_id=plants[0]['global_area_id'],
        destination_id=areas[2]['global_id'],
        plant_ids=[plants[0]['global_id']],
        batch_id=plants[0]['global_batch_id'],
        external_id='harvest-1',
        harvested_at=harvested_at,
        flower_wet_weight=33,
        other_wet_weight=3.33,
        uom='gm'
    )

    # Create inventory lots.
    # Requires previous creation of area, strain, batch, and inventory type.
    # Endpoint: '/inventories'
    
    # Create an inventory adjustment.
    # Requires the previous creation of an inventory lot.
    # Endpoint: '/inventory_adjustments'
    
    # Create an inventory adjustment.
    # Requires the previous creation of an inventory lot.
    # Endpoint: '/inventory_transfers'

    # Create a lab result for a sample transferred to a lab.
    # Requires the previous creation of an inventory transfer, a lab user, 
    # and an inventory lot.
    # Endpoint: '/lab_result'
    
    # Create a sale.
    # Requires the previous creation of an area, batch, and inventory item.
    # Endpoint: '/sales'
    

    
    
    # Print out successful calls and save a log of the recorded requests.





