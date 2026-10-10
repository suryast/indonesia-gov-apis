# Satgas Waspada Investasi — Investment Fraud Alerts

**Agency:** OJK / Multi-agency task force
**Portal:** https://waspadainvestasi.ojk.go.id
**Kind:** government; **catalog ID:** `satgas-waspada`; **tier:** tier6
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Financial publications and alerts are time-specific. Confirm licensing with the relevant regulator; no alert match is not evidence of authorization or safety.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Financial publications and alerts are time-specific. Confirm licensing with the relevant regulator; no alert match is not evidence of authorization or safety.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** OJK / Multi-agency task force
**Portal:** https://waspadainvestasi.ojk.go.id
**API type:** ✅ Public list (scrapeable, frequently updated)

## Overview
Official list of illegal investment platforms, unlicensed MLM, robot trading scams, crypto frauds. Updated frequently. High-value data source.

## Usage
```python
import requests
from bs4 import BeautifulSoup

resp = requests.get(
    "https://waspadainvestasi.ojk.go.id/",
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    timeout=30,
)
soup = BeautifulSoup(resp.text, "html.parser")
# Parse alert list table
```

## Gotchas
1. Direct list page is scrapeable
2. High-value, frequently searched
3. Critical for any fintech legitimacy checker
4. Updated weekly — worth automating scrapes

</details>
