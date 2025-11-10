
import datetime
def md_report(summary, title="AntibioticEnv Report"):
    now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    def _table_md(df, max_rows=20):
        if df is None or getattr(df,'empty',True): return "\n_Empty_\n"
        x=df.head(max_rows); h="| "+" | ".join(map(str,x.columns))+" |"; s="| "+" | ".join(["---"]*len(x.columns))+" |"
        rows=["| "+" | ".join(map(lambda v:str(v)[:80], r))+" |" for r in x.to_numpy().tolist()]
        return "\n".join([h,s]+rows)
    parts=[f"# {title}", f"_Generated: {now}_\n", "## Overview", f"- **Rows**: {summary.get('rows')}",
           f"- **Matrices**: {', '.join(map(str, summary.get('matrices', [])))}",
           f"- **Compounds**: {', '.join(map(str, summary.get('compounds', [])))}",
           "\n## Descriptive Statistics (preview)", _table_md(summary.get("stats")),
           "\n## Completeness (preview)", _table_md(summary.get("completeness"))]
    return "\n\n".join(parts)
def save_markdown(path, content):
    with open(path,"w",encoding="utf-8") as f: f.write(content)
