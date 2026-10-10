# Kemendikdasmen — Education Data

**Agency:** Kementerian Pendidikan Dasar dan Menengah
**Portal:** https://data.kemendikdasmen.go.id
**Kind:** government; **catalog ID:** `kemendikdasmen`; **tier:** tier4
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Distinguish public aggregate publications from ministry operational systems. No account-gated, student, patient, employee or land-owner records should be extracted without authorization.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Distinguish public aggregate publications from ministry operational systems. No account-gated, student, patient, employee or land-owner records should be extracted without authorization.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Kementerian Pendidikan Dasar dan Menengah
**Portal:** https://data.kemendikdasmen.go.id | https://referensi.data.kemdikbud.go.id
**API type:** ⚠️ Partial API (school registry has REST, full DAPODIK needs partnership)

## School Registry API
```python
import requests
resp = requests.get("https://referensi.data.kemdikbud.go.id/api/sekolah", params={
    "nama": "SMA Negeri 1",
    "propinsi": "030000",  # DKI Jakarta
})
schools = resp.json()
```

## Key Data
- School registry (NPSN — unique school ID)
- Student counts by school
- Teacher registry (GTK)
- Accreditation status

## Gotchas
> Historical access/limit assertion withdrawn; verify publisher guidance.
2. Full DAPODIK data requires partnership
3. Province codes follow BPS coding system

</details>
