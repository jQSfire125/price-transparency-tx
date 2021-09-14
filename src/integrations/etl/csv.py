# import libraries
import os
import pandas as pd

# must match a reference ontology
# path in final version will be /opt/data/dim/
concept = pd.read_csv('volumes/data/dim/CONCEPT.csv.gz', header=0, sep='\t', low_memory=False)
concept = concept[['concept_code', 'concept_id']]
concept.drop_duplicates(inplace=True)
concept.rename(columns= {'concept_code': 'cpt'}, inplace=True)

# make a control file to iterate through
# path in final version will be /opt/data/raw/
path = 'volumes/data/raw/'
files = os.listdir(path)
csv_files = [x for x in files if x.endswith(".csv.gz")]
# removes '.csv.gz' (7 characters)
hospital_ids = [int(x[:-7]) for x in csv_files] 
control = pd.DataFrame({'file': csv_files, 'hospital_id': hospital_ids})

#cross reference the control file with the static dimension table
# path in final version will be /opt/dta/dim/
dim = pd.read_csv('volumes/data/dim/hospital.csv', usecols=['hospital_id', 'affiliation'])
control = control.merge(dim, how= 'left', on='hospital_id')
control.sort_values(by='hospital_id', inplace=True, ignore_index=True)

## loop PENDING

# read in the data
df = pd.read_csv('volumes/data/raw/' + control.file[0], low_memory=False)

# hospital specific configuration
out = pd.DataFrame({
    'cpt': df['CPT/HCPCS Code'],
    'gross': df['Unit Price'],
    'cash': df['Cash Discount Price'],
    'max': df['Maximum Amount'],
    'min': df['Minimum Amount']
})
out.drop_duplicates(inplace=True)
