# JDIH BPK — National Legal Documentation Network

**Agency:** Badan Pemeriksa Keuangan
**Portal:** https://jdih.bpk.go.id
**Kind:** government; **catalog ID:** `jdih-bpk`; **tier:** tier1
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

BPK legal documentation and Perpusnas are different publishers. Do not treat their sites or metadata/search routes as one interchangeable API. Old example routes are unverified; identify the original official legal text before relying on a third-party index.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Tier 1 is a historical routing group, not an assurance of an open API. Confirm the publisher, license, endpoint and response shape before integration.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Badan Pemeriksa Keuangan (BPK) + Perpusnas (National Library)
**BPK Portal:** https://peraturan.bpk.go.id
**Perpusnas API:** https://api-jdih.perpusnas.go.id
**API type:** ✅ Partial JSON API (Perpusnas) + structured HTML scraping (BPK)

## Overview

JDIH (Jaringan Dokumentasi dan Informasi Hukum) is Indonesia's national legal documentation network. Two access points:

- **BPK JDIH** (`peraturan.bpk.go.id`) — most comprehensive, structured HTML
- **Perpusnas JDIH API** (`api-jdih.perpusnas.go.id`) — partial JSON API, paginated

## Perpusnas JDIH API (JSON)

```python
import requests

BASE = "https://api-jdih.perpusnas.go.id"

resp = requests.get(BASE, params={
    "page": 1,
    "type": "peraturan",
    "keyword": "ketenagakerjaan",
})
data = resp.json()

for reg in data.get("data", []):
    print(f"{reg['jenis']} No.{reg['nomor']}/{reg['tahun']}: {reg['judul']}")
```

## BPK JDIH Scraping

```python
from bs4 import BeautifulSoup
import requests

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0"

resp = session.get("https://peraturan.bpk.go.id/Search", params={
    "query": "upah minimum",
    "PerPage": 20,
    "PageNum": 1,
})
soup = BeautifulSoup(resp.text, "html.parser")

for item in soup.select(".regulation-item"):
    title = item.select_one(".title").text.strip()
    year = item.select_one(".year").text.strip()
    print(f"({year}): {title}")
```

## Regulation Types

| Code | Type |
|------|------|
| UU | Undang-Undang |
| PP | Peraturan Pemerintah |
| Perpres | Peraturan Presiden |
| Permen | Peraturan Menteri |
| Perda | Peraturan Daerah |
| Kepres | Keputusan Presiden |

## Gotchas

1. **BPK JDIH is HTML-only** — parse with BeautifulSoup; structure is consistent
2. **Perpusnas API is undocumented** — parameters discovered via DevTools
3. **Some regulations are PDF-only** — full text needs PDF parsing (`pdfplumber`)
4. **Revocation status** may lag — cross-check with pasal.id for live status
> Historical access/limit assertion withdrawn; verify publisher guidance.

</details>
