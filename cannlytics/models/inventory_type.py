"""
Batch Model | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>  
Created: 11/5/2021  
Updated: 11/5/2021  

Batch data model.
"""
# Standard imports.
from dataclasses import dataclass
from datetime import datetime

# Internal imports.
from .base import Model


@dataclass
class InventoryType(Model):
    """The type for any physical inventory item."""
    _collection = 'organizations/%s/inventory_types'
    admin_method: str = ''
    brand: str = ''
    name: str = ''
    category_type: str = ''
    quantity_type: str = ''
    strain_required: bool = False
    #  "Name": "Buds",
    # "ProductCategoryType": "Buds",
    # "QuantityType": "WeightBased",
    # "RequiresStrain": true,
    # "RequiresItemBrand": false,
    # "RequiresAdministrationMethod": false,
    # "RequiresUnitCbdPercent": false,
    # "RequiresUnitCbdContent": false,
    # "RequiresUnitCbdContentDose": false,
    # "RequiresUnitThcPercent": false,
    # "RequiresUnitThcContent": false,
    # "RequiresUnitThcContentDose": false,
    # "RequiresUnitVolume": false,
    # "RequiresUnitWeight": false,
    # "RequiresServingSize": false,
    # "RequiresSupplyDurationDays": false,
    # "RequiresNumberOfDoses": false,
    # "RequiresPublicIngredients": false,
    # "RequiresDescription": false,
    # "RequiresProductPhotos": 0,
    # "RequiresLabelPhotos": 0,
    # "RequiresPackagingPhotos": 0,
    # "CanContainSeeds": true,
    # "CanBeRemediated": true
