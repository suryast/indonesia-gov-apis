# Indonesia Government Data — Agent Skill

Use this skill when you need to query Indonesian government data sources. Each section below gives you a ready-to-run pattern. Copy, adapt, execute.

---

## 1. Search Halal-Certified Businesses (BPJPH)

**When:** User asks about halal certification, halal products, or food safety in Indonesia.

```python
import requests

resp = requests.post(
    "https://cmsbl.halal.go.id/api/search/data_penyelia",
    json={"nama_penyelia": "QUERY", "start": 0, "length": 20},
    headers={"Content-Type": "application/json"},
    timeout=30,
)
for biz in resp.json().get("data", []):
    print(f"{biz['nama']} | {biz.get('kota_kab', '')} | Cert: {biz.get('nomor_sertifikat', '')} | Expires: {biz.get('berlaku_sampai', '')}")
```

- No auth needed. Max 100 per page.
- `nama_penyelia` is a supervisor name prefix filter — use single letters ("A", "B") for broad results.
- For bulk: iterate A-Z prefixes with 1s delay.

---

## 2. Check Food/Drug Registration (BPOM)

**When:** User asks if a product is registered with BPOM, or about food/drug safety.

```python
import requests
from bs4 import BeautifulSoup

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

# Step 1: Get CSRF token
page = session.get("https://cekbpom.pom.go.id/produk/pangan-olahan", timeout=30)
csrf = BeautifulSoup(page.text, "html.parser").find("meta", {"name": "csrf-token"})["content"]

# Step 2: Search
resp = session.post("https://cekbpom.pom.go.id/produk-dt", data={
    "_token": csrf, "draw": 1, "start": 0, "length": 25,
    "search[value]": "QUERY",
}, headers={"X-Requested-With": "XMLHttpRequest"}, timeout=30)

for item in resp.json().get("data", []):
    print(f"{item['no_reg']} | {item['nama_produk']} | {item['merk']} | {item['pendaftar']}")
```

- CSRF token required — always fetch page first.
- Categories: `/produk/pangan-olahan` (food), `/produk/obat` (drugs), `/produk/kosmetik` (cosmetics).
- Rate limit: 2s between requests minimum.

---

## 3. Check Financial Entity Legality (OJK)

**When:** User asks if a fintech, investment platform, or financial entity is legal/licensed.

```python
import requests
from bs4 import BeautifulSoup

resp = requests.get(
    "https://sikapiuangmu.ojk.go.id/FrontEnd/AlertPortal/Search",
    params={"q": "COMPANY_NAME"},
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    timeout=30,
)
soup = BeautifulSoup(resp.text, "html.parser")
for row in soup.select("table tbody tr"):
    cols = [td.text.strip() for td in row.find_all("td")]
    if cols:
        print(f"⚠️ {' | '.join(cols)}")
```

- Also check the illegal investment alert list: `waspadainvestasi.ojk.go.id`
- No result does NOT mean legal — it may not be in the database.

---

## 4. Get Weather & Earthquake Data (BMKG)

**When:** User asks about weather in Indonesia, earthquakes, or tsunami alerts.

```python
import requests

# Latest earthquake
resp = requests.get("https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json", timeout=30)
q = resp.json()["Infogempa"]["gempa"]
print(f"M{q['Magnitude']} | {q['Wilayah']} | {q['Tanggal']} {q['Jam']} | Depth: {q['Kedalaman']}")

# Recent 15 earthquakes
resp = requests.get("https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json", timeout=30)
for q in resp.json()["Infogempa"]["gempa"]:
    print(f"M{q['Magnitude']} | {q['Wilayah']}")

# Weather forecast (XML) — replace province code
# resp = requests.get("https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-DKIJakarta.xml")
```

- No auth, no rate limit stated. Real-time data.
- Province codes for weather: `DKIJakarta`, `JawaBarat`, `JawaTimur`, `Bali`, etc.

---

## 5. Search National Statistics (BPS)

**When:** User asks about Indonesian GDP, inflation, population, poverty, trade data.

```python
import requests

API_KEY = "YOUR_BPS_API_KEY"  # Free at webapi.bps.go.id/developer
BASE = "https://webapi.bps.go.id/v1/api"

# List variables/indicators
resp = requests.get(f"{BASE}/list/model/var/domain/0000/key/{API_KEY}", timeout=30)

# Get specific data (var=1 = CPI)
resp = requests.get(f"{BASE}/list/model/data/domain/0000/var/1/key/{API_KEY}", timeout=30)
for item in resp.json().get("data", []):
    print(f"{item.get('tahun')}: {item.get('data_content')}")
```

- Free API key — register at `webapi.bps.go.id/developer`.
- Domain `0000` = national. Provinces use `XX00` codes.
- ~100 requests/day limit.

---

## 6. Get Exchange Rates (Bank Indonesia)

**When:** User asks about IDR exchange rate, USD/IDR, or BI Rate.

```python
import requests
from bs4 import BeautifulSoup

resp = requests.get(
    "https://www.bi.go.id/id/statistik/informasi-kurs/transaksi-bi/Default.aspx",
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    timeout=30,
)
soup = BeautifulSoup(resp.text, "html.parser")
table = soup.find("table", class_="table1")
for row in table.find_all("tr")[1:]:
    cols = [td.text.strip() for td in row.find_all("td")]
    if len(cols) >= 3:
        print(f"{cols[0]}: Buy {cols[1]} / Sell {cols[2]}")
```

- JISDOR published at 10:00 WIB (03:00 UTC) each trading day.
- No weekend/holiday rates.
- BI API sandbox: `api-sandbox.bi.go.id` (needs OAuth2 registration).

---

## 7. Search Indonesian Law (pasal.id MCP)

**When:** User asks about Indonesian regulations, laws (UU), or specific pasal/articles.

### Option A: MCP (if available)
```bash
claude mcp add --transport http pasal-id https://pasal-mcp-server-production.up.railway.app/mcp
```
Then ask Claude: "What does UU Perlindungan Data Pribadi say about consent?"

### Option B: Direct API
```python
import requests

# Search regulations
resp = requests.get("https://pasal-mcp-server-production.up.railway.app/api/search", params={
    "q": "perlindungan data pribadi",
    "limit": 10,
}, timeout=30)
```

- 40,143 regulations, 937,155 articles.
- Tools: `search_laws`, `get_pasal`, `get_law_status`, `get_law_content`.

---

## 8. Search Open Data Portal (data.go.id / CKAN)

**When:** User asks for Indonesian government datasets on any topic.

```python
import requests

# Works for: data.go.id, satudata.jakarta.go.id, opendata.jabarprov.go.id, etc.
PORTAL = "data.go.id"

resp = requests.get(f"https://{PORTAL}/api/3/action/package_search", params={
    "q": "KEYWORD_IN_INDONESIAN",  # e.g., "keuangan", "kesehatan", "penduduk"
    "rows": 10,
}, timeout=30)

for ds in resp.json()["result"]["results"]:
    print(f"{ds['title']}")
    for r in ds.get("resources", []):
        print(f"  └ {r['format']}: {r['url']}")
```

- Same CKAN API works for all portals: data.go.id, Jakarta, Jabar, Jatim, Surabaya, Bandung.
- Search queries should be in Indonesian (Bahasa).

---

## 9. Check Disaster Risk by Location (InaRisk)

**When:** User asks about natural disaster risk for a specific location in Indonesia.

```python
import requests

resp = requests.get("https://inarisk.bnpb.go.id/api/risk/score", params={
    "lat": -6.2088,   # latitude
    "lon": 106.8456,  # longitude
}, timeout=30)
risk = resp.json()
# Returns risk scores per hazard: flood, earthquake, tsunami, volcano, landslide
```

- No auth needed. Coordinate-based queries.
- Complements BMKG for comprehensive disaster awareness.

---

## 10. Look Up Indonesian Companies (AHU / OpenCorporates)

**When:** User asks to verify if a company is legally registered in Indonesia.

```python
import requests

# Option A: OpenCorporates (structured, rate-limited)
resp = requests.get("https://api.opencorporates.com/v0.4/companies/search", params={
    "q": "COMPANY_NAME",
    "jurisdiction_code": "id",
}, timeout=30)

# Option B: OCCRP Aleph (beneficial ownership, leaks)
API_KEY = "your-aleph-key"  # Free at aleph.occrp.org
resp = requests.get("https://aleph.occrp.org/api/2/entities", params={
    "q": "COMPANY_NAME",
    "filter:countries": "id",
}, headers={"Authorization": f"ApiKey {API_KEY}"}, timeout=30)
```

- OpenCorporates: 500 free requests/day. Indonesian data from AHU.
- OCCRP Aleph: 60 req/min. Includes Panama/Pandora Papers data.
- AHU direct (`ahu.go.id`): has CAPTCHA, harder to automate.

---

## 11. Get Stock Market Data (IDX)

**When:** User asks about Indonesian stocks, IHSG, or specific tickers.

```python
import yfinance as yf

# Indonesian stocks use .JK suffix
stock = yf.Ticker("BBCA.JK")
hist = stock.history(period="1mo")
print(hist[["Close", "Volume"]].tail())

# IHSG composite index
ihsg = yf.Ticker("^JKSE")
print(f"IHSG: {ihsg.history(period='1d')['Close'].iloc[-1]:.2f}")
```

- Use Yahoo Finance — IDX has no official public API.
- Common tickers: BBCA.JK, BBRI.JK, BMRI.JK, TLKM.JK, ASII.JK, GOTO.JK.

---

## Common Gotchas (All Sources)

### IP Blocking
Most Indonesian gov sites block datacenter IPs. If requests fail with 403/timeout:
- Route through a Cloudflare Workers proxy
- Add 2-5s delays between requests
- Use residential proxy as last resort

### Headers
Always include User-Agent. Some sites also check Accept-Language:
```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
}
```

### Data Formats
- Government sites love **Excel (.xlsx)** and **PDF** — use `openpyxl` and `pdfplumber`
- JSON APIs are the exception, not the rule
- Always check encoding — most UTF-8, some older sites use Windows-1252
