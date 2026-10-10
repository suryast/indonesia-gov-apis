# SIGAP / InaRisk — Disaster Risk Assessment

**Agency:** BNPB (Badan Nasional Penanggulangan Bencana)
**Portal:** https://sigap.bnpb.go.id
**Kind:** government; **catalog ID:** `sigap-inarisk`; **tier:** tier7
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

No official contract for the historical `/api/risk/score` route or its illustrative response was established. Do not convert a map-layer legend into a property-level safety score. Verify layer date, scale, methodology and permissions; disaster-risk information is not a real-time emergency warning.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Separate official publications from community indexes. Map layers, complaint systems and legal search tools have different permissions; do not assume a public API from an accessible landing page.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** BNPB (Badan Nasional Penanggulangan Bencana)
**Portal:** https://sigap.bnpb.go.id | https://inarisk.bnpb.go.id
**API type:** ✅ REST API + WMS

## Overview
Indonesia Disaster Risk Index (IRBI) by kabupaten/kota. Flood, earthquake, tsunami, volcanic risk scores. Essential for property and location risk assessment.

## Usage
```python
import requests

# Get risk score by coordinates
resp = requests.get("https://inarisk.bnpb.go.id/api/risk/score", params={
    "lat": -6.2088,
    "lon": 106.8456,
})
risk = resp.json()
# Returns risk scores by hazard type (flood, earthquake, tsunami, etc.)
```

## Gotchas
1. InaRisk REST API: `inarisk.bnpb.go.id/api`
2. Returns risk scores per hazard type for given coordinates
3. WMS layers also available for map visualization
4. Complements BMKG data for comprehensive disaster awareness

</details>
