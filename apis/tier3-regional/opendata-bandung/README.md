# Open Data Kota Bandung — Bandung City Open Data

**Agency:** Pemerintah Kota Bandung
**Portal:** https://opendata.bandung.go.id
**Kind:** government; **catalog ID:** `opendata-bandung`; **tier:** tier3
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

One bounded GET of the historical CKAN search route on 2026-10-10 observed HTTP 404, http_error. This does not establish a working CKAN API or prove that the portal has no other API.[24]

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Portal technology and download access must be checked separately. Do not assume CKAN, a datastore, an authless API or a universal quota from a regional portal name.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Pemerintah Kota Bandung
**Portal:** https://opendata.bandung.go.id
**API type:** ✅ CKAN API

## Overview

Bandung was one of Indonesia's earliest adopters of open data, driven by its smart city program. Datasets include air quality, traffic conditions, budget, social services, and UMKM data.

## CKAN API

```python
import requests

CKAN = "https://opendata.bandung.go.id/api/3/action"

# Search datasets
resp = requests.get(f"{CKAN}/package_search", params={
    "q": "kualitas udara",
    "rows": 10,
})
for ds in resp.json()["result"]["results"]:
    print(ds["title"])

# Get dataset details
resp = requests.get(f"{CKAN}/package_show", params={"id": "dataset-slug"})
dataset = resp.json()["result"]
```

## Gotchas

1. **Early adopter** — dataset catalog is mature but some older datasets are stale
2. **Smart city data** — IoT sensor data (air quality, traffic) available in some datasets
> Historical access/limit assertion withdrawn; verify publisher guidance.
4. **Bahasa Indonesia** — all metadata in Indonesian

</details>
