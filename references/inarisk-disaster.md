# InaRisk — Disaster Risk by Location

**Reviewed:** 2026-10-10. Supplementary guide, not an additional source or live API test.

## SIGAP / InaRisk — Disaster Risk Assessment

No official contract for the historical `/api/risk/score` route or its illustrative response was established. Do not convert a map-layer legend into a property-level safety score. Verify layer date, scale, methodology and permissions; disaster-risk information is not a real-time emergency warning.

Access/auth: Current auth/API contract unverified; use only explicitly permitted public material.

[Canonical source documentation](../apis/tier7-civil-society/sigap-inarisk/README.md).

## BNPB — Disaster Data & Risk Portal

One bounded GET of the historical CKAN search route on 2026-10-10 observed HTTP 200, ckan_shape_observed. A JSON CKAN success/result/results shape was observed for dataset search only; datastore access and the separate risk-score routes are unverified.[26]

Access/auth: Current auth/API contract unverified; use only explicitly permitted public material.

[Canonical source documentation](../apis/tier1-open-apis/bnpb-disaster/README.md).

Stop at login, CAPTCHA, 403 or other access-denial controls. Do not bypass restrictions or publish credentials/PII. For evidence and outstanding validation, see the [source review](../docs/source-review-2026-10-10.md).
