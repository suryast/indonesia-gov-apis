# Satu Data Komdigi — Digital & Telecoms Data

**Agency:** Kementerian Komunikasi dan Digital (Ministry of Digital Affairs)
**Portal:** https://data.komdigi.go.id
**Kind:** government; **catalog ID:** `komdigi`; **tier:** tier4
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Distinguish public aggregate publications from ministry operational systems. No account-gated, student, patient, employee or land-owner records should be extracted without authorization.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Distinguish public aggregate publications from ministry operational systems. No account-gated, student, patient, employee or land-owner records should be extracted without authorization.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.


### Broken-link remediation — October 10, 2026

Publisher portal only (HTTP 200 HTML shell); specific open-data/download and desa-broadband routes unavailable/unverified. Navigate the official portal or request publisher assistance; no replacement data API is verified.

- Historical failed route: `https://data.komdigi.go.id/opendata` — HTTP 404 in the dated repository link audit; unavailable, not a working recipe.
- Historical failed route: `https://data.komdigi.go.id/opendata/desa-broadband` — HTTP 404 in the dated repository link audit; unavailable, not a working recipe.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Kementerian Komunikasi dan Digital (Ministry of Digital Affairs)
**Portal:** `https://data.komdigi.go.id/opendata` (historical unavailable route; HTTP 404 observed 2026-10-10)
**API type:** ✅ XLSX/CSV downloads

## Overview

Internet penetration, broadband subscriber counts, press freedom index, 4G village coverage, digital literacy metrics, and spectrum allocation data.

## Access Data

Recipe withdrawn: its historical route returned HTTP 404 on October 10, 2026. Use the reviewed publisher navigation above; no endpoint resurrection is claimed.

## Key Datasets

| Dataset | Description | Freq |
|---------|-------------|------|
| Penetrasi internet | Internet penetration by province | Annual |
| Pelanggan broadband | Broadband subscribers by ISP | Quarterly |
| Desa 4G | Village 4G coverage progress | Monthly |
| Literasi digital | Digital literacy index by province | Annual |
| Siaran pers | Press release data and announcements | Continuous |

## Digital Village Coverage

Recipe withdrawn: its historical route returned HTTP 404 on October 10, 2026. Use the reviewed publisher navigation above; no endpoint resurrection is claimed.

## Gotchas

1. **Ministry recently renamed** — was Kominfo (Komisi Informasi), now Komdigi; URLs changing
2. **XLSX format** — primary download format; use `pandas.read_excel()` or `openpyxl`
3. **Annual cadence** — most indicators updated annually
4. **ISP data** — operator-level subscriber data is aggregate, not per-user
5. **PDNS incident** — 2024 ransomware attack on national data center; some data may be affected

</details>
