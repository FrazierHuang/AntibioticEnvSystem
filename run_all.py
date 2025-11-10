# run_all.py (增强版)
import os, sys
import pandas as pd
from antibiotic_env import (read_data, clean_columns, standardize_units, handle_lod,
    flag_outliers, compute_rq, compute_pi, compute_rrq, seasonal_index, flux_mass_balance,
    md_report, save_markdown, to_excel)
from antibiotic_env.viz import plot_spatiotemporal, plot_risk_matrix, plot_exceedance
import matplotlib.pyplot as plt
from pathlib import Path

DATA = os.environ.get("DATA_FILE") or (sys.argv[1] if len(sys.argv) > 1 else "examples/synthetic_antibiotics_data.csv")
OUTDIR = os.environ.get("OUT_DIR") or (sys.argv[2] if len(sys.argv) > 2 else "outputs")

Path(OUTDIR).mkdir(parents=True, exist_ok=True)

print(f"[INFO] Input: {DATA}")
print(f"[INFO] Outdir: {OUTDIR}")

df = read_data(DATA)
df = clean_columns(df); df = standardize_units(df); df = handle_lod(df, method="lod/2")
df = flag_outliers(df); df = compute_rq(df); df = compute_pi(df); df = compute_rrq(df); df = seasonal_index(df)
df["flow_m3_s"] = 200; df = flux_mass_balance(df)

# 图表输出到指定 OUTDIR
plt.clf(); plot_spatiotemporal(df); plt.title("Spatiotemporal Trends"); plt.tight_layout(); plt.savefig(f"{OUTDIR}/plot_spatiotemporal.png", dpi=180)
plt.clf(); plot_risk_matrix(df);   plt.title("Risk Matrix (MEC vs PNEC)"); plt.tight_layout(); plt.savefig(f"{OUTDIR}/plot_risk_matrix.png", dpi=180)
plt.clf(); plot_exceedance(df);    plt.title("Fraction of RQ > 1"); plt.tight_layout(); plt.savefig(f"{OUTDIR}/plot_exceedance.png", dpi=180)

summary = {
    "rows": len(df),
    "matrices": df["matrix"].dropna().unique().tolist(),
    "compounds": df["compound"].dropna().unique().tolist(),
    "stats": df.groupby(["matrix","compound"])["value"].describe().reset_index(),
    "completeness": df.groupby(["matrix","compound"])["value"].apply(lambda s: s.notna().mean()).reset_index(name="completeness"),
}
save_markdown(f"{OUTDIR}/outputs_report.md", md_report(summary))
to_excel(f"{OUTDIR}/outputs.xlsx", {"data": df, "stats": summary["stats"], "completeness": summary["completeness"]})

print("[DONE] Generated:")
print(f" - {OUTDIR}/plot_spatiotemporal.png")
print(f" - {OUTDIR}/plot_risk_matrix.png")
print(f" - {OUTDIR}/plot_exceedance.png")
print(f" - {OUTDIR}/outputs_report.md")
print(f" - {OUTDIR}/outputs.xlsx")