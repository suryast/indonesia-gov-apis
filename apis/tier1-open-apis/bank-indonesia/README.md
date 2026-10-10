# Bank Indonesia — Central Bank Data

**Agency:** Bank Indonesia (BI)
**Portal:** https://www.bi.go.id/id/statistik/
**Kind:** government; **catalog ID:** `bank-indonesia`; **tier:** tier1
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Use official BI statistical publications, separating JISDOR from transaction exchange rates. The old guessed `dataapi.bi.go.id/dataexchange/v1/*` routes, 10:00 publication-time claim and payment-transfer sandbox example are withdrawn: no statistics API contract was established in this review.[16]

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Tier 1 is a historical routing group, not an assurance of an open API. Confirm the publisher, license, endpoint and response shape before integration.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.
