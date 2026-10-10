# Putusan Mahkamah Agung — Supreme Court Decisions

**Agency:** Mahkamah Agung RI (Supreme Court of Indonesia)
**Portal:** https://putusan3.mahkamahagung.go.id
**Kind:** government; **catalog ID:** `putusan-ma`; **tier:** tier1
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

**Agency:** Mahkamah Agung RI (Supreme Court of Indonesia)
**Portal:** https://putusan3.mahkamahagung.go.id
**API type:** ✅ Public web search + full-text HTML/PDF access

## Overview

Millions of Indonesian court decisions publicly accessible: civil, criminal, commercial, administrative (TUN), and religious courts. Searchable by keyword, case number, judge, court, and year.

## Search

```python
import requests

BASE = "https://putusan3.mahkamahagung.go.id"

resp = requests.post(
    f"{BASE}/search/index/pencarian/ajax/putusan",
    json={
        "q": "wanprestasi kontrak",
        "tahun": "2024",
        "jenis_doc": "Putusan",
        "page": 1,
    },
    headers={"X-Requested-With": "XMLHttpRequest"},
    timeout=30,
)
results = resp.json()
```

## Pagination

```python
import time

for page in range(1, 50):
    data = requests.post(
        f"{BASE}/search/index/pencarian/ajax/putusan",
        json={"q": "wanprestasi", "tahun": "2023", "page": page},
        headers={"X-Requested-With": "XMLHttpRequest"},
        timeout=30,
    ).json()
    decisions = data.get("data", [])
    if not decisions:
        break
    for d in decisions:
        print(d.get("nomor"), d.get("tanggal_musyawarah"))
    time.sleep(1)
```

## Court Types

| Code | Description |
|------|-------------|
| `PN` | Pengadilan Negeri (District Court) |
| `PT` | Pengadilan Tinggi (High Court) |
| `MA` | Mahkamah Agung (Supreme Court) |
| `PA` | Pengadilan Agama (Religious Court) |
| `PTUN` | Pengadilan Tata Usaha Negara (Administrative Court) |

## Case Types

| Code | Type |
|------|------|
| `Pdt.G` | Civil lawsuit |
| `Pid.B` | Criminal |
| `Pdt.Sus-PHI` | Labor dispute |
| `TUN` | Administrative |
| `Ag` | Religious/Islamic |

## Gotchas

> Historical access/limit assertion withdrawn; verify publisher guidance.
2. **POST for search, GET for detail** — different verbs
3. **Millions of records** — use specific queries + year filters
4. **Older decisions are scanned PDFs** — need OCR for text extraction
> Historical access/limit assertion withdrawn; verify publisher guidance.

</details>
