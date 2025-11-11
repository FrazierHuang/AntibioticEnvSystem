import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def plot_spatiotemporal(df: pd.DataFrame, outdir: Path):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    plt.figure()
    pivot = df.pivot_table(values='Concentration_ngL', index='Site_ID', columns='Season', aggfunc='mean')
    pivot.plot(marker='o')
    plt.ylabel('Concentration (ng/L)'); plt.title('Spatiotemporal Distribution'); plt.tight_layout()
    p = outdir / 'plot_spatiotemporal.png'; plt.savefig(p, dpi=160); plt.close(); return p

def plot_risk_matrix(df: pd.DataFrame, outdir: Path):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    plt.figure()
    plt.scatter(df['PNEC_ngL'], df['Concentration_ngL'])
    plt.xlabel('PNEC (ng/L)'); plt.ylabel('MEC (ng/L)'); plt.title('Risk Matrix (MEC vs PNEC)'); plt.tight_layout()
    p = outdir / 'plot_risk_matrix.png'; plt.savefig(p, dpi=160); plt.close(); return p

def plot_exceedance(exceed_df: pd.DataFrame, outdir: Path):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    plt.figure()
    plt.bar(exceed_df['Antibiotic'], exceed_df['ExceedFrac'])
    plt.xticks(rotation=45, ha='right'); plt.ylabel('Fraction RQ > 1'); plt.title('Exceedance by Antibiotic'); plt.tight_layout()
    p = outdir / 'plot_exceedance.png'; plt.savefig(p, dpi=160); plt.close(); return p
