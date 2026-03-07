# OJK Financial Entity Legality

## Quick Check — SikapiUangmu Search

```python
import requests
from bs4 import BeautifulSoup

resp = requests.get("https://sikapiuangmu.ojk.go.id/FrontEnd/AlertPortal/Search",
    params={"q": "COMPANY_NAME"},
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, timeout=30)
soup = BeautifulSoup(resp.text, "html.parser")
for row in soup.select("table tbody tr"):
    cols = [td.text.strip() for td in row.find_all("td")]
    if cols: print(f"⚠️ {' | '.join(cols)}")
```

**Important:** No result does NOT mean legal — the entity may not be in the database.

## Illegal Investment Alert List (Satgas Waspada)

```python
resp = requests.get("https://waspadainvestasi.ojk.go.id/",
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, timeout=30)
# Parse the alert list table
```

Updated weekly. Covers: illegal P2P, unlicensed MLM, robot trading scams, crypto fraud.

## Licensed Entity Sources

| Type | URL | Format |
|------|-----|--------|
| Fintech P2P | `ojk.go.id/id/kanal/iknb/.../fintech/` | PDF |
| Investment Managers | `reksadana.ojk.go.id/Public/ManajerInvestasiList.aspx` | HTML |
| Securities | `ojk.go.id/id/kanal/pasar-modal/.../data-perusahaan-efek/` | Excel |
| Insurance | `ojk.go.id/id/kanal/iknb/.../asuransi/` | HTML |
| Pension Funds | `ojk.go.id/id/kanal/iknb/.../dana-pensiun/` | HTML |
| Multi-finance | `ojk.go.id/id/kanal/iknb/.../perusahaan-pembiayaan/` | HTML |

## Recommended Architecture

No unified API exists. Build your own:
1. Scrape all sources periodically (weekly)
2. Normalize into local database
3. Build search API on top

## Gotchas
- No stable API — OJK redesigns frequently
- ASP.NET ViewState on some pages
- P2P lending list is a PDF that changes URL each update
- Datacenter IPs may be blocked — use 2-5s delays
- BAPPEBTI (separate agency) covers crypto/futures
