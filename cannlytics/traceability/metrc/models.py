# -*- coding: utf-8 -*-
"""
cannlytics.traceability.metrc.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains common Metrc models.
"""


class Employee(object):
    """An organization's employee or team member. E.g.
        {
            "FullName": "Keegan Skeate",
            "License": None
        },
    """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Employee's ID."""
        return self._properties['id']
    
    @property
    def name(self):
        """Employee's name."""
        return self._properties.get('FullName', '')
    
    @property
    def license_number(self):
        """Employee's license number."""
        return self._properties.get('License', '')
    
    def to_dict(self):
        return self._properties


class Facility(object):
    """A Facility represents a building licensed for the growing,
    processing, and/or selling of product. E.g.
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
        },
    """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Facility's ID."""
        return self._properties['License']['Number']
    
    @property
    def name(self):
        """Employee's name."""
        return self._properties.get('DisplayName', '')
    
    @property
    def license_number(self):
        """Employee's license number."""
        return self._properties['License']['Number']
    
    def create_location(self):
        """Create a location at the facility."""
        # self.license_number
        return NotImplementedError
    
    def update_location(self):
        """Create a location at the facility."""
        # self.license_number
        return NotImplementedError

    def delete_location(self):
        """Create a location at the facility."""
        # self.license_number
        return NotImplementedError
    
    def to_dict(self):
        return self._properties
    
    # Employee permissions include:
    # • Administration – Provides the capability to perform all administrative functions,
    # including ordering tags, setting up strains, locations, and items, and adding
    # employees (it is recommended that the number of users granted administrative
    # permissions be limited).
    # • Plants – Provides the capability to create plantings, move plants, change growth
    # phase, log waste, and create harvests in Metrc.
    # • Packages – Provides the capability to create, adjust, and re-package packages into
    # smaller or larger quantities, as well as create packages of production batches.
    # • Transfers – Provides the capability to create, modify, void, and receive/reject
    # transfers.
    # • Transfer Hub – Provides the capability to view a manifest, edit transporter
    # information, and record actual departure, arrival, layover check-in, and layover
    # check-out dates/times.
    # • Sales – Provides the capability to input sales data or initiate sales uploads.
    # • Reports – Provides the capability to generate pre-defined reports.

    # The Account Manager can use Facilities to grant each employee access to one
    # or more facilities at once instead of entering that person into each individual
    # facility’s license number.


class Location(object):
    """A class that represents a cannabis-production location. E.g.
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

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties
        self._parameters = {
            'name': 'Name',
            'location_type': 'LocationTypeName',
            'batches': 'ForPlantBatches',
            'plants': 'ForPlants',
            'harvests': 'ForHarvests',
            'packages': 'ForPackages'
        }
    
    @property
    def uid(self):
        """Location ID."""
        return self._properties['Id']

    @property
    def name(self):
        """Location name."""
        return self._properties['Name']
    
    @property
    def location_type(self):
        """Location type."""
        return self._properties['LocationTypeName']

    def update(self, **kwargs):
        """Update location."""
        update = self._properties
        for param in kwargs:
            key = self._parameters.get(param, param)
            update[key] = kwargs[param]
        self.client.update_locations([update])

    def delete(self):
        """Delete location."""
        self.client.delete_location(self.uid)

    def to_dict(self):
        return self._properties


class Strain(object):
    """A class that represents a cannabis strain. E.g.
        {
            "Id": 1,
            "Name": "Spring Hill Kush",
            "TestingStatus": "InHouse",
            "ThcLevel": 0.1865,
            "CbdLevel": 0.1075,
            "IndicaPercentage": 25.0,
            "SativaPercentage": 75.0
        }
    """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties
        self._parameters = {
            'name': 'Name',
            'testing_status': 'TestingStatus',
            'thc': 'ThcLevel',
            'cbd': 'CbdLevel',
            'percent_indica': 'IndicaPercentage',
            'percent_sativa': 'SativaPercentage',
        }

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']
    
    def update(self, **kwargs):
        """Update the strain given parameters as keyword arguments."""
        update = self._properties
        for param in kwargs:
            key = self._parameters.get(param, param)
            update[key] = kwargs[param]
        self.client.update_strains([update])

    def delete(self):
        """Delete the strain."""
        self.client.delete_strain(self.uid)
    
    def to_dict(self):
        return self._properties


class Inventory(object):
    """ """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class Item(object):
    """Items are used to track the licensee’s inventory through the supply chain life cycle. The
    Item Names are used to identify what type of item is packed into a package. An
    inventory list of a licensee’s current plants or packaged product is a good starting point
    to create the items in Metrc.
    An item name cannot be just simply a category name. It must be specific to the
    item in that package or production batch.
    Items cannot be created for multiple
    facilities at one time.
    Each facility creates its own items that are unique with item name, category and
    strain. A facility cannot create duplicate item names.
    Each item requires a pre-defined category selection.
    The purpose of the categories is for grouping similar items for reporting
    purposes. The item name will identify what is in the package and the category the item
    belongs in.
    """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']



# The facility that packages an item will assign the item name to the package. The
# package will retain that item name unless it is re-packaged.
# 11.When creating a packag


class Plant(object):
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

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


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


class Harvest(object):
    """A class that represents a cannabis harvest.
    
    A harvest batch is created and given a
    unique Harvest Name when plants
    or plant material are harvested.
    """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']
    

class Waste(object):
    """A class that represents a cannabis waste.
    
    A harvest batch is created and given a
    unique Harvest Name when plants
    or plant material are harvested.

    Plant waste must be recorded within three business days of destruction. In Metrc
    plant waste can be recorded by Immature Plant Lot, Flowering Plant or by
    Location.
    2. Waste can also be recorded by Harvest Batch. See Metrc User Guide for details.
    3. When recording Flowering Plant waste, the waste from multiple plants can be
    recorded as a single waste event but the flowering plants contributing to the
    waste must be individually identified.
    4. If a plant is no longer viable, the waste must be recorded prior to recording its
    destruction.
    5. The reason for the waste must be identified using the Waste Reasons defined by
    the State of California as listed in Exhibit 38 below. Use of some Waste
    Reasons may be limited to certain license types, as determined by the State.

    """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class Package(object):
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

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class LabResult(object):
    """A class that represents a cannabis lab result.
    
    The Lab Results tab displays the details of each individual lab test performed on
    the package. A Document Download button is available on each row on the Lab
    Results tab to view the associated certificate of analysis (COA), which the
    laboratory staff uploads when test results are recorded. The test results and
    COA are available on the source package and any related packages only after
    the laboratory staff releases the results
    """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class Transfer(object):
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

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class TransferTemplate(object):
    """A class that represents a cannabis transfer template.
    
    Licensed transfers made on a regular basis to the same Destination licensee utilizing
    the same Planned Route, Transporter(s), Driver(s) and/or Vehicle(s) can be recorded in
    Metrc most efficiently when a transfer template is employed.
    A template can be used to record these types of transfers with minimal data input to suit
    the circumstances of a particular transfer and specify the packages to be transferred.
    The template can also be copied as a starting point to create additional templates.
    """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']



class Driver(object):
    """A class that represents a cannabis transfer driver."""

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class Vehicle(object):
    """A class that represents a cannabis transfer driver."""

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class Sale(object):
    """A class that represents a cannabis sale.
    
    Sales are reported by the industry to record the transfer of cannabis products to a
    consumer, patient or caregiver
    """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']

