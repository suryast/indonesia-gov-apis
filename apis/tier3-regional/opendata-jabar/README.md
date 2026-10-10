# Open Data Jabar — Jawa Barat Provincial Open Data

**Agency:** Pemerintah Provinsi Jawa Barat
**Portal:** https://opendata.jabarprov.go.id
**Kind:** government; **catalog ID:** `opendata-jabar`; **tier:** tier3
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

One bounded GET of the historical CKAN search route on 2026-10-10 observed HTTP 403, http_error. This does not establish a working CKAN API or prove that the portal has no other API.[21]

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Portal technology and download access must be checked separately. Do not assume CKAN, a datastore, an authless API or a universal quota from a regional portal name.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Pemerintah Provinsi Jawa Barat
**Portal:** https://opendata.jabarprov.go.id
**Statistical tables:** https://data.jabarprov.go.id
**API type:** ✅ CKAN API

## Overview

Jawa Barat (West Java) has one of Indonesia's more active regional open data programs. Datasets span agriculture, population, economy, health, and education. Also integrates with Pikobar (COVID-era dashboard) and Jabar Saber Hoaks fact-checking.

## CKAN API

```python
import requests

CKAN = "https://opendata.jabarprov.go.id/api/3/action"

# Search datasets
resp = requests.get(f"{CKAN}/package_search", params={
    "q": "penduduk",
    "rows": 10,
})
for ds in resp.json()["result"]["results"]:
    print(ds["title"])

# Query dataset records
resp = requests.get(f"{CKAN}/datastore_search", params={
    "resource_id": "resource-id-here",
    "limit": 100,
})
records = resp.json()["result"]["records"]
```

## Statistical Tables Portal

```python
# data.jabarprov.go.id has structured statistical tables (non-CKAN)
resp = requests.get("https://data.jabarprov.go.id/api/bigdata/bps/v2", params={
    "kode_provinsi": "32",  # 32 = Jawa Barat
    "kode_kabkota": "3201",  # optional kabupaten/kota filter
    "id_dataset": "dataset-id",
})
```

## Gotchas

1. **Two portals** — CKAN at `opendata.jabarprov.go.id` + stat tables at `data.jabarprov.go.id`
2. **CKAN is primary** — use it for bulk data download
> Historical access/limit assertion withdrawn; verify publisher guidance.
4. **38 kabupaten/kota** in Jawa Barat — largest province by # of cities
5. **Bahasa Indonesia only** — all metadata and data in Indonesian

</details>
