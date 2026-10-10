# ATR/BPN — Land & Property Registry

**Agency:** Kementerian ATR / Badan Pertanahan Nasional
**Portal:** https://atrbpn.go.id
**Kind:** government; **catalog ID:** `atr-bpn`; **tier:** tier4
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Distinguish public aggregate publications from ministry operational systems. No account-gated, student, patient, employee or land-owner records should be extracted without authorization.

**Access/auth:** Account/authorization required for private records; no public lookup API verified.

Distinguish public aggregate publications from ministry operational systems. No account-gated, student, patient, employee or land-owner records should be extracted without authorization.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Kementerian ATR / Badan Pertanahan Nasional
**Portal:** https://atrbpn.go.id | https://bhumi.atrbpn.go.id
**API type:** ❌ Login required (BHUMI viewer is public for visualization only)

## Overview
Land certificate status (SHM, HGB, HGU), PTSL land registration progress, spatial land data. BHUMI is a public map viewer but certificate verification requires MoU or partnership.

## Public Access
- **BHUMI Map Viewer:** `bhumi.atrbpn.go.id` — view land parcels, zoning
- **PTSL Progress:** publicly reported statistics on land registration

## Gotchas
1. Certificate verification needs API partnership or MoU
2. BHUMI viewer is WMS-based — can extract tile data but not structured records
3. Land data is politically sensitive — access is tightly controlled
4. Regional BPN offices may have different data availability

</details>
