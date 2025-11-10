
import pandas as pd
from antibiotic_env import (read_data, clean_columns, standardize_units, handle_lod,
    flag_outliers, compute_rq, compute_pi, compute_rrq, seasonal_index, flux_mass_balance)
from antibiotic_env.viz import plot_spatiotemporal, plot_risk_matrix, plot_exceedance
import matplotlib.pyplot as plt

df = read_data("examples/synthetic_antibiotics_data.csv")
df = clean_columns(df); df = standardize_units(df); df = handle_lod(df, method="lod/2")
df = flag_outliers(df); df = compute_rq(df); df = compute_pi(df); df = compute_rrq(df); df = seasonal_index(df)
df["flow_m3_s"] = 200; df = flux_mass_balance(df)

plot_spatiotemporal(df); plt.title("Spatiotemporal Trends (Synthetic)"); plt.tight_layout(); plt.savefig("examples/plot_spatiotemporal.png", dpi=200)
plot_risk_matrix(df);   plt.title("Risk Matrix (MEC vs PNEC)");       plt.tight_layout(); plt.savefig("examples/plot_risk_matrix.png", dpi=200)
plot_exceedance(df);    plt.title("Fraction of RQ > 1");              plt.tight_layout(); plt.savefig("examples/plot_exceedance.png", dpi=200)
print("Done.")
