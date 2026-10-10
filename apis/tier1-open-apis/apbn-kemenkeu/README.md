# Portal APBN Kemenkeu — State Budget Data

**Agency:** Kementerian Keuangan (Ministry of Finance)
**Portal:** https://data-apbn.kemenkeu.go.id
**Kind:** government; **catalog ID:** `apbn-kemenkeu`; **tier:** tier1
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Tier 1 is a historical routing group, not an assurance of an open API. Confirm the publisher, license, endpoint and response shape before integration.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Tier 1 is a historical routing group, not an assurance of an open API. Confirm the publisher, license, endpoint and response shape before integration.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.


### Broken-link remediation — October 10, 2026

Use the [publisher navigation](https://djpb.kemenkeu.go.id/portal/id/berita/lainnya/realisasi-apbn.html) (HTTP 200 landing/index observed October 10, 2026). Specific historical search/download routes below are unavailable; no data API or replacement search contract is verified.

- Historical failed route: `https://djpb.kemenkeu.go.id/portal/id/data/apbn-realisasi.html` — HTTP 404 in the dated repository link audit; unavailable, not a working recipe.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Kementerian Keuangan (Ministry of Finance)
**Portal:** https://data-apbn.kemenkeu.go.id
**DJPB Portal:** https://djpb.kemenkeu.go.id
**MONEV:** https://monev.anggaran.kemenkeu.go.id
**API type:** ✅ CSV/XLSX downloads + web scraping

## Overview

APBN (Anggaran Pendapatan dan Belanja Negara) revenue and expenditure data published monthly. Covers ministry-level breakdowns, transfers to regions, debt, and financing.

## Download Budget Execution Data

Recipe withdrawn: its historical route returned HTTP 404 on October 10, 2026. Use the reviewed publisher navigation above; no endpoint resurrection is claimed.

## Parse Monthly Excel Report

```python
import openpyxl

wb = openpyxl.load_workbook("apbn-realisasi-jan-2025.xlsx")
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    print(f"Sheet: {sheet_name}")
    for row in ws.iter_rows(min_row=3, max_row=20, values_only=True):
        if row[0]:
            print(row)
```

## Data Categories

| Category | Description |
|----------|-------------|
| Pendapatan Negara | Revenue: taxes, PNBP, grants |
| Belanja Pemerintah Pusat | Central expenditure by ministry |
| Transfer ke Daerah | Regional transfers (DAU, DAK) |
| Pembiayaan Anggaran | Debt issuance and repayment |

## Ministry Codes (sample)

| Code | Ministry |
|------|----------|
| 001 | MPR |
| 004 | BPK |
| 012 | Kemenkumham |
| 015 | Kemenkeu |
| 023 | Kemenaker |
| 024 | Kemenkes |

## Gotchas

1. **Download URLs change each period** — always scrape the index page, not hardcode URLs
2. **Excel format varies by year** — sheet names and column layouts change annually
3. **Data lag** — monthly reports published 2-3 weeks after month end
4. **MONEV** (`monev.anggaran.kemenkeu.go.id`) has sub-activity level granularity
5. **Ministry codes** — 3-digit; full list on Kemenkeu website

</details>
