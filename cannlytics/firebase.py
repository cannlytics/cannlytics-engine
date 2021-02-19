"""
Firebase Module | Cannlytics
Copyright © 2021 Cannlytics
Author: Keegan Skeate <contact@cannlytics.com>
Created: 2/7/2021

License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Resources:
    https://firebase.google.com/docs/

Description:
    A wrapper of firebase_admin to make interacting with the Firestore database
    and Firebase Storage buckets even easier.
"""
from os import listdir
from os.path import isfile, join
from re import sub, findall
from django.utils.crypto import get_random_string
from firebase_admin import auth, firestore, initialize_app, storage
from google.cloud.firestore import ArrayUnion, ArrayRemove, Increment
from google.cloud.firestore_v1.collection import CollectionReference
from pandas import notnull, read_csv, read_excel, DataFrame, Series
from uuid import uuid4


# ------------------------------------------------------------#
# Example credentials
# ------------------------------------------------------------#

# Get credentials
# import os
# import environ
# env = environ.Env()
# env.read_env("../.env")
# credentials = env("GOOGLE_APPLICATION_CREDENTIALS")
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials
# bucket_name = environ.get("FIREBASE_STORAGE_BUCKET")


# ------------------------------------------------------------#
# Firestore
# ------------------------------------------------------------#


def initialize_firebase():
    """Initialize Firebase, unless already initialized.
    
    Returns:
        (Firestore client): A Firestore database instance.
    """
    try:
        initialize_app()
    except ValueError:
        pass
    return firestore.client()


def create_reference(database, path):
    """Create a database reference for a given path.

    Args:
        database (Firestore Client): The Firestore Client.
        path (str): The path to the document or collection.

    Returns:
        (ref): Either a document or collection reference.
    """
    ref = database
    parts = path.split("/")
    for i in range(len(parts)):
        part = parts[i]
        if i % 2:
            ref = ref.document(part)
        else:
            ref = ref.collection(part)
    return ref


def add_to_array(ref, field, value):
    """Add an element to a given field for a given reference.
    
    Args:
        ref (str): A document reference.
        field (str): A list field to create or update.
        value (dynamic): The value to be added to the list.
    """
    database = firestore.client()
    doc = create_reference(database, ref)
    doc.update({field: ArrayUnion([value])})


def remove_from_array(ref, field, value):
    """Remove an element from a given field for a given reference.
    
    Args:
        ref (str): A document reference.
        field (str): A list field to update.
        value (dynamic): The value to be removed from the list.
    """
    database = firestore.client()
    doc = create_reference(database, ref)
    doc.update({field: ArrayRemove([value])})


def increment_value(ref, field, amount=1):
    """Increment a given field for a given reference.
    
    Args:
        ref (str): A document reference.
        field (str): A numeric field to create or update.
        amount (int): The amount to increment, default 1.
    """
    database = firestore.client()
    doc = create_reference(database, ref)
    doc.update({field: Increment(amount)})


def update_document(ref, values):
    """Update a given document with given values.
    
    Args:
        ref (str): A document reference.
        values (str): A dictionary of values to update.
    """
    database = firestore.client()
    doc = create_reference(database, ref)
    doc.set(values, merge=True)


def get_document(ref):
    """Get a given document.
    
    Args:
        ref (str): A document reference.
    
    Returns:
        (dict): Returns the document as a dictionary.
            Returns an empty dictionary if no data is found.
    """
    database = firestore.client()
    doc = create_reference(database, ref)
    data = doc.get()
    if data is None:
        return {}
    else:
        return data.to_dict()


def get_collection(ref, limit=None, order_by=None, desc=False, filters=[]):
    """Get documents from a collection.
    
    Args:
        ref (str): A document reference.
        limit (int): The maximum number of documents to return. The default is no limit.
        order_by (str): A field to order the documents by, with the default being none.
        desc (bool): The direction to order the documents by the order_by field.
        filters (list): Filters are dictionaries of the form
            `{"key": "", "operator": "", "value": ""}`.
            Filters apply [Firebase queries](https://firebase.google.com/docs/firestore/query-data/queries)
            to the given `key` for the given `value`.
            Operators include: `==`, `>=`, `<=`, `>`, `<`, `!=`,
            `in`, `not_in`, `array_contains`, `array_contains_any`.
    
    Returns
        (list): A list of documents.
    """
    docs = []
    database = firestore.client()
    collection = create_reference(database, ref)
    if filters:
        for filter in filters:
            collection = collection.where(
                filter["key"], filter["operation"], filter["value"]
            )
    if order_by and desc:
        collection = collection.order_by(order_by, direction="DESCENDING")
    elif order_by:
        collection = collection.order_by(order_by)
    if limit:
        collection = collection.limit(limit)
    query = collection.stream()  # Only handles streams less than 2 mins.
    for doc in query:
        data = doc.to_dict()
        docs.append(data)
    return docs


def import_data(db, ref, data_file):
    """Import data into Firestore.

    Wishlist
      - Batch upload
      - Handle types <https://hackersandslackers.com/importing-excel-dates-times-into-pandas/>

    Args:
        db (Firestore Client):
        ref (str): A collection or document reference.
        data_file (str): The path to the local data file to upload.
    """
    try:
        data = read_csv(
            data_file,
            header=0,
            skip_blank_lines=True, 
            encoding='latin-1'
        )
    except:
        try:
            data = read_csv(data_file, sep=" ", header=None)
        except:
            try:
                data = read_csv(
                    data_file,
                    header=0,
                    skip_blank_lines=True, 
                    encoding="utf-16",
                    sep='\t',
                )
            except:
                data = read_excel(data_file, header=0)
    data.columns = map(snake_case, data.columns)
    data = data.where(notnull(data), None)
    data_ref = create_reference(db, ref)
    if isinstance(data_ref, CollectionReference):
        for index, values in data.iterrows():
            doc_id = str(index)
            doc_data = values.to_dict()
            data_ref.document(doc_id).set(doc_data, merge=True)
    else:
        doc_data = data.to_dict(orient="index")
        data_ref.set(doc_data, merge=True)


def export_data(db, ref, data_file):
    """Export data from Firestore.

    Wishlist
      - Parse fields that are objects into fields. E.g.

        from pandas.io.json import json_normalize
        artist_and_track = json_normalize(
            data=tracks_response['tracks'],
            record_path='artists',
            meta=['id'],
            record_prefix='sp_artist_',
            meta_prefix='sp_track_',
            sep="_"
        )
    
    Args:
        db (Firestore Client):
        ref (str): A collection or document reference.
        data_file (str): The path to the local data file to upload.
    """
    data_ref = create_reference(db, ref)
    if isinstance(data_ref, CollectionReference):
        data = []
        docs = data_ref.stream()
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data["id"] = doc.id
            data.append(doc_data)
        output = DataFrame(data)
    else:
        doc = data_ref.get()
        output = Series(doc.to_dict())
        output.name = doc.id
    if data_file.endswith('.csv'):
        output.to_csv(data_file)
    else:
        output.to_excel(data_file)


# ------------------------------------------------------------#
# Authentication
# ------------------------------------------------------------#


def create_account(name, email, notification=True):
    """
    Given user name and email, create an account.
    If the email is already being used, then nothing is returned.

        Args:
            name (str): A name for the user.
            email (str): The user's email.
            notification (bool): Whether to notify the user.

        Returns
            (tuple): User object, random password

    """
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$-_"
    password = get_random_string(42, chars)
    photo_url = f"https://robohash.org/{email}?set=set5"
    try:
        user = auth.create_user(
            uid=str(uuid4()),
            email=email,
            email_verified=False,
            password=password,
            display_name=name,
            photo_url=photo_url,
            disabled=False,
        )
        return user, password
    except:
        return None, None


def create_custom_claims(uid, email=None, claims=None):
    """Create custom claims for a user to grant granular permission.
    The new custom claims will propagate to the user's ID token the
    next time a new one is issued.
    
    Args:
        uid (str): A user's ID.
        email (str): A user's email.
        claims (dict): A dictionary of the user's custom claims.
    """
    if email:
        user = auth.get_user_by_email(email)
        uid = user.uid
    auth.set_custom_user_claims(uid, claims)


def get_custom_claims(name):
    """Get custom claims for a user.
    
    Args:
        name (str): A user ID or user email.
    """
    user = get_user(name)
    return user.custom_claims


def create_custom_token(uid, email=None, claims=None):
    """Create a custom token for a given user, expires after one hour.
    
    Args:
        uid (str): A user's ID.
        email (str): A user's email.
        claims (dict):  A dictionary of the user's claims.
    """
    if email:
        user = auth.get_user_by_email(email)
        uid = user.uid
    return auth.create_custom_token(uid, claims)


def verify_token(token):
    """Verify a user's custom token.
    
    Args:
        token (str): The custom token to authenticate a user.
    """
    return auth.verify_id_token(token)


def get_user(name):
    """Get a user by user ID or by email.
    
    Args:
        name (str): A user ID, email, or phone number.
    
    Returns:
        (Firebase user): A Firebase user object.
    """
    user = None
    try:
        user = auth.get_user(name)
    except:
        pass
    if user is None:
        try:
            user = auth.get_user_by_email(name)
        except:
            pass
    if user is None:
        try:
            user = auth.get_user_by_phone_number(name)
        except:
            pass
    return user


def get_users():
    """Get all Firebase users.
    
    Returns:
        (list): A list of Firebase users.
    """
    users = []
    for user in auth.list_users().iterate_all():
        users.append(user)
    return users


def update_user(existing_user, data):
    """Update a user.
    
    Args:
        existing_user (Firebase user):
        data (dict): The values of the user to update, which can include
            email, phone_number, email_verified, diplay_name, photo_url,
            and disabled.
    """
    values = {}
    fields = [
        "email",
        "phone_number",
        "email_verified",
        "display_name",
        "photo_url",
        "disabled",
    ]
    for field in fields:
        new_value = data.get(field)
        if new_value:
            values[field] = new_value
        else:
            values[field] = getattr(existing_user, field)
    return auth.update_user(
        existing_user.uid,
        email=values["email"],
        phone_number=values["phone_number"],
        email_verified=values["email_verified"],
        display_name=values["display_name"],
        photo_url=values["photo_url"],
        disabled=values["disabled"],
    )


def delete_user(uid):
    """Delete a user from Firebase.
    
    Args:
        uid (str): A user's ID.
    """
    auth.delete_user(uid)


# Optional: Implement custom email.
# def send_password_reset(email):
#     """Send a password reset to a user given an email."""
#     link = auth.generate_password_reset_link(email)
#     send_custom_email(email, link)


# ------------------------------------------------------------#
# Storage
# ------------------------------------------------------------#


def download_file(bucket_name, source_blob_name, destination_file_name, verbose=True):
    """Downloads a file from Firebase Storage.
    
    Args:
        bucket_name (str): The name of the storage bucket.
        source_blob_name (str): The file name to upload.
        destination_file_name (str): The destination file name.
        verbose (bool): Whether or not to print status.
    """
    bucket = storage.bucket(name=bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    if verbose:
        print(
            "Blob {} downloaded to {}.".format(source_blob_name, destination_file_name)
        )


def download_files(bucket_name, bucket_folder, local_folder, verbose=True):
    """Download all files in a given Firebase Storage folder.
    
    Args:
        bucket_name (str): The name of the storage bucket.
        bucket_folder (str): A folder in the storage bucket.
        local_folder (str): The local folder to download files.
        verbose (bool): Whether or not to print status.
    """
    bucket = storage.bucket(name=bucket_name)
    file_list = list_files(bucket_name, bucket_folder)
    for file in file_list:
        blob = bucket.blob(file)
        file_name = blob.name.split("/")[-1]
        blob.download_to_filename(local_folder + '/' + file_name)
        if verbose:
            print(f"{file_name} downloaded from bucket.")


def upload_file(bucket_name, destination_blob_name, source_file_name, verbose=True):
    """Upload file to Firebase Storage.

    Args:
        bucket_name (str): The name of the storage bucket.
        destination_blob_name (str): The name to save the file as.
        source_file_name (str): The local file name.
        verbose (bool): Whether or not to print status.
    """
    bucket = storage.bucket(name=bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    if verbose:
        print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))


def upload_files(bucket_name, bucket_folder, local_folder, verbose=True):
    """Upload multiple files to Firebase Storage.
    
    Args:
        bucket_name (str): The name of the storage bucket.
        bucket_folder (str): A folder in the storage bucket to upload files.
        local_folder (str): The local folder of files to upload.
        verbose (bool): Whether or not to print status.
    """
    bucket = storage.bucket(name=bucket_name)
    files = [f for f in listdir(local_folder) if isfile(join(local_folder, f))]
    for file in files:
        local_file = join(local_folder, file)
        blob = bucket.blob(bucket_folder + '/' + file)
        blob.upload_from_filename(local_file)
    if verbose:
        print(f'Uploaded {len(files)} to "{bucket_folder}" bucket.')


def list_files(bucket_name, bucket_folder):
    """List all files in GCP bucket folder.
    
    Args:
        bucket_name (str): The name of the storage bucket.
        bucket_folder (str): A folder in the storage bucket to list files.
    """
    bucket = storage.bucket(name=bucket_name)
    files = bucket.list_blobs(prefix=bucket_folder)
    return [file.name for file in files if "." in file.name]


def delete_file(bucket_name, bucket_folder, file_name, verbose=True):
    """Delete file from GCP bucket.
    
    Args:
        bucket_name (str): The name of the storage bucket.
        bucket_folder (str): A folder in the storage bucket.
        file_name (str): The name of the file to delete.
        verbose (bool): Whether or not to print status.
    """
    bucket = storage.bucket(name=bucket_name)
    bucket.delete_blob(bucket_folder + '/' + file_name)
    if verbose:
        print(f"{file_name} deleted from bucket.")


def rename_file(bucket_name, bucket_folder, file_name, newfile_name, verbose=True):
    """Rename file in GCP bucket.
    
    Args:
        bucket_name (str): The name of the storage bucket.
        bucket_folder (str): A folder in the storage bucket.
        file_name (str): The name of the file to rename.
        newfile_name (str): The new name for the file.
        verbose (bool): Whether or not to print status.
    """
    bucket = storage.bucket(name=bucket_name)
    blob = bucket.blob(bucket_folder + '/' + file_name)
    bucket.rename_blob(blob, new_name=newfile_name)
    if verbose:
        print(f"{file_name} renamed to {newfile_name}.")


# ------------------------------------------------------------#
# Misc
# ------------------------------------------------------------#


def get_keywords(name):
    """Get keywords for a given string.

    Args:
        string (str): A string to get keywords for.
    """
    keywords = name.lower().split(" ")
    keywords = [x.strip() for x in keywords if x]
    keywords = list(set(keywords))
    return keywords


def snake_case(name):
    """Turn a given string to snake case.
    Args:
        string (str): The string to turn to snake case.
    """
    clean_name = name.replace(' ', '_')
    clean_name = clean_name.replace('&', 'and')
    clean_name = clean_name.replace('%', 'percent')
    clean_name = clean_name.replace('#', 'number')
    clean_name = clean_name.replace('$', 'dollars')
    clean_name = clean_name.replace('/', '_')
    clean_name = clean_name.replace(r'\\', '_')
    clean_name = sub("[!@#$%^&*()[]{};:,./<>?\|`~-=+]", " ", clean_name)
    words = findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', clean_name)
    return '_'.join(map(str.lower, words))

