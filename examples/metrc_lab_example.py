"""
Lab Workflow | Cannlytics
Copyright (c) 2021-2022 Cannlytics

Authors: Keegan Skeate <contact@cannlytics.com>
Created: 12/21/2021
Updated: 1/10/2022
License: <https://github.com/cannlytics/cannlytics-engine/blob/main/LICENSE>
"""
from cannlytics import metrc

# Initialize a Metrc API client.
track = metrc.authorize(
    'your-vendor-api-key',
    'your-user-api-key',
    primary_license='your-user-license-number',
    state='ma',
)

# Post lab results.
track.post_lab_results([{...}, {...}])

# Get a tested package.
test_package = track.get_packages(label='abc')

# Get the tested package's lab result.
lab_results = track.get_lab_results(uid=test_package.id)
