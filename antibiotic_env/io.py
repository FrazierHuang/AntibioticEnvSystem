
import pandas as pd
def read_data(path, sheet=None):
    if path.lower().endswith(('.xls','.xlsx')):
        df = pd.read_excel(path, sheet_name=sheet)
    else:
        df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    for c in ["lon","lat","value","lod","loq"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df
def to_long(df, id_cols, value_vars):
    return df.melt(id_vars=id_cols, value_vars=value_vars, var_name="compound", value_name="value")
def to_wide(df, index_cols):
    w = df.pivot_table(index=index_cols, columns="compound", values="value", aggfunc="mean")
    return w.reset_index()
