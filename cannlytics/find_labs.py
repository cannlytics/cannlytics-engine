# -*- coding: utf-8 -*-
"""
Find Labs | Cannlytics
Copyright © 2021 Cannlytics
Author: Keegan Skeate <keegan@cannlytics.com>
Created: 1/10/2021

License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Resources:
    https://stackoverflow.com/questions/54416896/how-to-scrape-email-and-phone-numbers-from-a-list-of-websites
    https://hackersandslackers.com/scraping-urls-with-beautifulsoup/
    https://developers.google.com/maps/documentation/timezone/overview

Description:
    Find data points for all cannabis-testing labs using any existing
    information about the labs.
"""
import math
import pandas as pd
import os
from datetime import datetime
from firebase_admin import initialize_app
from logistics import geocode_addresses, get_place_details
from phonenumbers import timezone, parse, format_number, PhoneNumberFormat
from scraper import get_page_metadata, get_phone, get_email


# TODO: Set reference to your Firebase service account.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""

def find_lab_data(lab):
    """Find as many data points as possible about a lab.
    Expects a default lab dictionary with at least the lab's name.
    Where a lab is represented as:
        {
            "name": "",
            "website": "",
            "image_url": "",
            "phone": "",
            "email": "",
            "street": "",
            "city": "",
            "state": "",
            "zip": "",
            "description": "",
            "hours": "",
            "theme_color": "",
            "timezone": "",
        }
    """
    
    # Format address if needed.
    if lab.get("formatted_address") and not lab.get("street"):
        try:
            address_parts = lab["formatted_address"].split(',')
            lab["street"] = address_parts[0]
            lab["city"] = address_parts[1].title().strip()
            lab["zip"] = address_parts[2].replace(lab["state"], '').strip()
        except IndexError:
            pass
    
    # Try to get the place details for the lab.
    try:
        details = get_place_details(lab["name"])
        lab = {**details, **lab}
    except IndexError:
        pass
    
    # Get the lab's website.
    if lab.get("website"):
        url = lab["website"]
    else:
        print("TODO: Implement custom search for website")
        return

    # Try to get metadata from the lab's website.
    try:
        response, html, metadata = get_page_metadata(url)
        lab = {**lab, **metadata}
    except:
        pass
    
    # Try to find any email on the website.
    if not lab.get("email"):
        try:
            if not math.isnan(lab.get("email")):
                lab["email"] = get_email(html, response)
        except TypeError:
            pass
    
    # Try to find a phone number on the lab's website.
    if not lab.get("phone"):
        try:
            if not math.isnan(lab.get("phone")):
                lab["phone"] = get_phone(html, response)
        except TypeError:
            pass

    # Format any phone number and get it's timezone.
    try:
        number = parse(lab["phone"], 'US')
        lab["phone"] = format_number(
            number,
            PhoneNumberFormat.NATIONAL, # TODO: Handle international labs.
        )
        lab["timezone"] = timezone.time_zones_for_number(number)[0]
        # Optional: Use Google timezone service.
        # https://developers.google.com/maps/documentation/timezone/overview
    except:
        pass

    return lab


def clean_string_columns(df):
    """Clean string columns in a dataframe."""
    try:
        df.email = df.email.str.lower()
        df.website = df.website.str.lower()
    except AttributeError:
        pass
    str_columns = ["name", "trade_name", "city", "county"]
    for column in str_columns:
        try:
            df[column] = df[column].astype(str).str.title()
            df[column] = df[column].astype(str).str.replace('Llc', 'LLC')
            df[column] = df[column].astype(str).str.replace('L.L.C.', 'LLC')
            df[column] = df[column].astype(str).str.strip()
        except (AttributeError, KeyError):
            pass
    return df


def create_lab_contacts(labs):
    """Create and save contacts for given lab(s)."""
    # Save contacts
    # entry["contacts"] = [{
    #     "name": row["Business Owner"],
    #     "position": "Owner",
    # }]
    print('TODO: Creating contacts...')


def find_labs(input_file):
    """Find data points for all labs in a given input file."""

    STATES = ['MI', 'MT', 'MO', 'NV', 'NH', 'NJ',
              'NM', 'ND', 'NY', 'OH', 'OK', 'OR', 'PA', 'TN', 'VT',
              'WA',
              'AK', 'AZ', 'CA', 'CO', 'CT',
              'DE', 'DC', 'FL', 'HI', 'IL',
              'LA', 'MA', 'ME', 'MD', ] # TODO: WV

    # COUNTRIES = ['Canada', 'South Africa', 'Columbia']
    
    # Initialize Firebase.
    try:
        initialize_app()
    except ValueError:
        pass    

    # Get data points for each lab.
    lab_data = []
    for state in STATES:
        print('---------------------------')
        print('Getting lab data in:', state)
        print('---------------------------')
        labs = pd.read_excel(input_file, sheet_name=state)
        labs = clean_string_columns(labs)
        # labs.email = labs.email.str.lower()
        # labs.website = labs.website.str.lower()
        for index, row in labs.iterrows():
            values = row.to_dict()
            data = find_lab_data(values)
            lab_data.append(data)
            print('Found data for:', values["name"])
    
    # Geocode addresses.
    labs = pd.DataFrame(lab_data)
    labs = geocode_addresses(labs)

    # Save results
    timestamp = datetime.now().isoformat()[:16].replace(':', '-')
    output_file = f'./data/labs_{timestamp}.xlsx'
    labs.to_excel(output_file, index=False, sheet_name='All Labs')


if __name__ == "__main__":
    
    find_labs("./data/labs.xlsx")

