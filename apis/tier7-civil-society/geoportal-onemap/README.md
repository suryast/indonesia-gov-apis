# Indonesia Geoportal — One Map Policy

**Agency:** BIG / KLHK / Multiple
**Portal:** https://geoportal.indonesia.go.id
**Kind:** government; **catalog ID:** `geoportal-onemap`; **tier:** tier7
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

An HTML `/home` page is not a verified WMS endpoint. Discover services from publisher metadata and GetCapabilities before using layer names, permissions, axis order or projections. The old 85-layer count is historical and unverified.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Separate official publications from community indexes. Map layers, complaint systems and legal search tools have different permissions; do not assume a public API from an accessible landing page.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** BIG / KLHK / Multiple
**Portal:** https://geoportal.indonesia.go.id
**API type:** ✅ WMS/WFS/REST

## Overview
Implementation of One Map Policy. 85 thematic maps including forest concessions, plantation licenses, HGU land, oil & gas blocks. Critical for spatial compliance.

## Usage
```python
import requests

# WMS GetCapabilities
resp = requests.get("https://geoportal.indonesia.go.id/home", params={
    "service": "WMS",
    "version": "1.1.1",
    "request": "GetCapabilities",
})

# WFS for vector data
resp = requests.get("https://map.big.go.id/wfs", params={
    "service": "WFS",
    "version": "2.0.0",
    "request": "GetFeature",
    "typeName": "ne:batas_desa_desil_all",
    "outputFormat": "json",
    "maxFeatures": 100,
})
```

## Key Layers
- Administrative boundaries (province, kabupaten, desa)
- Forest concessions (HPH, HTI)
- Mining permits (IUP)
- Spatial planning (RTRW)

## Gotchas
1. WMS/WFS services from 20+ agencies
2. `map.big.go.id/wfs` for admin boundary vector data
3. RTRW zoning layers available
4. Some layers require specific agency WMS endpoints

</details>
