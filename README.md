<!-- mcp-name: io.github.stobo-app/seo-audit -->

# Stobo MCP Server

MCP server for [Stobo](https://trystobo.com) — AI-powered SEO/AEO content optimization. Use Stobo's audit, tone extraction, llms.txt generation, and optimization tools directly from Claude Desktop.

## Install

```bash
pip install stobo-mcp
```

## Setup

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "stobo": {
      "command": "stobo-mcp",
      "env": {
        "STOBO_API_KEY": "your-api-key",
        "STOBO_BASE_URL": "https://api.trystobo.com"
      }
    }
  }
}
```

## Available Tools (19)

### Site & Article Audits

| Tool | Auth | Description |
|------|------|-------------|
| `audit_site` | Free | **Main entry point.** Full site audit: 30 SEO + 7 AEO checks + blog detection + sitemap discovery |
| `audit_article` | Free | Article-level SEO + AEO audit (for specific blog posts) |
| `audit_seo` | Free | SEO-only audit on a single page |
| `audit_aeo` | Free | AEO-only audit on a single page |
| `get_audit` | Key | Fetch audit results by ID |
| `list_audits` | Key | List recent audits |

### Brand Voice & Optimization

| Tool | Auth | Description |
|------|------|-------------|
| `extract_tone` | Paid | Extract brand voice profile from a blog (500 credits) |
| `get_tone` | Key | Get a stored tone profile |
| `list_tone_profiles` | Key | List all tone profiles |
| `delete_tone` | Key | Delete a stored tone profile |
| `optimize` | Paid | Start full optimization pipeline: audit + tone + rewrite (1,000 credits) |
| `get_job` | Key | Check optimization job status |
| `get_job_preview` | Key | Get before/after preview of a completed optimization |
| `list_jobs` | Key | List optimization jobs |

### Content & Reports

| Tool | Auth | Description |
|------|------|-------------|
| `generate_llms_txt` | Paid | Generate a llms.txt file for AI discoverability (500 credits) |
| `freshness_audit` | Free | Audit sitemap for content freshness (dateModified schema) |
| `get_freshness` | Key | Get a previously completed freshness audit |
| `export_report` | Paid | Generate a markdown report (200 credits) |
| `get_export` | Key | Get a cached export report |

### Account

| Tool | Auth | Description |
|------|------|-------------|
| `get_credits` | Key | Check credit usage, balance, and breakdown |

## Routing Rules

- **Default:** Use `audit_site` for any domain, homepage, or generic "audit this" request
- **Only** use `audit_article` when the URL is clearly a specific blog post (contains `/blog/`, `/post/`, `/article/`)

Examples:
- "audit phantombuster.com" -> `audit_site`
- "audit https://example.com" -> `audit_site`
- "check https://example.com/blog/my-post" -> `audit_article`

## Usage in Claude Desktop

Just ask Claude:

- "Audit https://example.com" (uses audit_site)
- "Deep-dive https://example.com/blog/my-post" (uses audit_article)
- "Extract the brand voice from https://example.com/blog"
- "Generate a llms.txt for https://example.com"
- "Optimize https://example.com/blog/my-article"
- "How many credits do I have left?"

## What's New in 0.2.0

- `audit_site` — full website audit with combined score, SEO categories, AEO checklist, blog detection, sitemap discovery
- `generate_llms_txt` — create spec-compliant llms.txt files
- `delete_tone` — delete stored brand voice profiles
- `get_job_preview` / `list_jobs` — optimization job management
- `get_freshness` / `get_export` — retrieve cached results
- `get_credits` — check credit usage and balance
- Improved tool descriptions with routing rules and formatting guidance

## Why MCP instead of web_fetch?

Without Stobo, auditing a site means fetching every page with `web_fetch`, pasting raw HTML into context, and asking Claude to parse it. A single `audit_site` run would cost **~386,000 tokens** and 16 separate fetches — and still miss metrics that require server-side computation.

With Stobo MCP, the same audit is **one tool call, ~20,000 tokens**.

| | Manual (web_fetch) | Stobo MCP |
|---|---|---|
| `audit_site` | 71,000 tk / 6 fetches | 20,000 tk / 1 call |
| `audit_freshness` | 60,000 tk / 20 fetches | 3,000 tk / 1 call |
| `generate_llms_txt` | 35,000 tk / 6 fetches | 3,000 tk / 1 call |
| `extract_tone` | 35,000 tk / 10 fetches | 5,000 tk / 1 call |
| **All 9 tools** | **264,500 tk / 56 fetches** | **47,000 tk / 9 calls** |

That's **82% fewer tokens** across the full tool suite.

Stobo also computes metrics Claude can't get from raw HTML alone: Core Web Vitals (Playwright), TTFB timing, HTTP status codes for all links, and Flesch-Kincaid readability scoring.

## Get an API Key

1. Sign up at [trystobo.com](https://trystobo.com)
2. Go to Settings > API Keys
3. Create a new key and add it to your Claude Desktop config

## License

MIT
