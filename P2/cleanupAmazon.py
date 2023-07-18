import pandas as pd
import numpy as np
from collections import Counter

def split_info(row):
    #possible attributes (just found looking in 'Product Info' I extracted, like some other attributes but these ones are the most consistent)
    attributes = ['Display Size', 'Disk Size', 'RAM', 'Operating System']

    #if row is not a string, return NaNs
    if not isinstance(row, str):
        return pd.Series([np.nan] * len(attributes), index=attributes)

    info_dict = {attr: np.nan for attr in attributes}
    segments = row.split('|')
    for i in range(0, len(segments), 3):
        if segments[i] in info_dict:  #ensures only defined attributes are populated
            value = segments[i+2].split(' ')
            if segments[i] == 'Operating System':
                info_dict[segments[i]] = ' '.join(value)
            elif segments[i] == 'Disk Size' and len(value) > 1 and value[1] == 'TB':  #convert TB to GB for consistency
                info_dict[segments[i]] = float(value[0]) * 1000
            else:
                try:
                    info_dict[segments[i]] = float(value[0])
                except ValueError:
                    info_dict[segments[i]] = np.nan
    return pd.Series(info_dict)

#load data in
fA = pd.read_csv('C:\\Users\\kiing\\scripts\\tableAmazon.csv')

#apply function
info_df = fA['Product Information'].apply(split_info)

#merge new data into original DataFrame
fA = pd.concat([fA, info_df], axis=1)

#replace '-' with an empty string
fA = fA.replace('-', '')

#save units for columns
units = {
    'Display Size': 'inches',
    'RAM': 'GB',
    'Disk Size': 'GB'
}

#rename the columns
fA.rename(columns={k: f"{k} ({v})" for k, v in units.items() if k in fA.columns and k != 'Operating System'}, inplace=True)

#drops product information, since everything should be organized outside of it
fA = fA.drop(columns=['Product Information'])

#clean up the 'Rating' column, from 'X.X out of 5' to just 'X.X', I'll edit the column title manually then
fA['Rating'] = fA['Rating'].str.split(' ', expand=True)[0]
fA['Rating'] = fA['Rating'].astype(float)

#clean up the 'Number of Ratings' column, as there seem to be misplaced non-numerics (likely chose a poor tag or something, might be skewing the data here)
fA['Number of Ratings'] = pd.to_numeric(fA['Number of Ratings'], errors='coerce')
fA['Number of Ratings'] = fA['Number of Ratings'].fillna('')

#output to file
fA.to_csv('C:\\Users\\kiing\\scripts\\tableAmazon.csv', index=False)