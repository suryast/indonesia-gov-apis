# Open Data Jawa Timur — East Java Provincial Open Data

**Agency:** Pemerintah Provinsi Jawa Timur
**Portal:** https://opendata.jatimprov.go.id
**Kind:** government; **catalog ID:** `opendata-jatim`; **tier:** tier3
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

One bounded GET of the historical CKAN search route on 2026-10-10 observed HTTP 403, http_error. This does not establish a working CKAN API or prove that the portal has no other API.[22]

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Portal technology and download access must be checked separately. Do not assume CKAN, a datastore, an authless API or a universal quota from a regional portal name.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Pemerintah Provinsi Jawa Timur
**Portal:** https://opendata.jatimprov.go.id
**API type:** ✅ CKAN API

## Overview

East Java's CKAN-based open data portal covering economy, infrastructure, employment, population, health, and tourism across 38 kabupaten/kota.

## CKAN API

```python
import requests

CKAN = "https://opendata.jatimprov.go.id/api/3/action"

# List all datasets
resp = requests.get(f"{CKAN}/package_list")
all_datasets = resp.json()["result"]

# Search
resp = requests.get(f"{CKAN}/package_search", params={
    "q": "kemiskinan",
    "rows": 20,
})
results = resp.json()["result"]["results"]

# Datastore query
resp = requests.get(f"{CKAN}/datastore_search", params={
    "resource_id": "resource-id",
    "limit": 500,
    "offset": 0,
})
records = resp.json()["result"]["records"]
```

## Gotchas

> Historical access/limit assertion withdrawn; verify publisher guidance.
2. **38 kabupaten/kota** — large province; filter by location field in datasets
3. **Dataset freshness varies** — check `metadata_modified` field per dataset
4. **Download formats** — mostly CSV and Excel; some GeoJSON for spatial data

</details>
