# Satu Data Surabaya — Surabaya City Open Data

**Agency:** Pemerintah Kota Surabaya
**Portal:** https://satudata.surabaya.go.id
**Kind:** government; **catalog ID:** `satu-data-surabaya`; **tier:** tier3
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

One bounded GET of the historical CKAN search route on 2026-10-10 observed HTTP 404, http_error. This does not establish a working CKAN API or prove that the portal has no other API.[23]

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Portal technology and download access must be checked separately. Do not assume CKAN, a datastore, an authless API or a universal quota from a regional portal name.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Pemerintah Kota Surabaya
**Portal:** https://satudata.surabaya.go.id
**Mirror:** https://opendata.surabaya.go.id
**API type:** ✅ CKAN API

## Overview

One of Indonesia's most complete city-level open data portals. Surabaya was an early adopter of open data. Covers demographics, UMKM registry, social welfare, public facilities, and city budget.

## CKAN API

```python
import requests

CKAN = "https://satudata.surabaya.go.id/api/3/action"

# Search
resp = requests.get(f"{CKAN}/package_search", params={
    "q": "UMKM",
    "rows": 20,
})
for ds in resp.json()["result"]["results"]:
    print(f"{ds['title']} — {ds.get('metadata_modified', 'N/A')}")

# Direct datastore access
resp = requests.get(f"{CKAN}/datastore_search", params={
    "resource_id": "resource-id",
    "limit": 1000,
})
```

## Notable Datasets

| Dataset | Description |
|---------|-------------|
| Data kependudukan | Population by RT/RW |
| UMKM terdaftar | Registered micro-enterprises |
| Fasilitas umum | Public facilities with coordinates |
| Realisasi APBD | City budget execution |
| Perizinan | Business permits issued |

## Gotchas

1. **Two URLs** — `satudata.surabaya.go.id` (primary) and `opendata.surabaya.go.id` (may redirect)
2. **e-Kinerja integration** — city performance data available alongside open data
3. **Data granularity** — some datasets go down to RT/RW level (very fine-grained)
4. **UMKM registry** — one of the more complete city-level SME registries

</details>
