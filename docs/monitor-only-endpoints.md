# Monitoring-only endpoints

This inventory preserves the **18 additions** obtained by AST comparison of
`087e244:status/check.py` and `0508c7b` (`origin/main`) `status/check.py`.
Upstream provenance: `status/2026-10-10-update.md`; this is repository evidence,
not independent API verification. The machine inventory is
[catalog/monitor-only.json](../catalog/monitor-only.json).

The 59 canonical source documents remain a separate population. Their 57 mapped
monitor IDs plus these 18 monitoring-only IDs cover 75 configured monitors.
These rows create no source documents and do not certify APIs, publisher identity,
licensing, authentication, quotas or response contracts. Names, URLs, agency and
tier labels below are retained verbatim from upstream, not independently verified.
All entries are **unverified**, reviewed as inventory on October 10, 2026.

Only public GET of the exact configured URL is in scope. Do not log in, submit
complaints, search beneficiary/personal records, bypass CAPTCHAs or collect in bulk.
Complaint and social-assistance fronts are not public personal-record APIs.
Respect publisher access limits; permission and quotas remain unverified.

A content marker is an approximate body-text heuristic, not an API contract or
schema validation. HTTP success alone is not functional API verification. A 403
is an observed access block and a timeout is a probe-local transport observation;
neither proves a global outage or its cause. No live requests were made for this
inventory.

| ID | Upstream name | Configured URL | Agency | Tier | Surface (inventory classification) |
| --- | --- | --- | --- | --- | --- |
| `inaproc-api` | INAPROC Data API (docs) | `https://data.inaproc.id/docs/dokumentasi/guides/migration-from-isb` | LKPP | 9 | Documentation page (not API execution) |
| `inaproc-satudata` | Satu Data eProc | `https://inaproc.id/satudata` | LKPP | 9 | Procurement landing page |
| `sirup` | SIRUP / RUP | `https://sirup.inaproc.id` | LKPP | 9 | Procurement landing page |
| `bgn-sppg` | SPPG Operasional (MBG) | `https://www.bgn.go.id/operasional-sppg` | BGN | 9 | Program listing front |
| `cekbansos` | Cek Bansos | `https://cekbansos.kemensos.go.id/` | Kemensos | 9 | Social-assistance front; no personal-record search |
| `djpk-sikd` | Portal Data SIKD (APBD) | `https://djpk.kemenkeu.go.id/portal/data/apbd` | DJPK Kemenkeu | 9 | Budget data portal front |
| `pihps` | PIHPS Harga Pangan | `https://www.bi.go.id/hargapangan` | BI | 9 | Food-price landing page |
| `panelharga` | Panel Harga Pangan | `https://panelharga.badanpangan.go.id/` | Bapanas | 9 | Food-price dashboard front |
| `sdi-ckan` | Satu Data CKAN API | `https://katalog.data.go.id/api/3/action/package_search?rows=0` | Bappenas | 10 | Configured CKAN endpoint; contract unverified |
| `bmkg-forecast` | BMKG Forecast API | `https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=31.71.03.1001` | BMKG | 10 | Configured forecast endpoint; contract unverified |
| `bnpb-ckan` | Satu Data Bencana (CKAN) | `https://data.bnpb.go.id/api/3/action/status_show` | BNPB | 10 | Configured CKAN endpoint; contract unverified |
| `referensi-pendidikan` | Data Referensi Pendidikan | `https://referensi.data.kemendikdasmen.go.id/` | Kemendikdasmen | 10 | Education reference front |
| `sipp-jakut` | SIPP PN Jakarta Utara | `https://sipp.pn-jakartautara.go.id/` | MA | 11 | Court case-information front; no personal-record search |
| `sipp-sleman` | SIPP PN Sleman | `https://sipp.pn-sleman.go.id/` | MA | 11 | Court case-information front; no personal-record search |
| `sipp-medan` | SIPP PN Medan | `https://sipp.pn-medankota.go.id/` | MA | 11 | Court case-information front; no personal-record search |
| `sipp-palembang` | SIPP PN Palembang | `https://sipp.pn-palembang.go.id/` | MA | 11 | Court case-information front; no personal-record search |
| `sipp-semarang` | SIPP PN Semarang | `https://sipp.pn-semarangkota.go.id/` | MA | 11 | Court case-information front; no personal-record search |
| `jdihn` | JDIHN | `https://jdihn.go.id/` | BPHN | 11 | Legal-document landing page |
