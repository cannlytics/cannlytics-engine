'''
Leaf Integration Test | Cannlytics

Author: Keegan Skeate
Contact: keegan@cannlytics.com
Created: Thu Mar 18 16:08:18 2021
License: MIT License

Description:

    Perform required tests for Leaf Data Systems integration.
    The validation process requires completion of at least
    1 example of each API call listed in the Worksheet,
    and provide the Global ID and timestamp for each call.
    The MJ Freeway engineering team will pull logs and
    review the calls identified in the worksheet for
    successful completion:

        • Do the calls contain the required data?
        • Did the calls return errors?
        • Did the integrator use an excessive number of
        calls to complete the action?
    
Resources:

'''

# External imports
import os
from datetime import datetime
from dotenv import dotenv_values

# Local imports
import sys
sys.path.insert(0, os.path.abspath('../../'))
from cannlytics.traceability import leaf # pylint: disable=no-name-in-module, import-error


if __name__ == '__main__':
    
    #------------------------------------------------------------------
    # Initialization
    #------------------------------------------------------------------
    
    # Initialize the current time.
    now = datetime.now()
    current_time = now.isoformat()
    current_date = now.strftime('%m/%d/%Y')
    today = current_time[:10]

    # Initialize the Leaf client.
    config = dotenv_values('../../.env')
    api_key = config['LEAF_TEST_API_KEY']
    mme_code = config['LEAF_TEST_PRODUCER_MME_CODE']
    track = leaf.authorize(api_key=api_key, mme_code=mme_code)

    print('--------------------------------------------')
    print('Performing Leaf Data Systems Validation Test')
    print(current_time)
    print('--------------------------------------------')

    #------------------------------------------------------------------
    # Facilities
    #------------------------------------------------------------------

    # Create users for a facilities and
    # get the users with: '/user'
    users = track.get_users()

    #------------------------------------------------------------------
    # Areas
    #------------------------------------------------------------------


    # Create areas.
    # areas = [
    #     {
    #         'name': 'Seed Vault',
    #         'type': 'non-quarantine',
    #         'external_id': 'area-1'
    #     },
    #     {
    #         'name': 'Waste Room',
    #         'type': 'quarantine',
    #         'external_id': 'area-2'
    #     },
    #     {
    #         'name': 'Drying Room',
    #         'type': 'quarantine',
    #         'external_id': 'area-3'
    #     },
    # ]
    # areas = track.create_areas(areas)
    areas = track.get_areas()

    #------------------------------------------------------------------
    # Batches
    #------------------------------------------------------------------

    # Create a strain.
    # strains = [{'name': 'Old-Time Moonshine'}]
    # strains = track.create_strains(strains)

    # Create plant batches.
    # Requires the previous creation of strain and area.
    # Endpoint: '/batches'
    # batches = [{
    #     'type': 'propagation material',
    #     'origin': 'seed',
    #     'global_area_id': areas[0]['global_id'],
    #     'global_strain_id': strains[0]['global_id'],
    #     'num_plants': '33'
    # }]
    # batches = track.create_batches(batches)
    batches = track.get_batches()

    #------------------------------------------------------------------
    # Plants
    #------------------------------------------------------------------

    # Create a plant and add it to a batch.
    # Requires the previous creation of strain, area, and batch.
    # Endpoint: '/plants'
    # plants =  [{
    #     'origin': 'seed',
    #     'stage': 'growing',
    #     'global_batch_id': batches[0]['global_id'],
    #     'plant_created_at': current_date,
    # }]
    # plants = track.create_plants(plants)

    #------------------------------------------------------------------
    # Disposals
    #------------------------------------------------------------------
    
    # Create a partial disposal from a batch.
    # Requires the previous creation of inventory lot, batch, or plant.
    # Endpoint: '/disposals'
    # disposed_at = now.strftime('%m/%d/%Y %h:%m')
    # disposals = [{
    #     'external_id': 'disposal-1',
    #     'reason': 'unhealthy',
    #     'disposal_at': '06/07/2016 12:34pm',
    #     'qty': '13',
    #     'uom': 'ea',
    #     'source': 'batch',
    #     'global_batch_id': batches[0]['global_id'],
    #     'global_area_id': areas[1]['global_id'], # Area for waste.
    #     'global_plant_id': plants[0]['global_id'],
    #     'global_inventory_id': ''
    # }]
    # disposals = track.create_disposals(disposals)
    
    # https://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python

    #------------------------------------------------------------------
    # Harvests
    #------------------------------------------------------------------

    # Create harvest batches.
    # Requires the previous creation of batch of plants.
    # Endpoint: '/plants/harvest_plants'
    # harvested_at = now.strftime('%m/%d/%Y %h:%m')
    # harvested_at = now.isoformat()
    # harvest = track.harvest_plants(
    #     area_id=plants[0]['global_area_id'],
    #     destination_id=areas[2]['global_id'],
    #     plant_ids=[plants[0]['global_id']],
    #     batch_id=plants[0]['global_batch_id'],
    #     external_id='harvest-1',
    #     harvested_at=harvested_at,
    #     flower_wet_weight=33,
    #     other_wet_weight=3.33,
    #     uom='gm'
    # )

    #------------------------------------------------------------------
    # Inventory
    #------------------------------------------------------------------

    # Create inventory lots.
    # Requires previous creation of area, strain, batch, and inventory type.
    # Endpoint: '/inventories'
    
    # Create an inventory adjustment.
    # Requires the previous creation of an inventory lot.
    # Endpoint: '/inventory_adjustments'
    
    # Create an inventory adjustment.
    # Requires the previous creation of an inventory lot.
    # Endpoint: '/inventory_transfers'


    #------------------------------------------------------------------
    # Lab results
    #------------------------------------------------------------------

    # Create a lab result for a sample transferred to a lab.
    # Requires the previous creation of an inventory transfer, a lab user, 
    # and an inventory lot.
    # Endpoint: '/lab_result'
    lab_result_data = {
        'external_id': 'test',
        'tested_at': '04/18/2018 12:34pm',
        'testing_status': 'completed',
        'notes': 'test notes',
        'received_at': '01/23/2018 4:56pm',
        'type': 'harvest_materials',
        'intermediate_type': 'flower_lots',
        'moisture_content_percent': '1',
        'moisture_content_water_activity_rate': '.635',
        'cannabinoid_editor': 'WAWA1.US4',
        'cannabinoid_status': 'completed',
        'cannabinoid_d9_thca_percent': '13.57',
        'cannabinoid_d9_thca_mg_g': 0,
        'cannabinoid_d9_thc_percent': '24.68',
        'cannabinoid_d9_thc_mg_g': 0,
        'cannabinoid_cbd_percent': '3.21',
        'cannabinoid_cbd_mg_g': 0,
        'cannabinoid_cbda_percent': '1.23',
        'cannabinoid_cbda_mg_g': 0,
        'microbial_editor': 'WAWA1.US4',
        'microbial_status': 'completed',
        'microbial_bile_tolerant_cfu_g': '0.00',
        'microbial_pathogenic_e_coli_cfu_g': '0.00',
        'microbial_salmonella_cfu_g': '0.00',
        'mycotoxin_editor': 'WAWA1.US4',
        'mycotoxin_status': 'completed',
        'mycotoxin_aflatoxins_ppb': '19.99',
        'mycotoxin_ochratoxin_ppb': '19.99',
        'metal_editor': '',
        'metal_status': 'not_started',
        'metal_arsenic_ppm': 0,
        'metal_cadmium_ppm': 0,
        'metal_lead_ppm': 0,
        'metal_mercury_ppm': 0,
        'pesticide_editor': '',
        'pesticide_status': 'not_started',
        'pesticide_abamectin_ppm': 0,
        'pesticide_acephate_ppm': 0,
        'pesticide_acequinocyl_ppm': 0,
        'pesticide_acetamiprid_ppm': 0,
        'pesticide_aldicarb_ppm': 0,
        'pesticide_azoxystrobin_ppm': 0,
        'pesticide_bifenazate_ppm': 0,
        'pesticide_bifenthrin_ppm': 0,
        'pesticide_boscalid_ppm': 0,
        'pesticide_carbaryl_ppm': 0,
        'pesticide_carbofuran_ppm': 0,
        'pesticide_chlorantraniliprole_ppm': 0,
        'pesticide_chlorfenapyr_ppm': 0,
        'pesticide_chlorpyrifos_ppm': 0,
        'pesticide_clofentezine_ppm': 0,
        'pesticide_cyfluthrin_ppm': 0,
        'pesticide_cypermethrin_ppm': 0,
        'pesticide_daminozide_ppm': 0,
        'pesticide_ddvp_dichlorvos_ppm': 0,
        'pesticide_diazinon_ppm': 0,
        'pesticide_dimethoate_ppm': 0,
        'pesticide_ethoprophos_ppm': 0,
        'pesticide_etofenprox_ppm': 0,
        'pesticide_etoxazole_ppm': 0,
        'pesticide_fenoxycarb_ppm': 0,
        'pesticide_fenpyroximate_ppm': 0,
        'pesticide_fipronil_ppm': 0,
        'pesticide_flonicamid_ppm': 0,
        'pesticide_fludioxonil_ppm': 0,
        'pesticide_hexythiazox_ppm': 0,
        'pesticide_imazalil_ppm': 0,
        'pesticide_imidacloprid_ppm': 0,
        'pesticide_kresoxim_methyl_ppm': 0,
        'pesticide_malathion_ppm': 0,
        'pesticide_metalaxyl_ppm': 0,
        'pesticide_methiocarb_ppm': 0,
        'pesticide_methomyl_ppm': 0,
        'pesticide_methyl_parathion_ppm': 0,
        'pesticide_mgk_264_ppm': 0,
        'pesticide_myclobutanil_ppm': 0,
        'pesticide_naled_ppm': 0,
        'pesticide_oxamyl_ppm': 0,
        'pesticide_paclobutrazol_ppm': 0,
        'pesticide_permethrinsa_ppm': 0,
        'pesticide_phosmet_ppm': 0,
        'pesticide_piperonyl_butoxideb_ppm': 0,
        'pesticide_prallethrin_ppm': 0,
        'pesticide_propiconazole_ppm': 0,
        'pesticide_propoxur_ppm': 0,
        'pesticide_pyrethrinsbc_ppm': 0,
        'pesticide_pyridaben_ppm': 0,
        'pesticide_spinosad_ppm': 0,
        'pesticide_spiromesifen_ppm': 0,
        'pesticide_spirotetramat_ppm': 0,
        'pesticide_spiroxamine_ppm': 0,
        'pesticide_tebuconazole_ppm': 0,
        'pesticide_thiacloprid_ppm': 0,
        'pesticide_thiamethoxam_ppm': 0,
        'pesticide_trifloxystrobin_ppm': 0,
        'solvent_editor': 'WAWA1.US4',
        'solvent_status': 'completed',
        'solvent_acetone_ppm': 0,
        'solvent_benzene_ppm': 0,
        'solvent_butanes_ppm': 0,
        'solvent_cyclohexane_ppm': 0,
        'solvent_chloroform_ppm': 0,
        'solvent_dichloromethane_ppm': 0,
        'solvent_ethyl_acetate_ppm': 0,
        'solvent_heptane_ppm': 0,
        'solvent_hexanes_ppm': 0,
        'solvent_isopropanol_ppm': 0,
        'solvent_methanol_ppm': 0,
        'solvent_pentanes_ppm': 0,
        'solvent_propane_ppm': 0,
        'solvent_toluene_ppm': 0,
        'solvent_xylene_ppm': 0,
        'foreign_matter_stems': '1',
        'foreign_matter_seeds': '0',
        'test_for_terpenes': '0',
        'global_for_mme_id': 'WAWA1.MM1X9',
        'global_inventory_id': 'WAL400004.IN7EB5'
    }
    # lab_result = LabResult.create_from_json(lab_result_data)


    #------------------------------------------------------------------
    # Sale
    #------------------------------------------------------------------
    
    # Create a sale.
    # Requires the previous creation of an area, batch, and inventory item.
    # Endpoint: '/sales'
    sale_data = {
        'external_id': '12345',
        'type': 'retail_recreational',
        'patient_medical_id': '',
        'caregiver_id': '',
        'sold_at': '12/01/2017',
        'price_total': '30.00',
        'status': 'sale',
        'global_sold_by_user_id': 'WAR030303.USA7G6',
        'sale_items': [
            {
                'external_id': '12345',
                'type': 'sale',
                'sold_at': '12/01/2017',
                'qty': '2.00',
                'uom': 'ea',
                'unit_price': '30.00',
                'price_total': '60.00',
                'name': 'Dewberry Haze Pre-Packs 3.5gm',
                'global_batch_id': 'WAR030303.BAEV',
                'global_inventory_id': 'WAR030303.IN9A'
            }
        ]
    }

    # sale = Sale.create_from_json(sale_data)


