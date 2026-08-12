# You.com Search MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that provides web search capabilities using the You.com API, specifically designed to enhance Indonesian government data research.

## Features

- **Web Search**: General web search with optional domain filtering
- **News Search**: Targeted news search for Indonesian government and policy updates
- **Government Focus**: Pre-configured for Indonesian government domains and news sources
- **Flexible Authentication**: Works with or without You.com API key
- **Error Handling**: Robust error handling with informative messages

## Installation

```bash
npm install
npm run build
```

## Configuration

### Environment Variables

- `YDC_API_KEY` (optional): You.com API authentication key
  - If provided, uses authenticated API with higher rate limits
  - If not provided, falls back to keyless API (limited requests)
- `YOUCOM_BASE_URL` (optional): Base URL for You.com API (default: `https://api.you.com`)

### Claude Desktop Setup

Add to your Claude Desktop MCP configuration:

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

### Claude CLI Setup

```bash
claude mcp add youcom-search /path/to/youcom-search-mcp-server/dist/index.js
```

## Available Tools

### `youcom_search`

Search the web using You.com API for Indonesian government policy research, news, and contextual information.

**Parameters:**
- `query` (required): Search query for Indonesian government data, policy, or related information
- `domains` (optional): Array of domains to search within (e.g., `["gov.id", "kemenkeu.go.id"]`)
- `count` (optional): Number of results to return (default: 10, max: 20)

**Example:**
```
Search for "Indonesian digital transformation policy" within government domains
```

### `youcom_news_search`

Search for recent news about Indonesian government, policies, or agencies.

**Parameters:**
- `query` (required): News search query related to Indonesian government or policies
- `days` (optional): Number of days to search back (default: 30)
- `count` (optional): Number of results to return (default: 10, max: 20)

**Example:**
```
Find recent news about "BPOM food safety regulations"
```

## Use Cases

### Government Data Context
When working with Indonesian government APIs, use You.com search to:
- Find policy context for statistical data from BPS
- Research background on regulatory changes from BPOM or OJK
- Get news coverage about ministry announcements
- Find additional context for disaster data from BMKG or BNPB

### Example Queries

1. **Policy Research**: "UU Perlindungan Data Pribadi implementation 2026"
2. **Regulatory Updates**: "BPOM halal certification new requirements"
3. **Economic Context**: "Bank Indonesia interest rate policy 2026"
4. **Disaster Context**: "BMKG earthquake early warning system upgrades"

### Domain-Specific Search

Target specific government domains:
```json
{
  "query": "budget transparency initiative",
  "domains": ["kemenkeu.go.id", "djpb.kemenkeu.go.id"]
}
```

Common Indonesian government domains:
- `gov.id` - General government
- `kemenkeu.go.id` - Ministry of Finance
- `bps.go.id` - Central Statistics Agency  
- `ojk.go.id` - Financial Services Authority
- `bpom.go.id` - Food and Drug Authority
- `bmkg.go.id` - Meteorology Agency

## Error Handling

The server provides informative error messages for common issues:
- **401 Unauthorized**: Invalid or missing API key
- **429 Rate Limited**: Too many requests, retry later
- **Network errors**: Connection or timeout issues
- **Invalid parameters**: Missing required fields or invalid values

## Development

```bash
# Development mode with auto-reload
npm run dev

# Build for production
npm run build

# Run built server
npm start
```

## Integration with Indonesian Government APIs

This MCP server complements the Indonesian government data sources in this repository by providing contextual web search. Use it alongside government APIs to:

1. **Enhance BPS Statistics**: Search for economic analysis and policy context
2. **Contextualize BPOM Data**: Find news about food safety incidents or regulatory changes  
3. **Research OJK Regulations**: Get background on financial policy changes
4. **Understand BMKG Alerts**: Find news coverage and impact analysis of weather events

## License

MIT