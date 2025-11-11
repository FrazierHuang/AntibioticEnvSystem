import pandas as pd

def compute_metrics(df: pd.DataFrame):
    df = df.copy()
    df['RQ'] = df['Concentration_ngL'] / df['PNEC_ngL']
    per_site = df.groupby(['Site_ID'], as_index=False).agg(PI=('RQ','mean'), RRQ=('RQ','sum'))
    exceed = (df.assign(exceed=df['RQ']>1).groupby(['Antibiotic'], as_index=False)['exceed'].mean().rename(columns={'exceed':'ExceedFrac'}))
    return df, per_site, exceed
