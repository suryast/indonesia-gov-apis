# Kemenag — Religious Affairs Data

**Agency:** Kementerian Agama
**Portal:** https://simas.kemenag.go.id
**Kind:** government; **catalog ID:** `kemenag`; **tier:** tier4
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Distinguish public aggregate publications from ministry operational systems. No account-gated, student, patient, employee or land-owner records should be extracted without authorization.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Distinguish public aggregate publications from ministry operational systems. No account-gated, student, patient, employee or land-owner records should be extracted without authorization.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.


### Broken-link remediation — October 10, 2026

Use the [publisher navigation](https://simas.kemenag.go.id) (HTTP 200 landing/index observed October 10, 2026). Specific historical search/download routes below are unavailable; no data API or replacement search contract is verified.

- Historical failed route: `https://simas.kemenag.go.id/search` — HTTP 404 in the dated repository link audit; unavailable, not a working recipe.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Kementerian Agama
**Portal:** https://simas.kemenag.go.id | https://emis.kemenag.go.id
**API type:** ⚠️ Scraping (web search interfaces)

## Mosque Registry (SIMAS)
Recipe withdrawn: its historical route returned HTTP 404 on October 10, 2026. Use the reviewed publisher navigation above; no endpoint resurrection is claimed.

## Pesantren & Madrasah (EMIS)
- Pesantren registry: `emis.kemenag.go.id/emis_sdm`
- Madrasah data: integrated with education statistics

## Key Data
- 300,000+ mosques registered in SIMAS
- Pesantren locations and student counts
- Madrasah accreditation data

## Gotchas
1. SIMAS is the most complete mosque database in Indonesia
2. EMIS has pesantren and madrasah data
3. Web scraping only — no public API
4. Useful for cross-referencing halal supply chain data

</details>
