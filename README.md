# 🇮🇩 Indonesia Government APIs & Data Sources

A comprehensive reference for **50 Indonesian government data portals, APIs, and data sources** — with practical Python examples, scraping patterns, and gotchas learned from production use.

> **Why this exists:** Indonesian government APIs are poorly documented, frequently change without notice, and have quirks not covered in official docs. This repo captures real-world knowledge from building production applications against these data sources.

## 🤖 Use as an AI Agent Skill

This repo includes a [`SKILL.md`](SKILL.md) that makes it usable as a Claude/OpenClaw agent skill:

```bash
# Clone and use as a local skill reference
git clone https://github.com/suryast/indonesia-gov-apis.git
```

## 🔌 MCP Servers

Connect Indonesian data sources to AI assistants via [Model Context Protocol](https://modelcontextprotocol.io):

```bash
# Connect pasal.id (third-party Indonesian law index) to Claude
claude mcp add --transport http pasal-id https://pasal-mcp-server-production.up.railway.app/mcp
```

See [`mcp-servers/`](mcp-servers/) for full setup instructions and a list of data sources ready for MCP wrapping.

---

## Data Sources by Tier

### Tier 1: Open APIs — Ready to Consume (12 sources)

| # | Source | Agency | Docs | API? |
|---|--------|--------|------|------|
| 1 | [Portal Satu Data (SDI)](apis/tier1-open-apis/data-go-id/) | Bappenas | CKAN portal, 10K+ datasets | ✅ CKAN API |
| 2 | [BPS Statistics](apis/tier1-open-apis/bps/) | Badan Pusat Statistik | GDP, CPI, population, trade | ✅ REST API |
| 3 | [BMKG Weather](apis/tier1-open-apis/bmkg/) | BMKG | Weather, earthquakes, tsunami | ✅ JSON feeds |
| 4 | [IDX / BEI](apis/tier1-open-apis/idx/) | Bursa Efek Indonesia | Stock prices, corporate data | ⚠️ Unofficial |
| 5 | [DJPB Treasury](apis/tier1-open-apis/djpb-treasury/) | Kemenkeu | Treasury, disbursement data | ✅ CKAN API |
| 6 | [JDIH BPK](apis/tier1-open-apis/jdih-bpk/) | BPK / Perpusnas | Legal documentation network | ✅ Partial API |
| 7 | [Putusan MA](apis/tier1-open-apis/putusan-ma/) | Mahkamah Agung | Court decisions (millions) | ✅ Public search |
| 8 | [LPSE / INAPROC](apis/tier1-open-apis/lpse-inaproc/) | LKPP | Government procurement tenders | ⚠️ Migrating to inaproc.id (CF challenge) |
| 9 | [Portal APBN](apis/tier1-open-apis/apbn-kemenkeu/) | Kemenkeu | State budget data | ✅ CSV/XLSX |
| 10 | [Bank Indonesia](apis/tier1-open-apis/bank-indonesia/) | Bank Indonesia | Exchange rates, BI Rate | ✅ REST API |
| 11 | [BIG Geospatial](apis/tier1-open-apis/big-geospatial/) | BIG | Admin boundaries, zoning | ✅ WMS/WFS |
| 12 | [BNPB Disaster](apis/tier1-open-apis/bnpb-disaster/) | BNPB | Disaster events, risk data | ✅ REST + GeoJSON |

### Tier 2: Scrapeable Web — Structured Data, No Formal API (10 sources)

| # | Source | Agency | Docs | Format |
|---|--------|--------|------|--------|
| 13 | [BPJPH Halal](apis/tier2-scrapeable/bpjph/) | BPJPH Kemenag | 1.98M halal businesses | JSON POST |
| 14 | [BPOM Products](apis/tier2-scrapeable/bpom/) | BPOM | 242K food/drug registrations | DataTables+CSRF |
| 15 | [AHU Company Registry](apis/tier2-scrapeable/ahu-company/) | Kemenkumham | All registered PT, CV, Firma | HTML+CAPTCHA |
| 16 | [OSS / NIB](apis/tier2-scrapeable/oss-nib/) | BKPM | Business ID (NIB) lookup | HTML forms |
| 17 | [OJK Registry](apis/tier2-scrapeable/ojk/) | OJK | Licensed financial entities | HTML+XLS |
| 18 | [KPK e-LHKPN](apis/tier2-scrapeable/kpk-lhkpn/) | KPK | Officials' wealth declarations | HTML+PDF |
| 19 | [Putusan MK](apis/tier2-scrapeable/putusan-mk/) | Mahkamah Konstitusi | Constitutional court decisions | HTML+PDF |
| 20 | [KSEI Statistics](apis/tier2-scrapeable/ksei/) | KSEI | Securities investor stats | PDF/XLSX |
| 21 | [e-PPID](apis/tier2-scrapeable/ppid/) | All Ministries | Public information requests | Per ministry |
| 22 | [Pajak / DJP](apis/tier2-scrapeable/pajak-djp/) | DJP | NPWP verification | Login required |

### Tier 3: Regional Open Data Portals (6 sources)

| # | Source | Region | Docs | Quality |
|---|--------|--------|------|---------|
| 23 | [Satu Data Jakarta](apis/tier3-regional/satu-data-jakarta/) | DKI Jakarta | Best-in-class regional | ⭐ CKAN API |
| 24 | [Open Data Jabar](apis/tier3-regional/opendata-jabar/) | Jawa Barat | Good API quality | ⭐ CKAN API |
| 25 | [Open Data Jatim](apis/tier3-regional/opendata-jatim/) | Jawa Timur | 38 kabupaten/kota | ✅ CKAN API |
| 26 | [Satu Data Surabaya](apis/tier3-regional/satu-data-surabaya/) | Surabaya | Complete city-level | ✅ CKAN API |
| 27 | [Open Data Bandung](apis/tier3-regional/opendata-bandung/) | Bandung | Smart city data | ✅ CKAN API |
| 28 | [Open Data Bali](apis/tier3-regional/opendata-bali/) | Bali | Tourism, agriculture | ⚠️ CSV/XLSX |

### Tier 4: Ministry-Specific Data (8 sources)

| # | Source | Ministry | Docs | Key Data |
|---|--------|----------|------|----------|
| 29 | [Kemnaker](apis/tier4-ministry/kemnaker/) | Ketenagakerjaan | UMR/UMP wages, employment stats | ⚠️ Partial API |
| 30 | [Komdigi](apis/tier4-ministry/komdigi/) | Komunikasi Digital | Internet penetration, digital literacy | ⚠️ XLSX |
| 31 | [ESDM Energy](apis/tier4-ministry/esdm-energy/) | ESDM | Energy production, mining permits | ⚠️ PDF/XLSX |
| 32 | [KKP Fisheries](apis/tier4-ministry/kkp-fisheries/) | Kelautan & Perikanan | Fish catch, aquaculture, vessels | ⚠️ XLSX |
| 33 | [ATR/BPN Land](apis/tier4-ministry/atr-bpn/) | ATR / BPN | Land certificates, PTSL | ❌ Login |
| 34 | [Kemendikdasmen](apis/tier4-ministry/kemendikdasmen/) | Pendidikan | School registry (NPSN), teachers | ⚠️ Partial API |
| 35 | [Kemenkes Health](apis/tier4-ministry/kemenkes/) | Kesehatan | Hospital/clinic registry, SATUSEHAT | ⚠️ Partial API |
| 36 | [Kemenag](apis/tier4-ministry/kemenag/) | Agama | 300K+ mosques, pesantren registry | ⚠️ Scrape |

### Tier 5: Anti-Corruption & Transparency (5 sources)

| # | Source | Organization | Docs | Key Data |
|---|--------|-------------|------|----------|
| 37 | [OCCRP Aleph](apis/tier5-transparency/occrp-aleph/) | OCCRP | Beneficial ownership, leaks data | ✅ REST API |
| 38 | [OpenCorporates](apis/tier5-transparency/opencorporates/) | OpenCorporates | Global company registry (ID subset) | ✅ REST API |
| 39 | [EITI Indonesia](apis/tier5-transparency/eiti-indonesia/) | EITI / ESDM | Mining & oil/gas revenue transparency | ⚠️ Reports |
| 40 | [AHU-BO](apis/tier5-transparency/ahu-bo/) | Kemenkumham | Beneficial ownership registry | ⚠️ Web search |
| 41 | [ICW Corruption Watch](apis/tier5-transparency/icw-corruption/) | ICW (NGO) | Corruption case tracker | ⚠️ Web database |

### Tier 6: Financial Sector (4 sources)

| # | Source | Agency | Docs | Key Data |
|---|--------|--------|------|----------|
| 42 | [OJK SIKEPO](apis/tier6-financial/ojk-sikepo/) | OJK | Fintech/crypto licensed platforms | ⚠️ PDF+HTML |
| 43 | [Satgas Waspada Investasi](apis/tier6-financial/satgas-waspada/) | OJK Task Force | Illegal investment alerts | ✅ Public list |
| 44 | [KSEI Investor Stats](apis/tier6-financial/ksei-stats/) | KSEI | Monthly investor statistics | ⚠️ XLSX/PDF |
| 45 | [DJPB Budget](apis/tier6-financial/djpb-budget/) | DJPB Kemenkeu | APBN spending execution | ⚠️ XLS/CSV |

### Tier 7: Civil Society & Geospatial (5 sources)

| # | Source | Organization | Docs | Key Data |
|---|--------|-------------|------|----------|
| 46 | [LAPOR!](apis/tier7-civil-society/lapor/) | KemenPANRB | Public complaint system | ⚠️ Web portal |
| 47 | [IndoLII](apis/tier7-civil-society/indolii/) | USAID | Bilingual legal information | ⚠️ Web search |
| 48 | [OGP Indonesia](apis/tier7-civil-society/ogp-indonesia/) | OGP | Ministry transparency scores | ⚠️ Reports |
| 49 | [Geoportal One Map](apis/tier7-civil-society/geoportal-onemap/) | BIG / KLHK | 85 thematic maps, One Map Policy | ✅ WMS/WFS |
| 50 | [SIGAP / InaRisk](apis/tier7-civil-society/sigap-inarisk/) | BNPB | Disaster risk scores by location | ✅ REST API |
| 51 | [pasal.id](apis/tier7-civil-society/pasal-id/) | Community (third-party) | 40K regulations, 937K articles via MCP | 🔵 MCP Ready |

---

## Quick Start

```python
# Search BPJPH halal database
import requests

resp = requests.post(
    "https://cmsbl.halal.go.id/api/search/data_penyelia",
    json={"length": 20, "start": 0, "nama_penyelia": "A"},
    headers={"Content-Type": "application/json"}
)
businesses = resp.json()["data"]
print(f"Found {len(businesses)} businesses")
```

```python
# Get BMKG earthquake data (no auth needed)
resp = requests.get("https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json")
quake = resp.json()["Infogempa"]["gempa"]
print(f"Latest: M{quake['Magnitude']} at {quake['Wilayah']}")
```

## Common Gotchas

### 🚫 IP Blocking
Most Indonesian gov sites block datacenter IPs (AWS, GCP, DO). Use Cloudflare Workers proxy or residential proxy.

### 📄 Data Formats
Government sites love Excel and PDF. Use `openpyxl` for Excel, `pdfplumber` for PDF.

### 🔐 CSRF Tokens
BPOM and some OJK pages require session cookies + CSRF tokens. Always use `requests.Session()`.

### 🔄 CKAN API
data.go.id, Jakarta, Jabar, Jatim, Surabaya, Bandung all use CKAN. Same API pattern works everywhere:
```python
requests.get("https://{portal}/api/3/action/package_search", params={"q": "keyword", "rows": 10})
```

## Project Structure

```
├── README.md
├── SKILL.md                      # AI agent skill file
├── mcp-servers/                  # MCP server setup guides
├── apis/
│   ├── tier1-open-apis/          # 12 sources with REST/JSON APIs
│   ├── tier2-scrapeable/         # 10 sources requiring scraping
│   ├── tier3-regional/           # 6 regional open data portals
│   ├── tier4-ministry/           # 8 ministry-specific sources
│   ├── tier5-transparency/       # 5 anti-corruption sources
│   ├── tier6-financial/          # 4 financial sector sources
│   └── tier7-civil-society/      # 5 civil society & geospatial
└── examples/                     # Working Python examples
```

## 📅 Portal Status Timeline

Daily log of which Indonesian government portals are accessible, blocked, or down. Monitored from Sydney (AU), Singapore, and Jakarta (ID) via [indonesia-civic-signal-monitor](https://github.com/suryast/indonesia-civic-signal-monitor).

**Why this matters:** Indonesian government websites frequently go down, change URLs, add geo-blocks, or break without notice. There's no public status page. This is the closest thing to one.

### 2026-03-16 (Monday)

Checked from Sydney, Australia (AU) and Jakarta, Indonesia (ID). Status: ✅ Working, ⚠️ Degraded/Blocked, ❌ Down.

#### Tier 1: Open APIs

| # | Portal | AU | ID | Status | Notes |
|---|--------|----|----|--------|-------|
| 1 | **Satu Data** (data.go.id) | ✅ 200 | ✅ | ✅ Working | CKAN API stable |
| 2 | **BPS** (webapi.bps.go.id) | ❌ 403 | ❌ 403 | ⚠️ CF Challenge | Cloudflare bot protection on both AU and ID. API works with key via `requests` but not `curl` |
| 3 | **BMKG** (data.bmkg.go.id) | ✅ 200 | ✅ | ✅ Working | Earthquake + weather JSON feeds stable |
| 4 | **IDX** (idx.co.id) | ❌ 403 | ❌ 403 | ⚠️ CF Challenge | Cloudflare bot protection. Web works in browser |
| 5 | **DJPB Treasury** (data.treasury.kemenkeu.go.id) | ❌ DNS | ❌ DNS | ❌ DNS Dead | NXDOMAIN from everywhere |
| 6 | **JDIH BPK** (jdih.bpk.go.id) | ❌ 403 | ✅ 200 | ⚠️ Geo-blocked | Blocked from AU datacenter IPs |
| 7 | **Putusan MA** (putusan3.mahkamahagung.go.id) | ❌ Timeout | ❌ Timeout | ❌ Down | DNS resolves (103.16.79.91) but connection times out from both AU and ID |
| 8 | **LPSE** (spse.inaproc.id) | ❌ 403 | ✅ 200 | ⚠️ Geo-blocked | CF Turnstile challenge. Individual `lpse.*.go.id` portals all broken — LKPP CNAME migration to `ars.inaproc.id` caused "CNAME Cross-User Banned" on CF. 589 portals affected |
| 9 | **Portal APBN** (data.anggaran.kemenkeu.go.id) | ❌ DNS | ❌ DNS | ❌ DNS Dead | NXDOMAIN from everywhere |
| 10 | **Bank Indonesia** (www.bi.go.id) | ⚠️ 302 | ✅ | ✅ Working | Redirects to `/id/` — normal behavior |
| 11 | **BIG Geospatial** (tanahair.indonesia.go.id) | ❌ Timeout | ❌ Timeout | ❌ Down | DNS resolves (202.4.179.23) but server unresponsive |
| 12 | **BNPB Disaster** (dibi.bnpb.go.id) | ✅ 200 | ✅ | ✅ Working | REST + GeoJSON API stable |

#### Tier 2: Scrapeable Web

| # | Portal | AU | ID | Status | Notes |
|---|--------|----|----|--------|-------|
| 13 | **BPJPH** (sertifikasi.halal.go.id) | ❌ DNS | ❌ DNS | ❌ DNS Dead | Old cert search portal gone. `bpjph.halal.go.id` is alive but it's a Gatsby news site — no public cert search API |
| 14 | **BPOM** (cekbpom.pom.go.id) | ✅ 200 | ✅ | ✅ Working | Redesigned — old `/produk/0/{id}` URLs all 404. New endpoint: `POST /produk-dt/all` (DataTables + CSRF). 639K+ products |
| 15 | **AHU** (ahu.go.id) | ❌ Timeout | ✅ 200 | ⚠️ Geo-blocked | Company registry in extended maintenance. Accessible from ID but returns 0 records |
| 16 | **OSS** (oss.go.id) | ✅ 200 | ✅ 200 | ⚠️ Changed | Site loads but `/informasi/pencarian-nib` returns 404 from everywhere — public NIB search page removed |
| 17 | **OJK Registry** (sikapiuangmu.ojk.go.id) | ❌ 403 | ✅ 200 | ⚠️ Geo-blocked | Blacklist data accessible only via Indonesian IP |
| 18 | **OJK API** (api.ojk.go.id) | ❌ DNS | ❌ DNS | ❌ DNS Dead | NXDOMAIN from everywhere since at least Mar 10 |
| 19 | **LHKPN** (elhkpn.kpk.go.id) | ✅ 200 | ✅ 200 | ⚠️ Auth Wall | Page loads but redirects to reCAPTCHA + login. Wealth declaration search was previously public |
| 20 | **Putusan MK** (putusan.mahkamahkonstitusi.go.id) | ❌ DNS | ❌ DNS | ❌ DNS Dead | NXDOMAIN from everywhere |
| 21 | **KSEI** (www.ksei.co.id) | ❌ Timeout | ✅ 200 | ⚠️ Geo-blocked | Blocks datacenter IPs |
| 22 | **e-PPID** (ppid.kemenkeu.go.id) | ❌ DNS | ❌ DNS | ❌ DNS Dead | NXDOMAIN from everywhere |
| 23 | **Pajak / DJP** (ereg.pajak.go.id) | ❌ Timeout | ❌ Timeout | ❌ Down | DNS resolves (103.28.106.134) but connection times out from both |

#### Tier 3: Regional Open Data

| # | Portal | AU | ID | Status | Notes |
|---|--------|----|----|--------|-------|
| 24 | **Satu Data Jakarta** (data.jakarta.go.id) | ✅ 200 | ✅ | ✅ Working | Best regional portal, CKAN API |
| 25 | **Open Data Jabar** (opendata.jabarprov.go.id) | ❌ 403 | ❌ 403 | ❌ CF Challenge | Cloudflare blocking from both AU and ID |
| 26 | **Open Data Jatim** (data.jatimprov.go.id) | ❌ DNS | ❌ DNS | ❌ DNS Dead | NXDOMAIN |
| 27 | **Satu Data Surabaya** (data.surabaya.go.id) | ❌ DNS | ❌ DNS | ❌ DNS Dead | NXDOMAIN |
| 28 | **Open Data Bandung** (data.bandung.go.id) | ❌ Timeout | ❌ Timeout | ❌ Down | DNS resolves (202.58.242.113) but unresponsive |
| 29 | **Open Data Bali** (data.baliprov.go.id) | ❌ DNS | ❌ DNS | ❌ DNS Dead | NXDOMAIN |

#### Tier 4: Ministry-Specific

| # | Portal | AU | ID | Status | Notes |
|---|--------|----|----|--------|-------|
| 30 | **Kemnaker** (kemnaker.go.id) | ✅ 200 | ✅ | ✅ Working | |
| 31 | **Komdigi** (komdigi.go.id) | ❌ 403 | ❌ 403 | ❌ CF Challenge | Cloudflare blocking from both |
| 32 | **ESDM** (www.esdm.go.id) | ✅ 200 | ✅ | ✅ Working | |
| 33 | **KKP** (kkp.go.id) | ✅ 200 | ✅ | ✅ Working | |
| 34 | **ATR/BPN** (www.atrbpn.go.id) | ✅ 200 | ✅ | ✅ Working | |
| 35 | **Kemendikdasmen** (dapo.kemdikbud.go.id) | ❌ DNS | ❌ DNS | ❌ DNS Dead | NXDOMAIN — ministry restructured from Kemdikbud |
| 36 | **Kemenkes** (sirs.kemkes.go.id) | ✅ 200 | ✅ | ✅ Working | Hospital/clinic registry |
| 37 | **Kemenag** (simas.kemenag.go.id) | ✅ 200 | ✅ | ✅ Working | Mosque registry |

#### Tier 5: Transparency

| # | Portal | AU | ID | Status | Notes |
|---|--------|----|----|--------|-------|
| 38 | **OCCRP Aleph** (aleph.occrp.org) | ✅ 200 | ✅ | ✅ Working | International — no geo-blocking |
| 39 | **OpenCorporates** (opencorporates.com) | ❌ 403 | ❌ 403 | ⚠️ Bot Protection | Rate-limited, needs API key |
| 40 | **EITI Indonesia** (eiti.esdm.go.id) | ❌ DNS | ❌ DNS | ❌ DNS Dead | NXDOMAIN |
| 41 | **AHU-BO** (ahu.go.id) | ❌ Timeout | ✅ 200 | ⚠️ Geo-blocked | Same as AHU (#15) — accessible from ID only |
| 42 | **ICW** (antikorupsi.org) | ✅ 200 | ✅ | ✅ Working | |

#### Tier 6: Financial

| # | Portal | AU | ID | Status | Notes |
|---|--------|----|----|--------|-------|
| 43 | **OJK SIKEPO** (ojk.go.id) | ❌ Timeout | ✅ 200 | ⚠️ Geo-blocked | Main OJK site blocked from AU |
| 44 | **Satgas Waspada** (sikapiuangmu.ojk.go.id) | ❌ 403 | ✅ 200 | ⚠️ Geo-blocked | Same as OJK Registry (#17) |
| 45 | **KSEI Stats** (www.ksei.co.id) | ❌ Timeout | ✅ 200 | ⚠️ Geo-blocked | Same as KSEI (#21) |
| 46 | **DJPB Budget** (djpb.kemenkeu.go.id) | ✅ 200 | ✅ | ✅ Working | |

#### Tier 7: Civil Society & Geospatial

| # | Portal | AU | ID | Status | Notes |
|---|--------|----|----|--------|-------|
| 47 | **LAPOR!** (www.lapor.go.id) | ✅ 200 | ✅ | ✅ Working | |
| 48 | **IndoLII** (www.indolii.org) | ❌ DNS | ❌ DNS | ❌ DNS Dead | NXDOMAIN — project may have shut down |
| 49 | **Geoportal** (tanahair.indonesia.go.id) | ❌ Timeout | ❌ Timeout | ❌ Down | Same as BIG (#11) |
| 50 | **InaRisk** (inarisk.bnpb.go.id) | ✅ 200 | ✅ | ✅ Working | |
| 51 | **pasal.id** (pasal.id) | ✅ 200 | ✅ | ✅ Working | Community-run, MCP-ready |

#### Summary

| Category | Count | Portals |
|----------|-------|---------|
| ✅ **Working** (from everywhere) | **19** | Satu Data, BMKG, BI, BNPB, BPOM, OSS*, Kemnaker, ESDM, KKP, ATR/BPN, Kemenkes, Kemenag, OCCRP, ICW, DJPB Budget, LAPOR!, InaRisk, pasal.id, Jakarta |
| ⚠️ **Geo-blocked** (ID only) | **8** | JDIH BPK, LPSE, AHU/AHU-BO, OJK Registry, OJK SIKEPO, Satgas Waspada, KSEI |
| ⚠️ **CF Challenge** (bot protection) | **4** | BPS, IDX, Jabar, Komdigi |
| ⚠️ **Changed/Degraded** | **2** | LHKPN (auth wall), OSS (search page removed) |
| ❌ **DNS Dead** | **13** | DJPB Treasury, APBN, BPJPH, OJK API, Putusan MK, e-PPID, Jatim, Surabaya, Bali, Kemendikdasmen, EITI, IndoLII, sertifikasi.halal.go.id |
| ❌ **Down** (DNS ok, server dead) | **5** | Putusan MA, BIG Geospatial, Pajak/DJP, Bandung, SIMBG |

**13 out of 51 portals have dead DNS.** That's 25% of Indonesian government data infrastructure with completely broken domain records.

---

## Related Projects

| Project | Description |
|---------|-------------|
| [**indonesia-civic-stack**](https://github.com/suryast/indonesia-civic-stack) | Production-ready Python SDK + MCP server wrapping 11 government portals |
| [**indonesia-civic-signal-monitor**](https://github.com/suryast/indonesia-civic-signal-monitor) | Anomaly detection engine — monitors civic data for newsworthy changes |

This repo is the **reference documentation** layer. The civic-stack SDK is the **code** layer. The signal monitor is the **intelligence** layer.

## Contributing

Know an Indonesian government API not listed here? Found a gotcha? PRs welcome!

## Disclaimer

This project documents publicly available government data sources for educational and research purposes. It is not affiliated with any Indonesian government agency. Always respect rate limits and terms of service.

## License

MIT
