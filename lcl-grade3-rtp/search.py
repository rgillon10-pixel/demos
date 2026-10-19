"""Literature search for grade 3 LCL/PLC return-to-play.
Queries PubMed, Europe PMC and OpenAlex; logs every query + hit count to
search_hits.json and saves retrieved records (title/abstract/ids) to records.json."""
import json, sys, time, xml.etree.ElementTree as ET
import requests

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
S = requests.Session()
LOG, RECS = [], {}

def get(url, params, tries=6):
    for i in range(tries):
        r = S.get(url, params=params, timeout=60)
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(3 * (i + 1)); continue
        r.raise_for_status(); return r
    r.raise_for_status()

EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def pubmed(q, label):
    r = get(EU + "esearch.fcgi", {"db": "pubmed", "term": q, "retmax": 300, "retmode": "json",
                                  "mindate": "2000", "maxdate": "2026", "datetype": "pdat"}).json()
    ids = r["esearchresult"]["idlist"]
    LOG.append({"db": "PubMed", "label": label, "query": q, "hits": int(r["esearchresult"]["count"])})
    time.sleep(0.5)
    for i in range(0, len(ids), 100):
        x = get(EU + "efetch.fcgi", {"db": "pubmed", "id": ",".join(ids[i:i+100]), "retmode": "xml"}).text
        for a in ET.fromstring(x).findall(".//PubmedArticle"):
            pmid = a.findtext(".//PMID")
            doi = next((e.text for e in a.findall(".//ArticleId") if e.get("IdType") == "doi"), "")
            rec = RECS.setdefault("PMID:" + pmid, {"pmid": pmid, "doi": doi, "sources": []})
            rec["title"] = "".join(a.find(".//ArticleTitle").itertext())
            rec["abstract"] = " ".join("".join(t.itertext()) for t in a.findall(".//AbstractText"))
            rec["year"] = a.findtext(".//PubDate/Year") or (a.findtext(".//PubDate/MedlineDate") or "")[:4]
            rec["journal"] = a.findtext(".//Journal/ISOAbbreviation")
            au = a.findall(".//Author/LastName"); rec["first_author"] = au[0].text if au else ""
            rec["pubtypes"] = [p.text for p in a.findall(".//PublicationType")]
            rec["sources"].append("PubMed:" + label)
        time.sleep(0.5)
    return ids

def europepmc(q, label):
    r = get("https://www.ebi.ac.uk/europepmc/webservices/rest/search",
            {"query": q, "format": "json", "pageSize": 300, "resultType": "core"}).json()
    LOG.append({"db": "EuropePMC", "label": label, "query": q, "hits": r.get("hitCount", 0)})
    for it in r.get("resultList", {}).get("result", []):
        key = "PMID:" + it["pmid"] if it.get("pmid") else "EPMC:" + it["id"]
        rec = RECS.setdefault(key, {"pmid": it.get("pmid", ""), "doi": it.get("doi", ""), "sources": []})
        rec.setdefault("title", it.get("title", "")); rec.setdefault("year", it.get("pubYear", ""))
        if not rec.get("abstract"): rec["abstract"] = it.get("abstractText", "")
        rec.setdefault("journal", it.get("journalInfo", {}).get("journal", {}).get("isoabbreviation", ""))
        rec.setdefault("first_author", (it.get("authorString") or "").split(" ")[0])
        rec["sources"].append("EuropePMC:" + label)
    time.sleep(1)

def openalex(q, label):
    r = get("https://api.openalex.org/works", {"search": q, "per-page": 100,
            "filter": "from_publication_date:2000-01-01"}).json()
    LOG.append({"db": "OpenAlex", "label": label, "query": q, "hits": r["meta"]["count"]})
    out = [(w.get("doi") or "", w["display_name"], w.get("publication_year"), w.get("cited_by_count"), w["id"])
           for w in r["results"]]
    time.sleep(3); return out

CORE_PM = ('("lateral collateral ligament"[tiab] OR "fibular collateral ligament"[tiab] OR "posterolateral corner"[tiab]) '
           'AND ("grade III"[tiab] OR "grade 3"[tiab] OR complete[tiab] OR rupture[tiab] OR reconstruction[tiab] OR repair[tiab]) '
           'AND ("return to sport"[tiab] OR "return to play"[tiab] OR "return to sports"[tiab] OR "return to activity"[tiab]) '
           'AND humans[mh] AND english[la] NOT elbow[tiab] NOT ankle[tiab]')
pubmed(CORE_PM, "core")
pubmed(CORE_PM.replace(" AND humans[mh]", ""), "core-no-MeSH-humans (catches unindexed recent)")
pubmed('("lateral collateral ligament"[tiab] OR "fibular collateral ligament"[tiab]) AND (isolated[tiab]) AND (athlete*[tiab] OR football[tiab] OR soccer[tiab] OR NFL[tiab]) AND english[la] NOT elbow[tiab] NOT ankle[tiab]', "isolated-FCL-athletes")
pubmed('("posterolateral corner"[tiab] OR "fibular collateral"[tiab] OR "lateral collateral ligament"[tiab]) AND (repair[tiab]) AND (reconstruction[tiab]) AND (failure[tiab] OR "systematic review"[pt] OR meta-analysis[pt]) AND english[la] NOT elbow[tiab] NOT ankle[tiab]', "repair-vs-recon")
pubmed('("varus stress"[tiab]) AND (radiograph*[tiab]) AND ("posterolateral"[tiab] OR "fibular collateral"[tiab] OR "lateral collateral"[tiab]) NOT elbow[tiab] NOT ankle[tiab]', "varus-stress-radiograph")
pubmed('("multiligament"[tiab] OR "multi-ligament"[tiab] OR "knee dislocation"[tiab]) AND ("return to play"[tiab] OR "return to sport"[tiab]) AND (athlete*[tiab] OR NFL[tiab] OR football[tiab] OR soccer[tiab]) AND english[la]', "multiligament-RTP")
pubmed('("posterolateral corner"[tiab] OR "fibular collateral"[tiab]) AND (weightbearing[tiab] OR "weight bearing"[tiab] OR rehabilitation[tiab]) AND ("systematic review"[tiab] OR review[pt])', "PLC-rehab-weightbearing")
pubmed('("lateral collateral ligament"[tiab]) AND knee[tiab] AND ("return-to-performance"[tiab] OR "case report"[tiab] OR "professional"[tiab]) AND (repair[tiab] OR reconstruction[tiab] OR rupture[tiab]) NOT elbow[tiab] NOT ankle[tiab]', "LCL-professional-case")

europepmc('("lateral collateral ligament" OR "fibular collateral ligament" OR "posterolateral corner") AND ("grade III" OR "grade 3" OR complete OR rupture OR reconstruction OR repair) AND ("return to sport" OR "return to play") AND PUB_YEAR:[2000 TO 2026] AND LANG:eng NOT elbow NOT ankle', "core")
europepmc('("fibular collateral ligament" OR "lateral collateral ligament") AND "professional football" AND knee', "aspetar/pro-football")

oa = {}
for q, l in [("isolated fibular collateral ligament injuries athletes return to play", "FCL-athletes"),
             ("lateral collateral ligament knee grade III return to play", "LCL-grade3-RTP"),
             ("posterolateral corner repair versus reconstruction failure systematic review", "PLC-repair-vs-recon"),
             ("multiligament knee injuries NFL return to play", "MLKI-NFL")]:
    try: oa[l] = openalex(q, l)
    except Exception as e: LOG.append({"db": "OpenAlex", "label": l, "query": q, "hits": f"error {e}"})

json.dump(LOG, open(f"{OUT}/search_hits.json", "w"), indent=1)
json.dump(RECS, open(f"{OUT}/records.json", "w"), indent=1)
json.dump(oa, open(f"{OUT}/openalex.json", "w"), indent=1)
for l in LOG: print(l["db"], l["label"], l["hits"])
print("unique records", len(RECS))
