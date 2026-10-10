# OCCRP Aleph — Global Beneficial Ownership & Leaks

**Agency:** OCCRP (Organized Crime and Corruption Reporting Project)
**Portal:** https://aleph.occrp.org
**Kind:** non-government; **catalog ID:** `occrp-aleph`; **tier:** tier5
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Record the original publisher and publication date. Third-party company or leak indexes are research leads, not findings of wrongdoing or current proof of registration.

**Access/auth:** API credentials, collection permissions and current service terms must be checked; not authenticated here.

Record the original publisher and publication date. Third-party company or leak indexes are research leads, not findings of wrongdoing or current proof of registration.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Organization:** OCCRP (Organized Crime and Corruption Reporting Project)
**Portal:** https://aleph.occrp.org
**API type:** ✅ REST API (free registration)

## API Usage
```python
import requests

API_KEY = "your-api-key"  # Free at aleph.occrp.org
resp = requests.get("https://aleph.occrp.org/api/2/entities", params={
    "q": "company name",
    "filter:schema": "Company",
    "filter:countries": "id",  # Indonesia
}, headers={"Authorization": f"ApiKey {API_KEY}"})
results = resp.json()
```

## Key Data
- Panama Papers, Pandora Papers, and other leaks
- Indonesian company/person data from beneficial ownership disclosures
- Cross-jurisdictional corporate structures

## Rate Limit
60 requests/minute with free API key.

## Gotchas
1. Free API key — register at aleph.occrp.org
2. Contains Indonesian entity data from major leaks
3. Useful for cross-referencing AHU company data
4. Data is from investigations — not official government records

</details>
