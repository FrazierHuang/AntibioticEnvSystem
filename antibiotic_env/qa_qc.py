
import pandas as pd, numpy as np
def flag_outliers(df, by=("matrix","compound")):
    x=df.copy(); x["outlier_flag"]=False
    for _,grp in x.groupby(list(by)):
        med=grp["value"].median(); mad=(grp["value"]-med).abs().median() or 1e-9
        z=0.6745*(grp["value"]-med)/mad; x.loc[grp.index[z.abs()>3.5],"outlier_flag"]=True
    return x
def summary_report(df):
    stats=df.groupby(["matrix","compound"])["value"].agg(["count","mean","median","min","max","std"]).reset_index()
    comp=df.groupby(["matrix","compound"])["value"].apply(lambda s:s.notna().mean()).reset_index(name="completeness")
    return {"stats":stats,"completeness":comp}
