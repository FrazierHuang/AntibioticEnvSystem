
import pandas as pd
def to_excel(path, data: dict):
    with pd.ExcelWriter(path, engine="xlsxwriter") as xw:
        for name,obj in data.items():
            if hasattr(obj, "to_excel"): obj.to_excel(xw, sheet_name=str(name)[:31], index=False)
            else: pd.DataFrame({"value":[str(obj)]}).to_excel(xw, sheet_name=str(name)[:31], index=False)
