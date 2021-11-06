"""
Metrc Constants | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Author: Keegan Skeate <keegan@cannlytics.com>
Created: 11/5/2021
Updated: 11/5/2021

This module contains Metrc variables that are constant.
"""

additive_types = ['Fertilizer', 'Pesticide', 'Other']

adjustment_reasons = [
    {'Name': 'API Related Error', 'RequiresNote': True},
    {'Name': 'Drying', 'RequiresNote': True},
    {'Name': 'Mandatory State Destruction', 'RequiresNote': True},
    {'Name': 'Theft', 'RequiresNote': True},
    {'Name': 'Typing/Entry Error', 'RequiresNote': True}
]

analyses = [
    {
        'Id': 1,
        'Name': 'THC',
        'RequiresTestResult': False,
        'InformationalOnly': False,
        'AlwaysPasses': False,
        'LabTestResultMode': 0,
        'LabTestResultMinimum': None,
        'LabTestResultMaximum': None,
        'DependencyMode': 0
    },
    {
        'Id': 2,
        'Name': 'THCa',
        'RequiresTestResult': False,
        'InformationalOnly': False,
        'AlwaysPasses': False,
        'LabTestResultMode': 0,
        'LabTestResultMinimum': None,
        'LabTestResultMaximum': None,
        'DependencyMode': 0
    },
    {
        'Id': 3,
        'Name': 'CBD',
        'RequiresTestResult': False,
        'InformationalOnly': False,
        'AlwaysPasses': False,
        'LabTestResultMode': 0,
        'LabTestResultMinimum': None,
        'LabTestResultMaximum': None,
        'DependencyMode': 0
    },
    {
        'Id': 4,
        'Name': 'CBDa',
        'RequiresTestResult': False,
        'InformationalOnly': False,
        'AlwaysPasses': False,
        'LabTestResultMode': 0,
        'LabTestResultMinimum': None,
        'LabTestResultMaximum': None,
        'DependencyMode': 0
    },
    {
        'Id': 5,
        'Name': 'Pesticides',
        'RequiresTestResult': False,
        'InformationalOnly': False,
        'AlwaysPasses': False,
        'LabTestResultMode': 0,
        'LabTestResultMinimum': None,
        'LabTestResultMaximum': None,
        'DependencyMode': 'RequiresOne'
    }
]

batch_types = ['Seed', 'Clone']

categories = [
    'Flower & Buds',
    'Immature Plants',
    # Concentrate (Non-Solvent Based) (Count-Volume)
    # Concentrate (Non-Solvent Based) (Count-Weight)
    # Concentrate (Weight Based)
    # Edibles (Count-Volume)
    # Edibles (Count-Weight)
    # Extracts (Solvent Based) (Count-Volume)
    # Extracts (Solvent Based) (Count-Weight)
    # Flower & Buds
    # Immature Plants
    # Kief
    # Mature Plants
    # Metered Dose Nasal Spray Products
    # MMJ Waste
    # Pre-Roll (Flower Only)
    # Pre-Roll (Infused)
    # Pressurized Metered Dose Inhaler Products
    # Rectal/Vaginal Administration Products (Count-Volume)
    # Rectal/Vaginal Administration Products (Count-Weight)
    # Seeds
    # Shake/Trim
    # Shake/Trim (by Strain)
    # Tinctures (Count-Volume)
    # Tinctures (Count-Weight)
    # Topicals (Count-Volume)
    # Topicals (Count-Weight)
    # Transdermal Patches
    # Vape Cartridges
    # Whole Wet Plant
]

customer_types = [
    'Consumer',
    'Patient',
    'Caregiver',
    'ExternalPatient',
]

item_types = [
    {
        'Name': 'Buds',
        'ProductCategoryType': 'Buds',
        'QuantityType': 'WeightBased',
        'RequiresStrain': True,
        'RequiresItemBrand': False,
        'RequiresAdministrationMethod': False,
        'RequiresUnitCbdPercent': False,
        'RequiresUnitCbdContent': False,
        'RequiresUnitCbdContentDose': False,
        'RequiresUnitThcPercent': False,
        'RequiresUnitThcContent': False,
        'RequiresUnitThcContentDose': False,
        'RequiresUnitVolume': False,
        'RequiresUnitWeight': False,
        'RequiresServingSize': False,
        'RequiresSupplyDurationDays': False,
        'RequiresNumberOfDoses': False,
        'RequiresPublicIngredients': False,
        'RequiresDescription': False,
        'RequiresProductPhotos': 0,
        'RequiresLabelPhotos': 0,
        'RequiresPackagingPhotos': 0,
        'CanContainSeeds': True,
        'CanBeRemediated': True
    },
    {
        'Name': 'Immature Plants',
        'ProductCategoryType': 'Plants',
        'QuantityType': 'CountBased',
        'RequiresStrain': True,
        'RequiresItemBrand': False,
        'RequiresAdministrationMethod': False,
        'RequiresUnitCbdPercent': False,
        'RequiresUnitCbdContent': False,
        'RequiresUnitCbdContentDose': False,
        'RequiresUnitThcPercent': False,
        'RequiresUnitThcContent': False,
        'RequiresUnitThcContentDose': False,
        'RequiresUnitVolume': False,
        'RequiresUnitWeight': False,
        'RequiresServingSize': False,
        'RequiresSupplyDurationDays': False,
        'RequiresNumberOfDoses': False,
        'RequiresPublicIngredients': False,
        'RequiresDescription': False,
        'RequiresProductPhotos': 0,
        'RequiresLabelPhotos': 0,
        'RequiresPackagingPhotos': 0,
        'CanContainSeeds': True,
        'CanBeRemediated': False
    },
    {
        'Name': 'Infused',
        'ProductCategoryType': 'InfusedEdible',
        'QuantityType': 'CountBased',
        'RequiresStrain': False,
        'RequiresItemBrand': False,
        'RequiresAdministrationMethod': False,
        'RequiresUnitCbdPercent': False,
        'RequiresUnitCbdContent': False,
        'RequiresUnitCbdContentDose': False,
        'RequiresUnitThcPercent': False,
        'RequiresUnitThcContent': True,
        'RequiresUnitThcContentDose': False,
        'RequiresUnitVolume': False,
        'RequiresUnitWeight': True,
        'RequiresServingSize': False,
        'RequiresSupplyDurationDays': False,
        'RequiresNumberOfDoses': False,
        'RequiresPublicIngredients': False,
        'RequiresDescription': False,
        'RequiresProductPhotos': 0,
        'RequiresLabelPhotos': 0,
        'RequiresPackagingPhotos': 0,
        'CanContainSeeds': False,
        'CanBeRemediated': True
    },
    {
        'Name': 'Infused Liquid',
        'ProductCategoryType': 'InfusedEdible',
        'QuantityType': 'CountBased',
        'RequiresStrain': False,
        'RequiresItemBrand': False,
        'RequiresAdministrationMethod': False,
        'RequiresUnitCbdPercent': False,
        'RequiresUnitCbdContent': False,
        'RequiresUnitCbdContentDose': False,
        'RequiresUnitThcPercent': False,
        'RequiresUnitThcContent': True,
        'RequiresUnitThcContentDose': False,
        'RequiresUnitVolume': True,
        'RequiresUnitWeight': False,
        'RequiresServingSize': False,
        'RequiresSupplyDurationDays': False,
        'RequiresNumberOfDoses': False,
        'RequiresPublicIngredients': False,
        'RequiresDescription': False,
        'RequiresProductPhotos': 0,
        'RequiresLabelPhotos': 0,
        'RequiresPackagingPhotos': 0,
        'CanContainSeeds': False,
        'CanBeRemediated': True
    }
]

growth_phases = ['Young', 'Vegetative', 'Flowering']

# TODO: Vary by state?
# harvest_waste_types = ['Plant Material', 'Fibrous', 'Root Ball']
harvest_waste_types = ['MMJ Waste', 'Waste']
# waste_types = {
#     'Contamination': 'Degradation of plant(s) by environmental elements such as pests, filth/foreign material, mold/mildew.',
#     'Contamination (BCC)': 'Degradation of plant(s) by environmental elements such as pests, filth/foreign material, mold/mildew. Displays for BCC licensees only.',
#     'Damage': 'Damage to the plant(s).',
#     Damage (BCC) Damage to the plant(s). Displays for BCC licensees only.
#     Failure to Thrive Failure to grow or develop vigorously.
#     Failure to Thrive
#     (BCC)
#     Failure to grow or develop vigorously. Displays for BCC licensees
#     only.
#     Male Plants The plant(s) is male.
#     Male Plants (BCC) The plant(s) is male. Displays for BCC licensees only.
#     Mandated
#     Destruction
#     Cannabis plant(s) is destroyed as a result of a State– or local
#     authority–mandated or –supervised process.
#     Pesticides Improper usage and application of pesticides on plant(s).
#     64
#     Industry User’s Guide – CA Supplemental Rev 20.4
#     Waste Reason Reason Usage
#     Pruning Cannabis byproduct produced during pruning of plant(s).
# }

location_types = [
    {
        'Id': 1,
        'Name': 'Default',
        'ForPlantBatches': True,
        'ForPlants': True,
        'ForHarvests': True,
        'ForPackages': True,
    },
    {
        'Id': 2,
        'Name': 'Planting',
        'ForPlantBatches': True,
        'ForPlants': True,
        'ForHarvests': False,
        'ForPackages': False,
    },
    {
        'Id': 3,
        'Name': 'Packing',
        'ForPlantBatches': False,
        'ForPlants': False,
        'ForHarvests': False,
        'ForPackages': True,
    },
]

package_types = [
    'Product',
    'ImmaturePlant',
    'VegetativePlant',
    'PlantWaste',
    'HarvestWaste',
]

parameters = {
    'license_number': 'licenseNumber',
    'start': 'lastModifiedStart',
    'end': 'lastModifiedEnd',
    'sales_start': 'salesDateStart',
    'sales_end': 'salesDateEnd',
    'package_id': 'packageId',
    'from_mother': 'isFromMotherPlant',
    'source': 'source',
}

# TODO: Vary by state?
# rejection_types = {
# Damage There has been damage to the plant or package.
# Damage (BCC) There has been damage to the package. Notes section should be used
# to explain the damage. Displays for BCC licensees only.
# Data Entry Error A package(s) cannot be accepted by the receiving licensee due to a
# data entry error that occurred when the manifest was created.
# Incorrect Item
# (Transfer)
# A manifest was created with the incorrect item and must be rejected.
# Incorrect Quantity Package received via transfer that was not correctly weighed or
# counted. This should NOT be used to correct sales. If the package
# quantity varies significantly, it should be rejected.
# Notes section should be used to explain the error.
# Non-Compliant
# Label
# Package received via transfer that contains non-compliant label.
# 126
# Industry User’s Guide – CA Supplemental Rev 20.4
# Spoilage Deterioration of packaged product.
# Theft Rejection of a package when product has been stolen in transit.
# Licensing Authority must be notified. Notes section should be used to
# }

test_statuses = [
    'NotSubmitted',
    'SubmittedForTesting',
    'TestFailed',
    'TestPassed',
    'TestingInProgress',
    'AwaitingConfirmation',
    'RetestFailed',
    'RetestPassed',
    'Remediated',
    'SelectedForRandomTesting',
    'NotRequired',
    'ProcessValidated',
]

transfer_statuses = [
    'Shipped',
    'Rejected',
    'Accepted',
    'Returned',
]

# TODO: Vary by state?
transfer_types = [
    {
        'Name': 'Affiliated Transfer',
        'ForLicensedShipments': True,
        'ForExternalIncomingShipments': False,
        'ForExternalOutgoingShipments': False,
        'RequiresDestinationGrossWeight': False,
        'RequiresPackagesGrossWeight': False,
    },
    {
        'Name': 'Beginning Inventory Transfer',
        'ForLicensedShipments': False,
        'ForExternalIncomingShipments': True,
        'ForExternalOutgoingShipments': False,
        'RequiresDestinationGrossWeight': False,
        'RequiresPackagesGrossWeight': False,
    },
    {
        'Name': 'Lab Sample Transfer',
        'ForLicensedShipments': True,
        'ForExternalIncomingShipments': False,
        'ForExternalOutgoingShipments': False,
        'RequiresDestinationGrossWeight': False,
        'RequiresPackagesGrossWeight': False,
    },
    {
        'Name': 'Unaffiliated (Wholesale) Transfer',
        'ForLicensedShipments': True,
        'ForExternalIncomingShipments': False,
        'ForExternalOutgoingShipments': False,
        'RequiresDestinationGrossWeight': False,
        'RequiresPackagesGrossWeight': False,
    },
    {
        'Name': 'Waste Disposal',
        'ForLicensedShipments': True,
        'ForExternalIncomingShipments': False,
        'ForExternalOutgoingShipments': False,
        'RequiresDestinationGrossWeight': False,
        'RequiresPackagesGrossWeight': False,
    }
]
# transfer_types = {
# Transfer Used for all transfers except transfers requiring the use of a
# Wholesale Manifest or Return manifest.
# Return A Return transfer is used only for the transfer of defective
# manufactured products back to the originating licensee.
# Wholesale Manifest A Wholesale Manifest transfer is used when transferring products
# to a Retailer licensee.
# When a Wholesale Manifest is used, the originator is required to
# record the wholesale price of each package in the transfer.
# A Microbusiness functioning as a Distributor with a transfer that
# includes a Retailer licensee, or another Microbusiness licensee
# functioning as a Retailer, shall follow the process above.
# It is recommended that Nurseries utilize a Wholesale Manifest
# when transferring seeds or immature plants to a Retailer.
# }

units = [
    {
        'QuantityType': 'CountBased',
        'Name': 'Each',
        'Abbreviation': 'ea',
    },
    {
        'QuantityType': 'WeightBased',
        'Name': 'Ounces',
        'Abbreviation': 'oz',
    },
    {
        'QuantityType': 'WeightBased',
        'Name': 'Pounds',
        'Abbreviation': 'lb',
    },
    {
        'QuantityType': 'WeightBased',
        'Name': 'Grams',
        'Abbreviation': 'g',
    },
    {
        'QuantityType': 'WeightBased',
        'Name': 'Milligrams',
        'Abbreviation': 'mg',
    },
    {
        'QuantityType': 'WeightBased',
        'Name': 'Kilograms',
        'Abbreviation': 'kg',
    },
]

waste_methods = [
    {'Name': 'Grinder'},
    {'Name': 'Compost'},
]

waste_reasons = [
    {
        'Name': 'Disease/Infestation',
        'RequiresNote': True,
    },
    {
        'Name': 'Mother Plant Destruction',
        'RequiresNote': True,
    },
    {
        'Name': 'Trimming/Pruning',
        'RequiresNote': False,
    }
]
