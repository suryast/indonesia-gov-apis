# OJK — Financial Entity Legality Check

**Agency:** Otoritas Jasa Keuangan (Financial Services Authority)
**Portal:** https://ojk.go.id
**Kind:** government; **catalog ID:** `ojk`; **tier:** tier2
**Review date:** 2026-10-10; **review state:** primary_documentation_reviewed

## Reviewed guidance

SIKePO is banking-regulation search, not a platform license registry. Use dated OJK sector-specific licensing publications. OJK records the crypto-regulation handover on January 10, 2025; older BAPPEBTI lists are historical. Alert absence does not prove legality. Global geo-restriction and universal proxy recommendations are withdrawn.[3][9]

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

A public webpage does not authorize bulk extraction. Use permitted public searches only; stop at login, CAPTCHA or access-denial screens. CSRF/session handling is not permission to bypass controls.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Otoritas Jasa Keuangan (Financial Services Authority)
**Portal:** https://ojk.go.id
**API type:** ❌ No unified API — HTML scraping + Excel/PDF downloads

## Overview

OJK maintains directories of **licensed** and **illegal** financial entities. There is no single API — data is scattered across multiple pages and formats.

## Licensed Entity Sources

| Entity Type | URL | Format |
|------------|-----|--------|
| Fintech P2P Lending | `ojk.go.id/id/kanal/iknb/.../fintech/` | PDF |
| Investment Managers | `reksadana.ojk.go.id/Public/ManajerInvestasiList.aspx` | HTML table |
| Securities Firms | `ojk.go.id/id/kanal/pasar-modal/.../data-perusahaan-efek/` | Excel |
| Insurance | `ojk.go.id/id/kanal/iknb/.../asuransi/` | HTML table |
| Pension Funds | `ojk.go.id/id/kanal/iknb/.../dana-pensiun/` | HTML table |
| Multi-finance | `ojk.go.id/id/kanal/iknb/.../perusahaan-pembiayaan/` | HTML table |

## Illegal Entity List (Investment Alert)

OJK publishes a list of entities flagged as illegal. Updated periodically.

```python
import requests
from bs4 import BeautifulSoup

# Scrape the illegal entity page
resp = requests.get(
    "https://sikapiuangmu.ojk.go.id/FrontEnd/AlertPortal/AlertList",
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    timeout=30,
)
soup = BeautifulSoup(resp.text, "html.parser")

# Parse table rows
for row in soup.select("table tbody tr"):
    cols = [td.text.strip() for td in row.find_all("td")]
    if len(cols) >= 3:
        name = cols[0]
        entity_type = cols[1]
        status = cols[2]
        print(f"{name} | {entity_type} | {status}")
```

## SikapiUangmu Portal

OJK's consumer-facing portal at `sikapiuangmu.ojk.go.id` has the most accessible data:

```python
# Search for an entity
resp = requests.get(
    "https://sikapiuangmu.ojk.go.id/FrontEnd/AlertPortal/Search",
    params={"q": "company name"},
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    timeout=30,
)
```

## BAPPEBTI (Commodities Futures)

Related agency for commodities regulation:

```python
resp = requests.get(
    "https://bappebti.go.id/pialang_berjangka",
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    timeout=30,
)
soup = BeautifulSoup(resp.text, "html.parser")
# Parse broker list from HTML table
```

## Practical Architecture for Legality Checking

Since there's no unified API, the practical approach is:

1. **Scrape all sources periodically** (weekly/monthly)
2. **Normalize into a local database** (SQLite or D1)
3. **Build your own search API** on top

```
OJK Website → Scraper → Local DB → Your API → App
BAPPEBTI Website ↗
```

## Endpoint Status (Updated March 2026)

| Endpoint | Status | Notes |
|----------|--------|-------|
| `api.ojk.go.id` | ❌ **DNS dead** (NXDOMAIN) | Was the REST API — no longer resolves |
| `investor.ojk.go.id` | ❌ **DNS dead** (NXDOMAIN) | Was InvestorAlert API — no longer resolves |
| `sikapiuangmu.ojk.go.id` | ✅ Alive | AlertPortal/Negative for waspada list |
| `www.ojk.go.id` | ✅ Alive | **Indonesia-only** (geo-restricted, 403 from non-ID IPs) |
| `reksadana.ojk.go.id` | ⚠️ Unknown | May have been retired |

### Geo-Restriction


## Gotchas

1. **No stable API** — OJK frequently redesigns their website; `api.ojk.go.id` was retired without notice
2. **Mixed formats** — some data is Excel, some PDF, some HTML
3. **ASP.NET ViewState** — some pages require session + ViewState token
> Historical access/limit assertion withdrawn; verify publisher guidance.
5. **Geo-blocking** — `www.ojk.go.id` blocks non-Indonesian IPs (403)
6. **Stale data** — illegal entity list updated irregularly
7. **P2P lending list** is a PDF that changes URL each update
8. **BAPPEBTI is separate from OJK** but covers crypto/futures regulation
9. **AlertPortal is JS-rendered** — `/FrontEnd/AlertPortal/Negative` needs browser/Playwright

</details>
