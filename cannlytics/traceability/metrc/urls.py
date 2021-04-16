# -*- coding: utf-8 -*-
"""
cannlytics.traceability.metrc.urls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Metrc API URLs.
"""

# FIXME: Make state dynamic
STATE = 'ok'
METRC_API_BASE_URL = f'https://sandbox-api-{STATE}.metrc.com'
METRC_API_BASE_URL_TEST = f'https://sandbox-api-{STATE}.metrc.com'

METRC_BATCHES_URL = METRC_API_BASE_URL + '/plantbatches/v1/%s'
METRC_EMPLOYEES_URL = METRC_API_BASE_URL + '/employees/v1/'
METRC_FACILITIES_URL = METRC_API_BASE_URL + '/facilities/v1/'
METRC_LOCATIONS_URL = METRC_API_BASE_URL + '/locations/v1/%s'
METRC_HARVESTS_URL = METRC_API_BASE_URL + '/harvests/v1/%s'
METRC_ITEMS_URL = METRC_API_BASE_URL + '/items/v1/%s'
METRC_LAB_RESULTS_URL = METRC_API_BASE_URL + '/labtests/v1/%s'
METRC_PACKAGES_URL = METRC_API_BASE_URL + '/packages/v1/%s'
METRC_PATIENTS_URL = METRC_API_BASE_URL + '/patients/v1/%s'
METRC_PLANTS_URL = METRC_API_BASE_URL + '/plants/v1/%s'
METRC_RECEIPTS_URL = METRC_API_BASE_URL + '/sales/v1/receipts/%s'
METRC_SALES_URL = METRC_API_BASE_URL + '/sales/v1/%s'
METRC_STRAINS_URL = METRC_API_BASE_URL + '/strains/v1/%s'
METRC_TRANSACTIONS_URL = METRC_API_BASE_URL + '/sales/v1/transactions/%s'
METRC_TRANSFERS_URL = METRC_API_BASE_URL + '/transfers/v1/%s'
METRC_TRANSFER_PACKAGES_URL = METRC_API_BASE_URL + '/transfers/v1/delivery/%s/%s'
METRC_TRANSFER_TEMPLATE_URL = METRC_API_BASE_URL + '/transfers/v1/templates/%s'
METRC_UOM_URL = METRC_API_BASE_URL + '/unitsofmeasure/v1/active'

# Unused
# METRC_CREATE_PACKAGES_URL = METRC_API_BASE_URL + '/harvests/v1/create/packages'
# METRC_CREATE_TESTING_PACKAGES_URL = METRC_API_BASE_URL + '/harvests/v1/create/packages/testing'
# METRC_SHIPMENTS_URL = METRC_API_BASE_URL + '/transfers/v1/%s/%s'
# METRC_TRANSFER_DETAILS_URL = METRC_API_BASE_URL + '/transfers/v1/%s/%s/details'
# METRC_WASTE_TYPES_URL = METRC_API_BASE_URL + '/harvests/v1/waste/types'

