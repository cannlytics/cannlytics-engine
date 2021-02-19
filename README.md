# Cannlytics Engine

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/VickiLanger/Queer-of-the-day-bot/fork)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<img align="center" height="75" alt="Cannlytics" src="https://cannlytics.com/static/cannlytics_website/images/logos/cannlytics_calyx_detailed.svg" style="float:left; margin-right:1.5rem; margin-bottom:1.5rem;">

Cannlytics provides a user-friendly interface to quickly receive samples, perform analyses, collect and review results, and publish certificates of analysis (CoAs). There are also built in logistics, CRM (client relationship management), inventory management, and invoicing tools. The Cannlytics engine comes with **batteries included**, but you are always welcome to supercharge your setup with modifications and custom components.


## Installation

You can install the Cannlytics engine from [PyPI](https://pypi.org/project/cannlytics/).

```shell
pip install cannlytics
```

## Database Usage

Cannlytics utilizes Firebase for back-end services. Firebase is initialized with `firebase.initialize_firebase`, which returns a Firestore database instance. A generic example of using the cannlytics package is as follows.

```py
from cannlytics import firebase

# TODO: Set the path to your Firebase service account.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""

# Initialize Firebase
database = firebase.initialize_firebase()

# Get a document.
lab = firebase.get_document("labs/cannlytics")
```

> You will need to provide credentials for your application by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable.
Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the file path of the JSON file that contains your [service account key](https://firebase.google.com/docs/admin/setup#initialize-sdk). This variable only applies to your current shell session, so if you open a new session, set the variable again.


### Firestore

The Firestore functions utilize `create_reference` to turn a path into a document or collection reference, depending on the length of the path. Odd length paths refer to collections and even length paths refer to documents. For example, `users` is a collection of users, `users/{uid}` is a user's document, and `users/{uid}/logs` is a sub-collection of logs for the user. With this functionality, you can easily get documents as follows.

```py
# Get all user documents.
users = firebase.get_collection("users")

# Get a document.
user = firebase.get_document("users/xyz")
```

And create or update documents as follows.

```py
from datetime import datetime

# Create a user log.
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
firebase.update_document(f"users/xyz/logs/{timestamp}", {
  "activity": "Something happened",
  "created_at": timestamp,
  "updated_at": timestamp
})

# Update the user.
firebase.update_document(f"users/xyz", {
  "recent_activity": timestamp,
})
```

<!-- Below is a table of all Firestore functions.

|  Function  |  Parameters  |  Description  |
|------------|--------------|---------------|
| `add_to_array`| `ref`, `field`, `value` | Add an element to a given field for a given reference. |
| `create_reference`| `database`, `ref` | Create either a collection or document reference. |
| `get_collection`| `ref`, `limit`, `order_by`, `desc`, `filters` | Get documents from a collection given a path reference. Optional parameters can `limit`, order with `order_by` and `desc`, and filter the documents. Filters are dictionaries of the form `{"key": "", "operator": "", "value": ""}`. Filters apply [Firebase queries](https://firebase.google.com/docs/firestore/query-data/queries) to the given `key` for the given `value`. Operators include: `==`, `>=`, `<=`, `>`, `<`, `!=`, `in`, `not_in`, `array_contains`, `array_contains_any`.  |
| `get_document`| `ref` | Get a given document given a path reference. |
| `increment_value`| `ref`, `field`, `amount` | Increment a given field for a given reference. The default `amount` is `1`. |
| `remove_from_array`| `ref`, `field`, `value` | Remove an element from a given field for a given reference. |
| `update_document`| `ref`, `values` | Update a given document with given values. | -->

<!-- ### Storage -->

<!-- Below is a table of all Firestore Storage functions.

|  Function  |  Parameters  |  Description  |
|------------|--------------|---------------|
| `download_file` | `bucket_name`, `source_blob_name`, `destination_file_name`, `verbose=True` | Downloads a file from Firebase Storage. |
| `download_files` | `bucket_name`, `bucket_folder`, `local_folder`, `verbose=True` | Download all files in a given Firebase Storage folder. |
| `upload_file` | `bucket_name`, `destination_blob_name`, `source_file_name`, `verbose=True` | Upload file to Firebase Storage. |
| `upload_files` | `bucket_name`, `bucket_folder`, `local_folder`, `verbose=True` | Upload multiple files to Firebase Storage. |
| `list_files` | `bucket_name`, `bucket_folder` | List all files in GCP bucket. |
| `delete_file` | `bucket_name`, `bucket_folder`, `file_name`, `verbose=True` | Delete file from GCP bucket. |
| `rename_file` | `bucket_name`, `bucket_folder`, `file_name`, `newfile_name`, `verbose=True` | Rename file in GCP bucket. | -->

<!-- ### Authentication -->

