<!-- mcp-name: io.github.stobo-app/seo-audit -->

# Stobo MCP Server

MCP server for [Stobo](https://trystobo.com) — AI-powered SEO & AEO content optimization. Audit websites, generate llms.txt, robots.txt, sitemaps, and optimize content directly from Claude Desktop, Cursor, or VS Code.

## Install

```bash
pip install stobo-mcp
```

Or run directly with uvx (no install needed):

```bash
uvx stobo-mcp
```

## Setup

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "stobo": {
      "command": "stobo-mcp",
      "env": {
        "STOBO_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Cursor

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "stobo": {
      "command": "stobo-mcp",
      "env": {
        "STOBO_API_KEY": "your-api-key"
      }
    }
  }
}
```

### VS Code / Windsurf

Add to `.vscode/mcp.json` or user settings:

```json
{
  "mcp": {
    "servers": {
      "stobo": {
        "command": "stobo-mcp",
        "env": {
          "STOBO_API_KEY": "your-api-key"
        }
      }
    }
  }
}
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `STOBO_API_KEY` | No | API key for paid tools. Free tools work without it. |
| `STOBO_BASE_URL` | No | API endpoint (default: `https://api.trystobo.com`) |

## Available Tools (11)

### Free — no setup needed

| Tool | Description |
|------|-------------|
| `audit_site` | Analyze a website's SEO and AI visibility (30 SEO + 7 AEO checks) |
| `audit_article` | Analyze a single blog post or article (7 SEO + 14 AEO checks) |
| `audit_freshness` | Check date markup across your blog posts via sitemap |
| `generate_robots_txt` | Create a robots.txt that welcomes AI crawlers |
| `generate_sitemap` | Create a sitemap.xml by crawling your website |
| `generate_freshness_code` | Create date markup for a page |
| `check_connection` | Verify API connectivity (diagnostic) |

### Requires API key

| Tool | Description |
|------|-------------|
| `generate_llms_txt` | Create an llms.txt so AI assistants understand your site |
| `extract_tone` | Analyze your brand's writing style from blog posts |
| `rewrite_article` | Rewrite an article for better SEO and AI visibility |
| `get_credits` | Check your remaining credits |

## Routing Rules

- **Default:** Use `audit_site` for any domain, homepage, or generic "audit this" request
- **Only** use `audit_article` when the URL is clearly a specific blog post (e.g. `/blog/my-post`)

## Usage

Just ask Claude:

- "Audit https://example.com" (uses audit_site)
- "Audit https://example.com/blog/my-post" (uses audit_article)
- "Generate an llms.txt for https://example.com"
- "Create an AI-friendly robots.txt for my site"
- "Extract the brand voice from https://example.com/blog"
- "How many credits do I have left?"

## Get an API Key

1. Sign up at [trystobo.com](https://trystobo.com)
2. Go to Settings > API Keys
3. Create a new key and add it to your editor config

## License

MIT
