# e-PPID — Public Information Request Portal

**Agency:** All ministries and agencies (Kemkominfo coordination)
**Portal:** https://ppid.kominfo.go.id
**Kind:** government; **catalog ID:** `ppid`; **tier:** tier2
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

A public webpage does not authorize bulk extraction. Use permitted public searches only; stop at login, CAPTCHA or access-denial screens. CSRF/session handling is not permission to bypass controls.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

A public webpage does not authorize bulk extraction. Use permitted public searches only; stop at login, CAPTCHA or access-denial screens. CSRF/session handling is not permission to bypass controls.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** All ministries and agencies (Kemkominfo coordination)
**Entry point:** https://ppid.kominfo.go.id (national directory)
**Per-agency:** https://ppid.[ministry].go.id
**API type:** ⚠️ Web portal per ministry (no central API)

## Overview

PPID (Pejabat Pengelola Informasi dan Dokumentasi) is Indonesia's public information disclosure system under UU 14/2008. Each government body has its own PPID portal where citizens can request documents and data. Useful for understanding what data exists even before it's published openly.

## Ministry PPID Portals (Sample)

| Ministry | URL |
|----------|-----|
| Kominfo (coordinator) | https://ppid.kominfo.go.id |
| Kemenkeu | https://ppid.kemenkeu.go.id |
| Kemenkumham | https://ppid.kemenkumham.go.id |
| BPS | https://ppid.bps.go.id |
| Kemenkes | https://ppid.kemkes.go.id |
| OJK | https://ppid.ojk.go.id |

## Scrape Published Information Lists (DIP)

Each PPID portal publishes a Daftar Informasi Publik (DIP) — the list of information they are obligated to provide:

```python
import requests
from bs4 import BeautifulSoup

# Example: BPS PPID
resp = requests.get("https://ppid.bps.go.id/daftar-informasi-publik", timeout=30)
soup = BeautifulSoup(resp.text, "html.parser")

for item in soup.select(".info-item, table tbody tr"):
    cells = item.find_all("td")
    if cells:
        print({
            "title": cells[0].text.strip(),
            "category": cells[1].text.strip() if len(cells) > 1 else "",
        })
```

## Submit a Request

Under UU 14/2008, agencies must respond within 10 working days (extendable to 17):

1. Register on the ministry's PPID portal
2. Submit request with: information description, intended use, format preference
3. Agency acknowledges within 1 day
4. Response due within 10 working days
5. Appeal to Komisi Informasi if denied

## Track Request Status

```python
# Most portals have a tracking endpoint
resp = requests.get("https://ppid.kominfo.go.id/tracking", params={
    "ticket": "REQ-2025-001234",
})
```

## Gotchas

1. **No central API** — each ministry runs independent PPID software
2. **Varied software** — some use PPID standard software, others custom builds
3. **10-day response SLA** — legally mandated but compliance varies
4. **DIP lists what exists** — request from DIP first; non-DIP requests take longer
5. **Exclusions** — confidential info (state secrets, privacy, commercial) can be refused
6. **Komisi Informasi** — appeal body if request is denied; decisions are binding

</details>
