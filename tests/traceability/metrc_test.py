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

# Import cannlytics locally for testing.
import sys
sys.path.insert(0, os.path.abspath('../../'))
from cannlytics import firebase as fb
from cannlytics.traceability import metrc # pylint: disable=no-name-in-module, import-error
from cannlytics.traceability.metrc.utils import clean_nested_dictionary # pylint: disable=no-name-in-module, import-error


from cannlytics.traceability.metrc.models import ( # pylint: disable=no-name-in-module, import-error
    Facility,
    Item
)


def main():
    '''Perform Metrc API integration test.'''
    return NotImplementedError


if __name__ == '__main__':

    #------------------------------------------------------------------
    # Initialization
    #------------------------------------------------------------------
    
    # Initialize Firebase to save data and log API requests.
    now = datetime.now()
    current_time = now.isoformat()
    current_date = now.strftime('%m/%d/%Y')
    config = dotenv_values('../../.env')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['GOOGLE_APPLICATION_CREDENTIALS']
    db = fb.initialize_firebase()
    log_collection = 'tests/metrc/metrc_logs'
    user = {
        'uid': 'test',
        'display_name': 'CannBot',
        'email': 'bot@cannlytics.com',
        'photo_url': 'https://robohash.org/bot@cannlytics.com',
    }

    print('--------------------------------------------')
    print('Performing Metrc Validation Test')
    print(current_time)
    print('--------------------------------------------')

    # Initialize the Metrc traceability system API.
    vendor_api_key = config['METRC_TEST_VENDOR_API_KEY']
    user_api_key = config['METRC_TEST_USER_API_KEY']
    track = metrc.authorize(vendor_api_key, user_api_key)

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
    cultivator = Facility(track, fb.get_document(f'{ref}/4a-X0001'))
    # retailer = Facility(track, fb.get_document(f'{ref}/3a-X0001'))
    # lab = Facility(track, fb.get_document(f'{ref}/405-X0001'))
        

    #------------------------------------------------------------------
    # Locations
    #------------------------------------------------------------------

    # Test: Create a new location using POST /locations/v1/create
    # by creating locations at the cultivator for growing.
    # cultivation= None
    # cultivation_name = 'CLT Cultivation'
    # cultivator.create_locations([cultivation_name])
    # locations = track.get_locations(action='active', license_number=cultivator.license_number)
    # for location in locations:
    #     if location.name == cultivation_name:
    #         cultivation = location

    # Create log in Firestore
    # firebase.create_log(
    #     log_collection,
    #     user,
    #     'Created a new location.',
    #     'traceability_test',
    #     'metrc',
    #     changes=[{
    #         'status_code': 200,
    #         'license_number': cultivator.license_number,
    #         'name': cultivation.name,
    #         'uid': cultivation.uid,
    #         'last_modified_date': None,
    #         'request': f'https://sandbox-api-ok.metrc.com/locations/v1/create?licenseNumber={cultivator.license_number}',
    #     }]
    # )

    # Update the name of the location using: POST /locations/v1/update
    # cultivator.update_locations([cultivation.uid], [f'{cultivation_name} Updated'])

    # View the location using GET /locations/v1/{id}
    # cultivations = cultivator.get_locations(uid=cultivation.uid)


    #------------------------------------------------------------------
    # Strains
    #------------------------------------------------------------------

    # Create a new strain using: POST /strains/v1/create
    # strain_name = 'Old-time Moonshine'
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
    # new_strain.update(thc=0.1333, cbd=0.0777)

    # View the Strain using GET /strains/v1/{id}
    # strains = track.get_strains(uid=new_strain.uid, license_number=cultivator.license_number)
    # for s in strains:
    #     print(s.name, '| THC:', s.thc, 'CBD:', s.cbd)

    #------------------------------------------------------------------
    # Items
    #------------------------------------------------------------------
    
    # Create an item using: POST /items/v1/create
    item_name = 'Old-time Moonshine Teenth'
    # item = Item.create_from_json(track, cultivator.license_number, {
    #     'ItemCategory': 'Flower & Buds',
    #     'Name': item_name,
    #     'UnitOfMeasure': 'Kilograms',
    #     'Strain': 'Old-time Moonshine',
    #     'ItemBrand': None,
    #     'AdministrationMethod': None,
    #     'UnitCbdPercent': None,
    #     'UnitCbdContent': None,
    #     'UnitCbdContentUnitOfMeasure': None,
    #     'UnitCbdContentDose': None,
    #     'UnitCbdContentDoseUnitOfMeasure': None,
    #     'UnitThcPercent': None,
    #     'UnitThcContent': None,
    #     'UnitThcContentUnitOfMeasure': None,
    #     'UnitThcContentDose': None,
    #     'UnitThcContentDoseUnitOfMeasure': None,
    #     'UnitVolume': None,
    #     'UnitVolumeUnitOfMeasure': None,
    #     'UnitWeight': None,
    #     'UnitWeightUnitOfMeasure': None,
    #     'ServingSize': None,
    #     'SupplyDurationDays': None,
    #     'NumberOfDoses': None,
    #     # 'Ingredients': None,
    #     'PublicIngredients': None,
    #     'ItemIngredients': None,
    #     'Description': None
    # })

    # Get the item's UID.
    new_item = None
    items = track.get_items(license_number=cultivator.license_number)
    for i in items:
        if i.name == item_name:
            new_item = i

    # Change the Unit Of Measure Type using: POST /items/v1/update
    new_item.update(unit_of_measure='Grams')

    # View the item using: GET /Items/v1/{id}
    traced_item = track.get_items(uid=new_item.id, license_number=cultivator.license_number)
    print('Successfully created, updated, and retrieved item:')
    print(traced_item.id, '|', traced_item.unit_of_measure)

    #------------------------------------------------------------------
    # Batches
    #------------------------------------------------------------------

    # Create a new plant batch containing
    # 6 plants using: POST /plantbatches/v1/createplantings

    # Create a package containing 3 clones from
    # The Plant Batch ceated in step 1 using:                                                           POST /plantbatches/v1/createpackages

    # Change the growth phase of 2 of the plants created in
    # Step 1 to the Vegetative Stage using:                                                                 POST /plantbatches/v1/changegrowthphase

    # Destroy 1 of the plants using: POST /plantbatches/v1/destroy


    #------------------------------------------------------------------
    # Plants
    #------------------------------------------------------------------

    # Plants Step 1                                                                      Using one of the Plants from Step 3 in the                      Plant batch section, Change growth phase from                                Vegetative to Flowering using:POST /plants/v1/changegrowthphases

    # Plants Step 2                                                                            Using the now Flowering Plant in step above,                                      Move that plant to a different room using:                                                       POST /plants/v1/moveplants

    # Plants Step 3                                                                                Using the other Plant created by Step 3                                       in the Plant batch section,                                                     Destroy that plant using:                                                         POST /plants/v1/destroyplants

    # Plants Step 4                                                                              Using the Plant now in the Flowering Stage from Step 1                                                         Manicure from the plant using:                                            POST /plants/v1/manicureplants

    # Plants Step 5                                                                               Using the Plant in the Flowering Stage from Step 2      Harvest the plant using:                                                       POST /plants/v1/harvestplants


    #------------------------------------------------------------------
    # Harvest
    #------------------------------------------------------------------

    # Harvest Step 1                                                                 Using the Harvest Created in Step 5 from Plants ,             Create a package using:                                                                           POST /harvests/v1/create/packages

    # Harvest Step 2                                                                 Using the Harvest Created in Step 5 from Plants ,            Remove the remaing weight as Waste (MOISTURE LOSS IS NOT REMOVED AS WASTE) :                                                                                POST /harvests/v1/removewaste

    # Harvest Step 3                                                                 Using the Harvest created in Plants Step 1                Finish that Harvest using:                                                         POST /harvests/v1/finish

    # Harvest Step 4                                                                        Using the Harvest finished in Step 3                      Unfinish that Harvest using:                                                                       POST /harvests/v1/unfinish


    #------------------------------------------------------------------
    # Packages
    #------------------------------------------------------------------

    # Packages Step 1                                                                Using the Package created in Harvest Step 1 OR create a package from an existing package that you have found. Note You can create more packages to use in the rest of the evaulation for sales and transfer templates.                                                                      Create a package from another package using: POST /packages/v1/create

    # Packages Step 2                                                               Using the new package created in Packages Step 1                             Change the item of a package using:                                POST/packages/v1/change/item

    # Packages Step 3                                                               Using the new package created in Packages Step 1                             Adjust the weight to 0 using:                                                       POST/packages/v1/adjust

    # Packages Step 4                                                               Using the new package created in Packages Step 1                             Finish a package using:                                                       POST/packages/v1/finish

    # Packages Step 5                                                               Using the new package created in Packages Step 1                             Unfinish a package using:                                                POST/packages/v1/unfinish


    #------------------------------------------------------------------
    # Incoming transfers
    #------------------------------------------------------------------

    #  Step 1a         Set up an external Incoming transfer                                                       POST/transfers/v1/external/incoming

    # Step 1b         Set up another external Incoming transfer                                                       POST/transfers/v1/external/incoming

    # Step 2             Find the two Transfers created in Step 1a and 1b                               by  using the date search                                                           GET/transfers/v1/incoming             

    # Step 3             Update one of the Transfers  created in Step 1 by                                                   PUT/transfers/v1/external/incoming


    #------------------------------------------------------------------
    # Transfer templates
    #------------------------------------------------------------------

    #  Step 1a          Set up a Template                                                                     POST/transfers/v1/templates

    # Step 1b        Set up another Template                                                         POST/transfers/v1/templates

    # Step 2             Find the two Templates created in Step 1a and 1b                               by  using the date search                                                           GET/transfers/v1/templates  

    # Step 3          Find a Template by the Template ID number                           GET/transfers/v1/templates/{id}/deliveries

    # Step 4             Update one of the Templates  created in Step 1 by PUT/transfers/v1/templates


    #------------------------------------------------------------------
    # Outgoing transfers
    #------------------------------------------------------------------

    #  Step 1          Find an Incoming Transfer                                                            GET/transfers/v1/incoming

    # Step 2                 Find an Outgoing  Transfer                                                           GET/transfers/v1/outgoing

    # Step 3        Find a Rejected  Transfer                                                                               GET/transfers/v1/rejected                                  

    # Step 4          Find a Transfer by the Manifest ID number                           GET/transfers/v1/{id}/deliveries

    # Step 5        Find The Packages Using the Delivery ID number                 GET/transfers/v1/delivery/{id}/packages

    # Transfers Wholesale Step 6                                                               Find Packages  Wholesale Pricing  Using the Delivery ID                                                                                     GET/transfers/v1/delivery/{id}/packages/wholesale


    #------------------------------------------------------------------
    # Lab results
    #------------------------------------------------------------------

    # Record a lab test result using:                              POST /labtests/v1/record

    #------------------------------------------------------------------
    # Sales
    #------------------------------------------------------------------

    #  Step 1                                                                             Create a sales receipt using:                                         POST /sales/v1/receipts                                              Using a package                                                               created in the Package Tab of the evaluation.

    # Step 2                                                                       Update the sales receipt created in Step 1 using:                                                                              PUT /sales/v1/receipts 

    # Step 3                                                                           Void the sales receipt created in Step 1 using:                                                                             DELETE /sales/v1/receipts/{id}

    #------------------------------------------------------------------
    # Get all logs for verification
    #------------------------------------------------------------------

    filters = [{'key': 'test', 'operation': '==', 'value': 'firebase_test'}]
    docs = fb.get_collection(log_collection, filters=filters)

