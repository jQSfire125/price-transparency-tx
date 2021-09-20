# import libraries
import os
import pandas as pd
import datetime as dt

# must match a reference ontology
# path in final version will be /opt/data/dim/
concept = pd.read_csv('../../../volumes/data/dim/CONCEPT.csv.gz',
                      header=0, sep='\t', low_memory=False)
concept = concept[['concept_code', 'concept_id']]
concept.drop_duplicates(inplace=True)
concept.rename(columns= {'concept_code': 'cpt'}, inplace=True)

# make a control file to iterate through
# path in final version will be /opt/data/raw/
path = '../../../volumes/data/raw/'
files = os.listdir(path)
csv_files = [x for x in files if x.endswith(".csv.gz")]
# removes '.csv.gz' (7 characters)
hospital_ids = [int(x[:-7]) for x in csv_files] 
control = pd.DataFrame({'file': csv_files, 'hospital_id': hospital_ids})

#cross reference the control file with the static dimension table
# path in final version will be /opt/dta/dim/
dim = pd.read_csv('../../../volumes/data/dim/hospital.csv',
                  usecols=['hospital_id', 'affiliation'])
control = control.merge(dim, how= 'left', on='hospital_id')
control.sort_values(by='hospital_id', inplace=True, ignore_index=True)

## loop PENDING

# print file you are working on now
# replace 0 with i in loop
print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + 
      ' - parsing hospital - ' + str(control.hospital_id[0]))

# read in the data
# replace 0 with i in loop
df = pd.read_csv('../../../volumes/data/raw/' + control.file[0], low_memory=False)

# hospital specific configuration
out = pd.DataFrame({
    'cpt': df['CPT/HCPCS Code'],
    'gross': df['Unit Price'],
    'cash': df['Cash Discount Price'],
    'max': df['Maximum Amount'],
    'min': df['Minimum Amount']
})
out.drop_duplicates(inplace=True)

# if out is not Null loop

# uniform
out.dropna(subset=['cpt'], inplace=True)
out = out[out.cpt != '']
out = out[out.cpt != '*']

# must match a reference code, usually CPT or HCPCS
out = out.merge(concept, on='cpt', sort=True)
out = out.drop('cpt', axis=1)

# melt from wide to long, and clean
long = pd.melt(out, id_vars='concept_id')
long['value'] = long['value'].str.strip()
long['value'] = long['value'].str.replace(',', '', regex=False)
# confirm that [$] is not a regex
long['value'] = long['value'].str.replace('[$]', '', regex=False)
long['value'] = long.value.astype(float)
long.dropna(subset=['value'], inplace=True)
long = long[long.value > 0]

# Add hospital id and order columns
# later change the 0 for i inside the loop
long['hospital_id'] = control.hospital_id[0]
long = long[long.columns[[3,0,1,2]]]

# write the data to a flatfile for postgres
# path will be later /opt/data/transformed/
# replace 0 with i inside the loop
if long.shape[0] > 0:
    out_path = '../../../volumes/data/transformed/' + str(control.hospital_id[0]) + '.csv'
    long.to_csv(out_path, header=False, index=None)

# clear variables from last iteration (inside the loop)
# del out
# del long

