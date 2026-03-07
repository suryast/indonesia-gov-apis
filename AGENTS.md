# AGENTS.md

This is a **documentation-only** repo — no build system, no tests, no deployable code.

## Purpose
Reference for 50 Indonesian government data sources, APIs, and MCP servers. Used by developers and AI agents building applications against Indonesian government data.

## Structure
- `apis/tier1-open-apis/` through `apis/tier7-civil-society/` — each source has a `README.md` with endpoints, Python examples, and gotchas
- `mcp-servers/` — MCP server setup guides (pasal.id for Indonesian law)
- `examples/` — Working Python scripts (no dependencies beyond `requests` and `beautifulsoup4`)
- `SKILL.md` — Quick reference table of all 50 sources with endpoints and auth requirements

## When contributing
- Each data source gets its own directory under the appropriate tier
- Include: agency name, portal URL, API type, Python example, gotchas section
- No PII, no project-specific references — this is a neutral public reference
- Test example code before committing (endpoints change frequently)

## Key files to read first
1. `README.md` — full source listing with tier tables
2. `SKILL.md` — compact reference with all endpoints
3. `mcp-servers/README.md` — MCP integration guide
