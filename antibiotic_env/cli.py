
import argparse, json
from .io import read_data
from .preprocess import clean_columns, standardize_units, handle_lod
from .qa_qc import flag_outliers, summary_report
from .indicators import compute_rq, compute_pi, compute_rrq
from .models import seasonal_index, flux_mass_balance
def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument("input"); p.add_argument("--lod",default="lod/2"); p.add_argument("--json",action="store_true")
    a=p.parse_args(argv)
    df=read_data(a.input); 
    from .preprocess import clean_columns, standardize_units, handle_lod
    df=clean_columns(df); df=standardize_units(df); df=handle_lod(df,method=a.lod)
    df=flag_outliers(df); df=compute_rq(df); df=compute_pi(df); df=compute_rrq(df); df=seasonal_index(df); df["flow_m3_s"]=200; df=flux_mass_balance(df)
    rep=summary_report(df); out={"rows":len(df),"stats_preview":rep["stats"].head(10).to_dict("records"),"completeness_preview":rep["completeness"].head(10).to_dict("records")}
    print(json.dumps(out, ensure_ascii=False, indent=2) if a.json else out)
if __name__=="__main__": main()
