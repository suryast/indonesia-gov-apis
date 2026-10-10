# MCP references for Indonesian data

**Reviewed October 10, 2026.** No MCP initialization, tool execution, OAuth flow or
API-key request was performed. Public documentation is not proof of a working
protocol integration or accurate legal coverage.

## Existing catalog: pasal.id

[pasal.id documentation](../apis/tier7-civil-society/pasal-id/README.md) identifies a
third-party legal-index project. The historical Railway endpoint, coverage counts,
weekly-sync schedule, tool list and guessed `/tools/*` routes remain unverified.
The former npm proxy configuration has been removed rather than asserted to work.
Discover tools through the actual MCP protocol and supported client documentation;
verify legal text against the original official publisher.

## Preserved catalog contribution: Aturan.org / PR #9

[Aturan.org source documentation](../apis/tier7-civil-society/aturan-org/README.md)
preserves PR #9, merged October 10, 2026 at `21cfe4b`. The publisher's
[REST documentation](https://aturan.org/api) specifies API-key Bearer authentication;
[MCP documentation](https://aturan.org/mcp) specifies Streamable HTTP at
`https://mcp.aturan.org/mcp` with OAuth or API-key options.[10][11][12][18]

Public documentation GETs returned HTTP 200 HTML; an unauthenticated GET to the
MCP transport returned HTTP 401 on October 10, 2026. Neither is an MCP
initialization or successful tool invocation. Nothing was installed or connected.
Use current publisher/client documentation and discover authorized tool schemas;
do not infer REST paths from MCP tool names or automatically approve all tools.
Review privacy, terms and original legal documents before sending queries.
Corpus counts, daily freshness and March AU/ID availability badges are not adopted.
No credential was requested or used.

## Wrapping official sources

- [BMKG](../apis/tier1-open-apis/bmkg/README.md): use the documented JSON interfaces,
  enforce publisher limits and display attribution. Offline wrapper tests do not
  establish current endpoint access.
- [BPS](../apis/tier1-open-apis/bps/README.md): approved key token, current metadata
  discovery and guarded response handling; do not embed a key in tool output.
- [SATUSEHAT](../apis/tier8-new/satusehat/README.md): not an open-data wrapper;
  organization authorization and sensitive-health-data controls are prerequisites.
- [Portal discovery](../references/ckan-portals.md): first establish the actual
  interface. Do not build CKAN tools around an HTML landing page.
- [BPJPH](../apis/tier2-scrapeable/bpjph/README.md): do not wrap a supervisor search
  as a halal-certification check or expose personal supervisor records.

Remote services can receive queries and data. Review their authority, privacy,
terms and tool permissions before connection; do not send private records or
credentials in prompts. Stop at explicit access restrictions rather than using
stealth, proxies or CAPTCHA solving.

Numbered references and retrieval limitations are in the
[dated source review](../docs/source-review-2026-10-10.md). The
[catalog](../catalog/sources.json) lists only adopted documentation records.
