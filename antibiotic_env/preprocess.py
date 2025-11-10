
import pandas as pd
_UNIT_MAP = {"ug/l":("ng/l",1000.0),"µg/l":("ng/l",1000.0),"mg/l":("ng/l",1e6),"ng/l":("ng/l",1.0),
             "ug/kg":("ng/g",1000.0),"mg/kg":("ng/g",1e6),"ng/g":("ng/g",1.0)}
def clean_columns(df):
    x = df.copy(); x.columns=[c.strip().lower() for c in x.columns]
    if "matrix" in x.columns: x["matrix"]=x["matrix"].str.strip().str.lower()
    return x.dropna(how="all")
def standardize_units(df):
    x=df.copy()
    if "unit" not in x.columns: return x
    def _norm(r):
        u=str(r.get("unit","")).lower(); tgt,f=_UNIT_MAP.get(u,(u,1.0))
        v=r.get("value")
        try: return v*f,tgt
        except: return v,u
    res=x.apply(lambda r: pd.Series(_norm(r),index=["value","unit_std"]),axis=1)
    x["value"]=res["value"]; x["unit"]=res["unit_std"]; return x
def handle_lod(df, method="lod/2"):
    x=df.copy(); v=x["value"]; lod=x["lod"] if "lod" in x.columns else 0
    if method=="lod/2": x.loc[v.isna()|(v<=0),"value"]=(lod if hasattr(lod,'fillna') else 0)/2.0
    elif method=="lod/sqrt2": x.loc[v.isna()|(v<=0),"value"]=(lod if hasattr(lod,'fillna') else 0)/1.41421356
    elif method=="zero": x.loc[v.isna()|(v<=0),"value"]=0.0
    return x
