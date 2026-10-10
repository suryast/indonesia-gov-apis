# Source review — October 10, 2026

## Scope and counting

The inventory was enumerated from `apis/**/README.md` and `references/**/*.md`,
not hand-counted from the old README. Before this refresh there were **53 source
documents**, including BAPPEBTI and the Japan NTA reference, and **11 supplementary
guides**. The old README advertised 57 but its numbered table ended at 56, had
five tier-8 entries without documents, and described tier 7 as five despite six
rows. This review creates the five missing documents and preserves the newly merged
Aturan.org contribution, producing **59 source records: 58 Indonesia-related
and one international reference**. These are
records of documentation, not unique agencies, distinct portals or verified APIs.

Portal/backend overlaps are explicit catalog `related_sources`. The BPJPH CMS
reference is not a second independently verified certification database, and the
KSEI, DJPB, geospatial and health records can describe overlapping services.
The 11 `references/` guides are mapped to their canonical sources and not counted
again. BAPPEBTI, NTA, OGP Indonesia and Aturan.org are explicitly unmonitored; monitored
endpoint IDs have a separate, exact mapping to `status/check.py`.

## Evidence levels and limits

- **unverified:** inventory and conservative documentation review only. Existing
  URLs/publisher labels may be stale. `document_inventory` evidence explicitly says
  the URL was not independently validated; it is not a successful live test.
- **primary_documentation_reviewed:** publisher documentation was directly read
  or, where retrieval failed, its search-indexed text was reviewed. The acquisition
  method and limitation are recorded below and in the catalog. This does not
  prove operational API access, authentication or response correctness.
- **endpoint_observed:** the exact bounded request and response-shape test was
  observed. This review uses that state only for BNPB CKAN dataset search.

Every source document was read and scanned for access/auth assumptions, invented
response examples, quotas, counts, geography claims, login/privacy issues and
bypass recommendations. High-risk recipes were replaced; other historical
endpoint/parsing context is in clearly marked, superseded historical sections.
Illustrative JSON responses and bypass/stealth/proxy recipes were removed rather
than represented as observed data. No credentials, personal-record queries,
health/tax data, declaration downloads or authenticated integrations were used.

Direct network requests were bounded to public documentation and metadata. Some
official sites returned transport failures from this host. The local browser
helper failed to start because of a scratch-profile lock permission error;
no browser search was completed. Failed retrieval is not evidence of global
outage, geographic restriction or project closure. External URL checks in the
catalog validator are syntactic. The separate [link audit report](link-audit-2026-10-10.md)
and [JSON snapshot](link-audit-2026-10-10.json) record link-status observations,
not API validation or permission to access data.

## High-risk corrections

### BPJPH: supervisor is not a certification record

BPJPH's directly retrieved article describes penyelia halal as an internal
assurance role. Supervisor-search data cannot be represented as a validated
business/product certificate database. The old business-shaped response, record
counts, certificate joins and bulk-person enumeration were withdrawn.[1]

The directly retrieved agency profile describes BPJPH as a non-ministerial
agency accountable to the president; the stale Kemenag attribution was removed.
No supervisor endpoint or certification query was run.[2]

### OJK: SIKePO and crypto authority

OJK's directly retrieved developer listing identifies SIKePO as **Sistem Informasi
Ketentuan Perbankan Online**, a banking-regulation search application. It is not
a fintech/crypto platform registry. The catalog points to it as regulations,
not proof of a financial entity's authorization.[3]

An indexed OJK release records the crypto/digital-financial-assets duty transfer
on January 10, 2025. Another indexed release states the transition ended on
January 20, 2026. BAPPEBTI crypto lists are historical references, not current
OJK licensing evidence. These dates were read from official indexed releases;
no regulator licensing API was exercised.[9][29]

### BPS: official key contract, not invented indicator meanings

Search-indexed official documentation confirms key-token identification and JSON
responses. Direct developer/documentation retrieval timed out. The fixed var=1
CPI mapping, indicator table, Gregorian-period assumptions and 100/day quota were
not substantiated and were withdrawn. Current metadata discovery and response
schema still need an authorized, credential-backed check; this review did not
execute one.[4]

### BMKG: current official public JSON documentation

Directly retrieved weather documentation describes three-day village/kelurahan
forecasts using `adm4` on the public JSON forecast endpoint, updated twice daily.
It states 60 requests/minute/IP and mandatory BMKG attribution. Province XML
recipes are not the recommended current interface.[5]

The separately retrieved earthquake documentation distinguishes M5+ and felt
earthquakes and lists JSON/XML feeds. This is documentation confirmation, not a
live end-to-end forecast/earthquake integration test.[6]

### Health, tax, building and election restrictions

Directly retrieved SATUSEHAT documentation requires approved partner access,
OAuth2 `client_credentials` and organization-specific validation, and prohibits
sharing secret access codes. It is not an open patient-record feed. The separate
public-facility references cannot establish anonymous health API access.[8]

Directly retrieved DJP guidance states Coretax serves tax administration from
January 2025 onward, with taxpayer account workflows. The old 2024 rollout
claim, anonymous NPWP lookup and ID-length/type heuristic were withdrawn.
No taxpayer-account operation or individual ID lookup was attempted.[15]

KPU's Info Pemilu entry was found in the primary-source index, but direct retrieval
failed and no general JSON API contract was verified. SIMBG's dashboard returned
an HTML application shell; its landing response does not verify public permit
search, record coverage or an API contract. Applicant/voter personal records were
not queried.[13][14]

BI's statistical page could not be fully retrieved from this host. Guessed
statistics API routes, a publication-time assertion and a payment-transfer
sandbox example were removed. No current statistics API contract is claimed.[16]

## Bounded CKAN checks

One unauthenticated GET per historical `package_search?rows=0` route was made
with a 15-second timeout and bounded body inspection. No dataset records were
published. Results below are host/date-specific, not permanent portal diagnoses.

| Historical candidate | Exact observation | What it does not prove |
|---|---|---|
| data.go.id | HTTP 404 | No functioning CKAN contract at that tested route; other APIs unknown.[19] |
| Satu Data Jakarta | HTTP 200, `text/html`, not JSON | Landing/SPA response is not API success.[20] |
| Open Data Jabar | HTTP 403 | Access denial does not reveal framework or geographic policy.[21] |
| Open Data Jatim | HTTP 403 | Same limitation; no bypass attempted.[22] |
| Satu Data Surabaya | HTTP 404 | Old path failed; replacement interface unknown.[23] |
| Open Data Bandung | HTTP 404 | Old path failed; replacement interface unknown.[24] |
| Open Data Bali | Transport `URLError` | No global outage or DNS cause inferred.[25] |
| BNPB data portal | HTTP 200, JSON `success: true`, object `result`, list `results` | Dataset-search CKAN shape only; datastore, licenses, freshness and risk APIs unverified.[26] |

The claim that every national/regional portal uses one CKAN pattern is withdrawn.
In particular, the plausible `/api/risk/score` InaRisk URL and sample scores were
never official evidence and remain historical/unverified; no property safety
assessment should use them without a verified publisher contract.

## Issue #1: dedicated LHKPN correction

The live GitHub issue was read via the public API. It was opened March 11, 2026,
reports a 404 for the old documented script, and links a suggested community
repository in a comment. It remained open during this read-only review; no issue
state/comment was changed.[17]

The removed recipe assumed an unsupported direct search route and invented DOM
selectors/detail ID. This is a repository documentation defect. The precise
server-side reason for the historical 404 is **not** established: current direct
requests returned `URLError`, not a reproduced 404.

Official search-indexed portal guidance describes public **e-Announcement** with
name/NIK, reporting year and institution filters, manual CAPTCHA, **Cari**, and
**Preview Cetak Pengumuman**, followed by the **Siapakah Anda** downloader form.
The indexed official FAQ separately describes account activation/login for
**e-Filing**. Do not conflate public announcement search with an official's
filing-account requirement merely because the shared portal URL contains `login`.
The exact current fragment, DOM schema, CAPTCHA type and session/API internals
were not confirmed from directly retrieved HTML. No public JSON replacement API
is claimed.[7]

The suggested repository's README/source were read, not executed. They advertise
Playwright extraction and stealth and use a fragment-based announcement URL;
these are third-party implementation claims, not verified KPK instructions. No
selectors, anti-detection code or personal records were copied. The dedicated
documentation now provides official manual guidance and precise limitations;
`tests/test_lhkpn_docs.py` guards against reintroducing broken routes, fake
selectors/detail ID or false public-API success claims.[27][28]

## PR #9: merged contribution preserved with caveats

PR #9 was open and unmerged during the initial read-only review. The fetched
`origin/main` now records its merge on October 10, 2026 at commit `21cfe4b`.
Its new Aturan.org source document is preserved in this worktree and adopted as
one non-government tier-7 documentation record with empty `monitor_ids`.[18]
The unsupported March historical AU/ID availability badges are not copied.

Current publisher pages were directly read again with bounded unauthenticated
GETs (12-second timeout, 1.5 MB body cap, verified TLS): the home, REST and MCP
documentation pages each returned HTTP 200 HTML. REST docs specify Bearer API-key
authentication and discovery-before-reading; MCP docs specify Streamable HTTP at
`https://mcp.aturan.org/mcp` with OAuth/API-key options. A separate unauthenticated
GET of that transport returned HTTP 401, not a successful protocol session.
No MCP initialization, tool execution, credential request or login was performed.[10][11][12]

The corrected official BPK regulations portal is `https://peraturan.bpk.go.id`.
Direct GET returned HTTP 403 here, so this final reconciliation did not retrieve
the portal content or independently establish Aturan.org's ingestion/provenance
chain. The corrected portal domain is retained, not asserted as a verified
corpus attribution. Verify each original document with its publisher.
Numeric corpus totals, completeness, OCR accuracy and daily freshness remain
unverified and are not adopted. Privacy, terms and authorized schema/protocol
checks remain prerequisites for integration.[30]

## Validation and outstanding work

`catalog/sources.json` stores exact per-record evidence/acquisition limits and
separate source/reference totals. `scripts/validate_catalog.py` checks schema,
source/reference coverage, unique IDs/paths, totals, monitor mapping, README
coverage and local links/anchors. `tests/test_catalog.py` includes mutation tests
for missing records, duplicate identities, invalid URLs/dates/access/evidence and
malformed inputs. These are offline consistency tests, not live API certification.

Outstanding live work: authenticated BPS metadata/query verification; official
BPJPH certificate interface/permissions; direct KPK UI/manual/session confirmation;
sector-specific OJK license publications; most ministry/regional download routes;
third-party terms and protocol integrations. Unverified catalog entries remain
unverified rather than receiving a blanket working label. Historical status files,
examples, monitoring, CI and deployments are owned by other upgrade lanes.

## Later upstream monitoring reconciliation

PR #10 was merged into `main` on October 10, 2026 (`0508c7b`) during this upgrade. Its 18 added probes and four moved portal URLs are preserved, making 75 monitored endpoints. [Monitoring-only documentation](monitor-only-endpoints.md) and a [separate exact registry](../catalog/monitor-only.json) cover the 18 additions without turning them into additional verified APIs or inflating the 59 source-document count. The revised checker retains transport-specific errors, secure local-only probing and explicit unknown geographic metadata. Expected-text checks are bounded heuristics; absence, truncation and transport failure are not interchangeable diagnoses. The upstream [dated expansion note](../status/2026-10-10-update.md) records its original implementation context; subsequent live observations belong to the generated status data, not invented historical badges.

## Verification results

Executed after the documentation edits: `python scripts/validate_catalog.py`
passed with 58 source records and 11 supplementary guides; catalog tests passed
19/19 and LHKPN documentation regressions passed 7/7. `git diff --check` and strict
citation-ledger validation passed. A scripted scan of all 69 source/guide documents
found no removed bypass recipe, broken LHKPN route/detail placeholder or old
BPJPH-business-total pattern. The catalog maps 57 monitor IDs independently of
its documentation total. These checks do not imply that unverified live APIs work.

## Final broken-link remediation — October 10, 2026

All **14 exact HTTP-404 URL identities** in the first-pass Markdown audit are
classified in their affected source context. Current recommendations for Komdigi,
DJPB budget, KSEI statistics and ESDM were replaced with the verified publisher
navigation below; catalog `portal_url`, evidence and per-source guidance agree.
Review states remain unverified for data/API functionality. Historical failed URLs
are retained as dated observations, not active recipes; a repeat audit can still
report their 404s. No audit report or monitoring observations were rewritten.

Verified-TLS unauthenticated GETs used curl with 5-second connect / 18-second total
timeouts, five redirects maximum and a 2 MB body cap. HTML titles/navigation were
inspected; no authenticated query, personal-record lookup, proxy or CAPTCHA bypass
was used. These are publication/landing checks, not API, PDF-download, external
fragment or data-freshness verification.

| Current publisher navigation | Observed result | Scope |
|---|---|---|
| https://data.komdigi.go.id | HTTP 200; final trailing-slash root; Portal Satu Data HTML shell | Publisher portal only; `/opendata` and `/opendata/desa-broadband` unavailable, replacement data contract unverified |
| https://djpb.kemenkeu.go.id/portal/id/berita/lainnya/realisasi-apbn.html | HTTP 200; Realisasi APBN / i Account HTML index | Followed publisher data/navigation link; dated report archive, not real-time API |
| https://web.ksei.co.id/publications/Data_Statistik_KSEI | HTTP 200; Data Statistik KSEI HTML index | Linked from official web.ksei.co.id home; monthly PDF links observed, individual files not validated |
| https://www.esdm.go.id/en/publikasi/handbook-of-energy-economic-statistics-of-indonesia | HTTP 200; HEESI HTML publication index | Annual handbook PDF links observed; downloads and mining API unverified |
| https://kkp.go.id | HTTP 200; final trailing-slash root | Agency navigation, not a replacement conservation data endpoint |
| https://oss.go.id | HTTP 200; final `/id` | Publisher navigation, not anonymous NIB search confirmation |
| https://simas.kemenag.go.id | HTTP 200; final trailing-slash root | Publisher navigation, not a replacement search endpoint |
| https://pasal.id | HTTP 200; final trailing-slash root | Third-party project navigation only, not official legal data/API validation |

Withdrawn historical recipes cover DJPB's `.html` data path, Komdigi catalog and
village path, KKP conservation path, OSS cari-nib, SIMAS search, ESDM handbook and
KSEI statistics. Both KSEI statistics URL host variants remain explicitly historical
404s. The guessed pasal MCP-root REST recipe was removed; `/mcp` separately returned
406 in the audit and was not diagnosed as 404 or protocol-tested. March 29 discovery
project names remain in publication history with October 10 404/unavailable notes;
the inaccessible signal-monitor hyperlink was removed from current README guidance.
Unrelated blocked, DNS-error and timeout links were not removed. A supplemental
attempt at a www.ksei.co.id PDF timed out; no availability claim is made for it.

Parent's supplemental static-HTML evidence records HTTP 200 for the Datarakyat
navigation, GitHub repository, status-page canonical URL and actual Google Fonts
CSS request; local `BaksoSapi.otf` exists. Google Fonts preconnect-only origin roots
returned 404: origin hints are not navigational links, and the CSS request succeeded.
External fragments and font binary retrieval were not verified by these checks.

Final scoped offline checks: catalog validator passed (58 sources / 11 guides),
catalog tests **19/19**, LHKPN docs **7/7**, link-audit tests **14/14** and
`git diff --check` passed. Parent reruns the full Markdown hash/status audit after
these edits; historical 404 observations are intentionally not erased.

## Upstream reconciliation verification

After preserving PR #9: catalog validator passed with **59 source records
(58 Indonesia-related + 1 NTA), tier 7 seven, and 11 guides**. Catalog tests
passed **20/20**, including an Aturan preservation regression; LHKPN docs passed
**7/7**. `.venv/bin/python scripts/check_repository.py` passed all **91 tests**,
the canonical-status regression, catalog validation, Ruff and offline zizmor;
`git diff --check` passed. The initial default-Python full check could not import
`requests`; rerunning in the existing project virtualenv resolved that environment
issue. Earlier 58-source verification figures above describe pre-reconciliation
checks. Parent must rerun the final all-links audit against these stable edits.
No monitor, status data, scripts, CI or audit reports were changed by this lane.

## Sources

[1] https://bpjph.halal.go.id/read/bpjph-penyelia-profesi-baru-penguat-ekosistem-halal-indonesia
[2] https://bpjph.halal.go.id/read/tentang-bpjph
[3] https://play.google.com/store/apps/details?hl=id&id=com.ojk.sikepo
[4] https://webapi.bps.go.id/documentation
[5] https://data.bmkg.go.id/prakiraan-cuaca
[6] https://data.bmkg.go.id/gempabumi
[7] https://elhkpn.kpk.go.id/portal/user/login
[8] https://satusehat.kemkes.go.id/platform/docs/id/api-catalogue/authentication
[9] https://ojk.go.id/en/berita-dan-kegiatan/siaran-pers/Pages/Bappebti-Transfers-Regulation-and-Supervision-Duties-on-Digital-Financial-Assets-Crypto-Assets-and-Derivatives-to-OJK-BI.aspx
[10] https://aturan.org
[11] https://aturan.org/api
[12] https://aturan.org/mcp
[13] https://infopemilu.kpu.go.id
[14] https://simbg.pu.go.id/dashboard
[15] https://pajak.go.id/id/coretaxdjp
[16] https://www.bi.go.id/en/statistik/informasi-kurs/jisdor/Default.aspx
[17] https://github.com/suryast/indonesia-gov-apis/issues/1
[18] https://github.com/suryast/indonesia-gov-apis/pull/9
[19] https://data.go.id/api/3/action/package_search?rows=0
[20] https://satudata.jakarta.go.id/api/3/action/package_search?rows=0
[21] https://opendata.jabarprov.go.id/api/3/action/package_search?rows=0
[22] https://opendata.jatimprov.go.id/api/3/action/package_search?rows=0
[23] https://satudata.surabaya.go.id/api/3/action/package_search?rows=0
[24] https://opendata.bandung.go.id/api/3/action/package_search?rows=0
[25] https://data.baliprov.go.id/api/3/action/package_search?rows=0
[26] https://data.bnpb.go.id/api/3/action/package_search?rows=0
[27] https://github.com/nichsedge/lhkpn/blob/master/README.md
[28] https://github.com/nichsedge/lhkpn/blob/master/lhkpn_scraper.py
[29] https://ojk.go.id/id/berita-dan-kegiatan/siaran-pers/Pages/Nota-Kesepahaman-OJK-Bappebti-2026.aspx
[30] https://peraturan.bpk.go.id
