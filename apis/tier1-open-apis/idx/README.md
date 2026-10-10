# IDX — Indonesia Stock Exchange

**Agency:** Bursa Efek Indonesia (Indonesia Stock Exchange)
**Portal:** https://www.idx.co.id
**Kind:** non-government; **catalog ID:** `idx`; **tier:** tier1
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Tier 1 is a historical routing group, not an assurance of an open API. Confirm the publisher, license, endpoint and response shape before integration.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Tier 1 is a historical routing group, not an assurance of an open API. Confirm the publisher, license, endpoint and response shape before integration.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Bursa Efek Indonesia (Indonesia Stock Exchange)
**Portal:** https://www.idx.co.id
**API type:** ⚠️ No official public API — unofficial endpoints + Yahoo Finance

## Overview

IDX does not provide an official public API. Data can be accessed through:
1. Unofficial IDX website endpoints
2. Yahoo Finance (recommended for most use cases)
3. IDX data feed services (paid)

## Yahoo Finance (Recommended)

Indonesian stocks use `.JK` suffix on Yahoo Finance.

```python
import yfinance as yf

# Get stock data
bbca = yf.Ticker("BBCA.JK")

# Historical prices
hist = bbca.history(period="1mo")
print(hist[["Open", "High", "Low", "Close", "Volume"]])

# Company info
info = bbca.info
print(f"Market Cap: {info.get('marketCap'):,}")
print(f"P/E Ratio: {info.get('trailingPE')}")

# Multiple stocks
tickers = yf.download(["BBCA.JK", "BBRI.JK", "TLKM.JK"], period="1mo")
```

### Popular Indonesian Stocks

| Ticker | Company |
|--------|---------|
| BBCA.JK | Bank Central Asia |
| BBRI.JK | Bank Rakyat Indonesia |
| BMRI.JK | Bank Mandiri |
| TLKM.JK | Telkom Indonesia |
| ASII.JK | Astra International |
| UNVR.JK | Unilever Indonesia |
| GOTO.JK | GoTo Group |

## Unofficial IDX Endpoints

These endpoints are used by the IDX website and may change without notice:

```python
import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Stock summary
resp = requests.get(
    "https://www.idx.co.id/primary/StockData/GetStockData",
    params={"start": 0, "length": 20, "code": "BBCA"},
    headers=headers,
    timeout=30,
)

# Trading summary
resp = requests.get(
    "https://www.idx.co.id/primary/TradingSummary/GetTradingSummary",
    params={"date": "20260307"},
    headers=headers,
    timeout=30,
)
```

## IDX Composite Index (IHSG)

```python
# IHSG via Yahoo Finance
ihsg = yf.Ticker("^JKSE")
hist = ihsg.history(period="1y")
print(f"Current IHSG: {hist['Close'].iloc[-1]:.2f}")
```

## Gotchas

1. **No official API** — IDX aggressively blocks automated access
2. **Yahoo Finance is the best free option** — reliable, but 15-minute delay
3. **`.JK` suffix required** — e.g., `BBCA.JK` not `BBCA`
4. **Trading hours** — 09:00-16:00 WIB (02:00-09:00 UTC), Mon-Fri
5. **Pre-opening session** — 08:45-09:00 WIB
6. **Corporate actions** — stock splits, rights issues affect historical data
7. **IDX website endpoints change frequently** — don't depend on them for production
8. **Paid alternatives** — Bloomberg, Refinitiv, or IDX data feed for real-time

</details>
