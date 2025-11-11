import pandas as pd

def read_data(path):
    if str(path).lower().endswith('.csv'):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    rename = {'concentration_ngl':'Concentration_ngL','pnec_ngl':'PNEC_ngL'}
    for k,v in rename.items():
        if k in df.columns and v not in df.columns:
            df = df.rename(columns={k:v})
    needed = ['Site_ID','Season','Antibiotic','Concentration_ngL','PNEC_ngL']
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise ValueError(f'Missing columns: {missing}. Required: {needed}')
    return df
