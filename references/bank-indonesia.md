# Bank Indonesia — Exchange Rates & Monetary Data

## Exchange Rates (Web Scraping)

```python
import requests
from bs4 import BeautifulSoup

resp = requests.get("https://www.bi.go.id/id/statistik/informasi-kurs/transaksi-bi/Default.aspx",
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, timeout=30)
table = BeautifulSoup(resp.text, "html.parser").find("table", class_="table1")
for row in table.find_all("tr")[1:]:
    cols = [td.text.strip() for td in row.find_all("td")]
    if len(cols) >= 3: print(f"{cols[0]}: Buy {cols[1]} / Sell {cols[2]}")
```

## BI API Sandbox

```python
# OAuth2 registration required at api-sandbox.bi.go.id
resp = requests.get("https://api-sandbox.bi.go.id/openapi/snap/v1/transfer-interbank",
    headers={"Authorization": "Bearer ACCESS_TOKEN"}, timeout=30)
```

## Key Data

| Data | Update | Source |
|------|--------|--------|
| JISDOR (USD/IDR) | Daily 10:00 WIB | Kurs page |
| BI 7-Day RR Rate | Monthly | Monetary page |
| Inflation | Monthly | Statistics section |
| M1/M2 Money Supply | Monthly | Excel download |

## Gotchas
- JISDOR published 10:00 WIB (03:00 UTC) business days only
- No weekend/holiday rates
- Web scraping needs ASP.NET ViewState handling for some pages
- API sandbox requires partnership for production access
- Excel downloads for detailed statistical data
