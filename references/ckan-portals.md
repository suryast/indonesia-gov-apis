# CKAN Open Data Portals

**Reviewed:** 2026-10-10. Supplementary guide, not an additional source or live API test.

## data.go.id — National Open Data Portal

One bounded GET of the historical CKAN search route on 2026-10-10 observed HTTP 404, http_error. This does not establish a working CKAN API or prove that the portal has no other API.[19]

Access/auth: Current auth/API contract unverified; use only explicitly permitted public material.

[Canonical source documentation](../apis/tier1-open-apis/data-go-id/README.md).

## Satu Data Jakarta — DKI Jakarta Open Data

One bounded GET of the historical CKAN search route on 2026-10-10 observed HTTP 200, not_json. This does not establish a working CKAN API or prove that the portal has no other API.[20]

Access/auth: Current auth/API contract unverified; use only explicitly permitted public material.

[Canonical source documentation](../apis/tier3-regional/satu-data-jakarta/README.md).

## Open Data Jabar — Jawa Barat Provincial Open Data

One bounded GET of the historical CKAN search route on 2026-10-10 observed HTTP 403, http_error. This does not establish a working CKAN API or prove that the portal has no other API.[21]

Access/auth: Current auth/API contract unverified; use only explicitly permitted public material.

[Canonical source documentation](../apis/tier3-regional/opendata-jabar/README.md).

## Open Data Jawa Timur — East Java Provincial Open Data

One bounded GET of the historical CKAN search route on 2026-10-10 observed HTTP 403, http_error. This does not establish a working CKAN API or prove that the portal has no other API.[22]

Access/auth: Current auth/API contract unverified; use only explicitly permitted public material.

[Canonical source documentation](../apis/tier3-regional/opendata-jatim/README.md).

## Satu Data Surabaya — Surabaya City Open Data

One bounded GET of the historical CKAN search route on 2026-10-10 observed HTTP 404, http_error. This does not establish a working CKAN API or prove that the portal has no other API.[23]

Access/auth: Current auth/API contract unverified; use only explicitly permitted public material.

[Canonical source documentation](../apis/tier3-regional/satu-data-surabaya/README.md).

## Open Data Kota Bandung — Bandung City Open Data

One bounded GET of the historical CKAN search route on 2026-10-10 observed HTTP 404, http_error. This does not establish a working CKAN API or prove that the portal has no other API.[24]

Access/auth: Current auth/API contract unverified; use only explicitly permitted public material.

[Canonical source documentation](../apis/tier3-regional/opendata-bandung/README.md).

## Open Data Bali — Bali Provincial Open Data

One bounded GET of the historical CKAN search route on 2026-10-10 observed transport_error. This does not establish a working CKAN API or prove that the portal has no other API.[25]

Access/auth: Current auth/API contract unverified; use only explicitly permitted public material.

[Canonical source documentation](../apis/tier3-regional/opendata-bali/README.md).

## BNPB — Disaster Data & Risk Portal

One bounded GET of the historical CKAN search route on 2026-10-10 observed HTTP 200, ckan_shape_observed. A JSON CKAN success/result/results shape was observed for dataset search only; datastore access and the separate risk-score routes are unverified.[26]

Access/auth: Current auth/API contract unverified; use only explicitly permitted public material.

[Canonical source documentation](../apis/tier1-open-apis/bnpb-disaster/README.md).

## Conditional CKAN discovery

Only use CKAN actions after checking publisher documentation or a bounded request for a JSON `success: true`, object `result` and list `results`. An HTML response with HTTP 200 is not a CKAN response. One observed action does not establish datastore support, licensing, freshness or quotas. No blanket CKAN classification is retained.

Stop at login, CAPTCHA, 403 or other access-denial controls. Do not bypass restrictions or publish credentials/PII. For evidence and outstanding validation, see the [source review](../docs/source-review-2026-10-10.md).
