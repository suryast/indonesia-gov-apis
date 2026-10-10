# OpenCorporates — Global Company Registry

**Agency:** OpenCorporates Ltd
**Portal:** https://opencorporates.com
**Kind:** non-government; **catalog ID:** `opencorporates`; **tier:** tier5
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

**Organization:** OpenCorporates Ltd
**Portal:** https://opencorporates.com
**API type:** ✅ REST API (free tier limited, paid for bulk)

## API Usage
```python
import requests

resp = requests.get("https://api.opencorporates.com/v0.4/companies/search", params={
    "q": "company name",
    "jurisdiction_code": "id",  # Indonesia
    "api_token": "your-api-token",
})
companies = resp.json()["results"]["companies"]
```

## Rate Limits
> Historical access/limit assertion withdrawn; verify publisher guidance.
- Paid: higher limits available

## Gotchas
1. Indonesian data sourced from AHU (Kemenkumham)
2. Free tier is limited but sufficient for lookups
3. Structured company data (name, status, officers, filings)

</details>
