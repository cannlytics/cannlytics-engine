# -*- coding: utf-8 -*-
"""
cannlytics.traceability.leaf.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains common Leaf Data Systems models.
"""
# from .exceptions import WorksheetNotFound, CellNotFound

# from .utils import ()

# from .urls import (

# )

BATCH_TYPES = ['propagation material', 'plant', 'harvest', 
'intermediate/ end product']

PLANT_STAGES = ['propagation source', 'growing', 
'harvested', 'packaged', 'destroyed']


class Area(object):
    """A class that represents physical locations at licensed facilities
    where plants and inventory will be located.

    type (str): Areas with a 'quarantine' designation are for circumstances such as
        waste/destruction hold periods, QA quarantine periods,
        or transfer hold periods as the licensee decides to use them.
        Allowed values:
            'quarantine' or 'non-quarantine'.
    """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Area global ID."""
        return self._properties['global_id']
    
    def update(self):
        """Update an Area."""
        body = {
            'area': {
                # 'name': source_sheet_id,
                # 'type': insert_sheet_index,
                # 'external_id': new_sheet_id,
                # 'global_id': new_sheet_name,
            }
        }
        # data = self.batch_update(body)
        # properties = data['replies'][0]['duplicateSheet']['properties']
        # worksheet = Worksheet(self, properties)
        # return worksheet


class Batch(object):
    """Batch class for propagation material, plants, harvests, and intermediate / end products.

    'Propagation Material' batches are used to create inventory lot of seeds, clones, and plant tissue so that these plants can be tracked 
    as inventory throughout their propagation phase. As plants shift from their propagation to vegetative phase, they are moved to 
    plants (see /move_inventory_to_plants API call), at which point the plant records are associated with a 'plant' type batch.
    
    'Plant' batches are a group of plants from the same strain, that are growing together within their vegetative and flowering phases. 
    Attributes of all of the plants within a batch can be modified at the batch level, which will apply changes across all of the plant 
    records. Additionally, plant records can be modified individually (see the /plants endpoint).
    
    'Harvest' batches represent a group of harvested material that is all of the same strain. These types of batches are used to denote 
    both 'wet' and 'dry' weight of 'flower' and 'other material' produced during the harvest. Resultant dry weight from a harvest batch is 
    separated into 'inventory lots'. While initial inventory in a harvest stage can be created at the 'batch' endpoint, in a general workflow 
    they are made by using the /harvest_plants API call.
    
    'Intermediate/ end product' batches are batches that consist of multiple harvest batches being combined, for example, combining 
    two different strains to make a blended concentrate product.

    The purpose of using batches to group together plant and inventory records is two-fold. Batches assist with creating the traceability 
    that the system is designed to offer. As well, batches allow producers to manage plants in any phase in groups, which enables mass 
    actions to be applied to numerous records simultaneously. Batches are not intended to constrain activities involving plant 
    movement, as plants can be shifted from one batch to another and do not have exclusive relationships with batches they are added 
    to.

        harvest_stage (str): the stage of the harvest process;
            only used for batches with type 'harvest'.
            Allowed values:
                'wet', 'cure', 'finished'

        origin (str): Indicates propagation source of the batch.
            Required if type='plant' or 'propagation material'.
            Allowed values:
                'seed', 'clone', 'plant', 'tissue'
        
        plant_stage (str): Current development stage of the plants in 
            the batch.
            Allowed values:
                'propagation source', 'growing', 
                'harvested', 'packaged', 'destroyed'
        
        type (str): Indicates the type of batch.
            Allowed values:
                'propagation material', 'plant', 'harvest', 
                'intermediate/ end product'


    """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class Disposal(object):
    """ Disposal records (referred to as "Destructions" within the UI) are
    inventory lots of waste that are created so that they can be 
    segregated from other inventory to undergo their 72-hour hold process.
    Once this time period has elapsed, physical destruction of 
    the lots may be performed. This can be accomplished through the "dispose_item" API call.
    Disposal records can be created from harvest batches (any waste associated with a harvest batch),
    inventory lots, or recorded as daily plant waste."""

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class InventoryType(object):
    """ """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']



class Inventory(object):
    """ """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class InventoryAdjustment(object):
    """ """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class InventoryTransfer(object):
    """ """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class LabResult(object):
    """ """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']

    def summary(self):
        """Returns a summary of the lab result."""
        return self._properties['global_id']


class Plant(object):
    """ """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class Sale(object):
    """ """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class Strain(object):
    """ """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class Licensee(object):
    """ """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']


class User(object):
    """ """

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Global ID."""
        return self._properties['global_id']

