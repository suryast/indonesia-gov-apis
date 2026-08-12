# MCP Servers for Indonesian Data

[Model Context Protocol (MCP)](https://modelcontextprotocol.io) servers provide structured tool access for AI assistants like Claude, making it easy to query data sources via natural language.

## Available MCP Servers

### 🔍 You.com Search — Web Search for Indonesian Government Research

Provides web search capabilities using You.com API to enhance Indonesian government data research with contextual information, policy background, and news coverage.

**Repository:** `mcp-servers/youcom-search/`
**Tools:** `youcom_search`, `youcom_news_search`

#### Setup (Claude Desktop)

```json
{
  "mcpServers": {
    "youcom-search": {
      "command": "node", 
      "args": ["/path/to/youcom-search-mcp-server/dist/index.js"],
      "env": {
        "YDC_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

#### Available Tools

| Tool | Description |
|------|-------------|
| `youcom_search` | Web search with optional domain filtering (e.g., gov.id domains) |
| `youcom_news_search` | Indonesian government and policy news search |

#### Example Queries
- "Indonesian digital transformation policy 2026"
- "BPOM halal certification requirements" 
- "Bank Indonesia interest rate policy context"

See [youcom-search/README.md](youcom-search/README.md) for full setup and usage instructions.

### 🇮🇩 pasal.id — Indonesian Law & Regulation (third-party)

The first open, AI-native Indonesian legal platform. 40,143 regulations and 937,155 pasal (articles) structured by article and clause.

**GitHub:** [ilhamfp/pasal](https://github.com/ilhamfp/pasal)
**URL:** `https://pasal-mcp-server-production.up.railway.app/mcp`

#### Setup (Claude Desktop)

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

#### Setup (Claude CLI)

```bash
claude mcp add --transport http pasal-id https://pasal-mcp-server-production.up.railway.app/mcp
```

#### Available Tools

| Tool | Description |
|------|-------------|
| `search_laws` | Full-text search across 40K+ regulations |
| `get_pasal` | Get specific article/clause by reference |
| `get_law_status` | Check if a regulation is still active/amended/revoked |
| `get_law_content` | Get full text of a regulation |

#### Example Queries
- "What does UU Perlindungan Data Pribadi say about consent?"
- "Is PP 71/2019 still active?"
- "Find regulations about halal certification"

## Reference: Similar Projects

| Project | Country | Data Sources | GitHub |
|---------|---------|--------------|--------|
| [us-gov-open-data-mcp](https://github.com/lzinga/us-gov-open-data-mcp) | 🇺🇸 USA | 39 APIs, 219 tools (Treasury, FRED, Congress, FDA, CDC) | lzinga/us-gov-open-data-mcp |
| [agrobr-mcp](https://github.com/bruno-portfolio/agrobr-mcp) | 🇧🇷 Brazil | Agricultural data (CEPEA, CONAB, IBGE, INPE, B3) | bruno-portfolio/agrobr-mcp |

## MCP Server Opportunities

These Indonesian data sources from this repo are good candidates for MCP server implementation:

| Source | Why | Difficulty |
|--------|-----|-----------|
| **BPS Statistics** | REST API already exists, just needs MCP wrapper | Easy |
| **BMKG Weather/Earthquake** | Real-time JSON feeds, no auth | Easy |
| **BPJPH Halal** | JSON API, high public interest | Easy |
| **BPOM Product Safety** | High public interest, needs CSRF handling | Medium |
| **OJK Alert List** | High value for fraud prevention | Medium |
| **InaRisk Disaster** | REST API with coordinate-based queries | Easy |
| **data.go.id (CKAN)** | Standard CKAN API, broad dataset coverage | Easy |

Building MCP servers for these would make Indonesian government data accessible through any MCP-compatible AI assistant.

**Note:** The You.com Search MCP server has been added to provide web search context for government data research.
