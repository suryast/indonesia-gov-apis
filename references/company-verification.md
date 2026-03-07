# Company Verification (AHU / OpenCorporates / OCCRP)

## OpenCorporates (Structured, Rate-Limited)

```python
import requests

resp = requests.get("https://api.opencorporates.com/v0.4/companies/search", params={
    "q": "COMPANY_NAME",
    "jurisdiction_code": "id",  # Indonesia
    "api_token": "YOUR_TOKEN",  # Optional, higher limits
}, timeout=30)

for c in resp.json()["results"]["companies"]:
    co = c["company"]
    print(f"{co['name']} | {co['company_number']} | {co['current_status']}")
```

- Free: 500 req/day. Indonesian data sourced from AHU.
- Returns: name, status, officers, filings.

## OCCRP Aleph (Beneficial Ownership + Leaks)

```python
API_KEY = "your-key"  # Free at aleph.occrp.org
resp = requests.get("https://aleph.occrp.org/api/2/entities", params={
    "q": "COMPANY_NAME",
    "filter:schema": "Company",
    "filter:countries": "id",
}, headers={"Authorization": f"ApiKey {API_KEY}"}, timeout=30)
```

- 60 req/min. Contains Panama/Pandora Papers data.
- Cross-ref with AHU for comprehensive due diligence.

## AHU Direct (Kemenkumham)

```python
# ahu.go.id — has CAPTCHA, harder to automate
# Beneficial ownership: bo.ahu.go.id — basic name search
resp = requests.get("https://bo.ahu.go.id/search", params={"q": "COMPANY"},
    headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
```

- CAPTCHA on main AHU site — Selenium needed
- BO portal has basic search, limited public fields

## Verification Strategy

For thorough verification, cross-reference:
1. **OpenCorporates** — is it registered?
2. **OJK** — is it licensed (if financial)?
3. **OCCRP Aleph** — any red flags in leaks?
4. **AHU-BO** — who are the beneficial owners?
5. **Satgas Waspada** — is it on the illegal list?

## Gotchas
- No single source is authoritative alone — always cross-reference
- AHU data updates lag behind reality
- CAPTCHA protection on ahu.go.id makes bulk access difficult
