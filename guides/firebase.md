## Cannlytics Firebase Module

Cannlytics utilizes Firebase for back-end services. Firebase is initialized with `cannlytics.firebase.initialize_firebase`, which returns a Firestore database instance. A generic example of using the `cannlytics` package is as follows.

```py
from cannlytics import firebase

# Set the path to your Firebase service account.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/path/to/your/service-account.json'

# Initialize Firebase
database = firebase.initialize_firebase()

# Get a document.
lab = firebase.get_document('organizations/cannlytics')
```

> You will need to provide credentials for your application by setting the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the file path of your [service account key](https://firebase.google.com/docs/admin/setup#initialize-sdk). This variable only applies to your current shell session, so if you open a new session, then you will need to set the variable again. If you are running your app in a Google environment, such as AppEngine, then `GOOGLE_APPLICATION_CREDENTIALS` is already set for you.

## Data

The Firestore functions utilize `create_reference` to turn a path into a document or collection reference, depending on the length of the path. Odd length paths refer to collections and even length paths refer to documents. For example, `users` is a collection of users, `users/{uid}` is a user's document, and `users/{uid}/logs` is a sub-collection of logs for the user. With this functionality, you can easily get documents as follows.

```py
# Get all user documents.
users = firebase.get_collection('users')

# Get a document.
user = firebase.get_document('users/xyz')
```

And create or update documents as follows.

```py
from datetime import datetime

# Create a user log.
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
firebase.update_document(f'users/xyz/logs/{timestamp}', {
  'activity': 'Something happened',
  'created_at': timestamp,
  'updated_at': timestamp
})

# Update the user.
firebase.update_document(f'users/xyz', {
  'recent_activity': timestamp,
})
```

If you need to work with arrays or simply increment a value, then there are utility functions for you.

```py
# Add an element to an array in a document.
firebase.add_to_array('tests/firebase_test', 'likes', 'Testing')
data = firebase.get_document('tests/firebase_test')

# Remove an element from an array in a document.
firebase.remove_from_array('tests/firebase_test', 'likes', 'Sandals')
data = firebase.get_document('tests/firebase_test')

# Increment a value in a document.
firebase.increment_value('tests/firebase_test', 'runs')
data = firebase.get_document('tests/firebase_test')
```

You query a collection of documents.

```py
# Get a collection.
limit = 1000
order_by = 'time'
filters = [{'key': 'test', 'operation': '==', 'value': 'firebase_test'}]
docs = firebase.get_collection('tests', limit=limit, order_by=order_by, filters=filters)
```

Finally, you can import and export data.

```py
# Import .csv data to Firestore.
ref = 'tests/test_collections/licensees'
data_file = './assets/data/licensees_partial.csv'
firebase.import_data(db, ref, data_file)

# Export data to .csv from Firestore.
output_csv_file = './assets/data/licensees_test.csv'
output_xlsx_file = './assets/data/licensees_test.xlsx'
firebase.export_data(db, ref, output_csv_file)
```

## File Storage

You can upload files to storage.

```py
# Upload a file to a Firebase Storage bucket.
firebase.upload_file(destination_blob_name, source_file_name, bucket_name)

# Upload all files in a folder to a Firebase Storage bucket.
firebase.upload_files(bucket_folder, local_folder, bucket_name)
```

You can then list files in a given bucket's folder.

```py
# List all files in the Firebase Storage bucket folder.
files = firebase.list_files(bucket_folder, bucket_name)
```

You can download files.

```py
# Download a file from Firebase Storage.
firebase.download_file(destination_blob_name, download_file_name, bucket_name)

# Download all files in a given Firebase Storage folder.
firebase.download_files(bucket_folder, download_folder, bucket_name)
```

Finally, you can rename and delete files if needed.

```py
# Rename a file in the Firebase Storage bucket.
firebase.rename_file(bucket_folder, file_name, newfile_name, bucket_name)

# Delete a file from the Firebase Storage bucket.
firebase.delete_file(bucket_folder, file_copy, bucket_name)
```

## Authentication

First, you can create a user.

```py
name = 'CannBot'
email = 'contact@cannlytics.com'
user, password = firebase.create_account(name, email, notification=True)
```

You can add custom claims for a user to control granular permissions.

```py
# Create and get custom claims.
claims = {'organizations': ['Cannlytics']}
firebase.create_custom_claims(user.uid, email=email, claims=claims)
custom_claims = firebase.get_custom_claims(email)
```

You can get a user token to authenticate in your client-side code.

```py
# Create custom token.
token = firebase.create_custom_token(user.uid, email=None, claims=custom_claims)
```

You can get a user or users.

```py
# Get user.
user = firebase.get_user(email)

# Get all users.
all_users = firebase.get_users()
```

You can update a user's `photo_url`, `display_name`, `email`, `phone_number`, `email_verified`, and `disabled` fields. Pass a dictionary with the desired key/value pairs that you wish to change.

```py
# Update user.
photo_url = f'https://robohash.org/{email}?set=set1'
user = firebase.update_user(user, {'photo_url': photo_url})
```

## Utilities

Below is a table of other included utility functions.

|  Function  |  Parameters  |  Description  |
|------------|--------------|---------------|
| `create_log`| `ref`, `claims`, `action`, `log_type`, `key`, `changes` | Create an activity log, where `ref (str)` is the path to a collection of logs; `claims (dict)` is a dict with user fields or a Firestore user object; `action (str)` is the activity that took place; `log_type (str)` is the log type; `key (str)` is a key to recognize the action; `changes (list)` is an optional list of changes that took place. |
| `get_keywords`| `name` | Create a list of keywords for a given string. |
| `snake_case`| `name` | Turn a given string to snake case. |
