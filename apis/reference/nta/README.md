# NTA — Japan Invoice Registry (Reference)

**Agency:** National Tax Agency (Japan) — 国税庁
**Portal:** https://www.invoice-kohyo.nta.go.jp/
**Kind:** government; **catalog ID:** `nta`; **tier:** reference
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Japan reference only. The old fixed approval duration, strictly enforced one-request/second quota and registration-number parameter assumptions remain unverified historical notes, not current official guarantees.

**Access/auth:** Application ID historically documented; current approval and quota not verified.

International reference only; not an Indonesian source and not monitored. Confirm the official API contract, approval requirements and current limits independently.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** National Tax Agency (Japan) — 国税庁
**Portal:** https://www.invoice-kohyo.nta.go.jp/
**API type:** ✅ REST API (requires Application ID — 4-6 week approval)

> **Note:** This is a Japanese government API included as a reference for the InvoiceCheck project. Not an Indonesian data source.

## Overview

Japan's Qualified Invoice System (インボイス制度) requires businesses to register for tax invoice numbers. The NTA provides a public API to validate these numbers.

## API Application

1. Apply at https://www.invoice-kohyo.nta.go.jp/web/api/
2. Wait 4-6 weeks for Application ID
> Historical access/limit assertion withdrawn; verify publisher guidance.

## Endpoints

```python
import requests

APP_ID = "your-application-id"

# Look up by registration number
resp = requests.get(
    "https://web-api.invoice-kohyo.nta.go.jp/1/num",
    params={
        "id": APP_ID,
        "number": "T1234567890123",  # 13-digit number with T prefix
        "type": "21",                 # 21 = JSON format
    },
    timeout=30,
)
data = resp.json()
```

## Response

> Historical illustrative JSON response removed: not independently observed.


## Gotchas

1. **Application ID required** — 4-6 week approval process
> Historical access/limit assertion withdrawn; verify publisher guidance.
3. **Japanese only** — responses are in Japanese
4. **T-prefix required** — registration numbers start with `T` + 13 digits
5. **Not an Indonesian API** — included for cross-reference only

</details>
