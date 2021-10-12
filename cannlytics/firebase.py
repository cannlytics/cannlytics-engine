"""
Firebase Module | Cannlytics

Authors: Keegan Skeate <contact@cannlytics.com>  
Created: 2/7/2021  
Updated: 7/30/2021  

Resources:

- https://firebase.google.com/docs/

Description:

A wrapper of firebase_admin to make interacting with the Firestore database
and Firebase Storage buckets even easier.

Example:

```py
import os
import environ

# Get and set all credentials.
env = environ.Env()
env.read_env('.env')
credentials = env('GOOGLE_APPLICATION_CREDENTIALS')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials
bucket_name = environ.get('FIREBASE_STORAGE_BUCKET')

# Initialize Firebase
db = initialize_firebase()
```
"""
try:
    # Standard imports
    from datetime import datetime, timedelta
    from os import listdir
    from os.path import isfile, join

    # External imports
    import requests
    import ulid
    from django.utils.crypto import get_random_string
    from firebase_admin import auth, firestore, initialize_app, storage
    from google.cloud import secretmanager
    try:
        from google.cloud.firestore import ArrayUnion, ArrayRemove, Increment
        from google.cloud.firestore_v1.collection import CollectionReference
        from google.cloud.firestore_v1.transforms import DELETE_FIELD
    except:
        pass
    try:
        from pandas import notnull, read_csv, read_excel, DataFrame, Series
    except:
        # FIXME: pandas has problems with Django on Cloud Run
        pass

    # Internal imports.
    from cannlytics.utils.utils import snake_case
except:
    pass # FIXME: Ignore import in Docs

# ------------------------------------------------------------#
# Firestore
# FIXME: Pass existing database reference to functions instead
# of creating a new `firestore.client()` each time.
# ------------------------------------------------------------#

def add_to_array(ref, field, value):
    """Add an element to a given field for a given reference.
    Args:
        ref (str): A document reference.
        field (str): A list field to create or update.
        value (dynamic): The value to be added to the list.
    """
    database = firestore.client()
    doc = create_reference(database, ref)
    doc.set({field: ArrayUnion([value])}, merge=True)


def create_document(ref, values):
    """Create a given document with given values, this leverages the
    same functionality as `update_document` thanks to `set` with `merge=True`.
    Args:
        ref (str): A document reference.
        values (str): A dictionary of values to update.
    """
    update_document(ref, values)


def create_reference(database, path):
    """Create a database reference for a given path.
    Args:
        database (Firestore Client): The Firestore Client.
        path (str): The path to the document or collection.
    Returns:
        (ref): Either a document or collection reference.
    """
    ref = database
    parts = path.split('/')
    for i in range(len(parts)):
        part = parts[i]
        if i % 2:
            ref = ref.document(part)
        else:
            ref = ref.collection(part)
    return ref


def delete_collection(ref, batch_size=420):
    """Delete a given collection, a batch at a time.
    Args:
        ref (str): A document reference.
        batch_size (int): The number of documents to delete at a time.
            The default is 420 and the maximum is 500.
    """
    database = firestore.client()
    col = create_reference(database, ref)
    docs = col.limit(batch_size).stream()
    deleted = 0
    for doc in docs:
        doc.reference.delete()
        deleted = deleted + 1
        if deleted >= batch_size:
            return delete_collection(col, batch_size)


def delete_document(ref):
    """Delete a given document.
    Args:
        ref (str): A document reference.
    """
    database = firestore.client()
    doc = create_reference(database, ref)
    doc.delete()


def delete_field(ref, field):
    """Delete a given field from a document.
    Args:
        ref (str): A document reference.
        field (str): The field to remove from the document.
    """
    database = firestore.client()
    doc = create_reference(database, ref)
    doc.set({field: DELETE_FIELD}, merge=True)


def remove_from_array(ref, field, value):
    """Remove an element from a given field for a given reference.
    Args:
        ref (str): A document reference.
        field (str): A list field to update.
        value (dynamic): The value to be removed from the list.
    """
    database = firestore.client()
    doc = create_reference(database, ref)
    doc.set({field: ArrayRemove([value])}, merge=True)


def increment_value(ref, field, amount=1):
    """Increment a given field for a given reference.
    Args:
        ref (str): A document reference.
        field (str): A numeric field to create or update.
        amount (int): The amount to increment, default 1.
    """
    database = firestore.client()
    doc = create_reference(database, ref)
    doc.set({field: Increment(amount)}, merge=True)


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


def update_document(ref, values):
    """Update a given document with given values.
    Args:
        ref (str): A document reference.
        values (str): A dictionary of values to update.
    """
    database = firestore.client()
    doc = create_reference(database, ref)
    doc.set(values, merge=True)


def update_documents(refs, data):
    """Batch update documents, up to 420 at a time (to give the 500
    limit set by Firebase a cushion).
    Args:
        refs (list): A list of document paths (str).
        data (list): A list of document data (dict).
    """
    n = 420
    database = firestore.client()
    ref_shards = [refs[i:i+n] for i in range(0, len(refs), n)]
    data_shards = [data[i:i+n] for i in range(0, len(data), n)]
    for s in range(len(ref_shards)):
        ref_shard = ref_shards[s]
        data_shard = data_shards[s]
        batch = database.batch()
        for i in range(len(ref_shard)):
            ref = ref_shard[i]
            values = data_shard[i]
            doc = create_reference(database, ref)
            batch.set(doc, values, merge=True)
        batch.commit()


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
        values = data.to_dict()
        if values is None:
            return {}
        return {**{'id': data.id}, **values}


def get_collection(ref, limit=None, order_by=None, desc=False, filters=[]):
    """Get documents from a collection.
    Args:
        ref (str): A document reference.
        limit (int): The maximum number of documents to return. The default is no limit.
        order_by (str): A field to order the documents by, with the default being none.
        desc (bool): The direction to order the documents by the order_by field.
        filters (list): Filters are dictionaries of the form
            `{'key': '', 'operation': '', 'value': ''}`.
            Filters apply [Firebase queries](https://firebase.google.com/docs/firestore/query-data/queries)
            to the given `key` for the given `value`.
            Operators include: `==`, `>=`, `<=`, `>`, `<`, `!=`,
            `in`, `not_in`, `array_contains`, `array_contains_any`.
    Returns:
        (list): A list of documents.
    """
    docs = []
    database = firestore.client()
    collection = create_reference(database, ref)
    if filters:
        for filter in filters:
            collection = collection.where(
                filter['key'], filter['operation'], filter['value']
            )
    if order_by and desc:
        collection = collection.order_by(order_by, direction='DESCENDING')
    elif order_by:
        collection = collection.order_by(order_by)
    if limit:
        collection = collection.limit(limit)
    query = collection.stream()  # Only handles streams less than 2 mins.
    for doc in query:
        data = doc.to_dict()
        docs.append({**{'id': doc.id}, **data})
    return docs


def import_data(db, ref, data_file):
    """Import data into Firestore.
    Args:
        db (Firestore Client):
        ref (str): A collection or document reference.
        data_file (str): The path to the local data file to upload.
    !!! info "Wishlist"
        It would be desirable for the following functionality to be implemented:
        - Batch upload
        - Handle types <https://hackersandslackers.com/importing-excel-dates-times-into-pandas/>
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
            data = read_csv(data_file, sep=' ', header=None)
        except:
            try:
                data = read_csv(
                    data_file,
                    header=0,
                    skip_blank_lines=True, 
                    encoding='utf-16',
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
        doc_data = data.to_dict(orient='index')
        data_ref.set(doc_data, merge=True)


def export_data(db, ref, data_file):
    """Export data from Firestore.    
    Args:
        db (Firestore Client):
        ref (str): A collection or document reference.
        data_file (str): The path to the local data file to upload.
    !!! info "Wishlist"
        Parse fields that are objects into fields, similar to below.
        ```py
        from pandas.io.json import json_normalize
        artist_and_track = json_normalize(
            data=tracks_response['tracks'],
            record_path='artists',
            meta=['id'],
            record_prefix='sp_artist_',
            meta_prefix='sp_track_',
            sep='_'
        )
        ```
    """
    data_ref = create_reference(db, ref)
    if isinstance(data_ref, CollectionReference):
        data = []
        docs = data_ref.stream()
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['id'] = doc.id
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


def create_id():
    """Generate a universal ID.
    Returns:
        (str): A unique, lexicographic ID, a ULID.
    """
    return ulid.new().str.lower()


def create_id_from_datetime(dt):
    """Create an ID from an existing datetime.
    Args:
        dt (datetime): The time to timestamp the ID.
    Returns:
        (str): A unique lexicographic ID.
    """
    return ulid.from_timestamp(dt)


def get_id_timestamp(uid):
    """Get the datetime that an ID was created.
    Args:
        uid (str): A unique ID string.
    Returns:
        (datetime): The date when a unique lexicographic ID was generated.
    """
    return ulid.from_str(uid).timestamp().datetime


# ------------------------------------------------------------#
# Authentication
# ------------------------------------------------------------#

def create_user(name, email):
    """
    Given user name and email, create an account.
    If the email is already being used, then nothing is returned.
    Args:
        name (str): A name for the user.
        email (str): The user's email.
    Returns:
        (tuple): User object, random password
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$-_'
    password = get_random_string(42, chars)
    photo_url = f'https://robohash.org/{email}?set=set5'
    try:
        user = auth.create_user(
            uid=create_id(),
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


def update_custom_claims(uid, email=None, claims=None):
    """Update custom claims for a user.
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
    existing_claims = get_custom_claims(uid)
    if not existing_claims:
        existing_claims = {}
    # if existing_claims:
    #     existing_owner = existing_claims.get('owner', [])
    # else:
    #     existing_claims = {}
    #     existing_owner = []
    # current_owner = claims.get('owner', [])
    # FIXME: For now, only 1 organization per user.
    # claims['owner'] = list(set(existing_owner + current_owner))
    auth.set_custom_user_claims(uid, {**existing_claims, **claims})


def get_custom_claims(name):
    """Get custom claims for a user.
    Args:
        name (str): A user ID or user email.
    """
    user = get_user(name)
    return user.custom_claims


def create_custom_token(uid='', email=None, claims=None):
    """Create a custom token for a given user, expires after one hour.
    Args:
        uid (str): A user's ID.
        email (str): A user's email.
        claims (dict):  A dictionary of the user's claims.
    Returns:
        (dict): A dictionary of custom claims.
    """
    if email:
        user = auth.get_user_by_email(email)
        uid = user.uid
    return auth.create_custom_token(uid, claims)


def create_session_cookie(id_token, expires_in=None):
    """Create a session cookie.
    Args:
        id_token (str): A user ID token passed from the client.
        expires_in (timedelta): The time until the session will expire.
    Returns:
        (bytes): A session cookie in bytes.
    """
    if expires_in is None:
        expires_in = timedelta(days=7)
    return auth.create_session_cookie(id_token, expires_in=expires_in)


def revoke_refresh_tokens(token):
    """Revoke a user's refresh token.
    Args:
        token (str): The refresh token to authenticate a user.
    """
    return auth.revoke_refresh_tokens(token)


def verify_token(token):
    """Verify a user's custom token.
    Args:
        token (str): The custom token to authenticate a user.
    Returns:
        (dict): A dictionary of key-value pairs parsed from the decoded JWT.
    """
    return auth.verify_id_token(token)


def verify_session_cookie(session_cookie, check_revoked=True, app=None): # FIXME: Don't hardcode
    """Verify a user's session cookie.
    Args:
        session_cookie (str): A session cookie to authenticate a user.
    Returns:
        (dict): A dictionary of key-value pairs parsed from the decoded JWT.
    """
    return auth.verify_session_cookie(
        session_cookie,
        check_revoked=check_revoked,
        app=app,
    )


def get_user(name):
    """Get a user by user ID or by email.
    Args:
        name (str): A user ID, email, or phone number.
    Returns:
        (UserRecord): A Firebase user object.
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
        'email',
        'phone_number',
        'email_verified',
        'display_name',
        'photo_url',
        'disabled',
    ]
    for field in fields:
        new_value = data.get(field)
        if new_value:
            values[field] = new_value
        else:
            values[field] = getattr(existing_user, field)
    return auth.update_user(
        existing_user.uid,
        email=values['email'],
        phone_number=values['phone_number'],
        email_verified=values['email_verified'],
        display_name=values['display_name'],
        photo_url=values['photo_url'],
        disabled=values['disabled'],
    )


def delete_user(uid):
    """Delete a user from Firebase.
    Args:
        uid (str): A user's ID.
    """
    auth.delete_user(uid)


# Optional: Implement custom password-reset email.
# def send_password_reset(email):
#     """Send a password reset to a user given an email."""
#     link = auth.generate_password_reset_link(email)
#     send_custom_email(email, link)


# ------------------------------------------------------------#
# Secret Management
# 'Secret Manager Admin' permissions needed for service account.
# https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets
# ------------------------------------------------------------#

def create_secret(project_id, secret_id, secret):
    """Create a new secret with the given name. A secret is a logical wrapper
    around a collection of secret versions. Secret versions hold the actual
    secret material.
    Args:
        project_id (str): The project associated with the secret.
        secret_id (str): An ID for the secret.
        secret (str): The secret data.
    """
    client = secretmanager.SecretManagerServiceClient()
    parent = f'projects/{project_id}'
    response = client.create_secret(parent, secret_id, {"replication": {"automatic": {}}})
    return response.name


def add_secret_version(project_id, secret_id, payload):
    """
    Add a new secret version to the given secret with the provided payload.
    A secret version contains the actual contents of a secret.
    A secret version can be enabled, disabled, or destroyed.
    To change the contents of a secret, you create a new version.
    Adding a secret version requires the Secret Manager Admin role
    (roles/secretmanager.admin) on the secret, project, folder, or organization.
    Roles can't be granted on a secret version.
    Args:
        project_id (str): A Firestore project ID.
        secret_id (str): An ID for the secret.
        payload (str): The secret.
    Returns:
        (str): The secret version's name.
    """
    client = secretmanager.SecretManagerServiceClient()
    parent = f'projects/{project_id}/secrets/{secret_id}'
    payload = payload.encode('UTF-8')
    response = client.add_secret_version(parent, {'data': payload})
    return response.name


def access_secret_version(project_id, secret_id, version_id):
    """
    Access the payload for a given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    !!! Warning
        Do not print the secret in a production environment.
    Args:
        project_id (str): A Firestore project ID.
        secret_id (str): An ID for the secret.
        version_id (str): A version for the secret.
    Returns:
        (str): The secret version's name.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f'projects/{project_id}/secrets/{secret_id}/versions/{version_id}'
    response = client.access_secret_version(name)
    return response.payload.data.decode('UTF-8')


# ------------------------------------------------------------#
# Storage
# FIXME: Allow user to not have to pass bucket_name.
# ------------------------------------------------------------#

def create_short_url(api_key, long_url, project_name='cannlytics'):
    """Create a short URL to a specified file.
    Args:
        api_key (str): An API key for Firebase dynamic links.
        long_url (str): A URL to create a short, dynamic link.
        project_name (str): The name of the Firebase project, `cannlytics` by default.
    Returns:
        (str): A short link to the given URL.
    """
    try:
        url = f'https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key={api_key}'
        data= {
            'dynamicLinkInfo': {
                'domainUriPrefix': f'https://{project_name}.page.link',
                'link': long_url,
            },
            'suffix': {'option': 'UNGUESSABLE'}
        }
        response = requests.post(url, json=data)
        return response.json()['shortLink']
    except ConnectionError:
        raise ConnectionError # Optional: Handle connection errors more elegantly?


def download_file(bucket_name, source_blob_name, destination_file_name, verbose=False):
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
            'Blob {} downloaded to {}.'.format(source_blob_name, destination_file_name)
        )


def download_files(bucket_name, bucket_folder, local_folder, verbose=False):
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
        file_name = blob.name.split('/')[-1]
        blob.download_to_filename(local_folder + '/' + file_name)
        if verbose:
            print(f'{file_name} downloaded from bucket.')


def get_file_url(ref, bucket_name=None, expiration=None):
    """Return the storage URL of a given file reference.
    Args:
        ref (str): The storage location of the file.
        bucket_name (str): The name of the storage bucket.
        expiration (datetime): The date for when the file link should expire.
    Returns:
        (str): The storage URL of the file.
    """
    if expiration is None:
        expiration = datetime.now() + timedelta(days=100 * 365)
    bucket = storage.bucket(name=bucket_name)
    blob = bucket.blob(ref)
    return blob.generate_signed_url(expiration)


def upload_file(
    bucket_name,
    destination_blob_name,
    source_file_name=None,
    data_url=None,
    content_type='image/jpg'
):
    """Upload file to Firebase Storage.
    Args:
        bucket_name (str): The name of the storage bucket.
        destination_blob_name (str): The name to save the file as.
        source_file_name (str): The local file name.
        data_url (str): The data URL to upload from a string.
        content_type (str): The content type of the file, when uploading from a string.
    """
    bucket = storage.bucket(name=bucket_name)
    blob = bucket.blob(destination_blob_name)
    if source_file_name:
        blob.upload_from_filename(source_file_name)
    else:
        blob.upload_from_string(data_url, content_type=content_type)

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
    Returns:
        (list): A list of file names in the given bucket.
    """
    bucket = storage.bucket(name=bucket_name)
    files = bucket.list_blobs(prefix=bucket_folder)
    return [file.name for file in files if '.' in file.name]


def delete_file(bucket_name, blob_name):
    """Delete file from GCP bucket.
    Args:
        bucket_name (str): The name of the storage bucket.
        blob_name (str): The name of the file to delete.
    """
    bucket = storage.bucket(name=bucket_name)
    bucket.delete_blob(blob_name)


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
        print(f'{file_name} renamed to {newfile_name}.')


# ------------------------------------------------------------#
# Misc
# ------------------------------------------------------------#

def create_log(ref, claims, action, log_type, key, changes=None):
    """Create an activity log.
    Args:
        ref (str): Path to a collection of logs.
        claims (dict): A dict with user fields or a Firestore user object.
        action (str): The activity that took place.
        log_type (str): The log type.
        key (str): A key to recognize the action.
        changes (list): An optional list of changes that took place.
    """
    now = datetime.now()
    timestamp = datetime.now().isoformat()
    log_id = now.strftime('%Y-%m-%d_%H-%M-%S')
    log_entry = {
        'action': action,
        'type': log_type,
        'key': key,
        'created_at': timestamp,
        'log_id': log_id,
        'user': claims.get('uid'),
        'user_name': claims.get('display_name'),
        'user_email': claims.get('email'),
        'user_photo_url': claims.get('photo_url'),
        'changes': changes,
    }
    update_document(f'{ref}/{log_id}', log_entry)
