# Open Data Bali — Bali Provincial Open Data

**Agency:** Pemerintah Provinsi Bali
**Portal:** https://data.baliprov.go.id
**Kind:** government; **catalog ID:** `opendata-bali`; **tier:** tier3
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

One bounded GET of the historical CKAN search route on 2026-10-10 observed transport_error. This does not establish a working CKAN API or prove that the portal has no other API.[25]

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Portal technology and download access must be checked separately. Do not assume CKAN, a datastore, an authless API or a universal quota from a regional portal name.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Pemerintah Provinsi Bali
**Portal:** https://data.baliprov.go.id
**API type:** ⚠️ CSV/XLSX downloads (less mature API)

## Overview

Bali's provincial open data portal covering tourism statistics, land use, population, and agriculture. Less mature than Jakarta/Jabar — primarily static file downloads rather than live API queries.

## Access Data

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0"

# Browse dataset catalog
resp = session.get("https://data.baliprov.go.id/dataset", timeout=30)
soup = BeautifulSoup(resp.text, "html.parser")

for ds in soup.select(".dataset-item"):
    title = ds.select_one("h3").text.strip()
    link = ds.select_one("a")["href"]
    print(f"{title}: https://data.baliprov.go.id{link}")

# Download a specific CSV dataset
csv_url = "https://data.baliprov.go.id/dataset/.../resource/.../download/data.csv"
df = pd.read_csv(BytesIO(session.get(csv_url, timeout=30).content))
print(df.head())
```

## Notable Datasets

| Dataset | Description |
|---------|-------------|
| Kunjungan wisatawan | Tourist arrival statistics by origin |
| Penginapan | Accommodation capacity by kabupaten |
| Pertanian | Agricultural production by crop type |
| Kependudukan | Population by district |
| Lahan | Land use classification |

## Gotchas

1. **Less mature** — primarily file downloads, limited live API
2. **Tourism focus** — best data is tourism-related (Bali's primary sector)
3. **Annual cadence** — most datasets updated annually, not monthly
4. **BPS Bali** (`bali.bps.go.id`) is more reliable for statistical data than the portal
5. **CKAN may be present** — check `/api/3/action/package_list` as some portals do expose CKAN

</details>
