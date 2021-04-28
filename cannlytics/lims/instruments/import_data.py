"""
Import Instrument Data | Cannlytics
"""



# helper function to move columns in a dataframe
def movecol(df, cols_to_move=[], ref_col='', place='After'):
    
    cols = df.columns.tolist()
    if place == 'After':
        seg1 = cols[:list(cols).index(ref_col) + 1]
        seg2 = cols_to_move
    if place == 'Before':
        seg1 = cols[:list(cols).index(ref_col)]
        seg2 = cols_to_move + [ref_col]
    
    seg1 = [i for i in seg1 if i not in seg2]
    seg3 = [i for i in cols if i not in seg1 + seg2]
    
    return(df[seg1 + seg2 + seg3].copy())

# helper function to cleanup column names
# this should be revisited to make a cleaner more general solution
def clean_col_names(df):
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.rstrip('.)]')
    df.columns = df.columns.str.replace('%',  'percent', regex=True)
    df.columns = df.columns.str.replace('#',  'number', regex=True)
    df.columns = df.columns.str.replace('[/,-]',  '_', regex=True)
    df.columns = df.columns.str.replace('[.,(,)]',  '', regex=True)
    df.columns = df.columns.str.replace(r"\'",'', regex=True)
    df.columns = df.columns.str.replace(r"[[]",  '_', regex=True)
    df.columns = df.columns.str.replace(r"[]]",  '', regex=True)
    df.columns = df.columns.str.replace(' ',  '_', regex=True)

    return df

def import_nexera(file_name):

    import pandas as pd

    # read in the data and the header data
    df = pd.read_csv(file_name, sep='\t', header=2)
    header_df = pd.read_csv(file_name, sep='\t', nrows=2, header=None)

    # drop the rows that are not needed, they are NAN in the Unnamed: 0 column
    df.dropna(subset = ['Unnamed: 0'], inplace = True)
    df.reset_index(inplace=True, drop=True)

    # get a list of indexes for the ID#s this will not include the first ID# because it is part of the header
    # and is not read in with the rest of the data hence the need for the header_df
    id_index = df.index[df['Unnamed: 0'] == 'ID#'].tolist()

    # create a dataframe with the ID#s by retrieving them from the dataframe by index
    ids_df = df.loc[id_index, ['Data Filename']]

    # rename the column name to reflect what it represents
    ids_df.rename(columns={'Data Filename': 'ID#'}, inplace=True)

    # get the first id, add it to index 0 and sort the indexes
    first_id = header_df.loc[0, 1]
    ids_df.loc[0] = first_id
    ids_df.sort_index(inplace=True)

    # do the same thing for the compounds using the fact that the compound's index is one more than the id#'s
    compound_index = [i + 1 for i in id_index]
    compound_df = df.loc[compound_index, ['Data Filename']]

    # set the compound's temp index to the same value as the id#'s
    compound_df['id_index'] = id_index

    # get the first compound from the header dataframe and add it to temp index 0
    first_compound = header_df.loc[1, 1]
    compound_df.loc[0] = [first_compound, 0]

    # set the dataframe's index to the temp index and delete the column name
    compound_df.set_index('id_index', inplace=True)
    compound_df.sort_index(inplace=True)
    compound_df.index.name = None

    # renmane the column names to something meaningful
    compound_df.rename(columns={'Data Filename' : 'Compound'}, inplace = True)

    # combine the two dataframes
    id_compound_df = pd.concat([ids_df, compound_df], axis=1)

    # repeat the values so that the values match the rows in the main dataframe
    # I feel like there is a better way to do this so it should be revisited at some point

    # the first rows are a special case because of the header
    for k in range(1, id_index[0]):
        id_compound_df.loc[k] = id_compound_df.loc[0, ['ID#', 'Compound']]

    # do the same thing for the remaining rows that all follow the same pattern
    num_entries = id_index[2]-id_index[1]
    for i in id_index:
        for j in range(1,num_entries):
            id_compound_df.loc[i+j] = id_compound_df.loc[i, ['ID#', 'Compound']]

    # sort the indexes so that they match the main dataframe
    id_compound_df.sort_index(inplace=True)

    # combine the dataframes
    combined_df = pd.concat([df, id_compound_df], axis=1)

    # move the added columns to the begining of the dataframe
    combined_df = movecol(combined_df, cols_to_move = ['ID#', 'Compound'], ref_col = "Data Filename", place = 'Before')

    # now that the ID# and Compound are in columns drop the rows that contained them
    combined_df.drop(combined_df.index[combined_df['Unnamed: 0'] == 'ID#'], inplace = True)
    combined_df.drop(combined_df.index[combined_df['Unnamed: 0'] == 'Name'], inplace = True)
    combined_df.reset_index(inplace=True, drop=True)

    # drop the Unnamed: 0 column
    combined_df.drop('Unnamed: 0', axis = 1, inplace = True)

    #clean the column names
    combined_df = clean_col_names(combined_df)
 
    return combined_df

