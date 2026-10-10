# DJPB Treasury — State Treasury & Budget Disbursement

**Agency:** Direktorat Jenderal Perbendaharaan (DJPB), Kementerian Keuangan
**Portal:** https://djpb.kemenkeu.go.id/portal/id/
**Kind:** government; **catalog ID:** `djpb-treasury`; **tier:** tier1
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Tier 1 is a historical routing group, not an assurance of an open API. Confirm the publisher, license, endpoint and response shape before integration.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Tier 1 is a historical routing group, not an assurance of an open API. Confirm the publisher, license, endpoint and response shape before integration.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Direktorat Jenderal Perbendaharaan (DJPB), Kementerian Keuangan
**Portal:** https://djpb.kemenkeu.go.id/portal/id/
**Open Data:** https://data.go.id (search "DJPB" or "perbendaharaan")
**API type:** ✅ CKAN API (via data.go.id)

## Overview

DJPB manages state treasury operations including budget disbursement, government account management, and fiscal reporting. Treasury data is published on data.go.id as datasets.

## Data Available

| Dataset | Description | Format |
|---------|-------------|--------|
| Realisasi APBN | Budget execution/disbursement by ministry | CSV/XLSX |
| Laporan Keuangan Pemerintah | Government financial statements | PDF |
| Data SPAN | State payment system transaction summaries | CSV |
| Posisi Kas Negara | State cash position reports | XLSX |

## API Access (via CKAN)

```python
import requests

# Search DJPB datasets on data.go.id
resp = requests.get("https://data.go.id/api/3/action/package_search", params={
    "q": "DJPB perbendaharaan",
    "rows": 10,
})
datasets = resp.json()["result"]["results"]
for ds in datasets:
    print(f"- {ds['title']} ({ds['num_resources']} resources)")
```

## Gotchas

1. **Most data is aggregated** — transaction-level treasury data is not publicly available
2. **Fiscal year alignment** — Indonesian fiscal year = calendar year (Jan-Dec)
3. **Delayed publication** — quarterly/annual reports lag 1-3 months
4. **PDF-heavy** — many reports published as PDF, not machine-readable
5. **SPAN system** — internal treasury system; only summaries are public

</details>
