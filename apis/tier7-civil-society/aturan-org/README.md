# Aturan.org — Indonesian Law & Regulation MCP Server

> ⚠️ **Third-party project** — Aturan.org is a community-maintained open-source project, NOT an official Indonesian government portal. It indexes data from the official bpk.peraturan.go.id.

**Provider:** Open source (community-maintained, third-party)  
**MCP Server:** https://mcp.aturan.org/mcp  
**Source data:** bpk.peraturan.go.id (official government regulation portal)  
**API type:** 🔵 MCP (Model Context Protocol) + HTTP-callable tools  

## Overview

Aturan.org provides structured access to 287,883+ Indonesian regulations and 5,322,464+ individual pasal (articles/clauses). Sourced from bpk.peraturan.go.id and processed with OCR correction for scanned PDFs. Updated daily.

## MCP Setup

Add Aturan.org MCP server in your app:
```json
{
  "mcpServers": {
    "aturanorg": {
      "url": "https://mcp.aturan.org/mcp",
      "headers": {
        "Authorization": "Bearer <free_api_key_provided_on_website>"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `cari_peraturan_terkait(query, top_k=40)` | Regulation discovery using semantic retrieval at article level, provided with snippet (max TopK=200). |
| `cari_pasal_terkait(query, top_k=10)` | Semantic retrieval of a spesific topic to all articles/pasal (max TopK=20).|
| `cari_judul_peraturan(query, top_k=10, sort="relevance")` | Full-text search across all regulations, sorted by relevance,newest,oldest (max TopK=20) |
| `baca_isi_pasal(regulation_id, pasal)` | Read pasal directly from specific known regulation by ID and article number. |

## REST Usage

### Query Peraturan Terkait
```bash
curl --silent --show-error --request POST \
  'https://aturan.org/api/v1/query/peraturan-terkait' \
  --header 'Authorization: Bearer aturanorg-api-ujicoba-1234567890abcdef' \
  --header 'Content-Type: application/json' \
  --data '{
    "query": "sanksi administratif pertambangan",
    "top_k": 30
  }'
```
### Query Pasal Terkait
```bash
curl --silent --show-error --request POST \
  'https://aturan.org/api/v1/query/pasal-terkait' \
  --header 'Authorization: Bearer aturanorg-api-ujicoba-1234567890abcdef' \
  --header 'Content-Type: application/json' \
  --data '{
    "query": "syarat pendirian perseroan terbatas",
    "top_k": 10
  }'
```

## Data Coverage

| Type | Description |
|------|-------------|
| UU | Undang-Undang (Parliament Acts) |
| PP | Peraturan Pemerintah (Government Regulations) |
| Perpres | Peraturan Presiden (Presidential Regulations) |
| Permen | Peraturan Menteri (Ministerial Regulations) |
| Perda | Peraturan Daerah (Regional Regulations) |

