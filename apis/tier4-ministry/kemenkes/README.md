# Kemenkes — Health Data & Facility Registry

**Agency:** Kementerian Kesehatan
**Portal:** https://yankes.kemkes.go.id
**Kind:** government; **catalog ID:** `kemenkes`; **tier:** tier4
**Review date:** 2026-10-10; **review state:** primary_documentation_reviewed

## Reviewed guidance

Public facility information and SATUSEHAT health interoperability are different access classes. SATUSEHAT requires approved partner credentials and organization-specific authorization; the old anonymous `/api/fasyankes` example is not a verified API contract.[8]

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Distinguish public aggregate publications from ministry operational systems. No account-gated, student, patient, employee or land-owner records should be extracted without authorization.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Kementerian Kesehatan
**Portal:** https://yankes.kemkes.go.id | https://satusehat.kemkes.go.id
**API type:** ⚠️ Partial API (facility registry public, SATUSEHAT needs registration)

## Facility Registry (Fasyankes)
```python
import requests
resp = requests.get("https://yankes.kemkes.go.id/api/fasyankes", params={
    "nama": "RSUD",
    "jenis": "RS",  # RS=Hospital, Puskesmas, Klinik
})
facilities = resp.json()
```

## SATUSEHAT Platform
New national health data exchange. Developer portal at `developers.kemkes.go.id`. Requires registration for API access.

## Key Data
- Hospital & clinic registry
- Doctor specialization lists
- Disease surveillance data
- Health facility accreditation

## Gotchas
1. Fasyankes registry at `yankes.kemkes.go.id` is publicly searchable
2. SATUSEHAT API requires developer registration
3. Historical health statistics available as Excel downloads

</details>
