# -*- coding: utf-8 -*-
"""
cannlytics.traceability.metrc.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains common Metrc models.
"""

from .exceptions import MetrcAPIError
from .utils import (
    clean_nested_dictionary,
    camel_to_snake,
    snake_to_camel,
    update_context,
    remove_dict_fields,
    remove_dict_nulls,
)


class Model(object):
    """Base class for all Metrc models."""

    def __init__(
        self,
        client,
        context,
        license_number='',
        function=camel_to_snake
    ):
        """Initialize the model, setting keys as properties."""
        self.client = client
        self._license = license_number
        properties = clean_nested_dictionary(context, function)
        for key in properties:
            self.__dict__[key] = properties[key]
    
    def __getattr__(self, key):
        return self.__dict__[key]
    
    def __setattr__(self, key, value):
        self.__dict__[key] = value
    
    @property
    def uid(self):
        """The model's unique ID."""
        return self.__dict__.get('id')

    def to_dict(self):
        """Returns the model's properties as a dictionary."""
        data = vars(self).copy()
        [data.pop(x, None) for x in ['_license', 'client']]
        return data


class Employee(Model):
    """An organization's employee or team member.
    
    E.g.
        {
            "FullName": "Keegan Skeate",
            "License": None
        }
    """
    pass


class Facility(Model):
    """A Facility represents a building licensed for the growing,
    processing, and/or selling of product. Facilities are created
    and have their permissions determined by a state.
    E.g.
        {
            "HireDate": "0001-01-01",
            "IsOwner": false,
            "IsManager": true,
            "Occupations": [],
            "Name": "Cultivation LLC",
            "Alias": "Cultivation on Road St",
            "DisplayName": "Cultivation on Road St",
            "CredentialedDate": "1969-08-15",
            "SupportActivationDate": null,
            "SupportExpirationDate": null,
            "SupportLastPaidDate": null,
            "FacilityType": null,
            "License": {
                "Number": "403-X0001",
                "StartDate": "2013-06-28",
                "EndDate": "2015-12-28",
                "LicenseType": "Medical Cultivation"
            }
        }
    """
    
    def get_locations(self, uid='', action=''):
        """Get locations at the facility.
        Args:
            uid (str): The UID of a location, takes precedent over action.
            action (str): A specific filter to apply, with options: `active`, `types`.
        """
        response = self.client.get_locations(uid=uid, action=action, license_number=self.license_number)
        return response
    
    def create_locations(self, names, types=[]):
        """Create locations at the facility.
        Args:
            names (list): A list of location names.
            types (list): A list of location types:
                `default`, `planting`, or `packing`.
        """
        data = []
        for i in range(len(names)):
            try:
                location_type = types[i]
            except IndexError:
                location_type = 'Default Location Type'
            data.append({
                'Name': names[i],
                'LocationTypeName': location_type
            })
        response = self.client.create_locations(
            data,
            license_number=self.license_number
        )
        return response
    
    def update_locations(self, ids, names, types=[]):
        """Update locations at the facility.
        Args:
            uids (list): A list of location IDs.
            names (list): A list of location names.
            types (list): A list of location types:
                `default`, `planting`, or `packing`.
        """
        data = []
        for i in range(len(ids)):
            try:
                location_type = types[i]
            except IndexError:
                location_type = 'Default Location Type'
            data.append({
                'Id': ids[i],
                'Name': names[i],
                'LocationTypeName': location_type
            })
        response = self.client.update_locations(
            data,
            license_number=self.license_number
        )
        return response

    def delete_location(self, uid):
        """Delete a location at the facility.
        Args:
            uid (str): The UID of a location to delete.
        """
        response = self.client.delete_location(
            uid,
            license_number=self.license_number
        )
        return response
    
    # TODO:
    # Get / Create / Update / Delete strains
    # Get / Create / Update / Delete items


class Location(Model):
    """A class that represents a cannabis-production location.
    E.g.
        {
            "Id": 1,
            "Name": "Harvest Location",
            "LocationTypeId": 1,
            "LocationTypeName": "Default",
            "ForPlantBatches": True,
            "ForPlants": True,
            "ForHarvests": True,
            "ForPackages": True
        }
    """

    def __init__(self, client, properties, license_number=''):
        super().__init__(client, properties, license_number)
        self._parameters = {
            'name': 'Name',
            'location_type': 'LocationTypeName',
            'batches': 'ForPlantBatches',
            'plants': 'ForPlants',
            'harvests': 'ForHarvests',
            'packages': 'ForPackages'
        }

    def update(self, **kwargs):
        """Update location."""
        data = self.to_dict()
        update = clean_nested_dictionary(data, snake_to_camel)
        for param in kwargs:
            key = self._parameters.get(param, param)
            update[key] = kwargs[param]
        self.client.update_locations([update])

    def delete(self):
        """Delete location."""
        self.client.delete_location(self.id)


class Strain(Model):
    """A class that represents a cannabis strain.
    
    E.g.
        {
            "Id": 1,
            "Name": "Old-time Moonshine",
            "TestingStatus": "InHouse",
            "ThcLevel": 0.1865,
            "CbdLevel": 0.1075,
            "IndicaPercentage": 25.0,
            "SativaPercentage": 75.0
        }
    """

    @classmethod
    def create_from_json(cls, client, json):
        obj = cls(client, json)
        obj.create()
        return obj

    def create(self):
        """Create a strain record in Metrc."""
        context = self.to_dict()
        data = clean_nested_dictionary(context, snake_to_camel)
        self.client.create_strains([data])
    
    def update(self, **kwargs):
        """Update the strain given parameters as keyword arguments."""
        context = self.to_dict()
        data = update_context(context, **kwargs)
        self.client.update_strains([data], license_number=self._license)

    def delete(self):
        """Delete the strain."""
        self.client.delete_strain(self.id, license_number=self._license)


class Item(Model):
    """Items are used to track a licensee's inventory at a given facility.
    Items belong to a single facility
    Each item has a unique item name, category, and strain.
    Item Names are used for identification, so an item name
    should not simply be a category name. Item names are
    specific to the item in that package or production batch.
    Categories are pre-defined. The item name
    identifies what is in the package and categories
    are used for grouping similar items for reporting purposes.    
    An item will retain its name unless it is re-packaged.

    E.g.
        {
            "Id": 1,
            "Name": "Buds",
            "ProductCategoryName": "Buds",
            "ProductCategoryType": "Buds",
            "QuantityType": "WeightBased",
            "DefaultLabTestingState": "NotSubmitted",
            "UnitOfMeasureName": "Ounces",
            "ApprovalStatus": "Approved",
            "ApprovalStatusDateTime": "0001-01-01T00:00:00+00:00",
            "StrainId": 1,
            "StrainName": "Spring Hill Kush",
            "AdministrationMethod": null,
            "UnitCbdPercent": null,
            "UnitCbdContent": null,
            "UnitCbdContentUnitOfMeasureName": null,
            "UnitCbdContentDose": null,
            "UnitCbdContentDoseUnitOfMeasureName": null,
            "UnitThcPercent": null,
            "UnitThcContent": null,
            "UnitThcContentUnitOfMeasureName": null,
            "UnitThcContentDose": null,
            "UnitThcContentDoseUnitOfMeasureName": null,
            "UnitVolume": null,
            "UnitVolumeUnitOfMeasureName": null,
            "UnitWeight": null,
            "UnitWeightUnitOfMeasureName": null,
            "ServingSize": null,
            "SupplyDurationDays": null,
            "NumberOfDoses": null,
            "UnitQuantity": null,
            "UnitQuantityUnitOfMeasureName": null,
            "PublicIngredients": null,
            "Description": null,
            "IsUsed": false
        }
    """

    RETURNED_VALUES = {
        'ProductCategoryName': 'item_category',
        'StrainName': 'strain',
        'UnitOfMeasureName': 'unit_of_measure',
        'QuantityType': [],
        'DefaultLabTestingState': [],
        'ApprovalStatus': [],
        'ApprovalStatusDateTime': [],
        'StrainId': [],
        'AdministrationMethod': [],
        'UnitQuantity': [],
        'UnitQuantityUnitOfMeasureName': [],
        
    }

    def __init__(self, client, properties, license_number=''):
        super().__init__(client, properties, license_number)
        for k, v in self.RETURNED_VALUES.items():
            try:
                self.__dict__[v] = properties[k]
            except (KeyError, TypeError):
                pass

    @classmethod
    def create_from_json(cls, client, license_number, json):
        new_obj = cls(client, json, license_number)
        new_obj.create(license_number)
        return new_obj
    
    def create(self, license_number):
        """Create an item record in Metrc."""
        context = self.to_dict()
        data = clean_nested_dictionary(context, snake_to_camel)
        self.client.create_items([data], license_number)
    
    def update(self, **kwargs):
        """Update the item given parameters as keyword arguments."""
        context = self.to_dict().copy()
        data = update_context(context, **kwargs)
        data = remove_dict_fields(data, self.RETURNED_VALUES.keys())
        data = remove_dict_nulls(data)
        self.client.update_items([data], self._license)

    def delete(self):
        """Delete the item."""
        self.client.delete_item(self.id, self._license)


class Plant(Model):
    """A class that represents a cannabis plant.
    
    Plants are tagged at the immature lot growth phase and at the mature / flowering growth
    phase.
    A UID number is assigned to an immature plant lot of
    up to 100 seeds or immature plants. Required corresponding UID
    number labels will need to be produced by the licensee
    . Once the immature lot has been
    established in Metrc, the death of an immature plant(s) must be recorded in Metrc by
    recording the associated waste amount and reducing the total number of the immature
    plants in the lot for each immature plant that was destroyed.

    Plant tags are assigned to individual plants when they are moved to a designated
    canopy area, or when the plant begins flowering.
    """

    pass


# HARVESTS
# A plant can be destroyed anytime during the growth phases shown in Exhibit 37.
# Any waste produced by the plant should be recorded prior to the destruction.
# 2. Any waste created during the immature growth phase must be recorded as waste
# using the Plant Waste function and destroyed.
# 3. When immature plants begin to flower, select the Change Growth Phase button
# to record the change and associate the new Plant Tag ID to the plant(s).
# 4. In Metrc, anytime something is trimmed from a flowering plant during growing
# with the intent to sell it, process it, or perform a partial harvest, a Manicure batch
# must be created.
# 5. Harvest steps include the following:
# A. Harvest Name – Harvests must be strain specific. The Harvest Name must be
# unique. It is a best practice for the harvest name to include the Strain Name
# and Harvest Date, but it is not required by the State.
# B. Weight – The plant is weighed individually in its entirety after being cut from
# root ball (stem, stalk, bud/flower, leaves, trim leaves, etc.).
# C. Waste – This can be recorded using multiple entries but must be reported
# within three days of destruction.
# D. Package – Package and tag the product from the Harvest Batch (Fresh
# Cannabis Plant, Flower, Leaf or Kief). These packages must be strain
# specific.
# E. Transfer – Licensee must create transfer manifest to move product to a
# Processor, Distributor, or Manufacturer.
# F. Finish – When the Harvest Batch (HB) has been fully packaged, there should
# be remaining wet weight to account for moisture loss. Selecting Finish
# Harvest will attribute any remaining weight to moisture loss.
# 6. A Harvest Batch package of Flower, Leaf, Kief or Fresh Cannabis Plant can only
# be created from the Harvested Tab using a single strain from plants harvested at
# the same time.


class Harvest(Model):
    """A class that represents a cannabis harvest.
    
    A harvest batch is created and given a
    unique Harvest Name when plants
    or plant material are harvested.
    """

    pass


class Package(Model):
    """A class that represents a cannabis package.
    
    Immature plants and seeds can be packaged by a nursery and transported by a
    distributor to a cultivator, distributor or retailer for sale.
    2. When a manufacturer is creating a concentrate that will then be used in multiple
    infused production batches, the concentrate must be created as a new package.
    The infused production batches will then be created from the concentrate
    package.
    A. The new package of concentrate is a production batch and will then be
    partially used in an infused product or sold to a customer.
    B. This makes it more easily recorded as connected to the finished infused
    product package.
    3. Packages made at a manufacturer facility that creates concentrates must be
    created by pulling from other packages.
    4. A package must exist in order for it to be selected for transfer. Transfers are realtime inventory dependent.
    5. There must be a contents section for each new package created from an existing
    package.
    6. When adjusting a package, use the appropriate adjustment reason.
    7. In order for a distributor to send a sample for testing, a test sample package must
    be created. A new test sample must have a new RFID package tag and be pulled
    from an existing package.
    8. Package tags may only be used once and may not be reused.
    """

    pass


class Patient(Model):
    """A class that represents a cannabis patient."""

    pass

class PlantBatch(Model):
    """A class that represents a cannabis plant batch."""

    pass


class LabResult(Model):
    """A class that represents a cannabis lab result.
    
    The Lab Results tab displays the details of each individual lab test performed on
    the package. A Document Download button is available on each row on the Lab
    Results tab to view the associated certificate of analysis (COA), which the
    laboratory staff uploads when test results are recorded. The test results and
    COA are available on the source package and any related packages only after
    the laboratory staff releases the results
    """

    pass


class Transfer(Model):
    """A class that represents a cannabis transfer.
    
    A transfer must be created anytime a package moves from one licensee to
    another, even if the two facilities are located on the same property.
    2. To print a manifest, select the manifest number to highlight it in orange, then
    select the View Manifest button and select Print.
    3. Packages can only be transported from one licensee to another by a licensed
    Distributor. A Testing Laboratory is allowed to transport test samples for official
    state testing. Distributors and Testing Laboratories are required to record the
    actual departure time from the origin facility and the actual arrival time at the
    destination facility in Metrc real-time.
    4. A package must be received in its entirety (the system DOES NOT allow
    receiving a partial package).
    5. A transfer can be rejected by individual package, or in whole by rejecting all
    packages.
    6. A rejected package requires the originating Licensee to receive the package
    back into inventory.
    7. A package must exist in order to be selected for transfer. Transfers are done in
    real time and are inventory dependent.
    8. When receiving a package, any adjustments to the weight, volume, or count may
    be reported to the State.
    9. If there are any questions about a transfer, reject it.

    A transfer can be modified as shown in Exhibit 64, or voided, up until the time that the
    Distributor or Testing Laboratory marks that it has departed the facility. Once the
    transfer process has begun, the transfer may not be modified except by the Distributor
    or Testing Laboratory to edit estimated departure and arrival times, or driver and vehicle
    information (see Edit Transporter Info below).
    When modifying transfers, each of the transfer fields may be modified at the same level
    of detail as when the transfer was created. Edits may be completed for a variety of
    reasons including: error correction, changes in destination, changes in product, etc. The
    transfer process is a key component of the chain of custody process, and modifying a
    transfer manifest should be handled appropriately.

    Voiding a transfer can only be completed by the originating business. Voiding a transfer
    permanently eliminates it and moves the product back into the originator’s inventory.
    Once a transfer has been voided, it cannot be reinstated and all associated packages
    will be returned to the transfer originator’s inventory

    Receiving a transfer is the final point of exchange in the chain of custody.
    """

    pass


class TransferTemplate(Model):
    """A class that represents a cannabis transfer template.
    
    Licensed transfers made on a regular basis to the same Destination licensee utilizing
    the same Planned Route, Transporter(s), Driver(s) and/or Vehicle(s) can be recorded in
    Metrc most efficiently when a transfer template is employed.
    A template can be used to record these types of transfers with minimal data input to suit
    the circumstances of a particular transfer and specify the packages to be transferred.
    The template can also be copied as a starting point to create additional templates.
    """

    pass


class Sale(Model):
    """A class that represents a cannabis sale.
    
    Sales are reported by the industry to record the transfer of cannabis products to a
    consumer, patient or caregiver
    """

    pass



# class Driver(Model):
#     """A class that represents a cannabis transfer driver."""

#     pass


# class Vehicle(Model):
#     """A class that represents a cannabis transfer driver."""

#     pass


# class Waste(Model):
#     """A class that represents a cannabis waste.
    
#     A harvest batch is created and given a
#     unique Harvest Name when plants
#     or plant material are harvested.

#     Plant waste must be recorded within three business days of destruction. In Metrc
#     plant waste can be recorded by Immature Plant Lot, Flowering Plant or by
#     Location.
#     2. Waste can also be recorded by Harvest Batch. See Metrc User Guide for details.
#     3. When recording Flowering Plant waste, the waste from multiple plants can be
#     recorded as a single waste event but the flowering plants contributing to the
#     waste must be individually identified.
#     4. If a plant is no longer viable, the waste must be recorded prior to recording its
#     destruction.
#     5. The reason for the waste must be identified using the Waste Reasons defined by
#     the State of California as listed in Exhibit 38 below. Use of some Waste
#     Reasons may be limited to certain license types, as determined by the State.

#     """

#     pass

