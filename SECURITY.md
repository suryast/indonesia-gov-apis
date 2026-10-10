# Security policy

## Supported code

Security fixes target the default branch. Python examples and development gates
support Python 3.11–3.14; the static status dashboard has no application framework.
Dependencies/actions are pinned and reviewed through Dependabot and CI audits.
Catalog entries can change outside this repository; published links or a successful
HTTP probe are not a security, certification, licensing or endorsement guarantee.

## Reporting

Do not disclose secrets, personal information or exploitation details in a public
issue. Use GitHub's private vulnerability reporting feature for this repository
if enabled. If unavailable, ask maintainers in a public issue for a private
reporting channel **without** including sensitive details. There is no guaranteed
response-time commitment or invented security contact address.

Provide the affected revision/path, minimal reproduction and impact, with all
credentials/PII redacted. Do not probe third-party services beyond their terms or
try to bypass authentication, CAPTCHAs, rate limits or access controls.

## Operational safeguards

- Keep API keys in environment variables or an approved secret manager; never
  commit them or expose request URLs containing BPS's path-based key.
- Do not disable TLS verification. Use bounded timeouts and check HTTP status.
- Treat upstream data/HTML as untrusted. Fail closed on unknown layouts; do not
  infer that missing financial warnings mean safety or halal supervisors mean
  product certification.
- Do not commit or serve private keys, response PII, provider errors or raw
  authenticated payloads in public monitoring output.
- CI on pull requests has read-only permissions and no deployment secrets. Avoid
  `pull_request_target`, interpolated untrusted shell input and persisted git credentials.
- Schedule/deployment runs are main-only. Grant Cloudflare tokens only the Pages
  permissions needed for the intended account/project; review platform scope limits.
- Deploy the static stager's allowlist, not the status source directory. No scripts,
  symlinks, arbitrary configs or credential files belong in the public site.
- A clean dependency audit is advisory coverage at a point in time, not proof of
  safety. Update lockfiles/actions and run offline gates before publishing.
