"""Pool RTP data for grade 3 LCL / PLC injuries from studies.csv and draw the figure.

Rules (from the research brief):
- group by isolated vs combined and by treatment (combined surgical also by cruciate base);
- pooled rate = sum(rate*n)/sum(n), cohorts only - case reports, n<10 subgroups
  that are not the sole evidence, systematic reviews and rows without n are never pooled;
- time to RTP is reported as a range of study-level means/medians, never averaged.
Usage: python analyze.py  (writes pooled_summary.csv and rtp_figure.png next to this file)
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).parent
df = pd.read_csv(HERE / "studies.csv", dtype=str).fillna("")
num = lambda s: pd.to_numeric(s, errors="coerce")
for c in ["n", "rtp_rate_pct", "rtp_same_level_pct", "time_to_rtp_weeks"]:
    df[c + "_v"] = num(df[c])

# Pooling groups: explicit mapping from row id prefix -> analysis group
GROUPS = {
    # Haslhofer's MRI-grade-3 subgroup had clinical laxity grade 0-2, so it is kept out of the grade 3 pool
    "Isolated | non-operative": ["bushnell2010_nonop"],
    "Isolated | non-operative, MRI grade 3 but clinical grade <=2": ["haslhofer2025_mri_g3"],
    "Isolated | repair": ["bushnell2010_repair"],
    "Combined | surgical, ACL-based": ["borque2020abs_acl_plc", "borque2020abs_acl_mcl_plc", "lutz2021_acl"],
    "Combined | surgical, PCL-based": ["borque2020abs_pcl_plc", "lutz2021_pcl"],
    "Combined | surgical, bicruciate": ["borque2020abs_bicruciate_plc", "borque2020abs_bicruciate_mcl_plc"],
    "Combined | treatment not reported (NFL)": ["bakshi2018_acl_pcl_lcl"],
    "Combined | repair (same level only)": ["minator2022_repair"],
    "Combined | reconstruction (same level only)": ["minator2022_recon"],
}

def pool(rows, col):
    r = rows.dropna(subset=[col + "_v", "n_v"])
    if r.empty: return None, 0, 0
    return (r[col + "_v"] * r["n_v"]).sum() / r["n_v"].sum(), int(r["n_v"].sum()), len(r)

out = []
for g, ids in GROUPS.items():
    rows = df[df["id"].isin(ids)]
    assert len(rows) == len(ids), f"missing ids in {g}"
    rtp, n_rtp, k_rtp = pool(rows, "rtp_rate_pct")
    same, n_same, k_same = pool(rows, "rtp_same_level_pct")
    t = rows["time_to_rtp_weeks_v"].dropna()
    out.append(dict(group=g, studies=rows["pmid"].replace("", "PMC7401073").nunique(), rows=len(rows),
                    n_total=int(rows["n_v"].sum()),
                    pooled_rtp_pct=None if rtp is None else round(rtp, 1), n_rtp=n_rtp,
                    pooled_same_level_pct=None if same is None else round(same, 1), n_same=n_same,
                    time_weeks_range="" if t.empty else f"{t.min():g}-{t.max():g}",
                    small_sample_flag="yes" if rows["n_v"].sum() < 10 else ""))
summary = pd.DataFrame(out)
summary.to_csv(HERE / "pooled_summary.csv", index=False)
pd.set_option("display.width", 200); pd.set_option("display.max_columns", 20)
print(summary.to_string(index=False))

# Case reports / small series - listed, never pooled
cr = df[df["case_report_or_n_lt_10"].str.contains("case", case=False) & df["rtp_rate_pct_v"].notna()]
print("\nCase reports / small series (not pooled):")
print(cr[["id", "n", "treatment", "rtp_rate_pct", "time_to_rtp_weeks", "time_stat"]].to_string(index=False))

# ---------------- Figure ----------------
TREAT = {  # validated reference palette, categorical slots 1-3 + neutral
    "non-operative": ("#2a78d6", "Non-operative"),
    "repair": ("#eb6834", "Repair"),
    "reconstruction": ("#1baf7a", "Reconstruction"),
    "surgical": ("#7a7974", "Surgery, type not split / not reported"),
}
def tkey(t):
    t = t.lower()
    if t.startswith("non-op"): return "non-operative"
    if t.startswith("repair"): return "repair"
    if t.startswith("reconstruction"): return "reconstruction"
    return "surgical"

PLOT = [  # (row id, label) top to bottom, grouped
    ("ISOLATED grade 3 LCL", None),
    ("bushnell2010_nonop", "Bushnell 2010, NFL"),
    ("haslhofer2025_mri_g3", "Haslhofer 2025, elite (80% soccer)*"),
    ("gnesutta2024", "Gnesutta 2024, pro soccer"),
    ("davenport2018", "Davenport 2018, youth soccer"),
    ("haddad2016", "Haddad 2016, HS wrestler"),
    ("bushnell2010_repair", "Bushnell 2010, NFL"),
    ("mitchell2024", "Mitchell 2024, pro soccer"),
    ("COMBINED PLC / multiligament", None),
    ("borque2020abs_acl_plc", "Borque 2020 abs, ACL+PLC"),
    ("borque2020abs_acl_mcl_plc", "Borque 2020 abs, ACL+MCL+PLC"),
    ("lutz2021_acl", "Lutz 2021, ACL-based"),
    ("laprade2017_case", "LaPrade 2017, NBA ACL+FCL"),
    ("paget2017_case", "Paget 2017, rugby ACL+PLC"),
    ("borque2020abs_pcl_plc", "Borque 2020 abs, PCL+PLC"),
    ("lutz2021_pcl", "Lutz 2021, PCL-based"),
    ("borque2020abs_bicruciate_plc", "Borque 2020 abs, ACL+PCL+PLC"),
    ("borque2020abs_bicruciate_mcl_plc", "Borque 2020 abs, 4-ligament"),
    ("barrerauso2025_lateral", "Barrera Uso 2025, dislocation"),
    ("bakshi2018_acl_pcl_lcl", "Bakshi 2018, NFL ACL+PCL/LCL"),
]
ink, ink2, grid = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": grid,
                     "xtick.color": ink2, "ytick.color": ink2})
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 8.2), sharey=True, gridspec_kw={"width_ratios": [1, 1]})
fig.patch.set_facecolor("#fcfcfb")
y = 0; yt, yl = [], []
for rid, label in PLOT:
    y -= 1
    if label is None:
        a1.text(-0.62, y, rid, fontsize=9.5, fontweight="bold", color=ink, va="center", ha="left",
                transform=a1.get_yaxis_transform())
        continue
    r = df[df["id"] == rid].iloc[0]
    col = TREAT[tkey(r["treatment"])][0]
    small = r["case_report_or_n_lt_10"] != ""
    face = "white" if small else col
    yt.append(y); yl.append(label)
    rate, t, n = r["rtp_rate_pct_v"], r["time_to_rtp_weeks_v"], int(r["n_v"]) if pd.notna(r["n_v"]) else None
    if pd.notna(rate):
        a1.plot(rate, y, "o", ms=8, mfc=face, mec=col, mew=2, zorder=3)
        a1.annotate(f"n={n}", (rate, y), xytext=(-8, 0), textcoords="offset points", ha="right", va="center", fontsize=7.5, color=ink2)
    if pd.notna(t):
        a2.plot(t, y, "o", ms=8, mfc=face, mec=col, mew=2, zorder=3)
        a2.annotate(f"n={n}", (t, y), xytext=(8, 0), textcoords="offset points", ha="left", va="center", fontsize=7.5, color=ink2)
    elif rid == "barrerauso2025_lateral":
        a2.plot([11 * 4.345, 22 * 4.345], [y, y], color=col, lw=2, solid_capstyle="round")
        a2.annotate("n=3 returners, range", (22 * 4.345, y), xytext=(8, 0), textcoords="offset points", va="center", fontsize=7.5, color=ink2)
    else:
        a2.text(2, y, "not reported", fontsize=7.5, color=ink2, va="center", style="italic")
for ax in (a1, a2):
    ax.set_facecolor("#fcfcfb"); ax.grid(axis="x", color=grid, lw=0.8); ax.set_axisbelow(True)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
a1.set_ylim(y - 0.6, -0.4); a1.set_yticks(yt); a1.set_yticklabels(yl, color=ink)
a1.set_xlim(-2, 105); a1.set_xlabel("Return to play, % of athletes", color=ink2)
a2.set_xlim(-3, 115); a2.set_xlabel("Time to return, weeks (study mean/median)", color=ink2)
a1.set_title("Return-to-play rate", loc="left", fontsize=11, color=ink, fontweight="bold")
a2.set_title("Time to return to play", loc="left", fontsize=11, color=ink, fontweight="bold")
handles = [Line2D([], [], marker="o", ls="", ms=8, mfc=c, mec=c, mew=2, label=l) for c, l in TREAT.values()]
handles.append(Line2D([], [], marker="o", ls="", ms=8, mfc="white", mec=ink2, mew=2, label="Hollow = case report or n<10"))
fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=8.5, bbox_to_anchor=(0.55, 0.0))
fig.suptitle("Grade 3 LCL tears: return to play by treatment, isolated vs combined injury", x=0.02, ha="left",
             fontsize=13, fontweight="bold", color=ink)
fig.text(0.02, 0.935, "*Haslhofer: MRI grade 3 but clinical laxity grade 0-2; subgroup time not reported (whole cohort median 76 d). "
         "Borque 2020 abs = conference abstract.", fontsize=7.5, color=ink2)
fig.tight_layout(rect=(0, 0.06, 1, 0.93))
fig.savefig(HERE / "rtp_figure.png", dpi=180, facecolor=fig.get_facecolor())
print("\nwrote rtp_figure.png, pooled_summary.csv")
