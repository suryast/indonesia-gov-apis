# KKP — Fisheries & Maritime Data

**Agency:** Kementerian Kelautan dan Perikanan (Ministry of Marine Affairs and Fisheries)
**Portal:** https://satudata.kkp.go.id
**Kind:** government; **catalog ID:** `kkp-fisheries`; **tier:** tier4
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Distinguish public aggregate publications from ministry operational systems. No account-gated, student, patient, employee or land-owner records should be extracted without authorization.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Distinguish public aggregate publications from ministry operational systems. No account-gated, student, patient, employee or land-owner records should be extracted without authorization.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.


### Broken-link remediation — October 10, 2026

Use the [publisher navigation](https://kkp.go.id) (HTTP 200 landing/index observed October 10, 2026). Specific historical search/download routes below are unavailable; no data API or replacement search contract is verified.

- Historical failed route: `https://kkp.go.id/djprl/p4k/page/3-data-kawasan-konservasi` — HTTP 404 in the dated repository link audit; unavailable, not a working recipe.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Kementerian Kelautan dan Perikanan (Ministry of Marine Affairs and Fisheries)
**Portal:** https://satudata.kkp.go.id
**Statistics:** https://statistik.kkp.go.id
**API type:** ⚠️ XLSX + web tables (early SDI adopter)

## Overview

Fish catch statistics, aquaculture production, fishing vessel registry, marine protected areas (KKP was an early adopter of Satu Data Indonesia). Data covers both capture fisheries and aquaculture.

## Statistics Portal

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0"

# Browse annual fisheries statistics
resp = session.get("https://statistik.kkp.go.id/home.php", timeout=30)
soup = BeautifulSoup(resp.text, "html.parser")

for link in soup.select("a[href*='download'], a[href$='.xlsx']"):
    print(link.text.strip(), ":", link.get("href", ""))
```

## Key Datasets

| Dataset | Description | Frequency |
|---------|-------------|-----------|
| Produksi perikanan tangkap | Capture fisheries production by species | Annual |
| Produksi perikanan budidaya | Aquaculture production by commodity | Annual |
| Kapal perikanan | Fishing vessel registry | Annual |
| Nilai ekspor hasil laut | Seafood export value | Monthly |
| Kawasan konservasi laut | Marine protected areas | Per designation |
| Pelabuhan perikanan | Fishing port statistics | Annual |

## Marine Protected Areas (KKP)

Recipe withdrawn: its historical route returned HTTP 404 on October 10, 2026. Use the reviewed publisher navigation above; no endpoint resurrection is claimed.

## Fish Price Monitoring

```python
# Daily fish price at major fishing ports
resp = requests.get("https://satudata.kkp.go.id/api/v1/harga-ikan", params={
    "tanggal": "2025-03-01",
    "pelabuhan": "Muara Baru",
})
```

## Gotchas

1. **SDI early adopter** — KKP was among first ministries on Satu Data; some API structure available
2. **Annual dominance** — most production data is annual; monthly data for prices/exports
3. **Vessel registry** — full vessel registry needs formal data request; aggregate stats public
4. **Export value** — good for commodity price trends; published monthly
5. **BRSDM data** — research arm has additional datasets at `brsdm.kkp.go.id`

</details>
