# OSS / NIB — Business Identification Number Lookup

**Agency:** BKPM / OSS (Online Single Submission)
**Portal:** https://oss.go.id
**Kind:** government; **catalog ID:** `oss-nib`; **tier:** tier2
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

A public webpage does not authorize bulk extraction. Use permitted public searches only; stop at login, CAPTCHA or access-denial screens. CSRF/session handling is not permission to bypass controls.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

A public webpage does not authorize bulk extraction. Use permitted public searches only; stop at login, CAPTCHA or access-denial screens. CSRF/session handling is not permission to bypass controls.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.


### Broken-link remediation — October 10, 2026

Use the [publisher navigation](https://oss.go.id) (HTTP 200 landing/index observed October 10, 2026). Specific historical search/download routes below are unavailable; no data API or replacement search contract is verified.

- Historical failed route: `https://oss.go.id/informasi/cari-nib` — HTTP 404 in the dated repository link audit; unavailable, not a working recipe.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** BKPM / OSS (Online Single Submission)
**Portal:** https://oss.go.id
**API type:** ⚠️ Form-based HTML (public lookup) / Login required for full data

## Overview

NIB (Nomor Induk Berusaha) is the master identifier for all licensed businesses in Indonesia. OSS assigns NIBs and links them to KBLI sector codes, risk level (I/II/III/IV), and license types. Since 2018, all new businesses must have NIB.

## Public NIB Lookup

Recipe withdrawn: its historical route returned HTTP 404 on October 10, 2026. Use the reviewed publisher navigation above; no endpoint resurrection is claimed.

## NIB Response Fields (Public)

| Field | Description |
|-------|-------------|
| NIB | 13-digit business ID |
| Nama pelaku usaha | Business name |
| KBLI | Sector codes (KBLI 2020) |
| Skala usaha | Business scale (Mikro/Kecil/Menengah/Besar) |
| Tingkat risiko | Risk level (I=lowest, IV=highest) |
| Status | Aktif / dll |

## KBLI Sector Codes

KBLI (Klasifikasi Baku Lapangan Usaha Indonesia) follows ISIC structure:

```python
# Common KBLI categories
KBLI_GROUPS = {
    "A": "Pertanian, Kehutanan, Perikanan",
    "C": "Industri Pengolahan",
    "F": "Konstruksi",
    "G": "Perdagangan Besar dan Eceran",
    "I": "Penyediaan Akomodasi dan Makan Minum",
    "J": "Informasi dan Komunikasi",
    "K": "Jasa Keuangan dan Asuransi",
    "Q": "Aktivitas Kesehatan",
}
```

## Gotchas

1. **Full license details require login** — OSS account needed for compliance data
2. **NIB is 13 digits** — leading zeros matter; store as string
3. **KBLI 2020** — latest classification; older businesses may have KBLI 2017 codes
4. **Risk level determines license type** — Level I/II = declaration only, III/IV = permit required
5. **Rate limiting** — use delays; OSS blocks aggressive scrapers
6. **DPMPTSP integration** — regional permits link back to OSS NIB

</details>
