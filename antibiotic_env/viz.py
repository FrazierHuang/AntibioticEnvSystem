
import matplotlib.pyplot as plt
def _theme(ax): ax.grid(True,alpha=0.3); ax.set_facecolor("white")
def plot_spatiotemporal(df, ax=None, hue="compound"):
    ax=ax or plt.figure().gca(); x=df.dropna(subset=["datetime","value"])
    for k, sub in x.groupby(hue): ax.plot(sub["datetime"], sub["value"], marker="o", linestyle="-", label=str(k), alpha=0.8)
    ax.set_xlabel("Date"); ax.set_ylabel(f"Concentration ({df.get('unit','ng/L')})"); ax.legend(ncol=2,fontsize=8); _theme(ax); return ax
def plot_risk_matrix(df, ax=None):
    ax=ax or plt.figure().gca(); x=df.dropna(subset=["value","pnec"]); ax.scatter(x["pnec"],x["value"],alpha=0.6)
    if not x.empty: mn=min(x["pnec"].min(), x["value"].min()); mx=max(x["pnec"].max(), x["value"].max()); ax.plot([mn,mx],[mn,mx],linestyle="--")
    ax.set_xlabel("PNEC"); ax.set_ylabel("MEC (value)"); ax.set_xscale("log"); ax.set_yscale("log"); _theme(ax); return ax
def plot_exceedance(df, ax=None):
    ax=ax or plt.figure().gca(); x=df.copy()
    if "rq" not in x.columns: return ax
    g=x.assign(exc=(x["rq"]>1).astype(int)).groupby(["matrix","compound"])["exc"].mean().reset_index()
    for m, sub in g.groupby("matrix"): ax.bar(sub["compound"]+" ("+m+")", sub["exc"], alpha=0.8)
    ax.tick_params(axis='x', rotation=45)
