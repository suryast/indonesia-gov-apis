# BPS Statistics API

## Setup
Register for free API key at `webapi.bps.go.id/developer`.

## List Indicators

```python
import requests
API_KEY = "YOUR_KEY"
BASE = "https://webapi.bps.go.id/v1/api"

resp = requests.get(f"{BASE}/list/model/var/domain/0000/key/{API_KEY}", timeout=30)
for v in resp.json().get("data", []):
    print(f"var={v['var_id']}: {v['title']}")
```

## Get Data

```python
resp = requests.get(f"{BASE}/list/model/data/domain/0000/var/1/key/{API_KEY}", timeout=30)
for item in resp.json().get("data", []):
    print(f"{item.get('tahun')}: {item.get('data_content')}")
```

## Key Variables

| var | Indicator | Frequency |
|-----|-----------|-----------|
| 1 | Consumer Price Index (CPI) | Monthly |
| 2 | GDP Current Prices | Quarterly |
| 3 | GDP Constant Prices | Quarterly |
| 104 | Population | Annual |
| 517 | Imports by Commodity | Monthly |
| 518 | Exports by Commodity | Monthly |

## Domain Codes

| Code | Region |
|------|--------|
| `0000` | National |
| `3100` | DKI Jakarta |
| `3200` | Jawa Barat |
| `3300` | Jawa Tengah |
| `3500` | Jawa Timur |
| `5100` | Bali |

## Static Tables

```python
resp = requests.get(f"{BASE}/list/model/statictable/domain/0000/key/{API_KEY}", timeout=30)
# Returns downloadable table metadata
```

## Gotchas
- ~100 requests/day per API key
- Returns HTML on error — always check content-type
- Variable IDs are not sequential — discover via list endpoint
- Data lags 1-3 months
- Some datasets only available as Excel downloads, not via API
