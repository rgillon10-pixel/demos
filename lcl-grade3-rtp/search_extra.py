"""Second-pass targeted searches (seed papers + gaps found during screening).
Run after search.py; appends to search_hits.json / records.json in the same folder."""
import json, sys, time, xml.etree.ElementTree as ET
import requests
OUT = sys.argv[1]
LOG = json.load(open(f"{OUT}/search_hits.json")); RECS = json.load(open(f"{OUT}/records.json"))
S = requests.Session(); EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def get(url, params, tries=6):
    for i in range(tries):
        r = S.get(url, params=params, timeout=60)
        if r.status_code == 429 or r.status_code >= 500: time.sleep(3 * (i + 1)); continue
        r.raise_for_status(); return r
    r.raise_for_status()

def pubmed(q, label):
    r = get(EU + "esearch.fcgi", {"db": "pubmed", "term": q, "retmax": 100, "retmode": "json"}).json()
    ids = r["esearchresult"]["idlist"]
    LOG.append({"db": "PubMed", "label": label, "query": q, "hits": int(r["esearchresult"]["count"])})
    time.sleep(0.5)
    if not ids: return
    x = get(EU + "efetch.fcgi", {"db": "pubmed", "id": ",".join(ids), "retmode": "xml"}).text
    for a in ET.fromstring(x).findall(".//PubmedArticle"):
        pmid = a.findtext(".//PMID")
        doi = next((e.text for e in a.findall(".//ArticleId") if e.get("IdType") == "doi"), "")
        rec = RECS.setdefault("PMID:" + pmid, {"pmid": pmid, "doi": doi, "sources": []})
        rec["title"] = "".join(a.find(".//ArticleTitle").itertext())
        rec["abstract"] = " ".join("".join(t.itertext()) for t in a.findall(".//AbstractText"))
        rec["year"] = a.findtext(".//PubDate/Year") or (a.findtext(".//PubDate/MedlineDate") or "")[:4]
        rec["journal"] = a.findtext(".//Journal/ISOAbbreviation")
        au = a.findall(".//Author/LastName"); rec["first_author"] = au[0].text if au else ""
        rec["sources"].append("PubMed:" + label)
    time.sleep(0.5)

Q = [
 ('Grawe[au] AND "lateral collateral ligament"[ti]', "seed: Grawe JAAOS"),
 ('LaPrade[au] AND "varus stress"[tiab] AND radiograph*[tiab]', "seed: varus stress radiograph thresholds"),
 ('("fibular collateral ligament"[tiab] OR "posterolateral"[tiab]) AND (acute[tiab]) AND ("grade III"[tiab] OR "grade-III"[tiab]) AND (repair[tiab] OR reconstruction[tiab])', "acute grade III PLC repair/recon"),
 ('("fibular collateral ligament"[tiab] OR "posterolateral corner"[tiab]) AND repair[tiab] AND reconstruction[tiab] AND multiligament*[tiab]', "repair vs recon in MLKI"),
 ('("fibular collateral ligament reconstruction"[tiab] OR "lateral collateral ligament reconstruction"[tiab]) AND knee[tiab] AND (outcome*[tiab] OR "return"[tiab]) NOT elbow[tiab] NOT ankle[tiab]', "FCL/LCL reconstruction outcomes"),
 ('("lateral collateral ligament"[tiab] OR "fibular collateral ligament"[tiab]) AND knee[tiab] AND (nonoperative[tiab] OR "non-operative"[tiab] OR conservative[tiab]) NOT elbow[tiab] NOT ankle[tiab]', "LCL nonoperative"),
 ('("lateral collateral ligament"[tiab] OR "fibular collateral ligament"[tiab]) AND knee[tiab] AND (soccer[tiab] OR football[tiab] OR rugby[tiab] OR basketball[tiab] OR "mixed martial"[tiab] OR combat[tiab] OR judo[tiab] OR wrestl*[tiab]) NOT elbow[tiab] NOT ankle[tiab]', "LCL pivoting/combat sports"),
 ('("posterolateral corner"[tiab] OR "fibular collateral ligament"[tiab]) AND ("return to sport"[tiab] OR "return to play"[tiab] OR "Tegner"[tiab])', "PLC/FCL RTS or Tegner"),
 ('"Isolated fibular collateral ligament injuries in athletes"[ti]', "seed: Sikka 2015"),
 ('"posterolateral corner"[tiab] AND (criteria[tiab]) AND ("return to sport"[tiab] OR "return to play"[tiab] OR rehabilitation[tiab])', "PLC RTS criteria"),
]
for q, l in Q: pubmed(q, l)

def epmc(q, label):
    r = get("https://www.ebi.ac.uk/europepmc/webservices/rest/search", {"query": q, "format": "json", "pageSize": 50, "resultType": "core"}).json()
    LOG.append({"db": "EuropePMC", "label": label, "query": q, "hits": r.get("hitCount", 0)})
    for it in r.get("resultList", {}).get("result", []):
        key = "PMID:" + it["pmid"] if it.get("pmid") else "EPMC:" + it["id"]
        rec = RECS.setdefault(key, {"pmid": it.get("pmid", ""), "doi": it.get("doi", ""), "sources": []})
        rec.setdefault("title", it.get("title", "")); rec.setdefault("year", it.get("pubYear", ""))
        if not rec.get("abstract"): rec["abstract"] = it.get("abstractText", "")
        rec.setdefault("first_author", (it.get("authorString") or "").split(" ")[0])
        rec["sources"].append("EuropePMC:" + label)
    time.sleep(1)
epmc('TITLE:"fibular collateral ligament" AND "professional football"', "seed: Aspetar FCL pro football")
epmc('TITLE:"lateral collateral ligament" AND (TITLE:"combat" OR TITLE:"martial" OR TITLE:"algorithm")', "seed: ISAKOS 2021 combat-sports algorithm")
epmc('ISSN:"2224-8579" OR JOURNAL:"Aspetar Sports Medicine Journal" AND "collateral"', "seed: Aspetar journal")
json.dump(LOG, open(f"{OUT}/search_hits.json", "w"), indent=1); json.dump(RECS, open(f"{OUT}/records.json", "w"), indent=1)
for l in LOG[-13:]: print(l["db"], l["label"], l["hits"])
