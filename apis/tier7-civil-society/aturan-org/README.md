# Aturan.org — Indonesian Legal Retrieval REST API & MCP

> **Non-government third-party publisher**, not an official Indonesian government service.
> Preserves the contribution merged in PR #9 on October 10, 2026 (`21cfe4b`).

**Publisher:** [Aturan.org](https://aturan.org)  
**REST documentation:** https://aturan.org/api  
**MCP documentation:** https://aturan.org/mcp  
**Review state:** primary documentation reviewed, October 10, 2026  
**Monitoring:** unmonitored (`monitor_ids: []`)

## Scope and provenance

Publisher documentation describes Indonesian regulation/title discovery, semantic
retrieval at regulation and pasal level, and reading discovered provisions.
Treat search results as candidates, not an authoritative legal conclusion.
Verify the original PDF and issuing institution, current validity and amendments.
The official [Database Peraturan JDIH BPK](https://peraturan.bpk.go.id) is distinct
from this third-party service. Direct GET returned 403 here; portal content
was not retrieved in this final check. Aturan.org's whole ingestion/provenance
chain, licensing, completeness, OCR accuracy and daily freshness were not verified.
No numeric corpus count is asserted.[10][30]

## REST interface (publisher-documented, not executed)

Base URL: `https://aturan.org/api/v1`. The publisher requires a Bearer API key
managed through its dashboard. Store authorized credentials in a secret manager
or environment variable; never commit, print or place them in a query URL.

| Documented method/path | Purpose |
|---|---|
| `POST /query/judul-peraturan` | Discover by regulation title/identity |
| `POST /query/peraturan-terkait` | Discover regulations through semantic retrieval |
| `POST /query/pasal-terkait` | Discover relevant provisions |
| `GET /query/isi-pasal` | Read a provision after discovery |

Follow the documented discovery → resolve → read workflow. Obtain `regulation_id`
and PDF links from discovery results; do not guess or enumerate IDs or fabricate
PDF paths. Refer to current publisher docs for parameters, schemas and limits.
No authenticated REST request or sample success response was produced.[11]

## MCP interface (publisher-documented, not connected)

The publisher documents **Streamable HTTP** at `https://mcp.aturan.org/mcp`, with
OAuth or API-key authentication. Documented tools include `cari_peraturan_terkait`,
`cari_pasal_terkait`, `cari_judul_peraturan`, `baca_isi_pasal` and
`baca_isi_pasal_batch`. Their descriptions are documentation evidence, not a
runtime tool listing. Use a supported client's current documentation; discover
actual authorized schemas and review permissions before invocation. Do not infer
REST routes from tool names or automatically approve every tool.[12]

## Exact observation and limits

Bounded unauthenticated GETs with verified TLS, a 12-second timeout and a 1.5 MB
body cap returned HTTP 200 HTML for the home, `/api` and `/mcp` documentation pages.
GET of the MCP transport returned **HTTP 401** on October 10, 2026. This is an
authentication-boundary observation, not proof of protocol interoperability or
successful search. No installation, MCP initialization, OAuth flow, login,
credential request or authenticated tool execution was performed.
Review privacy and terms before sending queries; do not send private records.
No geographic availability badge or March historical measurement is fabricated.

Numbered evidence is in the [dated source review](../../../docs/source-review-2026-10-10.md).
See also the [MCP guide](../../../mcp-servers/README.md).
