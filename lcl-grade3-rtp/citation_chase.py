"""Forward-citation chasing + keyword search via Semantic Scholar (OpenAlex returned HTTP 429 on every retry).
Usage: python citation_chase.py <outdir>   -> <outdir>/s2.json"""
import json, sys, time
import requests
S = requests.Session(); log = []; found = {}
def ss(url, params):
    for i in range(6):
        r = S.get(url, params=params, timeout=60)
        if r.status_code == 429: time.sleep(5 * (i + 1)); continue
        return r
    return r
for pmid, lab in [("19966106", "Bushnell 2010"), ("41341507", "Haslhofer 2025"), ("25545646", "Sikka 2015"),
                  ("37848567", "Fortier 2023"), ("39499973", "Mitchell 2024")]:
    r = ss(f"https://api.semanticscholar.org/graph/v1/paper/PMID:{pmid}/citations",
           {"fields": "title,year,externalIds", "limit": 200})
    if r.status_code != 200: log.append((lab, "citations", r.status_code)); continue
    d = r.json().get("data", []); log.append((lab, "forward citations", len(d)))
    for c in d:
        p = c["citingPaper"]; ids = p.get("externalIds") or {}
        found[p.get("title")] = (p.get("year"), ids.get("PubMed"), ids.get("DOI"), lab)
    time.sleep(4)
for q in ["isolated fibular collateral ligament injury professional football",
          "lateral collateral ligament combat sports algorithm reconstruction",
          "isolated lateral collateral ligament rupture knee athlete return"]:
    r = ss("https://api.semanticscholar.org/graph/v1/paper/search",
           {"query": q, "fields": "title,year,externalIds,venue", "limit": 50})
    if r.status_code != 200: log.append((q, "search", r.status_code)); continue
    j = r.json(); log.append((q, "search", j.get("total")))
    for p in j.get("data", []):
        ids = p.get("externalIds") or {}
        found[p["title"]] = (p.get("year"), ids.get("PubMed"), ids.get("DOI"), "S2 search: " + q)
    time.sleep(4)
json.dump({"log": log, "found": found}, open(f"{sys.argv[1]}/s2.json", "w"), indent=1)
