import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import axios from 'axios';

interface YoucomSearchResult {
  title: string;
  url: string;
  snippet: string;
  domain?: string;
}

interface YoucomApiResponse {
  hits: Array<{
    title: string;
    url: string;
    snippet: string;
  }>;
}

class YoucomSearchServer {
  private server: Server;
  private apiKey: string | undefined;
  private baseUrl: string;

  constructor() {
    this.server = new Server(
      {
        name: 'youcom-search-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.apiKey = process.env.YDC_API_KEY;
    this.baseUrl = process.env.YOUCOM_BASE_URL || 'https://api.you.com';

    this.setupToolHandlers();
  }

  private setupToolHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'youcom_search',
            description: 'Search the web using You.com API for Indonesian government policy research, news, and contextual information',
            inputSchema: {
              type: 'object',
              properties: {
                query: {
                  type: 'string',
                  description: 'Search query for Indonesian government data, policy, or related information',
                },
                domains: {
                  type: 'array',
                  items: { type: 'string' },
                  description: 'Optional list of domains to search within (e.g., ["gov.id", "kemenkeu.go.id"])',
                },
                count: {
                  type: 'number',
                  description: 'Number of search results to return (default: 10, max: 20)',
                  minimum: 1,
                  maximum: 20,
                },
              },
              required: ['query'],
            },
          },
          {
            name: 'youcom_news_search',
            description: 'Search for recent news about Indonesian government, policies, or agencies using You.com',
            inputSchema: {
              type: 'object',
              properties: {
                query: {
                  type: 'string',
                  description: 'News search query related to Indonesian government or policies',
                },
                days: {
                  type: 'number',
                  description: 'Number of days to search back (default: 30)',
                  minimum: 1,
                  maximum: 365,
                },
                count: {
                  type: 'number',
                  description: 'Number of news results to return (default: 10, max: 20)',
                  minimum: 1,
                  maximum: 20,
                },
              },
              required: ['query'],
            },
          },
        ],
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'youcom_search':
            return await this.handleWebSearch(args as any);
          case 'youcom_news_search':
            return await this.handleNewsSearch(args as any);
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`,
            },
          ],
        };
      }
    });
  }

  private async handleWebSearch(args: {
    query: string;
    domains?: string[];
    count?: number;
  }) {
    const { query, domains, count = 10 } = args;
    
    let searchQuery = query;
    if (domains && domains.length > 0) {
      searchQuery += ` site:${domains.join(' OR site:')}`;
    }

    const results = await this.searchYoucom(searchQuery, count);
    
    return {
      content: [
        {
          type: 'text',
          text: this.formatSearchResults(results, 'Web Search', query),
        },
      ],
    };
  }

  private async handleNewsSearch(args: {
    query: string;
    days?: number;
    count?: number;
  }) {
    const { query, days = 30, count = 10 } = args;
    
    // Add time constraint and Indonesian context to query
    const searchQuery = `${query} Indonesia government policy news site:detik.com OR site:kompas.com OR site:tempo.co OR site:liputan6.com OR site:antaranews.com`;

    const results = await this.searchYoucom(searchQuery, count);
    
    return {
      content: [
        {
          type: 'text',
          text: this.formatSearchResults(results, 'News Search', query),
        },
      ],
    };
  }

  private async searchYoucom(query: string, count: number): Promise<YoucomSearchResult[]> {
    const endpoint = this.apiKey ? '/web' : '/search';
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    
    if (this.apiKey) {
      headers['X-API-Key'] = this.apiKey;
    }

    const payload = {
      query,
      count: Math.min(count, 20),
    };

    try {
      const response = await axios.post<YoucomApiResponse>(
        `${this.baseUrl}${endpoint}`,
        payload,
        { headers, timeout: 10000 }
      );

      return response.data.hits.map(hit => ({
        title: hit.title,
        url: hit.url,
        snippet: hit.snippet,
        domain: this.extractDomain(hit.url),
      }));
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 401) {
          throw new Error('Authentication failed. Check YDC_API_KEY environment variable.');
        } else if (error.response?.status === 429) {
          throw new Error('Rate limit exceeded. Please try again later.');
        } else {
          throw new Error(`API request failed: ${error.response?.status} ${error.response?.statusText}`);
        }
      }
      throw new Error(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  private extractDomain(url: string): string {
    try {
      return new URL(url).hostname;
    } catch {
      return 'unknown';
    }
  }

  private formatSearchResults(results: YoucomSearchResult[], searchType: string, query: string): string {
    if (results.length === 0) {
      return `${searchType} Results for "${query}": No results found.`;
    }

    const formattedResults = results.map((result, index) => {
      return `${index + 1}. **${result.title}**
   URL: ${result.url}
   Domain: ${result.domain}
   Snippet: ${result.snippet}`;
    }).join('\n\n');

    return `${searchType} Results for "${query}" (${results.length} results):

${formattedResults}`;
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('You.com Search MCP server running on stdio');
  }
}

const server = new YoucomSearchServer();
server.run().catch(console.error);