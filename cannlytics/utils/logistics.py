"""
Logistics Utilities | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Authors: Keegan Skeate <keegan@cannlytics.com>
Created: 11/5/2021
Updated: 12/5/2021
License: <https://github.com/cannlytics/cannlytics-engine/blob/main/LICENSE>

Description: This script contains functions that are useful for logistics.
"""
# Standard imports.
from time import sleep
from typing import List, Optional

# External imports.
from googlemaps import Client, places

# Internal imports.
from ..firebase import initialize_firebase, get_document


def get_google_maps_api_key():
    """Get Google Maps API key.
    Returns:
        (str): Returns the Google Maps API key stored
            in the Firestore database.
    """
    # FIXME: Prefer using secret manager to Firestore for secrets.
    database = initialize_firebase()
    google_doc = get_document('admin/google', database=database)
    google_data = google_doc.to_dict()
    return google_data['google_maps_api_key']


def geocode_addresses(df, api_key: Optional[str] = None):
    """Geocode addresses in a dataframe.
    Args:
        df (DataFrame): A DataFrame containing the addresses to geocode.
    Returns:
        (DataFrame): Returns the DataFrame with geocoded latitudes and longitudes.
    """
    if api_key is None:
        api_key = get_google_maps_api_key()
    gmaps = Client(key=api_key)
    for index, item in df.iterrows():
        # TODO: Handle existing lat and long more elegantly.
        # try:
        #     if item.latitude and item.longitude:
        #         continue
        # except:
        #     pass
        address = f'{item.street}, {item.city}, {item.state} {item.zip}'
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            df.at[index, 'formatted_address'] = geocode_result[0]['formatted_address']
            location = geocode_result[0]['geometry']['location']
            print(item.name, '-->', location)
            df.at[index, 'latitude'] = location['lat']
            df.at[index, 'longitude'] = location['lng']
            # TODO: Round latitude and longitude (4-6 decimal places?)
            for info in geocode_result[0]['address_components']:
                key = info['types'][0]
                if key == 'administrative_area_level_2':
                    df.at[index, 'county'] = info['long_name']

        sleep(.2) # Prevents spamming Google's servers (necessary?).
    return df


def search_for_address(
        query: str,
        api_key: Optional[str] = None,
        fields: Optional[List[str]] = None,
) -> List[dict]:
    """Search for the address of a given name.
    Args:
        query (str): The text to use to search for an address.
        api_key (): Optional, None by default.
        fields (list): Optional, `formatted_address` is included by default.
    Returns:
        (list): A list of potential results.
    """
    if api_key is None:
        api_key = get_google_maps_api_key()
    if fields is None:
        fields = ['formatted_address']
    gmaps = Client(key=api_key)
    place = places.find_place(gmaps, query, 'textquery', fields=fields)
    return place['candidates']


def get_place_details(
        query: str,
        api_key: Optional[str] = None,
        fields: Optional[List[str]] = None,
):
    """Get the place details for a given a name.
    Args:
        query (str): The text to use to search for a place.
        api_key (str): Optional Google Maps API key, None by default.
        fields (list): Optional fields to retrieve.
    Returns:
        (dict): A dictionary of place details.
    """
    if api_key is None:
        api_key = get_google_maps_api_key()
    if not fields:
        fields = [
            'formatted_address',
            'photo',
            'opening_hours',
            'website',
        ]
    gmaps = Client(key=api_key)
    search = places.find_place(gmaps, query, 'textquery')
    place_id = search['candidates'][0]['place_id']
    place = places.place(gmaps, place_id, fields=fields)
    return place['result']
