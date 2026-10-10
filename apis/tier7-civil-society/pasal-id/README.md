# pasal.id — Indonesian Law & Regulation MCP Server

**Agency:** Open source (community-maintained, third-party)
**Portal:** https://pasal.id
**Kind:** non-government; **catalog ID:** `pasal-id`; **tier:** tier7
**Review date:** 2026-10-10; **review state:** unverified

## Reviewed guidance

Community legal index, not a government service. Counts, sync frequency, tool list and the guessed HTTP `/tools/*` routes are unverified historical claims. An MCP transport endpoint does not imply REST endpoints with tool names. Check the actual tool schema and original official legal document; no MCP session was executed.

**Access/auth:** Current auth/API contract unverified; use only explicitly permitted public material.

Separate official publications from community indexes. Map layers, complaint systems and legal search tools have different permissions; do not assume a public API from an accessible landing page.

No current working-API claim is made unless explicitly scoped above. A successful portal response is not a successful data query. Stop at access controls; do not use proxies, anti-detection or CAPTCHA solving to evade them. Never publish credentials or personal identifiers.


### Broken-link remediation — October 10, 2026

Use the [publisher navigation](https://pasal.id) (HTTP 200 landing/index observed October 10, 2026). Specific historical search/download routes below are unavailable; no data API or replacement search contract is verified. This is third-party project navigation, not an official legal publisher; verify original laws at peraturan.go.id. A root 404 does not diagnose the separate /mcp transport.

- Historical failed route: `https://pasal-mcp-server-production.up.railway.app` — HTTP 404 in the dated repository link audit; unavailable, not a working recipe.

## Evidence

See the [dated source review](../../../docs/source-review-2026-10-10.md) for numbered primary references and limitations. The [catalog](../../../catalog/sources.json) records this entry's exact evidence and monitor mapping.

<details>
<summary>Historical repository notes — unverified and superseded</summary>

The following pre-review notes are retained for endpoint discovery and parsing context only. Counts, timing, names, response shapes, API claims, auth assumptions and examples below were NOT revalidated. They must not override the reviewed guidance above; verify before use.

> ⚠️ **Third-party project** — pasal.id is a community-maintained open-source project, NOT an official Indonesian government portal. It indexes data from the official peraturan.go.id.

**Provider:** Open source (community-maintained, third-party)
**Historical MCP transport (not validated):** https://pasal-mcp-server-production.up.railway.app/mcp — audit GET returned HTTP 406, not the root route's 404; no MCP session was executed.
**Source data:** peraturan.go.id (official government regulation portal)
**API type:** 🔵 MCP (Model Context Protocol) + HTTP-callable tools

## Overview

pasal.id provides structured access to 40,143+ Indonesian regulations and 937,155+ individual pasal (articles/clauses). Sourced from peraturan.go.id and processed with OCR correction for scanned PDFs. Updated weekly.

## MCP Setup (Claude Desktop / Claude Code)

Setup command withdrawn as an unverified integration recipe. The separate `/mcp` transport requires protocol/schema validation; root HTTP 404 does not establish transport failure. Use project navigation to obtain current instructions.

## MCP Tools

| Tool | Description |
|------|-------------|
| `search_laws` | Full-text search across all regulations |
| `get_pasal` | Retrieve a specific article/clause by ID |
| `get_law_status` | Check if a regulation is active, amended, or revoked |

## REST Usage

Recipe withdrawn: its historical route returned HTTP 404 on October 10, 2026. Use the reviewed publisher navigation above; no endpoint resurrection is claimed.

## Data Coverage

| Type | Description |
|------|-------------|
| UU | Undang-Undang (Parliament Acts) |
| PP | Peraturan Pemerintah (Government Regulations) |
| Perpres | Peraturan Presiden (Presidential Regulations) |
| Permen | Peraturan Menteri (Ministerial Regulations) |
| Perda | Peraturan Daerah (Regional Regulations) |

## Gotchas

1. **Railway-hosted** — may have cold starts (5-10s); add retry logic with backoff
2. **Weekly sync** — very recent regulations may lag 1-7 days
3. **OCR quality varies** — scanned PDFs corrected but not perfect for old docs
> Historical access/limit assertion withdrawn; verify publisher guidance.
5. **For high-volume production** — consider self-hosting the open-source server
6. **Pasal IDs** — use law number + article number for stable cross-references

</details>
