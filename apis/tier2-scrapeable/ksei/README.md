# KSEI — Securities Ownership & Investor Statistics

**Agency:** Kustodian Sentral Efek Indonesia (Indonesian Central Securities Depository)
**Portal:** https://www.ksei.co.id
**Kind:** non-government; **catalog ID:** `ksei`; **tier:** tier2
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

A public webpage does not authorize bulk extraction. Use permitted public searches only; stop at login, CAPTCHA or access-denial screens. CSRF/session handling is not permission to bypass controls.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

A public webpage does not authorize bulk extraction. Use permitted public searches only; stop at login, CAPTCHA or access-denial screens. CSRF/session handling is not permission to bypass controls.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.


### Broken-link remediation — October 10, 2026

Use the [publisher navigation](https://web.ksei.co.id/publications/Data_Statistik_KSEI) (HTTP 200 landing/index observed October 10, 2026). Specific historical search/download routes below are unavailable; no data API or replacement search contract is verified. The statistics index exposes monthly PDF links; other retained KSEI timeout observations are not resolved by this check.

- Historical failed route: `https://www.ksei.co.id/publikasi/statistik` — HTTP 404 in the dated repository link audit; unavailable, not a working recipe.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

**Agency:** Kustodian Sentral Efek Indonesia (Indonesian Central Securities Depository)
**Portal:** https://www.ksei.co.id
**Statistics:** `https://www.ksei.co.id/publikasi/statistik` (historical unavailable route; HTTP 404 observed 2026-10-10)
**API type:** ⚠️ HTML + PDF/XLSX monthly downloads (no individual position data)

## Overview

KSEI is Indonesia's central securities depository. Public data includes aggregate investor statistics by province, sub-registry type, and product (shares, bonds, mutual funds). Individual position data is private — only aggregates are published.

## Scrape Monthly Statistics

Recipe withdrawn: its historical route returned HTTP 404 on October 10, 2026. Use the reviewed publisher navigation above; no endpoint resurrection is claimed.

## Download and Parse Stats File

```python
# Direct download of investor count by province
stats_url = "https://www.ksei.co.id/files/statistik/investor-statistics-2025-01.xlsx"
resp = session.get(stats_url, timeout=30)
df = pd.read_excel(BytesIO(resp.content), sheet_name=0)
print(df.head(10))
```

## Available Aggregates

| Dataset | Description |
|---------|-------------|
| Investor count by province | Number of SID holders per province |
| Investor count by sub-registry | Per broker/bank breakdown |
| AKSes statistics | Account access and activity |
| SBN holders | Government bond investor count |
| Reksadana | Mutual fund investor statistics |

## SID (Single Investor Identification)

Each investor in Indonesia has a unique SID. KSEI publishes total SID counts:

```python
# Parse SID growth over time from annual reports
resp = session.get("https://www.ksei.co.id/publikasi/laporan-tahunan", timeout=30)
soup = BeautifulSoup(resp.text, "html.parser")
annual_reports = [(a.text.strip(), a["href"]) for a in soup.select("a[href*='annual']")]
```

## Gotchas

1. **Aggregate only** — individual investor positions are never published
2. **Monthly lag** — statistics published ~2-3 weeks after month end
3. **Excel format changes** — column layouts shift periodically
4. **Sub-registry = broker** — "sub-registry" is the term for broker in KSEI context
5. **AKSes** — KSEI's investor self-service portal (separate from public stats)
6. **See also** — `tier6-financial/ksei-investor` for investor registry stats breakdown

</details>
