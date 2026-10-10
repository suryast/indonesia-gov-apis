# Company Verification (AHU / OpenCorporates / OCCRP)

**Reviewed:** 2026-10-10. Supplementary guide, not an additional source or live API test.

## AHU Online — Company Registry

A public webpage does not authorize bulk extraction. Use permitted public searches only; stop at login, CAPTCHA or access-denial screens. CSRF/session handling is not permission to bypass controls.

Access/auth: Current auth/API contract unverified; use only explicitly permitted public material.

[Canonical source documentation](../apis/tier2-scrapeable/ahu-company/README.md).

## AHU-BO — Beneficial Ownership Registry

Record the original publisher and publication date. Third-party company or leak indexes are research leads, not findings of wrongdoing or current proof of registration.

Access/auth: Current auth/API contract unverified; use only explicitly permitted public material.

[Canonical source documentation](../apis/tier5-transparency/ahu-bo/README.md).

## OpenCorporates — Global Company Registry

Record the original publisher and publication date. Third-party company or leak indexes are research leads, not findings of wrongdoing or current proof of registration.

Access/auth: API credentials, collection permissions and current service terms must be checked; not authenticated here.

[Canonical source documentation](../apis/tier5-transparency/opencorporates/README.md).

## OCCRP Aleph — Global Beneficial Ownership & Leaks

Record the original publisher and publication date. Third-party company or leak indexes are research leads, not findings of wrongdoing or current proof of registration.

Access/auth: API credentials, collection permissions and current service terms must be checked; not authenticated here.

[Canonical source documentation](../apis/tier5-transparency/occrp-aleph/README.md).

Registration, sector licensing, beneficial ownership and allegations are different questions. Match official company identifiers and publication dates only when collection and use are permitted. Do not infer wrongdoing from a third-party match or legitimacy from alert absence. Do not automate CAPTCHA solving or join personal tax IDs.

Stop at login, CAPTCHA, 403 or other access-denial controls. Do not bypass restrictions or publish credentials/PII. For evidence and outstanding validation, see the [source review](../docs/source-review-2026-10-10.md).
