# BMKG — Meteorology, Climatology & Geophysics Data

**Agency:** Badan Meteorologi, Klimatologi, dan Geofisika
**Portal:** https://data.bmkg.go.id
**Kind:** government; **catalog ID:** `bmkg`; **tier:** tier1
**Review date:** 2026-10-10; **review state:** primary_documentation_reviewed

## Reviewed guidance

Official weather documentation uses JSON at `https://api.bmkg.go.id/publik/prakiraan-cuaca` with `adm4`. It publishes three-day forecasts, updated twice daily, with a 60 requests/minute/IP limit and required BMKG attribution. Earthquake feeds have separate official documentation; felt earthquakes are not synonymous with M5+.[5][6]

**Access/auth:** Public feeds documented; publisher limits and attribution apply.

Tier 1 is a historical routing group, not an assurance of an open API. Confirm the publisher, license, endpoint and response shape before integration.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Official forecast pattern (documentation-derived, not executed here)

```python
import requests

response = requests.get(
    "https://api.bmkg.go.id/publik/prakiraan-cuaca",
    params={"adm4": "31.71.03.1001"}, timeout=30,
)
response.raise_for_status()
forecast = response.json()
# Verify the current schema; display BMKG attribution with derived output.
```

Legacy province XML examples are historical, not the recommended current interface.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.
