# LAPOR — National Public Complaint System

**Agency:** Kementerian PAN-RB (Ministry of Administrative Reform)
**Portal:** https://www.lapor.go.id
**Kind:** government; **catalog ID:** `lapor`; **tier:** tier7
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Public complaint browsing and authenticated submission are separate workflows. Do not infer that all complaints are public, that all are login-gated, or that no API exists merely from this documentation. Complaint text may expose personal details; use only authorized public material and redact identifiers.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Separate official publications from community indexes. Map layers, complaint systems and legal search tools have different permissions; do not assume a public API from an accessible landing page.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Kementerian PAN-RB (Ministry of Administrative Reform)
**Portal:** https://www.lapor.go.id
**API type:** ❌ No public API

## Overview

LAPOR (Layanan Aspirasi dan Pengaduan Online Rakyat) is Indonesia's national complaint handling system. Citizens submit complaints about public services, which get routed to relevant agencies.

## No API Available

LAPOR does not provide a public API. The platform is web-only with login required for submission. Data is not available for bulk download.

## What You Can Do

- **Submit complaints** via web form (requires registration)
- **Track complaint status** via tracking ID
- **Browse public complaints** (some are published)

## Potential Scraping

```python
import requests

# Browse published complaints (if publicly visible)
resp = requests.get(
    "https://www.lapor.go.id/laporan",
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    timeout=30,
)
# Limited public data — most complaints require authentication to view
```

## Gotchas

1. **No API** — not useful for data projects
2. **Authentication required** — most data behind login
3. **Government-to-government** — primarily for inter-agency complaint routing
4. **Included for completeness** — unlikely to be useful for data projects

</details>
