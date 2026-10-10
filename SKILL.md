---
name: querying-indonesian-gov-data
description: >
  Find and assess Indonesian public-data sources using a dated, evidence-backed
  catalog. Route statistics, weather, certification, finance, legal, geospatial
  and ministry queries to reviewed documentation. Respect authorization,
  privacy and publisher limits; do not treat historical examples as working APIs.
---

# Querying Indonesian public data

Read [catalog/sources.json](catalog/sources.json) first. Counts describe documentation
records, including overlapping services and non-government publishers, not verified
open APIs. Supplementary references are guides, not extra sources. The
[October 10, 2026 review](docs/source-review-2026-10-10.md) records primary evidence
and gaps. Empty `monitor_ids` means unmonitored; monitored HTTP success is not API success.
The separate [monitor-only registry](catalog/monitor-only.json) documents the 18 additional PR #10 probes; the validated monitoring inventory is 75 endpoints, independent of the source-document count.

**59 source records: 58 Indonesia-related and 1 Japan NTA reference; 11 supplementary guides.** Tier 7 has seven records. Aturan.org is a non-government, unmonitored documentation record, not a verified integration.

## Router

| Intent | Read | Boundaries |
|---|---|---|
| Halal certification | [BPJPH](references/bpjph-halal.md) | Supervisor records are not business/product certificates; no bulk personal-data queries. |
| Food/drug/cosmetic registration | [BPOM](references/bpom-products.md) | Product registration is not halal certification. Historical web internals are not a supported contract. |
| Financial authorization or alerts | [OJK](references/ojk-legality.md) | No negative-list match is not proof of a license. SIKePO contains banking regulations. |
| Weather/earthquakes | [BMKG](references/bmkg-weather.md) | Prefer official JSON documentation; respect limits and attribution. |
| Statistics | [BPS](references/bps-statistics.md) | API key required; discover metadata rather than hardcoding indicator meanings. |
| Exchange rates/monetary data | [Bank Indonesia](references/bank-indonesia.md) | Statistics publications are different from payment APIs. |
| Legal text | [Community legal index](references/pasal-id-law.md), [Aturan.org REST/MCP](apis/tier7-civil-society/aturan-org/README.md) | Third-party results are leads; verify the official source and discover actual MCP tool schemas. |
| National/regional datasets | [Portal discovery](references/ckan-portals.md) | Do not assume CKAN or datastore availability from the portal name. |
| Disaster risk | [InaRisk](references/inarisk-disaster.md) | Historical coordinate-score routes are unverified; risk maps are not emergency warnings. |
| Company information | [Company references](references/company-verification.md) | Registration, licensing, ownership and allegations are different evidence classes. |
| Stock data | [IDX](references/idx-stocks.md) | Third-party price feeds are not official exchange APIs. |
| Officials' wealth declarations | [KPK e-LHKPN](apis/tier2-scrapeable/kpk-lhkpn/README.md) | Use the official manual public-announcement flow; filing login is a separate workflow. |
| Health interoperability | [SATUSEHAT](apis/tier8-new/satusehat/README.md) | Approved partner credentials, organization-scoped access; no open patient API. |
| Tax administration | [Coretax](apis/tier8-new/coretax/README.md) | Authorized taxpayer workflow; no anonymous taxpayer enumeration. |

## Execution workflow

1. Read canonical source documentation and its `review`/`access` catalog fields.
2. Separate `unverified`, `primary_documentation_reviewed` and `endpoint_observed`.
   None means that every interface works, or that authenticated access was tested.
3. Prefer publisher documentation and licensed aggregate downloads. Obtain approved
   credentials through official channels and keep them out of URLs/logs/output where possible.
4. When permitted, use a bounded request with a timeout, HTTP-error handling,
   content-type checks and guarded parsing. Do not assume schemas from historical code.
5. Stop at login, CAPTCHA, access denial or other explicit restrictions. Do not use
   proxies, stealth fingerprints, CAPTCHA solvers or repeated requests to evade them.
6. Record exact date, endpoint, method and limitations without credentials or PII.
   A 200 landing page is not a successful data query; missing regional observations
   are unknown, not proof of geo-blocking.
7. Verify certification/licensing with the appropriate original publisher. Missing
   or stale results do not establish legality, compliance or safety.

## Failure handling

- **403/CAPTCHA/login:** stop and use the authorized/manual path. Do not guess a geography-based explanation.
- **Timeout/DNS:** record the vantage-point failure; do not conclude global outage or project closure.
- **429:** honor `Retry-After` and publisher guidance; no repository-wide numeric quota is valid.
- **HTML where JSON expected:** report an incompatible response, not an empty dataset.
- **CSRF/session change:** recheck permitted UI behavior; session handling is not access authorization.

[Offline catalog validation](scripts/validate_catalog.py) checks documentation
consistency only. [MCP references](mcp-servers/README.md) are separate from an
executed integration. Do not install the old guessed proxy package or infer
`/tools/<name>` HTTP routes from MCP tool names.
