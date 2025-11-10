
import pandas as pd, numpy as np
_DEFAULT_PNEC={"sulfamethoxazole":{"water":240.0,"sediment":12.0,"biota":5.0},
"ciprofloxacin":{"water":64.0,"sediment":18.0,"biota":10.0},
"tetracycline":{"water":1000.0,"sediment":25.0,"biota":8.0},
"erythromycin":{"water":300.0,"sediment":15.0,"biota":7.0},
"chloramphenicol":{"water":500.0,"sediment":20.0,"biota":9.0}}
def _pick_pnec(comp, mat, tbl=None):
    t=tbl or _DEFAULT_PNEC; return (t.get(str(comp).lower(),{}) or {}).get(mat if mat in ["water","sediment","biota"] else "water", np.nan)
def compute_rq(df, pnec_table=None):
    x=df.copy(); x["pnec"]=x.apply(lambda r:_pick_pnec(r.get("compound",""), r.get("matrix",""), pnec_table), axis=1)
    x["rq"]=x["value"]/x["pnec"]; return x
def compute_pi(df):
    x=df.copy(); bench=x.groupby(["matrix","compound"])["value"].quantile(0.75).rename("S")
    x=x.join(bench,on=["matrix","compound"]); x["pi_component"]=(x["value"]/x["S"].replace(0,np.nan))**2
    pi=x.groupby("sample_id")["pi_component"].mean().pipe(np.sqrt).rename("pi"); return x.merge(pi,on="sample_id",how="left")
def compute_rrq(df):
    x=df.copy(); mx=x.groupby("matrix")["value"].transform("max").replace(0,np.nan); x["rrq"]=x["value"]/mx; return x
def aggregate_by(df, dims=("matrix","class")):
    g=df.groupby(list(dims)); return g["value"].agg(["count","mean","median","max"]).reset_index()
