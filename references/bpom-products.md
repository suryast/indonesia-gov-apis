# BPOM Food, Drug & Cosmetics Registry

## Endpoint

`POST https://cekbpom.pom.go.id/produk-dt`

Requires: session cookie + CSRF token + `X-Requested-With: XMLHttpRequest` header.

## Setup Session

```python
import requests
from bs4 import BeautifulSoup

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

# Get CSRF token (must do before every search session)
page = session.get("https://cekbpom.pom.go.id/produk/pangan-olahan", timeout=30)
csrf = BeautifulSoup(page.text, "html.parser").find("meta", {"name": "csrf-token"})["content"]
```

## Search

```python
resp = session.post("https://cekbpom.pom.go.id/produk-dt", data={
    "_token": csrf,
    "draw": 1,
    "start": 0,
    "length": 25,
    "search[value]": "susu",
}, headers={"X-Requested-With": "XMLHttpRequest"}, timeout=30)

for p in resp.json().get("data", []):
    print(f"{p['no_reg']} | {p['nama_produk']} | {p['merk']} | {p['pendaftar']}")
```

## Product Categories

| Path | Category |
|------|----------|
| `/produk/pangan-olahan` | Processed food |
| `/produk/obat` | Drugs |
| `/produk/obat-tradisional` | Traditional medicine |
| `/produk/kosmetik` | Cosmetics |
| `/produk/suplemen-kesehatan` | Supplements |

Each has its own DataTables endpoint — same pattern, different CSRF page.

## Response Fields

| Field | Description |
|-------|-------------|
| `no_reg` | Registration number (MD/ML prefix) |
| `nama_produk` | Product name |
| `merk` | Brand |
| `kemasan` | Packaging |
| `pendaftar` | Registering company |
| `npwp` | Company tax ID |

## Gotchas
- CSRF expires after ~30min — re-fetch page to refresh
- Rate limit: 2s minimum between requests (aggressive blocking)
- Max page size: 100
- `X-Requested-With` header required
- Must use `requests.Session()` — not raw requests
- `npwp` field useful for cross-referencing with BPJPH data
