# -*- coding: utf-8 -*-
"""
cannlytics.traceability.metrc.client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains the Client class responsible for
communicating with the Metrc API.
"""

# FIXME:
# https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
# https://pynative.com/python-convert-json-data-into-custom-python-object/
# encode Object it
# studentJson = json.dumps(student, cls=StudentEncoder, indent=4)

# Decode JSON
# resultDict = json.loads(studentJson)

import requests

from json import dumps, loads # DEV
from requests import Session

from .exceptions import MetrcAPIError
from .models import *
from .urls import *
from .utils import format_params


class Client(object):
    """An instance of this class communicates with
    the Metrc API.

        vendor_api_key (str): A Metrc API key, obtained from Metrc
        upon successful certification. The vendor API key is the
        software provider's secret used in every instance, regardless
        of location or licensee.
            
        user_api_key (str): A licensee's user's secret obtained
        from the Metrc user interface. The user's permissions
        determine the level of access to the Metrc API.
    
    Example:
        
        track = metrc.Client(vendor_api_key='abc', user_api_key='xyz')
    """

    def __init__(self, vendor_api_key, user_api_key):
        self.base = METRC_API_BASE_URL
        self.test_api = METRC_API_BASE_URL_TEST
        self.user_api_key = user_api_key
        self.vendor_api_key = vendor_api_key
        # self.session = Session()
        # self.session.auth = (vendor_api_key, user_api_key)
        # self.headers = {'Content-Type': 'application/json'}

    def request(
        self,
        method,
        endpoint,
        data=None,
        params=None,
    ):
        """Make a request to the Metrc API."""
        # TODO: See if session is optimal
        # https://stackoverflow.com/questions/26745462/basic-authentication-not-working-with-requests-library
        # session = Session()
        # session.auth = (self.vendor_api_key, self.user_api_key)
        response = getattr(requests, method)(
            endpoint,
            auth=(self.vendor_api_key, self.user_api_key),
            json=data,
            # headers=self.headers,
            params=params,
        )
        print('\n\nREQUEST:', response.request.url)
        print('\n\nBODY:\n\n', response.request.body)
        print('\n\nSTATUS CODE:', response.status_code)
        try:
            print('\n\nRESPONSE:\n\n', dumps(response.json()), '\n\n')
        except ValueError:
            print('\n\nRESPONSE:\n\n', response.text, '\n\n')
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                return response.text
        else:
            raise MetrcAPIError(response)

    def parse(self, data, custom_object):
        """Parse JSON response into a given object type."""
        return loads(data, object_hook=custom_object)

    #------------------------------------------------------------------
    # Employees and facilities
    #------------------------------------------------------------------

    def get_employees(self, license_number=''):
        """Get all employees.
        Args:
            license_number (str): A licensee's license number.
        """
        url = METRC_EMPLOYEES_URL
        params = format_params(license_number=license_number)
        response = self.request('get', url, params=params)
        return [Employee(self, x) for x in response]


    def get_facilities(self):
        """Get all facilities."""
        url = METRC_FACILITIES_URL
        response = self.request('get', url)
        return [Facility(self, x) for x in response]
    

    #------------------------------------------------------------------
    # Harvests
    #------------------------------------------------------------------

    def get_harvests(
        self,
        uid='',
        action='',
        license_number='',
        start='',
        end='',
    ):
        """Get harvests.
        Args:
            uid (str): The UID of a harvest, takes precedent over action.
            action (str): A specific filter to apply, including:
                `active`, `onhold`, `inactive`, `waste/types`.
            license_number (str): The licensee's license number.
            start (str): An ISO 8601 formatted string to restrict the start
                by the last modified time.
            end (str): An ISO 8601 formatted string to restrict the end
                by the last modified time.
        """
        if uid:
            url = METRC_HARVESTS_URL % uid
        else:
            url = METRC_HARVESTS_URL % action
        params = format_params(license_number=license_number, start=start, end=end)
        response = self.request('get', url, params=params)
        try:
            return Harvest(self, response, license_number)
        except AttributeError:
            return [Harvest(self, x, license_number) for x in response]
    

    def finish_harvest(self, data, license_number=''):
        """Finish a harvests.
        Args:
            data (list): A list of packages (dict) to finish.
            license_number (str): A specific license number.
        """
        url = METRC_HARVESTS_URL % 'finish'
        params = format_params(license_number=license_number)
        return self.request('post', url, data=data, params=params)
    

    def unfinish_harvest(self, data, license_number=''):
        """Unfinish a harvests.
        Args:
            data (list): A list of packages (dict) to unfinish.
            license_number (str): A specific license number.
        """
        url = METRC_HARVESTS_URL % 'unfinish'
        params = format_params(license_number=license_number)
        return self.request('post', url, data=data, params=params)
    

    def remove_waste(self, data, license_number=''):
        """Remove's waste from a harvest.
        Args:
            data (list): A list of waste (dict) to unfinish.
            license_number (str): A specific license number.
        """
        url = METRC_HARVESTS_URL % 'removewaste'
        params = format_params(license_number=license_number)
        return self.request('post', url, data=data, params=params)
    

    def move_harvest(self, data, license_number=''):
        """Move a harvests.
        Args:
            data (list): A list of harvests (dict) to move.
            license_number (str): A specific license number.
        """
        url = METRC_HARVESTS_URL % 'move'
        params = format_params(license_number=license_number)
        return self.request('put', url, data=data, params=params)
    

    def create_harvest_packages(self, data, license_number=''):
        """Create packages from a harvest.
        Args:
            data (list): A list of packages (dict) to create.
            license_number (str): A specific license number.
        """
        url = METRC_HARVESTS_URL % 'create/packages'
        params = format_params(license_number=license_number)
        return self.request('post', url, data=data, params=params)
    

    def create_harvest_testing_packages(self, data, license_number=''):
        """Create packages from a harvest for testing.
        Args:
            data (list): A list of testing packages (dict) to create.
            license_number (str): A specific license number.
        """
        url = METRC_HARVESTS_URL % 'create/packages/testing'
        params = format_params(license_number=license_number)
        return self.request('post', url, data=data, params=params)


    #------------------------------------------------------------------
    # Items
    #------------------------------------------------------------------

    def get_items(
        self,
        uid='',
        action='active',
        license_number='',
    ):
        """Get items.
        Args:
            uid (str): The UID of an item.
            action (str): A specific type of item to filter by:
                `active`, `categories`, `brands`.
            license_number (str): A specific license number.
        """
        if uid:
            url = METRC_ITEMS_URL % uid
        else:
            url = METRC_ITEMS_URL % action
        params = format_params(license_number=license_number)
        response = self.request('get', url, params=params)
        try:
            return Item(self, response, license_number)
        except AttributeError:
            return [Item(self, x, license_number) for x in response]


    def create_items(self, data, license_number=''):
        """Create items.
        Args:
            data (list): A list of items (dict) to create.
        """
        url = METRC_ITEMS_URL % 'create'
        params = format_params(license_number=license_number)
        return self.request('post', url, data=data, params=params)


    def update_items(self, data, license_number=''):
        """Update items.
        Args:
            data (list): A list of items (dict) to update.
        """
        url = METRC_ITEMS_URL % 'update'
        params = format_params(license_number=license_number)
        return self.request('post', url, data=data, params=params)


    def delete_item(self, uid, license_number=''):
        """Delete item.
        Args:
            uid (str): The UID of an item to delete.
        """
        url = METRC_ITEMS_URL % uid
        params = format_params(license_number=license_number)
        return self.request('delete', url, params=params)


    #------------------------------------------------------------------
    # Lab Tests
    #------------------------------------------------------------------
    
    def get_lab_results(
        self,
        uid='',
        license_number='',
    ):
        """Get lab results.
        Args:
            uid (str): The UID for a package.
            license_number (str): A specific license number.
        """
        url = METRC_LAB_RESULTS_URL % 'results'
        params = format_params(
            license_number=license_number,
            package_id=uid
        )
        response = self.request('get', url, params=params)
        return [LabResult(self, x) for x in response]


    def get_analyses(self):
        """Get required quality assurance analyses."""
        url = METRC_LAB_RESULTS_URL % 'states'
        return self.request('get', url)
    

    def get_lab_statuses(self):
        """Get pre-defined lab statuses."""
        url = METRC_LAB_RESULTS_URL % 'states'
        return self.request('get', url)


    def post_lab_results(self, data):
        """Post lab result(s).
        Args:
            data (list): A list of lab results (dict) to create or update.
        """
        url = METRC_LAB_RESULTS_URL % 'record'
        return self.request('post', url, data=data)


    def upload_coas(self, data):
        """Upload lab result CoA(s).
        Args:
            data (list): A list of CoAs (dict) to upload.
        """
        url = METRC_LAB_RESULTS_URL % 'labtestdocument'
        return self.request('put', url, data=data)


    def release_lab_results(self, data):
        """Release lab result(s).
        Args:
            data (list): A list of package labels (dict) to release lab results.
        """
        url = METRC_LAB_RESULTS_URL % 'results/release'
        return self.request('put', url, data=data)


    #------------------------------------------------------------------
    # Locations
    #------------------------------------------------------------------

    def get_locations(
        self,
        uid='',
        action='active',
        license_number='',
    ):
        """Get locations.
        Args:
            uid (str): The UID of a location, takes precedent over action.
            action (str): A specific filter to apply, with options:
                `active`, `types`.
            license_number (str): A specific license number.
        """
        if uid:
            url = METRC_LOCATIONS_URL % uid
        else:
            url = METRC_LOCATIONS_URL % action
        params = format_params(license_number=license_number)
        response = self.request('get', url, params=params)
        try:
            return Location(self, response, license_number)
        except AttributeError:
            return [Location(self, x, license_number) for x in response]

    def create_locations(self, data, license_number=''):
        """Create location(s).
        Args:
            data (list): A list of locations (dict) to create.
            license_number (str): Optional license number filter.
        """
        url = METRC_LOCATIONS_URL % 'create'
        params = format_params(license_number=license_number)
        return self.request('post', url, data=data, params=params)

    def update_locations(self, data, license_number=''):
        """Update location(s).
        Args:
            data (list): A list of locations (dict) to update.
            license_number (str): Optional license number filter.
        """
        url = METRC_LOCATIONS_URL % 'update'
        params = format_params(license_number=license_number)
        return self.request('post', url, data=data, params=params)

    def delete_location(self, uid, license_number=''):
        """Delete location.
        Args:
            uid (str): The UID of a location to delete.
            license_number (str): Optional license number filter.
        """
        url = METRC_LOCATIONS_URL % uid
        params = format_params(license_number=license_number)
        return self.request('delete', url, params=params)

    #------------------------------------------------------------------
    # Packages
    #------------------------------------------------------------------

    def get_packages(
        self,
        uid='',
        action='',
        license_number='',
    ):
        """Get package(s).
        Args:
            uid (str): The UID for a package.
            license_number (str): A specific license number.
            action (str): `active`, `onhold`, `inactive`, `types`,
                `adjust/reasons`,
        """
        if uid:
            url = METRC_PACKAGES_URL % uid
        else:
            url = METRC_PACKAGES_URL % action
        params = format_params(license_number=license_number)
        response = self.request('get', url, params=params)
        try:
            return Package(self, response, license_number)
        except AttributeError:
            return [Package(self, x, license_number) for x in response]


    def create_packages(self, data, qa=False, plantings=False):
        """Create packages.
        Args:
            data (list): A list of packages (dict) to create.
            qa (bool): If the packages are for QA testing.
            plantings (bool): If the packages are for planting.
        """
        url = METRC_PACKAGES_URL % 'create'
        if qa:
            url += '/testing'
        elif plantings:
            url += '/plantings'
        return self.request('post', url, data=data)


    def update_packages(self, data):
        """Update packages
        Args:
            data (list): A list of packages (dict) to update.
        """
        url = METRC_PACKAGES_URL % 'update'
        return self.request('post', url, data=data)


    def delete_package(self, uid):
        """Delete a package.
        Args:
            uid (str): The UID of a package to delete.
        """
        url = METRC_PACKAGES_URL % uid
        return self.request('delete', url)


    def update_package_items(self, data):
        """Update package items.
        Args:
            data (list): A list of package items (dict) to update.
        """
        url = METRC_PACKAGES_URL % 'change/item'
        return self.request('post', url, data=data)
    

    def update_package_item_locations(self, data):
        """Update package item location(s).
        Args:
            data (list): A list of package items (dict) to move.
        """
        url = METRC_PACKAGES_URL % 'change/locations'
        return self.request('post', url, data=data)
    

    def manage_packages(self, data, action='adjust'):
        """Adjust package(s).
        Args:
            data (list): A list of packages (dict) to manage.
            action (str): The action to apply to the packages, with options:
                `adjust`, `finish`, `unfinish`, `remediate`.
        """
        url = METRC_PACKAGES_URL % 'change/locations'
        return self.request('post', url, data=data)
    

    def update_package_note(self, data):
        """Update package note(s).
        Args:
            data (list): A list of package notes (dict) to update.
        """
        url = METRC_PACKAGES_URL % 'change/note'
        return self.request('put', url, data=data)
    

    #------------------------------------------------------------------
    # Patients
    #------------------------------------------------------------------

    def get_patients(self, uid='', action='', license_number=''):
        """Get licensee member patients.
        Args:
            uid (str): A UID for a patient.
            action (str): An optional filter to apply: `active`.
            license_number (str): A licensee's license number to filter by.
        """
        if uid:
            url = METRC_PATIENTS_URL % uid
        else:
            url = METRC_PATIENTS_URL % action
        params = format_params(license_number=license_number)
        response = self.request('get', url, params=params)
        try:
            return Patient(self, response, license_number)
        except AttributeError:
            return [Patient(self, x, license_number) for x in response]


    def create_patient(self, data):
        """Create patient(s).
        Args:
            data (list): A list of patient (dict) to add.
        """
        url = METRC_PATIENTS_URL % 'add'
        return self.request('post', url, data=data)


    def update_patients(self, data):
        """Update strain(s).
        Args:
            data (list): A list of patients (dict) to update.
        """
        url = METRC_PATIENTS_URL % 'update'
        return self.request('put', url, data=data)


    def delete_patient(self, uid):
        """Delete patient.
        Args:
            uid (str): The UID of a patient to delete.
        """
        url = METRC_PATIENTS_URL % uid
        return self.request('delete', url)

    #------------------------------------------------------------------
    # Plant Batches
    # TODO: isFromMotherPlant on POST /plantbatches/v1/createpackages
    #------------------------------------------------------------------

    def get_batches(
        self,
        uid='',
        action='',
        license_number='',
        start='',
        end=''
    ):
        """Get plant batches(s).
        Args:
            uid (str): The UID for a plant batch.
            action (str): The action to apply to the plants, with options:
                `active`, `inactive`, `types`
            license_number (str): A specific license number.
            start (str): An ISO 8601 formatted string to restrict the start
                by the last modified time.
            end (str): An ISO 8601 formatted string to restrict the end
                by the last modified time.
        """
        if uid:
            url = METRC_BATCHES_URL % uid
        else:
            url = METRC_BATCHES_URL % action
        params = format_params(license_number=license_number, start=start, end=end)
        response = self.request('get', url, params=params)
        try:
            return PlantBatch(self, response, license_number)
        except AttributeError:
            return [PlantBatch(self, x, license_number) for x in response]


    def manage_batches(self, data, action, from_mother=False):
        """Manage plant batch(es) by applying a given action.
        Args:
            data (list): A list of plants (dict) to manage.
            action (str): The action to apply to the plants, with options:
                `createplantings`, `createpackages`, `split`,
                `/create/packages/frommotherplant`, `changegrowthphase`,
                `additives`, `destroy`.
            from_mother (bool): An optional parameter for the
                `createpackages` action.
        """
        url = METRC_BATCHES_URL % action
        params = format_params(from_mother=from_mother)
        return self.request('post', url, data=data, params=params)
    

    def move_batch(self, data):
        """Move plant batch(es).
        Args:
            data (list): A list of plant batches (dict) to move.
        """
        url = METRC_BATCHES_URL % 'moveplantbatches'
        return self.request('put', url, data=data)


    #------------------------------------------------------------------
    # Plants
    #------------------------------------------------------------------

    def get_plants(
        self,
        uid='',
        label='',
        action='',
        license_number='',
        start='',
        end=''
    ):
        """Get plant(s).
        Args:
            uid (str): The UID for a plant.
            label (str): The label for a given plant.
            action (str): A specific filter to apply, with options:
                `vegetative`, `flowering`, `onhold`,
                `inactive`, `additives`, `additives/types`,
                `growthphases`, `waste/methods`, `waste/reasons`.
            license_number (str): A specific license number.
            start (str): An ISO 8601 formatted string to restrict the start
                by the last modified time.
            end (str): An ISO 8601 formatted string to restrict the end
                by the last modified time.
        """
        if uid:
            url = METRC_PLANTS_URL % uid
        elif label:
            url = METRC_PLANTS_URL % label
        else:
            url = METRC_PLANTS_URL % action
        params = format_params(license_number=license_number, start=start, end=end)
        response = self.request('get', url, params=params)
        try:
            return Plant(self, response, license_number)
        except AttributeError:
            return [Plant(self, x, license_number) for x in response]


    def manage_plants(self, data, action):
        """Manage plant(s) by applying a given action.
        Args:
            data (list): A list of plants (dict) to manage.
            action (str): The action to apply to the plants, with options:
                `moveplants`, `changegrowthphases`, `destroyplants`,
                `additives`, `additives/bylocation`,
                `create/plantings`, `create/plantbatch/packages`,
                `manicureplants`, `harvestplants`.
        """
        url = METRC_PLANTS_URL % action
        return self.request('post', url, data=data)


    #------------------------------------------------------------------
    # Sales
    #------------------------------------------------------------------

    def get_receipts(
        self,
        uid='',
        action='',
        license_number='',
        start='',
        end='',
        sales_start='',
        sales_end='',
    ):
        """Get sale(s).
        Args:
            uid (str): The UID for a plant batch.
            action (str): The action to apply to the plants, with options:
                `active` or `inactive`
            license_number (str): A specific license number.
            start (str): An ISO 8601 formatted string to restrict the start
                by the last modified time.
            end (str): An ISO 8601 formatted string to restrict the end
                by the last modified time.
            sales_start (str): An ISO 8601 formatted string to restrict the start
                by the sales time.
            sales_end (str): An ISO 8601 formatted string to restrict the end
                by the sales time.
        """
        if uid:
            url = METRC_RECEIPTS_URL % uid
        else:
            url = METRC_RECEIPTS_URL % action
        params = format_params(
            license_number=license_number,
            start=start,
            end=end,
            sales_start=sales_start,
            sales_end=sales_end,
        )
        response = self.request('get', url, params=params)
        try:
            return Sale(self, response, license_number)
        except AttributeError:
            return [Sale(self, x, license_number) for x in response]


    def get_transactions(
        self,
        license_number='',
        start='',
        end='',
    ):
        """Get transaction(s).
        Args:
            license_number (str): A specific license number.
            start (str): An ISO 8601 formatted string to restrict the start
                by the sales time.
            end (str): An ISO 8601 formatted string to restrict the end
                by the sales time.
        """
        if start and end:
            url = METRC_TRANSACTIONS_URL % f'{start}/{end}'
        else:
            url = METRC_SALES_URL % 'transactions'
        params = format_params(license_number=license_number)
        return self.request('get', url, params=params)
    

    def get_customer_types(self):
        """Get all facilities."""
        url = METRC_SALES_URL % 'customertypes'
        return self.request('get', url)
    

    def create_receipts(self, data):
        """Create receipt(s).
        Args:
            data (list): A list of receipts (dict) to create.
        """
        url = METRC_SALES_URL % 'receipts'
        return self.request('post', url, data=data)


    def update_receipts(self, data):
        """Update receipt(s).
        Args:
            data (list): A list of receipts (dict) to update.
        """
        url = METRC_SALES_URL % 'receipts'
        return self.request('put', url, data=data)


    def delete_receipt(self, uid):
        """Delete receipt.
        Args:
            uid (str): The UID of a receipt to delete.
        """
        url = METRC_SALES_URL % f'receipts/{uid}'
        return self.request('delete', url)


    def create_transactions(self, data, date):
        """Create transaction(s).
        Args:
            data (list): A list of transactions (dict) to create.
            date (str): An ISO 8601 formatted string of the transaction date.
        """
        url = METRC_TRANSACTIONS_URL % date
        return self.request('post', url, data=data)


    def update_transactions(self, data, date):
        """Update transaction(s).
        Args:
            data (list): A list of transactions (dict) to update.
            date (str): An ISO 8601 formatted string of the transaction date.
        """
        url = METRC_TRANSACTIONS_URL % date
        return self.request('put', url, data=data)


    #------------------------------------------------------------------
    # Strains
    #------------------------------------------------------------------

    def get_strains(self, uid='', action='active', license_number=''):
        """Get strains.
        Args:
            uid (str): A UID for a strain.
            action (str): An optional filter to apply: `active`.
            license_number (str): A licensee's license number to filter by.
        """
        if uid:
            url = METRC_STRAINS_URL % uid
        else:
            url = METRC_STRAINS_URL % action
        params = format_params(license_number=license_number)
        response = self.request('get', url, params=params)
        try:
            return Strain(self, response, license_number)
        except AttributeError:
            return [Strain(self, x, license_number) for x in response]


    def create_strains(self, data, license_number=''):
        """Create strain(s).
        Args:
            data (list): A list of strains (dict) to create.
        """
        url = METRC_STRAINS_URL % 'create'
        params = format_params(license_number=license_number)
        return self.request('post', url, data=data, params=params)


    def update_strains(self, data, license_number=''):
        """Update strain(s).
        Args:
            data (list): A list of strains (dict) to update.
        """
        url = METRC_STRAINS_URL % 'update'
        params = format_params(license_number=license_number)
        return self.request('post', url, data=data, params=params)


    def delete_strain(self, uid, license_number=''):
        """Delete strain.
        Args:
            uid (str): The UID of a strain to delete.
        """
        url = METRC_STRAINS_URL % uid
        params = format_params(license_number=license_number)
        return self.request('delete', url, params=params)


    #------------------------------------------------------------------
    # Transfers
    #------------------------------------------------------------------

    # TODO: GET /transfers/v1/{id}/transporters
    # GET /transfers/v1/{id}/transporters/details

    def get_transfers(
        self,
        uid='',
        transfer_type='incoming',
        license_number='',
        start='',
        end='',
    ):
        """Get transfers.
        Args:
            uid (str): The UID for a transfer, takes precedent in query.
            transfer_type (str): The type of transfer:
                `incoming`, `outgoing`, or `rejected`.
            license_number (str): A specific license number.
            start (str): Optional ISO date to restrict earliest modified transfers.
            end (str): Optional ISO date to restrict latest modified transfers.
        """
        if uid:
            url = METRC_TRANSFERS_URL % uid + '/deliveries'
        else:
            url = METRC_TRANSFERS_URL % transfer_type
        params = format_params(license_number=license_number, start=start, end=end)
        response = self.request('get', url, params=params)
        try:
            return Transfer(self, response, license_number)
        except AttributeError:
            return [Transfer(self, x, license_number) for x in response]
    

    def get_transfer_packages(
        self,
        uid,
        action='packages',
    ):
        """Get shipments.
        Args:
            uid (str): Required UID of a shipment.
            action (str): The filter to apply to transfers:
                `packages`, `packages/wholesale`, `requiredlabtestbatches`.
        """
        if action == 'requiredlabtestbatches':
            url = METRC_TRANSFER_PACKAGES_URL % (f'package/{uid}', action)
        else:
            url = METRC_TRANSFER_PACKAGES_URL % (uid, action)
        return self.request('get', url)
    

    def get_transfer_types(self):
        """Get all transfer types."""
        url = METRC_TRANSFERS_URL % 'types'
        return self.request('get', url)


    def get_package_statuses(self):
        """Get all package status choices."""
        url = METRC_TRANSFERS_URL % 'delivery/packages/states'
        return self.request('get', url)

    
    def create_transfers(self, data):
        """Create transfer(s).
        Args:
            data (list): A list of transfers (dict) to create.
        """
        url = METRC_TRANSFERS_URL % 'external/incoming'
        return self.request('post', url, data=data)


    def update_transfers(self, data):
        """Update transfer(s).
        Args:
            data (list): A list of transfers (dict) to update.
        """
        url = METRC_TRANSFERS_URL % 'external/incoming'
        return self.request('put', url, data=data)


    def delete_transfer(self, uid):
        """Delete transfer.
        Args:
            uid (str): The UID of a transfer to delete.
        """
        url = METRC_TRANSFERS_URL % f'external/incoming/{uid}'
        return self.request('delete', url)


    #------------------------------------------------------------------
    # Transfer Templates
    #------------------------------------------------------------------

    # GET /transfers/v1/templates/{id}/transporters
    # GET /transfers/v1/templates/{id}/transporters/details

    def get_transfer_templates(
        self,
        uid='',
        action='',
        license_number='',
        start='',
        end='',
    ):
        """Get transfer template(s).
        Args:
            uid (str): A UID for a transfer template.
            action (str): An optional filter to apply: `deliveries`, `packages`.
            license_number (str): A specific license number.
            start (str): An ISO 8601 formatted string to restrict the start
                by the sales time.
            end (str): An ISO 8601 formatted string to restrict the end
                by the sales time.
        """
        if action == 'deliveries':
            url = METRC_TRANSFER_TEMPLATE_URL % f'{uid}/deliveries'
        elif action == 'packages':
            url = METRC_TRANSFER_TEMPLATE_URL % f'delivery/{uid}/packages'
        else:
            url = (METRC_TRANSFER_TEMPLATE_URL % '').rstrip('/')
        params = format_params(license_number=license_number, start=start, end=end)
        response = self.request('get', url, params=params)
        try:
            return TransferTemplate(self, response, license_number)
        except AttributeError:
            return [TransferTemplate(self, x, license_number) for x in response]


    def create_transfer_templates(self, data):
        """Create transfer_template(s).
        Args:
            data (list): A list of transfer templates (dict) to create.
        """
        url = METRC_TRANSFER_TEMPLATE_URL
        return self.request('post', url, data=data)


    def update_transfer_templates(self, data):
        """Update transfer template(s).
        Args:
            data (list): A list of transfer templates (dict) to update.
        """
        url = METRC_TRANSFER_TEMPLATE_URL
        return self.request('put', url, data=data)


    def delete_transfer_template(self, uid):
        """Delete transfer template.
        Args:
            uid (str): The UID of a transfer template to delete.
        """
        url = METRC_TRANSFER_TEMPLATE_URL % uid
        return self.request('delete', url)


    #------------------------------------------------------------------
    # Miscellaneous
    #------------------------------------------------------------------

    def get_uom(self):
        """Get all units of measurement."""
        url = METRC_UOM_URL
        return self.request('get', url)

