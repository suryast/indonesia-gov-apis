# ESDM — Energy & Mining Data

**Agency:** Kementerian Energi dan Sumber Daya Mineral
**Portal:** https://www.esdm.go.id/en/publikasi/handbook-of-energy-economic-statistics-of-indonesia
**Kind:** government; **catalog ID:** `esdm-energy`; **tier:** tier4
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Distinguish public aggregate publications from ministry operational systems. No account-gated, student, patient, employee or land-owner records should be extracted without authorization.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Distinguish public aggregate publications from ministry operational systems. No account-gated, student, patient, employee or land-owner records should be extracted without authorization.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.


### Broken-link remediation — October 10, 2026

Official HEESI publication/download index (HTTP 200 HTML) with annual handbook PDF links. Individual downloads, reuse rights and mining APIs remain unverified.

- Historical failed route: `https://www.esdm.go.id/id/statistik-dan-riset` — HTTP 404 in the dated repository link audit; unavailable, not a working recipe.
- Historical failed route: `https://www.esdm.go.id/id/statistik-dan-riset/publikasi/handbook-of-energy` — HTTP 404 in the dated repository link audit; unavailable, not a working recipe.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Kementerian Energi dan Sumber Daya Mineral
**Portal:** `https://www.esdm.go.id/id/statistik-dan-riset` (historical unavailable route; HTTP 404 observed 2026-10-10)
**Mining permits:** https://minerba.esdm.go.id/public
**API type:** ⚠️ PDF/XLSX annual handbooks + mining permit registry

## Overview

Energy production and consumption by sector, oil & gas lifting, electricity generation, coal and mineral production, and mining permit (IUP) registry.

## Handbook of Energy Statistics

Recipe withdrawn: its historical route returned HTTP 404 on October 10, 2026. Use the reviewed publisher navigation above; no endpoint resurrection is claimed.

## Mining Permit Registry (IUP)

```python
# Public mining permit registry
resp = requests.get("https://minerba.esdm.go.id/public/iup/list", params={
    "status": "aktif",
    "page": 1,
    "limit": 50,
}, timeout=30)
permits = resp.json()

for permit in permits.get("data", []):
    print(f"{permit['perusahaan']} — {permit['komoditas']} — {permit['luas_ha']} ha")
```

## Key Data Available

| Dataset | Source | Format |
|---------|--------|--------|
| Oil & gas lifting | Handbook | PDF/XLSX |
| Coal production by company | Handbook | PDF/XLSX |
| Electricity generation by source | Handbook | PDF/XLSX |
| Energy consumption by sector | Handbook | PDF/XLSX |
| Active mining permits (IUP) | minerba.esdm.go.id | Web/JSON |
| Oil & gas block assignments | esdm.go.id | PDF |

## Electricity Data (PLN Integration)

```python
# PLN publishes electricity statistics separately
resp = requests.get("https://www.pln.co.id/tentang-pln/statistik", timeout=30)
# Contains: generation capacity, production, sales by customer category
```

## Gotchas

1. **Handbook is annual** — published once a year; use for multi-year trend analysis
2. **Mining permit data** — `minerba.esdm.go.id/public` is the public-facing IUP registry
3. **PDF-heavy** — most statistical tables are embedded in PDFs; parse with `pdfplumber`
4. **Oil & gas contract data** — upstream contracts (PSC) are at SKK Migas, not ESDM
5. **EITI cross-reference** — see `tier5-transparency/eiti-indonesia` for verified production data

</details>
