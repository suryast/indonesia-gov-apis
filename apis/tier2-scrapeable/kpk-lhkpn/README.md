# KPK e-LHKPN — Public announcements and authorized filing

**Agency:** Komisi Pemberantasan Korupsi (KPK)
**Portal:** https://elhkpn.kpk.go.id
**Kind:** government; **catalog ID:** `kpk-lhkpn`; **tier:** tier2
**Review date:** 2026-10-10; **review state:** primary_documentation_reviewed

## Issue #1: documentation defect, not a repaired public API

[Issue #1](https://github.com/suryast/indonesia-gov-apis/issues/1), opened March 11,
2026, reports HTTP 404 when running the old search example. The old documentation
asserted a direct search route, guessed result-table/detail selectors and a made-up
detail ID without an official API contract. Those scripts and placeholders have
been removed, not replaced with another guessed endpoint.[17]

The reported 404 is historical issue evidence. Direct official portal requests
from the review host returned `URLError`, so this review did **not** reproduce a
current 404 or establish the exact server-side cause. It cannot determine whether
the old route was removed, never supported, or dependent on a session. The confirmed
repository defect was presenting an unverified route and DOM schema as usable code.

## Official public search flow (manual, CAPTCHA-gated)

Start at the [official e-LHKPN portal](https://elhkpn.kpk.go.id/portal/user/login)
and select **e-Announcement**. The official portal's search-indexed FAQ describes:

1. Search by the official's name or NIK, reporting year and institution.
2. Complete the displayed **CAPTCHA** manually and use **Cari**.
3. For an available announcement, use **Preview Cetak Pengumuman**.
4. Complete the **Siapakah Anda** downloader form and use **Download** to obtain
   the published PDF.[7]

This description is supported by indexed official guidance, **not a completed
browser search or download in this review**. Prefer name/year/institution to
personal identifier queries. Do not submit invented identity details. Verify the
current interface, purpose restrictions and privacy requirements with KPK before
access. No search for a person, form submission, CAPTCHA completion or declaration
download was performed.

### Public announcement is not filing-account login

KPK's indexed guidance separately describes account activation and login for
**e-Filing**, the authorized official's submission workflow. Do not infer that all
public announcements require an e-Filing account merely because both workflows
appear on a URL containing `login`. Conversely, public visibility is not a license
to bulk-download or republish personal records.[7]

**Access/auth:** public e-Announcement has a manual CAPTCHA/downloader-form flow;
e-Filing requires an activated, authorized account. No public JSON API contract
was verified. A landing page returning **HTTP 200 is not API success**, a completed
search, an authorized download or an absence of declarations.

## Suggested community replacement: reviewed, not endorsed

The issue comment links [nichsedge/lhkpn](https://github.com/nichsedge/lhkpn).
Its README and source were inspected read-only; nothing was installed or executed.
The project advertises Playwright-based extraction and stealth/anti-detection, and
uses a fragment-based announcement URL. Those are **untrusted third-party claims**,
not current official API documentation. The fragment was not independently
confirmed from live official HTML, so it is not adopted as a verified replacement.
No selectors or personal-record examples were copied.[27][28]

Do not bypass CAPTCHA, use stealth/proxies to evade restrictions, harvest personal
identifiers, or treat third-party scraped data as an official KPK response.
For programmatic access, obtain KPK's approved access terms and documented interface
before implementing a client. **Current API access remains unverified.**

## Evidence and regression protection

[Source review](../../../docs/source-review-2026-10-10.md) records retrieval limits
and numbered primary references. [Catalog](../../../catalog/sources.json) contains
this source's evidence and monitor mapping. Direct official HTML and the candidate
PDF manuals could not be retrieved from this host; CAPTCHA type, DOM selectors
and session/API internals remain unverified.

[Offline documentation tests](../../../tests/test_lhkpn_docs.py) reject the removed
routes, fake selectors/detail ID and unsupported public-API success claims. They
protect documentation integrity, not live portal behavior.
