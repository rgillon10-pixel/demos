# Search log — grade 3 LCL / PLC return to play

Run date: 2026-10-19. Scripts: `search.py` (pass 1), `search_extra.py` (pass 2: seed papers + gaps found while screening), `citation_chase.py` (Semantic Scholar). Raw query/hit log: `search_hits.json`.

**API status.** PubMed E-utilities and Europe PMC REST worked. OpenAlex returned HTTP 429 on every query even after 6 back-off retries, so citation chasing used Semantic Scholar instead (one of its searches was also rate-limited). PubMed dates were restricted to publication date 2000–2026. Europe PMC searches full text, which explains its high hit counts; only the first 300 records of query 9 were downloaded.

## Queries and hit counts

| # | Database | Purpose | Query | Hits |
|---|---|---|---|---|
| 1 | PubMed | core | `("lateral collateral ligament"[tiab] OR "fibular collateral ligament"[tiab] OR "posterolateral corner"[tiab]) AND ("grade III"[tiab] OR "grade 3"[tiab] OR complete[tiab] OR rupture[tiab] OR reconstruction[tiab] OR repair[tiab]) AND ("return to sport"[tiab] OR "return to play"[tiab] OR "return to sports"[tiab] OR "return to activity"[tiab]) AND humans[mh] AND english[la] NOT elbow[tiab] NOT ankle[tiab]` | 22 |
| 2 | PubMed | core-no-MeSH-humans (catches unindexed recent) | `("lateral collateral ligament"[tiab] OR "fibular collateral ligament"[tiab] OR "posterolateral corner"[tiab]) AND ("grade III"[tiab] OR "grade 3"[tiab] OR complete[tiab] OR rupture[tiab] OR reconstruction[tiab] OR repair[tiab]) AND ("return to sport"[tiab] OR "return to play"[tiab] OR "return to sports"[tiab] OR "return to activity"[tiab]) AND english[la] NOT elbow[tiab] NOT ankle[tiab]` | 45 |
| 3 | PubMed | isolated-FCL-athletes | `("lateral collateral ligament"[tiab] OR "fibular collateral ligament"[tiab]) AND (isolated[tiab]) AND (athlete*[tiab] OR football[tiab] OR soccer[tiab] OR NFL[tiab]) AND english[la] NOT elbow[tiab] NOT ankle[tiab]` | 16 |
| 4 | PubMed | repair-vs-recon | `("posterolateral corner"[tiab] OR "fibular collateral"[tiab] OR "lateral collateral ligament"[tiab]) AND (repair[tiab]) AND (reconstruction[tiab]) AND (failure[tiab] OR "systematic review"[pt] OR meta-analysis[pt]) AND english[la] NOT elbow[tiab] NOT ankle[tiab]` | 46 |
| 5 | PubMed | varus-stress-radiograph | `("varus stress"[tiab]) AND (radiograph*[tiab]) AND ("posterolateral"[tiab] OR "fibular collateral"[tiab] OR "lateral collateral"[tiab]) NOT elbow[tiab] NOT ankle[tiab]` | 64 |
| 6 | PubMed | multiligament-RTP | `("multiligament"[tiab] OR "multi-ligament"[tiab] OR "knee dislocation"[tiab]) AND ("return to play"[tiab] OR "return to sport"[tiab]) AND (athlete*[tiab] OR NFL[tiab] OR football[tiab] OR soccer[tiab]) AND english[la]` | 30 |
| 7 | PubMed | PLC-rehab-weightbearing | `("posterolateral corner"[tiab] OR "fibular collateral"[tiab]) AND (weightbearing[tiab] OR "weight bearing"[tiab] OR rehabilitation[tiab]) AND ("systematic review"[tiab] OR review[pt])` | 30 |
| 8 | PubMed | LCL-professional-case | `("lateral collateral ligament"[tiab]) AND knee[tiab] AND ("return-to-performance"[tiab] OR "case report"[tiab] OR "professional"[tiab]) AND (repair[tiab] OR reconstruction[tiab] OR rupture[tiab]) NOT elbow[tiab] NOT ankle[tiab]` | 29 |
| 9 | EuropePMC | core | `("lateral collateral ligament" OR "fibular collateral ligament" OR "posterolateral corner") AND ("grade III" OR "grade 3" OR complete OR rupture OR reconstruction OR repair) AND ("return to sport" OR "return to play") AND PUB_YEAR:[2000 TO 2026] AND LANG:eng NOT elbow NOT ankle` | 537 |
| 10 | EuropePMC | aspetar/pro-football | `("fibular collateral ligament" OR "lateral collateral ligament") AND "professional football" AND knee` | 57 |
| 11 | OpenAlex | FCL-athletes | `isolated fibular collateral ligament injuries athletes return to play` | HTTP 429 after 6 retries (no result) |
| 12 | OpenAlex | LCL-grade3-RTP | `lateral collateral ligament knee grade III return to play` | HTTP 429 after 6 retries (no result) |
| 13 | OpenAlex | PLC-repair-vs-recon | `posterolateral corner repair versus reconstruction failure systematic review` | HTTP 429 after 6 retries (no result) |
| 14 | OpenAlex | MLKI-NFL | `multiligament knee injuries NFL return to play` | HTTP 429 after 6 retries (no result) |
| 15 | PubMed | seed: Grawe JAAOS | `Grawe[au] AND "lateral collateral ligament"[ti]` | 1 |
| 16 | PubMed | seed: varus stress radiograph thresholds | `LaPrade[au] AND "varus stress"[tiab] AND radiograph*[tiab]` | 20 |
| 17 | PubMed | acute grade III PLC repair/recon | `("fibular collateral ligament"[tiab] OR "posterolateral"[tiab]) AND (acute[tiab]) AND ("grade III"[tiab] OR "grade-III"[tiab]) AND (repair[tiab] OR reconstruction[tiab])` | 19 |
| 18 | PubMed | repair vs recon in MLKI | `("fibular collateral ligament"[tiab] OR "posterolateral corner"[tiab]) AND repair[tiab] AND reconstruction[tiab] AND multiligament*[tiab]` | 51 |
| 19 | PubMed | FCL/LCL reconstruction outcomes | `("fibular collateral ligament reconstruction"[tiab] OR "lateral collateral ligament reconstruction"[tiab]) AND knee[tiab] AND (outcome*[tiab] OR "return"[tiab]) NOT elbow[tiab] NOT ankle[tiab]` | 9 |
| 20 | PubMed | LCL nonoperative | `("lateral collateral ligament"[tiab] OR "fibular collateral ligament"[tiab]) AND knee[tiab] AND (nonoperative[tiab] OR "non-operative"[tiab] OR conservative[tiab]) NOT elbow[tiab] NOT ankle[tiab]` | 42 |
| 21 | PubMed | LCL pivoting/combat sports | `("lateral collateral ligament"[tiab] OR "fibular collateral ligament"[tiab]) AND knee[tiab] AND (soccer[tiab] OR football[tiab] OR rugby[tiab] OR basketball[tiab] OR "mixed martial"[tiab] OR combat[tiab] OR judo[tiab] OR wrestl*[tiab]) NOT elbow[tiab] NOT ankle[tiab]` | 24 |
| 22 | PubMed | PLC/FCL RTS or Tegner | `("posterolateral corner"[tiab] OR "fibular collateral ligament"[tiab]) AND ("return to sport"[tiab] OR "return to play"[tiab] OR "Tegner"[tiab])` | 82 |
| 23 | PubMed | seed: Sikka 2015 | `"Isolated fibular collateral ligament injuries in athletes"[ti]` | 0 |
| 24 | PubMed | PLC RTS criteria | `"posterolateral corner"[tiab] AND (criteria[tiab]) AND ("return to sport"[tiab] OR "return to play"[tiab] OR rehabilitation[tiab])` | 10 |
| 25 | EuropePMC | seed: Aspetar FCL pro football | `TITLE:"fibular collateral ligament" AND "professional football"` | 0 |
| 26 | EuropePMC | seed: ISAKOS 2021 combat-sports algorithm | `TITLE:"lateral collateral ligament" AND (TITLE:"combat" OR TITLE:"martial" OR TITLE:"algorithm")` | 0 |
| 27 | EuropePMC | seed: Aspetar journal | `ISSN:"2224-8579" OR JOURNAL:"Aspetar Sports Medicine Journal" AND "collateral"` | 0 |
| 28 | Semantic Scholar | forward citations | Bushnell 2010 | 43 |
| 29 | Semantic Scholar | forward citations | Haslhofer 2025 | 0 |
| 30 | Semantic Scholar | forward citations | Sikka 2015 | 15 |
| 31 | Semantic Scholar | forward citations | Fortier 2023 | 16 |
| 32 | Semantic Scholar | forward citations | Mitchell 2024 | 1 |
| 33 | Semantic Scholar | search | isolated fibular collateral ligament injury professional football | 211 |
| 34 | Semantic Scholar | search | lateral collateral ligament combat sports algorithm reconstruction | HTTP 429 after 6 retries (no result) |
| 35 | Semantic Scholar | search | isolated lateral collateral ligament rupture knee athlete return | 344 |

## Screening flow

1. **Retrieved:** 635 unique records (PubMed + Europe PMC, deduplicated on PMID).
2. **Automatic pre-screen** (first pass only): kept records whose title/abstract contains *both* an RTP term (return to sport/play/activity/pre-injury level/competition, RTP, RTS) *and* an LCL/FCL/PLC/multiligament term, with no elbow/ankle/cadaver/thumb/wrist/shoulder in the title. This left 114 candidates. Second-pass records (queries 15–27) and Semantic Scholar hits were screened by title by hand, because the decision-threshold and failure studies seldom mention RTP.
3. **Abstracts read:** about 75 records. Full text was pulled from Europe PMC where open access (Bakshi 2018, Haslhofer 2025, Lutz 2021, Morris 2021, Paget 2017, Barrera Uso 2025). Haddad 2016 and Davenport 2018 returned only stubs.
4. **Included in `studies.csv`:** 24 studies in 35 rows (some studies give one row per treatment arm or injury pattern). Of these:
   - 16 report RTP. 10 are cohorts, systematic reviews or conference abstracts; 6 are case reports or tiny series (n≤3).
   - 8 are failure/laxity-only studies (no RTP). They are kept because research question 3 needs them, and are **never pooled for RTP**.

## Included studies and their role

| Study | Role |
|---|---|
| Bushnell 2010 (PMID 19966106) | Isolated, non-op vs repair, pooled |
| Haslhofer 2025 (41341507) | Isolated MRI grade 3 subset (n=27), non-op, pooled; baseline paper |
| Sikka 2015 (25545646) | Isolated NFL; numbers only second-hand via Haslhofer full text; not pooled |
| Haddad 2016, Davenport 2018, Gnesutta 2024, Mitchell 2024 | Isolated case reports/series; not pooled |
| Borque 2020 conference abstract (Europe PMC PMC7401073) | Combined, by cruciate base, pooled |
| Borque 2022 (35279739) | Combined, lateral subgroup n unknown, likely overlaps the 2020 abstract; not pooled |
| Lutz 2021 (33483769) | Combined reconstruction, ACL- vs PCL-based, pooled |
| Bakshi 2018 (29638200) | Combined NFL, treatment not reported, pooled alone |
| Minator Sajjadi 2022 (35721588) | Combined repair vs reconstruction (same-level only) |
| Barrera Uso 2025 (40416994) | Combined lateral subgroup extracted from patient tables (n=4); not pooled |
| LaPrade 2017, Paget 2017 | Combined case reports; not pooled |
| Fortier 2023 (37848567), White 2025 (39672245), Geeslin 2016 (26260464), Morris 2021 (33796586) | Systematic reviews; reported separately, never pooled with primary studies |
| Stannard 2005, Levy 2010, Moran 2022, Geeslin 2011, LaPrade 2010 | Failure/laxity only |

**Context papers.** These are cited in the README but are not RTP studies, so they are not in `studies.csv`:

- Thresholds and diagnosis: LaPrade 2008 (18829903) for the 2.7 / 4.0 mm varus-stress thresholds (a cadaver study, used only for the threshold); Kane 2018 (29884567) for stress radiographs vs MRI.
- Consensus: Chahla 2019 (30478468) and LaPrade 2025 (40414466).
- Review: Grawe 2018 (29443704).
- Pivoting-sport function testing: Ebert 2025 (39101299).

## Exclusions (records whose abstracts were read), with reasons

| Record | Reason |
|---|---|
| Soda 2022 (36873324), judo repair | No objective instability on varus stress XR, so not a documented grade 3 |
| Castle 2023 (37042501), PRP soldier | Grade not reported; return to military duty, not sport |
| Temponi 2019 (30719481), BJJ | Partial LCL tears (not grade 3) |
| Perry 2022 (35081054) | RTP not explicitly reported; noted only as a non-op failure that went on to repair |
| Lundblad 2020 (32494208), UEFA | LCL injuries of all grades pooled; lay-off not grade-specific |
| Chahla 2018 (29146160), NFL Combine | Outcome = draft position/games started, not RTP |
| Moulton 2015, Dekker 2021, Kennedy 2019, Plain 2026, Ramos 2019, Yeatts 2021, Godin 2017, Percutaneous LCL-R 2024 (37839902) | No RTP outcome (PROMs/Tegner/laxity only) |
| Hirschmann 2010, Cain 2024, Fine 2023, D'Ambrosi 2024, Trøan 2026, Ebert 2025, Jones 2025 (LARS), Suarez-Ahedo 2025, Poster 339 (PMC10392346) | Multiligament RTP data **not broken down by LCL/PLC involvement** in the retrieved text |
| Maheshwer 2021, Jackson 2024 | Failure SRs overlapping Fortier/White, or chronic-only; not needed |
| Mitchnik 2025 | Online rehab protocols, not patient outcomes |
| 24284050 and other cadaver studies | Cadaver-only (LaPrade 2008, 18829903, is cited only as the source of the 2.7/4.0 mm thresholds) |
| Wang 2024 (39287283), Cho 2020 and others | Ankle or other joint "lateral collateral ligament" |
| Pre-2000 (Kannus 1989; 3780082, 1986; 4436355, 1974) | Outside date range |
| Remaining ~40 pre-screen candidates | Off-topic by title/abstract (ACL-only, MCL-only, PCL-only, technique notes, imaging, other joints) |

## Seed papers not retrievable via the APIs (therefore not used)

- **ISAKOS 2021 ePoster 14413** (combat-sports algorithm, >2.7 mm → reconstruct, RTP ~28 wk). Not indexed in PubMed, Europe PMC or Semantic Scholar, and the isakos.com URL redirects to a generic congress page. **Its numbers are not used anywhere.**
- **Aspetar Sports Medicine Journal, "Isolated FCL injury in professional football".** Not indexed (Europe PMC queries 25–27 returned 0; Semantic Scholar did not find it). Not used.
- **Sikka 2015.** The abstract was retrieved but the full text was not; its NFL grade 3 numbers come second-hand from the Haslhofer 2025 full text, and this is flagged on the row.

## Known data issues

- Borque 2020 (abstract) and Borque 2022 share a senior surgeon and an overlapping period (2001–2015 vs 2001–2019), so only the 2020 abstract's injury-pattern table is pooled. The 2020 record lists no authors; its attribution to the same group is an inference from design and period.
- Sikka 2015 and Bushnell 2010 both use NFL athletes from overlapping eras. The author groups differ, but overlap can't be excluded, so Sikka is not pooled.
- Haslhofer's MRI grade 3 subgroup had clinical laxity of grade 0–2 only. It is pooled as "isolated non-op" but is **not** evidence for clinically grade 3 (gross laxity) tears.
- Fortier 2023 reports RTS only for subsets (22/22 reconstruction, 48/51 repair) that are smaller than its failure denominators.
