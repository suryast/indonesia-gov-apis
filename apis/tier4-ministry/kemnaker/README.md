# Satu Data Kemnaker — Labor & Employment Data

**Agency:** Kementerian Ketenagakerjaan (Ministry of Manpower)
**Portal:** https://satudata.kemnaker.go.id
**Kind:** government; **catalog ID:** `kemnaker`; **tier:** tier4
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Distinguish public aggregate publications from ministry operational systems. No account-gated, student, patient, employee or land-owner records should be extracted without authorization.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Distinguish public aggregate publications from ministry operational systems. No account-gated, student, patient, employee or land-owner records should be extracted without authorization.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Kementerian Ketenagakerjaan (Ministry of Manpower)
**Portal:** https://satudata.kemnaker.go.id
**API type:** ✅ REST API + CSV downloads

## Overview

Employment statistics, provincial minimum wage (UMR/UMP) data, labor disputes, BPJS Ketenagakerjaan participation rates, and occupational safety records.

## Minimum Wage Data (UMP/UMR)

```python
import requests

# UMP (Provincial Minimum Wage) per province per year
resp = requests.get("https://satudata.kemnaker.go.id/api/v1/ump", params={
    "tahun": 2025,
}, timeout=30)
data = resp.json()

for province in data.get("data", []):
    print(f"{province['provinsi']}: Rp {province['ump']:,}/month")
```

### Current UMP Data (2025, selected provinces)

| Province | UMP 2025 (approx) |
|----------|--------------------|
| DKI Jakarta | Rp 5,396,761 |
| Papua | Rp 4,285,626 |
| Jawa Barat | Rp 2,191,232 |
| Jawa Tengah | Rp 2,169,348 |
| Jawa Timur | Rp 2,305,985 |

## Employment Statistics

```python
# Employment by sector and province
resp = requests.get("https://satudata.kemnaker.go.id/api/v1/tenaga-kerja", params={
    "tahun": 2024,
    "kode_provinsi": "31",  # DKI Jakarta
}, timeout=30)
```

## CSV Downloads

```python
from bs4 import BeautifulSoup

resp = requests.get("https://satudata.kemnaker.go.id/data", timeout=30)
soup = BeautifulSoup(resp.text, "html.parser")
for link in soup.select("a[href*='.csv'], a[href*='.xlsx']"):
    print(link.text.strip(), ":", link["href"])
```

## BPJS Ketenagakerjaan Coverage

```python
# Participation rates by sector
resp = requests.get("https://satudata.kemnaker.go.id/api/v1/bpjs-coverage", params={
    "tahun": 2024,
    "sektor": "formal",
})
```

## Gotchas

1. **API endpoints may require registration** — some endpoints need a key; try without first
2. **UMP vs UMK** — UMP is provincial, UMK is city/regency level (higher detail)
3. **Annual update** — UMP announced each November for the following year
4. **CSV fallback** — if API is unavailable, check the data portal for CSV downloads
5. **BPJS data** — separate from Kemnaker; cross-reference at `bpjsketenagakerjaan.go.id`

</details>
