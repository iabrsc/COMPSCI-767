import pandas as pd
from fuzzywuzzy import fuzz
import chardet


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def default_transform(val):
    return val



file_path_a = "C:\\Users\\kiing\\scripts\\AmazonTableCut.csv"
file_path_b = "C:\\Users\\kiing\\scripts\\NeweggTableCut.csv"

table_a = pd.read_csv(file_path_a, encoding=detect_encoding(file_path_a))
table_b = pd.read_csv(file_path_b, encoding=detect_encoding(file_path_b))

#creates mapping between columns in tables
column_mapping = {
    'Name': 'Name',        #e.g.'name' in amazon table could correspond to 'full_name' in newegg table (but it doesn't, format is 'Amazon.attr': 'Newegg.attr')
    'Display Size': 'Screen Size (inches)',
   
    'Screen Resolution': 'Resolution',
    'RAM (GB)': 'Memory',
    'GPU': 'GPU',
    'Brand': 'Brand',
    'Operating System': 'Operating System',
   # 'Storage': 'SSD',
    'Series': 'Series',
    
}

#define transformation functions to standardize values before comparison.
#if values in similar columns are represented differently across tables, use these functions to make them comparable.

def transform_name(val):
    if isinstance(val, str):
        return val.lower().strip()
    return str(val)  # Convert non-string values to string

def transform_general(val):
    return str(val).lower().strip()



#map columns to their respective transformation functions.
#this ensures each column gets the correct treatment before comparison.
#transform_general is a placeholder, works to return all values to lower though, in order to get rid of case sensitivity
transformations = {
    'Name': transform_name,
    'Display Size': transform_general,
   
    'Screen Resolution': transform_general,
    'RAM': transform_general,
    'GPU': transform_general,
    'Brand': transform_general,
    'Operating System': transform_general,
   # 'Storage': transform_general,
    'Series': transform_general,

}

#initialize an empty dictionary to build Table C.
table_c = {
    "ID": [],
    "Amazon_Item_ID": [],
    "Newegg_Item_ID": [],
    # Add more columns as needed...
}

#counter to provide unique IDs for entries in Table C
counter = 0

#start the matching logic
for index_a, row_a in table_a.iterrows():          #loop through each row in table_a
    for index_b, row_b in table_b.iterrows():      #for each row in table_a, loop through each row in table_b
        
        is_match = True  #initially, assume a pair of rows match
        
        #check each mapped column pair for similarity
        for col_a, col_b in column_mapping.items():
    
            #apply transformations to the values to standardize them before comparison
            transformed_val_a = transformations.get(col_a, default_transform)(row_a[col_a])
            transformed_val_b = transformations.get(col_b, default_transform)(row_b[col_b])
            
            #if either value is blank, skip the comparison for this column
            if not transformed_val_a or not transformed_val_b:
                continue

            #check similarity using fuzzy string comparison
            if isinstance(transformed_val_a, str) and isinstance(transformed_val_b, str):
                if fuzz.ratio(transformed_val_a, transformed_val_b) < 60:
                    is_match = False
                    break
        
        #if after checking all columns the rows are still considered a match, add them to Table C
        if is_match:
            table_c["ID"].append(counter)
            table_c["Amazon_Item_ID"].append(row_a["ID"])
            table_c["Newegg_Item_ID"].append(row_b["ID"])
           
            counter += 1

#convert the dictionary into a DataFrame for easier manipulation and exporting
table_c_df = pd.DataFrame(table_c)

#export the resulting Table C to a CSV file
table_c_df.to_csv("table_c2.csv", index=False)