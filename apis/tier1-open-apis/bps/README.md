# BPS — Statistics Indonesia

**Agency:** Badan Pusat Statistik (Central Bureau of Statistics)
**Portal:** https://www.bps.go.id
**Kind:** government; **catalog ID:** `bps`; **tier:** tier1
**Review date:** 2026-10-10; **review state:** primary_documentation_reviewed

## Reviewed guidance

Indexed official WebAPI documentation confirms key-token identification and JSON responses. Full direct documentation retrieval timed out; exact dynamic-table schema, variable mappings and quota were not validated here. Discover identifiers from current official metadata rather than guessing var=1 means CPI. The old fixed indicator table and 100/day claim are withdrawn.[4]

**Access/auth:** BPS API key token required; authenticated calls not executed.

Tier 1 is a historical routing group, not an assurance of an open API. Confirm the publisher, license, endpoint and response shape before integration.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Bounded request sketch (route/schema not exercised)

```python
import os
import requests

response = requests.get(
    "https://webapi.bps.go.id/v1/api/list",
    params={"model": "var", "domain": "0000", "key": os.environ["BPS_API_KEY"]},
    timeout=30,
)
response.raise_for_status()
payload = response.json()
# Confirm the current publisher response schema before reading records.
# Do not assume payload["data"] is a flat list of variable objects.
```

Never log the request URL containing the key. No fixed quota is asserted here.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.
