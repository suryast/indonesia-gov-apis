# pasal.id — Indonesian Law MCP Server

## MCP Setup

### Claude Desktop
```json
{
  "mcpServers": {
    "pasal-id": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-proxy", "https://pasal-mcp-server-production.up.railway.app/mcp"]
    }
  }
}
```

### Claude CLI
```bash
claude mcp add --transport http pasal-id https://pasal-mcp-server-production.up.railway.app/mcp
```

## Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| `search_laws` | Full-text search across 40K regulations | "cari UU tentang perlindungan data" |
| `get_pasal` | Get specific article by reference | "Pasal 5 UU 27/2022" |
| `get_law_status` | Check if regulation is active/amended/revoked | "status PP 71/2019" |
| `get_law_content` | Get full regulation text | "isi lengkap UU 11/2020" |

## Coverage
- 40,143 regulations
- 937,155 structured articles (pasal)
- Covers: UU, PP, Perpres, Permen, Perda
- Source: peraturan.go.id PDFs with Claude Vision OCR correction
- Weekly sync

## Example Queries
- "What does UU Perlindungan Data Pribadi say about consent?"
- "Is PP 71/2019 still active?"
- "Find regulations about halal certification"
- "Pasal berapa yang mengatur tentang NPWP?"

## GitHub
[ilhamfp/pasal](https://github.com/ilhamfp/pasal) — open source, FastMCP + Supabase + Next.js
