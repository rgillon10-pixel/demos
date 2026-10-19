"""Re-check that every pooled number and key per-row number quoted in README.md matches the CSVs."""
from pathlib import Path
import pandas as pd
H = Path(__file__).parent
R = (H / "README.md").read_text()
P = pd.read_csv(H / "pooled_summary.csv").fillna("")
D = pd.read_csv(H / "studies.csv", dtype=str).fillna("")
bad = []
for _, r in P.iterrows():
    for v, n in [(r.pooled_rtp_pct, r.n_rtp), (r.pooled_same_level_pct, r.n_same)]:
        if v != "" and not any(f"{x}% (n={int(n)}" in R for x in (f"{float(v):g}", f"{float(v):.1f}")): bad.append((r.group, v, n))
    if r.time_weeks_range and str(r.time_weeks_range).split("-")[0] not in R: bad.append((r.group, r.time_weeks_range))
for rid, col in [("stannard2005_repair", "failure_rate_pct"), ("stannard2005_recon", "failure_rate_pct"),
                 ("levy2010_recon", "failure_rate_pct"), ("fortier2023_repair", "failure_rate_pct"),
                 ("fortier2023_recon", "failure_rate_pct"), ("moran2022", "failure_rate_pct"),
                 ("bakshi2018_acl_pcl_lcl", "time_to_rtp_weeks"), ("bushnell2010_nonop", "time_to_rtp_weeks"),
                 ("bushnell2010_repair", "time_to_rtp_weeks"), ("mitchell2024", "time_to_rtp_weeks"),
                 ("davenport2018", "time_to_rtp_weeks"), ("bakshi2018_acl_pcl_lcl", "rtp_same_level_pct")]:
    v = D.loc[D.id == rid, col].iloc[0]
    if v not in R: bad.append((rid, col, v))
print("MISMATCHES:", bad or "none")
