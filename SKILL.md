---
name: querying-indonesian-gov-data
description: >
  Query 50 Indonesian government APIs and data sources — BPJPH halal certification,
  BPOM food safety, OJK financial legality, BPS statistics, BMKG weather/earthquakes,
  Bank Indonesia exchange rates, pasal.id law MCP, IDX stocks, CKAN open data portals.
  Use when building apps with Indonesian government data, scraping .go.id websites,
  checking halal certification, verifying company legality, looking up financial entity
  status, or connecting to Indonesian MCP servers. Includes ready-to-run Python patterns,
  CSRF handling, CKAN API usage, and IP blocking workarounds.
---

# Querying Indonesian Government Data

🇮🇩 STARTER_CHARACTER = 🇮🇩

Route the user's intent to the right child reference, then follow its patterns.

## Router

| User intent | Load reference | Quick pattern |
|------------|---------------|---------------|
| Halal certification, halal product check | [references/bpjph-halal.md](references/bpjph-halal.md) | `POST cmsbl.halal.go.id/api/search/data_penyelia` JSON, no auth |
| Food/drug/cosmetic registration, BPOM | [references/bpom-products.md](references/bpom-products.md) | Session + CSRF → `POST cekbpom.pom.go.id/produk-dt` |
| Is this fintech/investment legal, OJK | [references/ojk-legality.md](references/ojk-legality.md) | `GET sikapiuangmu.ojk.go.id/FrontEnd/AlertPortal/Search` |
| Weather in Indonesia, earthquake, tsunami | [references/bmkg-weather.md](references/bmkg-weather.md) | `GET data.bmkg.go.id/DataMKG/TEWS/autogempa.json` |
| GDP, inflation, population, trade stats | [references/bps-statistics.md](references/bps-statistics.md) | `GET webapi.bps.go.id/v1/api/...` (free API key) |
| USD/IDR exchange rate, BI Rate | [references/bank-indonesia.md](references/bank-indonesia.md) | Scrape `bi.go.id/id/statistik/informasi-kurs/` |
| Indonesian law, regulation, specific pasal | [references/pasal-id-law.md](references/pasal-id-law.md) | MCP: `claude mcp add --transport http pasal-id ...` |
| Government datasets on any topic | [references/ckan-portals.md](references/ckan-portals.md) | `GET {portal}/api/3/action/package_search` |
| Disaster risk for a location | [references/inarisk-disaster.md](references/inarisk-disaster.md) | `GET inarisk.bnpb.go.id/api/risk/score?lat=&lon=` |
| Verify company is registered | [references/company-verification.md](references/company-verification.md) | OpenCorporates → OCCRP → AHU cross-ref |
| Indonesian stock prices, IHSG | [references/idx-stocks.md](references/idx-stocks.md) | `yfinance` with `.JK` suffix |

## Workflow

1. Match user intent to a row in the Router table above
2. Read the linked reference file for full endpoint docs and code
3. Adapt the pattern with user's specific query/parameters
4. Execute and handle failures per the section below

## Failure Modes

**IP Blocked (403 / Timeout):** Most `.go.id` sites block datacenter IPs. Add 2-5s delays or route through Cloudflare Workers proxy.

**CSRF Expired:** Re-fetch the HTML page, extract fresh `csrf-token` from `<meta>` tag. Applies to BPOM.

**Rate Limits:** BPS ~100/day, OpenCorporates 500/day, OCCRP 60/min, BPOM 2s gap minimum.

**Required Headers:**
```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
}
```

**Data Formats:** Indonesian gov sites use Excel (.xlsx) and PDF heavily. Parse with `openpyxl` and `pdfplumber`. JSON APIs are the exception.

## Extended Docs

For sources not in the Router (procurement, courts, wealth declarations, geospatial, regional portals, ministry-specific data), see the full docs:
- `apis/tier1-open-apis/` — 12 sources with REST/JSON APIs
- `apis/tier2-scrapeable/` — 10 sources requiring scraping
- `apis/tier3-regional/` — 6 regional CKAN portals
- `apis/tier4-ministry/` through `apis/tier7-civil-society/` — 22 more sources
- `mcp-servers/` — MCP server setup and opportunities
