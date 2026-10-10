# BNPB — Disaster Data & Risk Portal

**Agency:** Badan Nasional Penanggulangan Bencana (National Disaster Management Agency)
**Portal:** https://data.bnpb.go.id
**Kind:** government; **catalog ID:** `bnpb-disaster`; **tier:** tier1
**Review date:** 2026-10-10; **review state:** endpoint_observed

## Reviewed guidance

One bounded GET of the historical CKAN search route on 2026-10-10 observed HTTP 200, ckan_shape_observed. A JSON CKAN success/result/results shape was observed for dataset search only; datastore access and the separate risk-score routes are unverified.[26]

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Tier 1 is a historical routing group, not an assurance of an open API. Confirm the publisher, license, endpoint and response shape before integration.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Badan Nasional Penanggulangan Bencana (National Disaster Management Agency)
**Data Portal:** https://data.bnpb.go.id
**InaRisk:** https://inarisk.bnpb.go.id
**API type:** ✅ REST JSON + CKAN-based data portal

## Overview

Two distinct services:
1. **data.bnpb.go.id** — CKAN portal with historical disaster event datasets
2. **InaRisk** — Risk scoring API by geographic coordinates (IRBI index)

## InaRisk — Risk Score by Coordinate

```python
import requests

resp = requests.get("https://inarisk.bnpb.go.id/api/risk/score", params={
    "lat": -6.2088,
    "lon": 106.8456,
}, timeout=15)
risk = resp.json()
# Returns per-hazard risk scores (flood, earthquake, tsunami, landslide, etc.)
print(risk)
```

### Risk Score Response

> Historical illustrative JSON response removed: not independently observed.


## IRBI — Disaster Risk Index by Kabupaten (Annual)

```python
resp = requests.get("https://inarisk.bnpb.go.id/api/irbi", params={"tahun": 2023})
irbi_data = resp.json()

top10 = sorted(irbi_data, key=lambda x: x.get("skor_total", 0), reverse=True)[:10]
for area in top10:
    print(f"{area['kabkota']}: {area['skor_total']}")
```

## Historical Events (CKAN)

```python
resp = requests.get("https://data.bnpb.go.id/api/3/action/package_search", params={
    "q": "banjir 2024",
    "rows": 20,
})
for ds in resp.json()["result"]["results"]:
    print(ds["title"], "—", ds.get("num_resources", 0), "resources")
```

## Hazard Types

| Bahasa | English |
|--------|---------|
| `banjir` | Flood |
| `gempa` | Earthquake |
| `tsunami` | Tsunami |
| `longsor` | Landslide |
| `gunung_api` | Volcanic eruption |
| `kekeringan` | Drought |
| `kebakaran_hutan` | Forest fire |

## Gotchas

1. **Two separate systems** — InaRisk API and data.bnpb.go.id CKAN are unrelated
2. **IRBI is annual** — updated once a year, covers all 514 kabupaten/kota
3. **CKAN API** — standard CKAN toolkit applies for the data portal
> Historical access/limit assertion withdrawn; verify publisher guidance.
5. **GeoJSON downloads** available for hazard zone polygons via data portal

</details>
