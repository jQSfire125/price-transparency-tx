# import libraries
import os
import pandas as pd
import numpy as np
import datetime as dt

# must match a reference ontology
concept = pd.read_csv('/opt/data/dim/CONCEPT.csv.gz',
                      header=0, sep='\t', low_memory=False)
concept = concept[['concept_code', 'concept_id']]
concept.drop_duplicates(inplace=True)
concept.rename(columns= {'concept_code': 'cpt'}, inplace=True)

# make a control file to iterate through
path = '/opt/data/raw/'
files = os.listdir(path)
csv_files = [x for x in files if x.endswith(".csv.gz")]
# removes '.csv.gz' (7 characters)
hospital_ids = [int(x[:-7]) for x in csv_files] 
control = pd.DataFrame({'file': csv_files, 'hospital_id': hospital_ids})

#cross reference the control file with the static dimension table
dim = pd.read_csv('/opt/data/dim/hospital.csv',
                  usecols=['hospital_id', 'affiliation'])
control = control.merge(dim, how= 'left', on='hospital_id')
control.sort_values(by='hospital_id', inplace=True, ignore_index=True)

# HCA is a group of hospitals
HCA = [39, 55, 58, 65] + list(range(45,53)) + list(range(67,72))

for i in range(control.shape[0]):    
    out = None
    
    # print file you are working on now
    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + 
          ' - parsing hospital - ' + str(control.hospital_id[i]))
    
    # hospital specific configuration
    if control.hospital_id[i] in [16]:
        # read in the file
        df = pd.read_csv('/opt/data/raw/' + control.file[i], 
                         low_memory=False, header=3)
        out = pd.DataFrame({
            'cpt': df['CPT Code'],
            'gross': df[' Charge '],
            'cash': df[' Self Pay Median Charge '],
            'max': df[' Maximum Reimbursement '],
            'min': df[' Minimum Reimbursement ']
            })
        out.drop_duplicates(inplace=True)
    
    elif control.hospital_id[i] in [17, 18, 19]:
        # read in the file
        df = pd.read_csv('/opt/data/raw/' + control.file[i], 
                         low_memory=False, header=4,
                         encoding_errors='ignore')
        out = pd.DataFrame({
            'cpt': df['CPT / HCPCS Code'],
            'gross': df['Gross Charge'],
            'cash': df['Discounted Cash Price'],
            'max': df['De-Identified Maximum Reimbursement'],
            'min': df['De-Identified Minimum Reimbursement']
            })
        out.drop_duplicates(inplace=True)
    
    elif control.hospital_id[i] in [21]:
        # read in the file
        df = pd.read_csv('/opt/data/raw/' + control.file[i], 
                         low_memory=False)
        out = pd.DataFrame({
            'cpt': df['CPT'],
            'gross': df['GROSS CHARGE'],
            'cash': df['DISCOUNTED CASH PRICE INPATIENT '],
            'max': df['DE-IDENTIFIED MAX'],
            'min': df['DE-IDENTIFIED MIN']
            })
        out.drop_duplicates(inplace=True)
    
    elif control.hospital_id[i] in [29]:
        # read in the file
        df = pd.read_csv('/opt/data/raw/' + control.file[i], 
                         low_memory=False)
        out = pd.DataFrame({
            'cpt': df['CPTHCPCSCodes'],
            'gross': df['GrossCharge'],
            'cash': df['DiscountedCashRate'],
            'max': df['MaximumNegotiatedCharge'],
            'min': df['MinimumNegotiatedCharge']
            })
        out.drop_duplicates(inplace=True)
        out.dropna(subset=['cpt'], inplace=True)
        out['cpt'] = out.cpt.astype(int).astype(str)    
        
    elif control.hospital_id[i] in [34, 35, 36]:
        # read in the file
        df = pd.read_csv('/opt/data/raw/' + control.file[i], 
                         low_memory=False, header=4, 
                         encoding_errors='ignore')
        out = pd.DataFrame({
            'cpt': df['BILLING_REVENUE_SERVICE_CODE'],
            'gross': df['GROSS_CHARGE'],
            'cash': df['DISCOUNTED_CASH_PRICE'],
            'max': df['DEIDENTIFIED_MAX_NEGOTIATED_CHARGE'],
            'min': df['DEIDENTIFIED_MIN_NEGOTIATED_CHARGE']
            })
        out.drop_duplicates(inplace=True)
        
    elif control.hospital_id[i] in [38]:
        # read in the file
        df = pd.read_csv('/opt/data/raw/' + control.file[i], 
                         low_memory=False, header=1)
        out = pd.DataFrame({
            'cpt': df['CPT Code'],
            'gross': df['Billed Charge'],
            'cash': df['Self Pay'],
            'max': df['Maximum Negotiated Charge'],
            'min': df['Minimum Negotiated Charge']
            })
        out.drop_duplicates(inplace=True)
        
    elif control.hospital_id[i] in HCA:
        # read in the file
        df = pd.read_csv('/opt/data/raw/' + control.file[i], 
                         low_memory=False, header=1)
        out = pd.DataFrame({
            'cpt': df['HCPCS/CPT Code'],
            'gross': df['Gross Charge'],
            'cash': df['Discounted Cash Price (Gross Charges)']
            })
        out.drop_duplicates(inplace=True)
        out['cpt'] = out['cpt'].str.upper().replace('^0', '', regex=True)
        out['cpt'] = out['cpt'].str.strip()
        out['cash'] = out['cash'].astype(str)
        
    elif control.hospital_id[i] in [43]:
        # read in the file
        df = pd.read_csv('/opt/data/raw/' + control.file[i], 
                         low_memory=False)
        out = pd.DataFrame({
            'cpt': df['CPT 1'],
            'gross': df['Gross Charges'],
            'cash': df['Negotiated Charges'],
            'max': df['Max Negotiated Charges for All Payers'],
            'min': df['Min Negotiated Charges for All Payers']
            })
        out.drop_duplicates(inplace=True)
        
    elif control.hospital_id[i] in [66]:
        # read in the file
        df = pd.read_csv('/opt/data/raw/' + control.file[i], 
                         low_memory=False, header=1, 
                         encoding_errors='ignore')
        out = pd.DataFrame({
            'cpt': df['HCPCS/DRG'],
            'gross': df['Gross Charge'],
            'cash': df['Discounted Cash Price'],
            'max': df['De-Identified Maximum'],
            'min': df['De-Identified Minimum']
            })
        out.drop_duplicates(inplace=True)
        
    elif control.hospital_id[i] in [76]:
        # read in the file
        df = pd.read_csv('/opt/data/raw/' + control.file[i], 
                         low_memory=False, encoding_errors='ignore')
        out = pd.DataFrame({
            'cpt': df['CPT/HCPCS'],
            'gross': df['Epic Price']
            })
        out.drop_duplicates(inplace=True)
   
    # Check if out was created in the previous step
    if out is not None:
        # uniform
        out.dropna(subset=['cpt'], inplace=True)
        out = out[out.cpt != '']
        out = out[out.cpt != '*']
        
        # must match a reference code, usually CPT or HCPCS
        out = out.merge(concept, on='cpt', sort=True)
        out = out.drop('cpt', axis=1)
        
        # melt from wide to long, and clean
        long = pd.melt(out, id_vars='concept_id')
        if long.value.dtypes not in ('float64', 'int64'):
            long['value'] = long['value'].str.replace('[,-]', '', regex=True)
            long['value'] = long['value'].str.replace('[$]', '', regex=True)
            long['value'] = long['value'].str.replace('[A-Za-z]', '', regex=True)
            long['value'] = long['value'].str.strip()
            # some values end up being an empty string
            long.loc[long['value'] == '', 'value'] = np.nan 
            long['value'] = long.value.astype(float)
        long.dropna(subset=['value'], inplace=True)
        long = long[long.value > 0]

        # Add hospital id and order columns
        long['hospital_id'] = control.hospital_id[i]
        long = long[long.columns[[3,0,1,2]]]
        
        # write the data to a flatfile for postgres
        if long.shape[0] > 0:
            out_path = '/opt/data/transformed/' + str(control.hospital_id[i]) + '.csv'
            long.to_csv(out_path, header=False, index=None)
    
        # clear variables from last iteration
        del out
        del long

