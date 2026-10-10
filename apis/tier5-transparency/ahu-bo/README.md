# AHU-BO — Beneficial Ownership Registry

**Agency:** Ditjen AHU
**Portal:** https://bo.ahu.go.id
**Kind:** government; **catalog ID:** `ahu-bo`; **tier:** tier5
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Record the original publisher and publication date. Third-party company or leak indexes are research leads, not findings of wrongdoing or current proof of registration.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Record the original publisher and publication date. Third-party company or leak indexes are research leads, not findings of wrongdoing or current proof of registration.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Kemenkumham AHU (Administrasi Hukum Umum)
**Portal:** https://bo.ahu.go.id
**API type:** ⚠️ Web search (limited public fields)

## Overview
Public-facing beneficial ownership search integrated with AHU company registry. Part of OECD/G20 transparency push. Shows ultimate beneficial owners of Indonesian legal entities. Launched 2019.

## Usage
```python
import requests
from bs4 import BeautifulSoup

resp = requests.get("https://bo.ahu.go.id/search", params={
    "q": "company name",
}, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
# Parse HTML response for BO data
```

## Gotchas
1. Basic name search only — limited public fields
2. More detailed data requires official access
3. Complements AHU company registry (ahu.go.id)

</details>
