# SATUSEHAT — Authorized Health Interoperability

**Agency:** Kementerian Kesehatan
**Portal:** https://satusehat.kemkes.go.id
**Kind:** government; **catalog ID:** `satusehat`; **tier:** tier8
**Review date:** 2026-10-10; **review state:** primary_documentation_reviewed

## Reviewed guidance

Official authentication documentation requires approved access and organization-scoped credentials. This is not an open patient-record API. Keep credentials private and use only authorized sandbox data; no token exchange or patient-data request was performed.[8]

**Access/auth:** OAuth2 client_credentials for approved partners; no credentials used.

These entries fill missing documentation for the additions listed in March 2026. Documentation review does not establish working integration.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.
