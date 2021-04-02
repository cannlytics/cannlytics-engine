# -*- coding: utf-8 -*-
"""
cannlytics.traceability.leaf.utils
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains functions that are useful
when interfacing with the Leaf Data Systems API.
"""


def format_time_filter(start, stop, field):
    """Formats a time filter for a given endpoint type.
    Args:
        start (str): An ISO date string, e.g. 2020-04-20.
        stop (str): An ISO date string, e.g. 2021-04-20.
        field (str): The time field to filter by.
    """
    start_date = start.split('-')
    end_date = stop.split('-')
    y1, m1, d1 = start_date[0], start_date[1], start_date[2]
    y2, m2, d2 = end_date[0], end_date[1], end_date[2]
    return f'?f_{field}1={m1}%2F{d1}%2F{y1}&f_{field}2={m2}%2F{d2}%2F{y2}'


# Optional:
def import_csv(self, file_id, data):
    """Imports data from a .csv to the Leaf Data Systems API.

    :param str data: A CSV string of data.

    Example:

    .. code::

        # Read CSV file contents
        content = open('file_to_import.csv', 'r').read()
        gc.import_csv(spreadsheet.id, content)

    .. note::

        This method removes all other worksheets and then entirely
        replaces the contents of the first worksheet.

    """
    return NotImplementedError
    # headers = {'Content-Type': 'text/csv'}
    # url = '{0}/{1}'.format(DRIVE_FILES_UPLOAD_API_V2_URL, file_id)

    # self.request(
    #     'put',
    #     url,
    #     data=data,
    #     params={
    #         'uploadType': 'media',
    #         'convert': True,
    #         'supportsAllDrives': True,
    #     },
    #     headers=headers,
    # )

# Optional:
def export_csv(self, file_id, data):
    """Exports data to a .csv from the Leaf Data Systems API.

    :param str data: A CSV string of data.

    Example:

    .. code::

        # Read CSV file contents
        content = open('file_to_import.csv', 'r').read()
        gc.import_csv(spreadsheet.id, content)

    .. note::

        This method removes all other worksheets and then entirely
        replaces the contents of the first worksheet.

    """
    return NotImplementedError
    # headers = {'Content-Type': 'text/csv'}
    # url = '{0}/{1}'.format(DRIVE_FILES_UPLOAD_API_V2_URL, file_id)

    # self.request(
    #     'put',
    #     url,
    #     data=data,
    #     params={
    #         'uploadType': 'media',
    #         'convert': True,
    #         'supportsAllDrives': True,
    #     },
    #     headers=headers,
    # )


#------------------------------------------------------------------
# Constants
#------------------------------------------------------------------

# TODO: Add analyses by sample type
analyses = {}
