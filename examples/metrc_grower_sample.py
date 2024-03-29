"""
Grower Workflow | Cannlytics
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

# Get a plant by it's ID.
plant = track.get_plants(uid='123')

# Change the growth phase from vegetative to flowering.
plant.flower(tag='your-plant-tag')

# Move the flowering plant to a new room.
plant.move(location_name='The Flower Room')

# Manicure useable cannabis from the flowering plant.
plant.manicure(harvest_name='Old-Time Moonshine', weight=4.20)

# Harvest the flowering plant.
plant.harvest(harvest_name='Old-Time Moonshine', weight=420)
