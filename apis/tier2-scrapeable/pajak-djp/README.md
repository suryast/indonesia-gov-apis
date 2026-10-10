# Pajak.go.id / DJP — Tax Authority Data

**Agency:** Direktorat Jenderal Pajak (DGT — Directorate General of Taxes)
**Portal:** https://pajak.go.id
**Kind:** government; **catalog ID:** `pajak-djp`; **tier:** tier2
**Review date:** 2026-10-10; **review state:** primary_documentation_reviewed

## Reviewed guidance

Use official DJP/Coretax account workflows for tax administration. The old anonymous NPWP lookup, taxpayer-type heuristic and claims about corporate ID lengths were not verified and are withdrawn. Format plausibility is not registration or tax-compliance verification. Coretax administration is described by DJP from January 2025 onward.[15]

**Access/auth:** Account/authorization required for private records; no public lookup API verified.

A public webpage does not authorize bulk extraction. Use permitted public searches only; stop at login, CAPTCHA or access-denial screens. CSRF/session handling is not permission to bypass controls.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.
