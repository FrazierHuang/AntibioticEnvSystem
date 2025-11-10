
import pandas as pd, numpy as np
def emp_source_index(df, source_cols=("livestock","wwtp","aquaculture","shipping")):
    out=df.copy()
    for c in source_cols:
        if c in out.columns:
            v=out[c].astype(float); out[c+"_std"]=(v-v.min())/(v.max()-v.min()+1e-9)
        else: out[c+"_std"]=0.0
    import numpy as np; w=np.array([1.0]*len(source_cols))
    out["source_index"]=sum(out[c+"_std"]*wi for c,wi in zip([s+"_std" for s in source_cols], w))/w.sum()
    return out
def seasonal_index(df):
    x=df.copy()
    if "datetime" not in x.columns: return x.assign(season_index=float("nan"))
    x["month"]=x["datetime"].dt.month; med=x["value"].median() or 1.0
    s=x.groupby("month")["value"].median()/(med if med!=0 else 1.0)
    return x.merge(s.rename("season_index"), on="month", how="left")
def flux_mass_balance(df, flow_col="flow_m3_s"):
    x=df.copy()
    if flow_col not in x.columns: x["flux_mg_s"]=float("nan"); return x
    x["flux_mg_s"]=x["value"]*x[flow_col]*1e-3; return x
