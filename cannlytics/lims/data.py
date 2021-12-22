"""
Data Collection | Cannlytics
Copyright (c) 2021 Cannlytics and Cannlytics Contributors

Authors:
  Keegan Skeate <keegan@cannlytics.com>
  Charles Rice <charles@ufosoftwarellc.com>
Created: 6/15/2021
Updated: 12/21/2021
"""
# External imports.
import pandas as pd

# Internal imports.
from cannlytics.firebase import update_document


def clean_column_names(df, column):
    """
    Args:
        df (DataFrame): A DataFrame with any column names.
        column (str): The name of the column(s) to clean
    Returns:
        (DataFrame): A DataFrame with snake_case column names.
    """
    df[column] = df[column].str.strip()
    df[column] = df[column].str.rstrip('.)]')
    df[column] = df[column].str.replace('%', 'percent', regex=True)
    df[column] = df[column].str.replace('#', 'number', regex=True)
    df[column] = df[column].str.replace('[/,-]', '_', regex=True)
    df[column] = df[column].str.replace('[.,(,)]', '', regex=True)
    df[column] = df[column].str.replace("\'",'', regex=True)
    df[column] = df[column].str.replace("[[]", '_', regex=True)
    df[column] = df[column].str.replace(r"[]]", '', regex=True)
    df[column] = df[column].str.replace(' ', '_', regex=True)
    df[column] = df[column].str.replace('β', 'beta', regex=True)
    df[column] = df[column].str.replace('Δ', 'delta', regex=True)
    df[column] = df[column].str.replace('δ', 'delta', regex=True)
    df[column] = df[column].str.replace('α', 'alpha', regex=True)
    df[column] = df[column].str.replace('__', '', regex=True)
    df[column] = df[column].str.lower()
    return df


def import_data_model(directory):
    """Import analyses to Firestore from a .csv or .xlsx file.
    Args:
        directory (str): The full filename of a data file.
    """
    analyses = pd.read_excel(directory + 'analyses.xlsx')
    analytes = pd.read_excel(directory + 'analytes.xlsx')
    for index, analysis in analyses.iterrows():
        analyte_data = []
        analyte_names = analysis.analyte_keys.split(', ')
        for analyte_key in analyte_names:
            analyte_item = analytes.loc[analytes.key == analyte_key]
            analyte_data.append(analyte_item.to_dict(orient='records'))
        analyses.at[index, 'analytes'] = analyte_data 
    analyses_data = analyses.to_dict(orient='records')
    raise NotImplementedError
    # for index, values in analyses_data.iterrows():
    #     doc_id = str(values.key)
    #     doc_data = values.to_dict()
    #     ref = '' # FIXME:
    #     update_document(ref, doc_data)    


def import_measurements():
    """Import measurements taken by scientific instruments."""
    raise NotImplementedError


def get_sample_name(df, sheetname='Sheet1', var='samplename'):
    """Return the sample name from a dictionary.
    Converts the first column of the first sheet to lowercase.
    Args:
        df (DataFrame): A DataFrame.
        sheetname (str): The worksheet name, 'Sheet1' by default.
        var (str): The variable used as a sample ID, 'samplename' by default.
    Returns:
        (dict): The sample name as a key, value pair.
    """
    df[sheetname].ObjClass = df[sheetname].ObjClass.str.lower()
    samples = dict(df[sheetname][df[sheetname].ObjClass == var].values)
    return samples


def get_compound_dataframe(df, sheetname='Compound'):
    """ Rename the columns in the `Compound` sheet to match the required
    names. For simplicity, make a copy of the `Compound` sheet to
    handle NaN values.
    Args:
        df (DataFrame): A DataFrame.
        sheetname (str): The worksheet name, 'Compound' by default.
    Returns:
        (DataFrame): A DataFrame with renamed compounds.
    """
    columns = {
        'Name':'analyte',
        'Amount': 'measurement',
    }
    df[sheetname].rename(columns=columns, inplace=True)
    compounds = df[sheetname].copy()
    criterion = (compounds.analyte.isnull()) & (compounds.measurement > 0)
    compounds.loc[criterion, 'analyte'] = 'wildcard'
    compounds.dropna(subset=['analyte'], inplace=True)
    return compounds


def import_agilent_gc_residual_solvents(file_name):
    """Read in all the excel sheets at one time, get the sample name,
    get and cleanup the compound df from the compound sheet,
    add the analyte names and measurements to an array of dictionaries,
    and add that to the main array.
    Args:
        file_name (str): A data file path.
    Returns:
        (dict): A dictionary of sample results.
    """
    df = pd.read_excel(file_name, sheet_name = None)
    samples = get_sample_name(df)
    compounds = get_compound_dataframe(df)
    samples['metrics'] = compounds[['analyte', 'measurement']].to_dict('records')
    return samples


def import_agilent_gc_terpenes(file_name):
    """Read in all the excel sheets at one time, get the sample name,
    get and cleanup the compound df from the compound sheet,
    replace special characters, add the analyte names and measurements
    to an array of dictionaries, and add that to the main array.
    Args:
        file_name (str): A data file path.
    Returns:
        (list): A list of measurements (dict).
    """
    df = pd.read_excel(file_name, sheet_name = None)
    samples = get_sample_name(df)
    compounds = get_compound_dataframe(df)
    compounds = clean_column_names(compounds, 'analyte')
    samples['metrics'] = compounds[['analyte', 'measurement']].to_dict('records')
    return samples


def import_agilent_cannabinoids(file_name):
    """This is the same as residual solvents routine.
    Args:
        file_name (str): A data file path.
    Returns:
        (dict): A dictionary of sample results.
    """
    return import_agilent_gc_residual_solvents(file_name)


def import_heavy_metals(file_name):
    """
    Args:
        file_name (str): A data file path.
    Returns:
        (list): A list of measurements (dict).
    """

    # Read in the log sheet and summary sheets seperately to parsing easier.
    log_df = pd.read_excel(file_name, sheet_name = 'Log')
    summary_df = pd.read_excel(file_name, sheet_name = 'Quant Summary')

    # Drop the rows that do not contain sample ids.
    log_df.dropna(subset = ['Sample Mass (g)'], inplace = True)

    # Rename columns to make parsing clearer.
    columns = {'Analysis': 'analyte', '-': 'mass'}
    summary_df.rename(columns=columns, inplace=True)

    # Get list of samples.
    sample_ids = log_df['Sample ID'].tolist()

    # Parse measurements.
    samples = []
    measurements = {}
    for sample_id in sample_ids:
        sample = {}
        sample['sample_id'] = sample_id
        sample['sample_mass'] = log_df[log_df['Sample ID'] == sample_id]['Sample Mass (g)'].values[0]
        sample['sample_dilution'] = log_df[log_df['Sample ID'] == sample_id]['Sample Dilution'].values[0]

        analytes = []
        measurements['measurements'] = analytes
        index = summary_df.index[(summary_df['analyte'] == 'ID:') & (summary_df['mass'] == sample_id)].tolist()
        for offset in range(index[0] + 20, index[0] + 27):
            analyte = {}
            analyte['analyte'] = summary_df.iloc[offset].analyte
            analyte['measurement'] = summary_df.iloc[offset+9].mass
            analytes.append(analyte)

        samples.append(sample)
        samples.append(measurements)

    return samples
