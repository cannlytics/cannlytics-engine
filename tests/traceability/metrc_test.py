'''
Metrc Integration Test | Cannlytics

Author: Keegan Skeate
Contact: keegan@cannlytics.com
Created: Mon Mar 29 14:18:18 2021
License: MIT License

Description:

    Perform required tests for Metrc integration, recording verification items;

        - Result code: The status code of the response.
        - ID Number: The UID for a created object, typically a 5 digit number. 
        - Names: Names for created objects, such as strain or location name.
        - Tag Number: Plant and package tags
        - Last Modified Date: The time the test or actions were ran.
        - Request Sent: The requested URL.
        - JSON Body: Minified JSON response.

    All successful requests will return a 200 status code. Get support if you cannot
    obtain a 200 status code for any request.

Resources:

    https://api-ok.metrc.com/Documentation

'''
import os
from dotenv import dotenv_values
from datetime import datetime
from time import sleep

# Import cannlytics locally for testing.
import sys
sys.path.insert(0, os.path.abspath('../../'))
from cannlytics import firebase as fb
from cannlytics.traceability import metrc # pylint: disable=no-name-in-module, import-error
from cannlytics.traceability.metrc.utils import clean_nested_dictionary # pylint: disable=no-name-in-module, import-error


from cannlytics.traceability.metrc.models import ( # pylint: disable=no-name-in-module, import-error
    Facility,
    Item,
    PlantBatch,
)


def main():
    '''Perform Metrc API integration test.'''
    return NotImplementedError


if __name__ == '__main__':

    #------------------------------------------------------------------
    # Initialization
    #------------------------------------------------------------------
    
    # Initialize the current time.
    now = datetime.now()
    current_time = now.isoformat()
    current_date = now.strftime('%m/%d/%Y')
    today = current_time[:10]

    # Initialize Firebase.
    config = dotenv_values('../../.env')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['GOOGLE_APPLICATION_CREDENTIALS']
    db = fb.initialize_firebase()

    # Initialize a Metrc client.
    vendor_api_key = config['METRC_TEST_VENDOR_API_KEY']
    user_api_key = config['METRC_TEST_USER_API_KEY']
    track = metrc.authorize(vendor_api_key, user_api_key)

    print('--------------------------------------------')
    print('Performing Metrc Validation Test')
    print(current_time)
    print('--------------------------------------------')

    #------------------------------------------------------------------
    # Facilities
    #------------------------------------------------------------------

    # Get facilities, with permissions set by the state for each facility type.
    # facilities = track.get_facilities()

    # Define primary cultivator, lab, and retailer for tests.
    # cultivator, lab, retailer = None, None, None
    # for facility in facilities:
    #     license_type = facility.license_type
    #     if cultivator is None and license_type == 'Grower':
    #         cultivator = facility
    #     elif lab is None and license_type == 'Testing Laboratory':
    #         lab = facility
    #     elif retailer is None and license_type == 'Dispensary':
    #         retailer = facility

        # Save facility to Firestore.
        # license_number = facility.license_number
        # ref = f'tests/metrc/organizations/1/facilities/{license_number}'
        # data = clean_nested_dictionary(facility.to_dict())
        # data['license_number'] = license_number
        # firebase.update_document(ref, data)
    
    # Get facilities from Firestore.
    ref = 'tests/metrc/organizations/1/facilities'
    cultivator = Facility(track, fb.get_document(f'{ref}/4b-X0002'))
    # retailer = Facility(track, fb.get_document(f'{ref}/3c-X0002'))
    # processor = Facility(track, fb.get_document(f'{ref}/5b-X0002'))
    # lab = Facility(track, fb.get_document(f'{ref}/405-X0001'))
        

    #------------------------------------------------------------------
    # Locations ✓
    #------------------------------------------------------------------

    # Create a new location using: POST /locations/v1/create
    cultivation_name = 'MediGrow'
    cultivation_original_name = 'medi grow'
    # cultivator.create_locations([cultivation_original_name]) # , 'Harvest Location', 'Plant Location'
    
    # Get created location
    # cultivation= None
    # locations = track.get_locations(action='active', license_number=cultivator.license_number)
    # for location in locations:
    #     if location.name == cultivation_original_name:
    #         cultivation = location

    # Update the name of the location using: POST /locations/v1/update
    # cultivator.update_locations([cultivation.uid], [cultivation_name])

    # View the location using GET /locations/v1/{id}
    cultivation_uid = '10705'
    traced_location = cultivator.get_locations(uid=cultivation_uid)


    #------------------------------------------------------------------
    # Strains ✓
    #------------------------------------------------------------------

    # Create a new strain using: POST /strains/v1/create
    strain_name = 'New Old-Time Moonshine'
    # strain = {
    #     'Name': strain_name,
    #     'TestingStatus': 'None',
    #     'ThcLevel': 0.2420,
    #     'CbdLevel': 0.0333,
    #     'IndicaPercentage': 0.0,
    #     'SativaPercentage': 100.0
    # }
    # track.create_strains([strain], license_number=cultivator.license_number)

    # Get the created strain's ID.
    # new_strain = None
    # strain_id = None
    # strains = track.get_strains(license_number=cultivator.license_number)
    # for s in strains:
    #     if s.name == strain_name:
    #         strain_id = s.uid
    #         new_strain = s

    # Change the THC and CBD levels using: POST /strains/v1/update
    # new_strain.update(thc_level=0.1333, cbd_level=0.0777)

    # View the Strain using GET /strains/v1/{id}
    strain_uid = '14504'
    traced_strain = track.get_strains(uid=strain_uid, license_number=cultivator.license_number)
    # print(traced_strain.name, '| THC:', traced_strain.thc_level, 'CBD:', traced_strain.cbd_level)


    #------------------------------------------------------------------
    # Items ✓
    #------------------------------------------------------------------
    
    # Create an item using: POST /items/v1/create
    # item_name = 'New Old-Time Moonshine Teenth'
    # item = Item.create_from_json(track, cultivator.license_number, {
    #     'ItemCategory': 'Flower & Buds',
    #     'Name': item_name,
    #     'UnitOfMeasure': 'Ounces',
    #     'Strain': strain_name,
    # })

    # Get the item's UID.
    # new_item = None
    # items = track.get_items(license_number=cultivator.license_number)
    # for i in items:
    #     print(i.name, '|', i.product_category_name)
    #     if i.name == item_name:
    #         new_item = i

    # Change the Unit Of Measure Type using: POST /items/v1/update
    # new_item.update(unit_of_measure='Grams')

    # View the item using: GET /Items/v1/{id}
    # traced_item = track.get_items(uid=new_item.id, license_number=cultivator.license_number)
    # print('Successfully created, updated, and retrieved item:')
    # print(traced_item.id, '|', traced_item.unit_of_measure)

    # Create items used for batches.
    # clone = Item.create_from_json(track, cultivator.license_number, {
    #     'ItemCategory': 'Seeds',
    #     'Name': 'New Old-Time Moonshine Mature Plants',
    #     'UnitOfMeasure': 'Each',
    #     'Strain': strain_name,
    # })

    # Get the clone for future use.
    clone_uid = '12324'
    clone_item = track.get_items(uid=clone_uid, license_number=cultivator.license_number)

    #------------------------------------------------------------------
    # Batches FIXME: Cannot create packages or change growth phase!
    #------------------------------------------------------------------

    # Create a new plant batch containing
    # 6 plants using: POST /plantbatches/v1/createplantings
    # batch_name = 'New Old-Time Moonshine SoG'
    # batch = PlantBatch.create_from_json(track, cultivator.license_number, {
    #     'Name': batch_name,
    #     'Type': 'Seed',
    #     'Count': 6,
    #     'Strain': strain_name,
    #     'Location': 'MediGrow',
    #     # 'PatientLicenseNumber': 'X00002',
    #     'ActualDate': today,
    # })
    # sleep(10) # Hack to wait for Metrc to create the batch

    # Get the plant batch
    # traced_batch = None
    # batches = track.get_batches(license_number=cultivator.license_number)
    # for b in batches:
    #     print(b.name, '|', b.type)
    #     if b.name == batch_name:
    #         traced_batch = b

    # batch_uid = '8502'
    # traced_batch = track.get_batches(uid=batch_uid, license_number=cultivator.license_number)

    # Create a package containing 3 clones from
    # The Plant Batch created in step 1 using: POST /plantbatches/v1/createpackages
    # batch_tag = 'ABCDEF012345670000013304'
    # package = {
    #     # 'id': traced_batch.id,
    #     # 'plant_batch': batch_name,
    #     'id': '8503',
    #     # 'plant_batch': 'New Old-Time Moonshine Sea of Green',
    #     'count': 3,
    #     'location': 'MediGrow',
    #     # 'Location': None,
    #     'item': 'New Old-Time Moonshine Clone',
    #     'tag': batch_tag,
    #     # 'patient_license_number': 'X00001',
    #     'note': 'A package containing 3 clones from the Old-time Moonshine Plant Batch',
    #     'is_trade_sample': False,
    #     'is_donation': False,
    #     'actual_date': today
    # }
    # traced_batch.create_package(package)

    # Change the growth phase of 2 of the plants created in
    # Step 1 to the Vegetative Stage using:  POST /plantbatches/v1/changegrowthphase
    # growth_stage = {
    #     'name': 'New Old-Time Moonshine Sea of Green',
    #     'count': 4,
    #     'starting_tag': 'ABCDEF012345670000013296',
    #     'growth_phase': 'Vegetative',
    #     'new_location': 'MediGrow',
    #     'growth_date': today,
    #     # 'PatientLicenseNumber': 'X00002'
    # }
    # traced_batch.change_growth_phase(growth_stage)

    # Destroy 1 of the plants using: POST /plantbatches/v1/destroy
    # traced_batch.destroy_plants(count=1, reason='Wrong facility.')



    #---------
    # SCRAP

        # package = {
    #     'id': traced_batch.id,
    #     # "plant_batch": batch_name,
    #     "count": 3,
    #     "location": 'Harvest Location',
    #     "item": "Old-time Moonshine Clone",
    #     "tag": batch_tag,
    #     # "PatientLicenseNumber": "P00001",
    #     "note": "A package containing 3 clones from the Old-time Moonshine Plant Batch.",
    #     "is_trade_sample": False,
    #     "is_donation": False,
    #     "actual_date": today
    # }
    # traced_batch.create_package_from_plants(package)


    #------------------------------------------------------------------
    # Plants FIXME: Depends on plant batches
    #------------------------------------------------------------------

    # Using one of the Plants from Step 3 in the Plant batch section,
    # Change growth phase from Vegetative to Flowering using:
    # POST /plants/v1/changegrowthphases
    # growth_stage = {
    #     'Name': 'Old-time Moonshine Flowering',
    #     'Count': 1,
    #     'StartingTag': batch_tag,
    #     'GrowthPhase': 'Flowering',
    #     'NewLocation': 'Harvest Location',
    #     'GrowthDate': '2021-04-06',
    #     # 'PatientLicenseNumber': 'X00002'
    # }
    # traced_batch.change_growth_phase(growth_stage)

    # Using the now Flowering Plant in step above,
    # Move that plant to a different room using: POST /plants/v1/moveplants
    # destination = {
    #     'Name': 'AK-47 Clone 1/31/2017',
    #     'Location': 'Plants Location',
    #     'MoveDate': '2015-12-15'
    # }

    # Using the other Plant created by Step 3  in the Plant batch section,
    # Destroy that plant using: POST /plants/v1/destroyplants

    # Using the Plant now in the Flowering Stage from Step 1
    # Manicure from the plant using: POST /plants/v1/manicureplants

    # Using the Plant in the Flowering Stage from Step 2
    # Harvest the plant using: POST /plants/v1/harvestplants


    #------------------------------------------------------------------
    # Harvest FIXME: Depends on plant batches
    #------------------------------------------------------------------

    # Step 1 Using the Harvest Created in Step 5 from Plants,
    # Create a package using: POST /harvests/v1/create/packages

    # Step 2  Using the Harvest Created in Step 5 from Plants,
    # Remove the remaining weight as Waste
    # (MOISTURE LOSS IS NOT REMOVED AS WASTE): POST /harvests/v1/removewaste

    # Step 3 Using the Harvest created in Plants Step 1
    # Finish that Harvest using: POST /harvests/v1/finish

    # Step 4 Using the Harvest finished in Step 3
    # Unfinish that Harvest using: POST /harvests/v1/unfinish


    #------------------------------------------------------------------
    # Packages
    #------------------------------------------------------------------

    # Step 1 Using the Package created in Harvest Step 1 OR create a
    # package from an existing package that you have found.
    # Note You can create more packages to use in the
    # rest of the evaluation for sales and transfer templates.
    # Create a package from another package using: POST /packages/v1/create
    packs = track.get_packages()

    package_label = 'ABCDEF012345670000020201'

    new_package = {
        "Tag": package_label,
        "Location": None,
        "Item": "Buds",
        "Quantity": 16.0,
        "UnitOfMeasure": "Ounces",
        "PatientLicenseNumber": "X00001",
        "Note": "Creation of a package from an existing package.",
        "IsProductionBatch": False,
        "ProductionBatchNumber": None,
        "IsDonation": False,
        "ProductRequiresRemediation": False,
        "UseSameItem": False,
        "ActualDate": today,
        "Ingredients": [
            {
                "Package": "ABCDEF012345670000010041",
                "Quantity": 8.0,
                "UnitOfMeasure": "Ounces"
            },
            {
                "Package": "ABCDEF012345670000010042",
                "Quantity": 8.0,
                "UnitOfMeasure": "Ounces"
            }
        ]
    }

    # Step 2 Using the new package created in Packages Step 1
    # change the item of a package using: POST/packages/v1/change/item
    item_change = {
        "Label":package_label,
        "Item": "Shake"
    }
    new_package.change_item(item_change)

    # Step 3 Using the new package created in Packages Step 1
    # adjust the weight to 0 using: POST/packages/v1/adjust
    adjustment = {
        "Label": "ABCDEF012345670000010041",
        "Quantity": -2.0,
        "UnitOfMeasure": "Ounces",
        "AdjustmentReason": "Drying",
        "AdjustmentDate": "2015-12-15",
        "ReasonNote": None
    }

    # Step 4 Using the new package created in Packages Step 1
    #  Finish a package using: POST/packages/v1/finish

    # Step 5 Using the new package created in Packages Step 1
    # Unfinish a package using: POST/packages/v1/unfinish

    #------------------------------------------------------------------
    # Incoming transfers
    #------------------------------------------------------------------

    # Step 1a Set up an external Incoming transfer
    # using: POST/transfers/v1/external/incoming

    # Step 1b Set up another external Incoming transfer
    # using: POST/transfers/v1/external/incoming

    # Step 2 Find the two Transfers created in Step 1a and 1b
    # by using the date search: GET/transfers/v1/incoming

    # Step 3 Update one of the Transfers created in Step 1 by
    # using: PUT/transfers/v1/external/incoming


    #------------------------------------------------------------------
    # Transfer templates
    #------------------------------------------------------------------

    # Step 1a Set up a Template using: POST/transfers/v1/templates

    # Step 1b Set up another Template using: POST/transfers/v1/templates

    # Step 2 Find the two Templates created in Step 1a and 1b by
    # using the date search: GET/transfers/v1/templates  

    # Step 3 Find a Template by the Template ID number
    # using: GET/transfers/v1/templates/{id}/deliveries

    # Step 4 Update one of the Templates created in Step 1
    # using: PUT/transfers/v1/templates


    #------------------------------------------------------------------
    # Outgoing transfers
    #------------------------------------------------------------------

    # Step 1 Find an Incoming Transfer: GET/transfers/v1/incoming

    # Step 2 Find an Outgoing Transfer: GET/transfers/v1/outgoing

    # Step 3 Find a Rejected Transfer: GET/transfers/v1/rejected                                  

    # Step 4 Find a Transfer by the Manifest ID number: GET/transfers/v1/{id}/deliveries

    # Step 5 Find The Packages Using the Delivery ID number: GET/transfers/v1/delivery/{id}/packages

    # Transfers Wholesale Step 6 Find Packages Wholesale Pricing
    # Using the Delivery ID GET/transfers/v1/delivery/{id}/packages/wholesale


    #------------------------------------------------------------------
    # Lab results
    #------------------------------------------------------------------

    # Record a lab test result using: POST /labtests/v1/record


    #------------------------------------------------------------------
    # Sales
    #------------------------------------------------------------------

    # Step 1 Create a sales receipt for a package using: POST /sales/v1/receipts
    
    # Step 2 Update the sales receipt using: PUT /sales/v1/receipts 

    # Step 3 Void the sales receipt using: DELETE /sales/v1/receipts/{id}

















    #------------------------------------------------------------------
    # Get all logs for verification (optional)
    #------------------------------------------------------------------

    # filters = [{'key': 'test', 'operation': '==', 'value': 'firebase_test'}]
    # docs = fb.get_collection(log_collection, filters=filters)

