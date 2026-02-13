<!-- mcp-name: io.github.stobo-app/seo-audit -->

# Stobo MCP Server

MCP server for [Stobo](https://trystobo.com) — AI-powered SEO & AEO content optimization. Audit websites, generate llms.txt, robots.txt, sitemaps, and optimize content directly from Claude Desktop, Cursor, or VS Code.

## Features

- **Site Audit** — 30 SEO checks + 7 AEO checks + blog detection + sitemap discovery
- **Article Audit** — Deep-dive SEO + AI readability analysis for individual posts
- **Fix Generators** — Instantly create llms.txt, robots.txt, sitemap.xml, and date markup
- **Brand Voice** — Extract your writing style from existing blog posts
- **Content Rewrite** — Rewrite articles for better SEO and AI visibility
- **Freshness Audit** — Scan your sitemap for missing date markup
- **Free tier** — 7 tools work without an API key

## Install

```bash
pip install stobo-mcp
```

Or run directly with uvx (no install needed):

```bash
uvx stobo-mcp
```

Or install from the Anthropic MCP Directory in Claude Desktop.

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

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `STOBO_API_KEY` | No | API key for paid tools. Free tools work without it. |
| `STOBO_BASE_URL` | No | API endpoint (default: `https://api.trystobo.com`) |

## Available Tools (11)

### Free — no setup needed

| Tool | Description | Annotation |
|------|-------------|------------|
| `audit_site` | Analyze a website's SEO and AI visibility (30 SEO + 7 AEO checks) | `readOnlyHint` |
| `audit_article` | Analyze a single blog post or article (7 SEO + 14 AEO checks) | `readOnlyHint` |
| `audit_freshness` | Check date markup across your blog posts via sitemap | `readOnlyHint` |
| `generate_robots_txt` | Create a robots.txt that welcomes AI crawlers | `readOnlyHint` |
| `generate_sitemap` | Create a sitemap.xml by crawling your website | `readOnlyHint` |
| `generate_freshness_code` | Create date markup for a page | `readOnlyHint` |
| `check_connection` | Verify API connectivity (diagnostic) | `readOnlyHint` |

### Requires API key

| Tool | Description | Annotation |
|------|-------------|------------|
| `generate_llms_txt` | Create an llms.txt so AI assistants understand your site | write |
| `extract_tone` | Analyze your brand's writing style from blog posts | write |
| `rewrite_article` | Rewrite an article for better SEO and AI visibility | write |
| `get_credits` | Check your remaining credits | `readOnlyHint` |

### Routing Rules

- **Default:** Use `audit_site` for any domain, homepage, or generic "audit this" request
- **Only** use `audit_article` when the URL is clearly a specific blog post (e.g. `/blog/my-post`)

## Usage Examples

### Example 1: Full Website Audit

**User prompt:** "Audit phantombuster.com for SEO and AI visibility"

**Expected behavior:**
- Stobo calls `audit_site` with the URL
- Runs 30 SEO checks across 7 categories (Content, Links, Technical, Performance, Security, Social, Accessibility)
- Runs 7 AEO checks (robots.txt AI access, llms.txt, freshness, FAQs, FAQ schema, direct answers, sitemap)
- Detects blog and sitemap
- Returns a combined score (e.g. "72% SEO + AEO") with category breakdowns and top recommendations
- Claude presents failing checks and offers to generate fixes (llms.txt, robots.txt, sitemap)

### Example 2: Generate an llms.txt File

**User prompt:** "My site is missing an llms.txt — can you generate one for https://example.com?"

**Expected behavior:**
- Stobo calls `generate_llms_txt` with the URL
- Crawls the site to understand its structure, products, and content
- Returns a spec-compliant llms.txt file with title, description, and key pages
- The user can copy the output and deploy it at their domain root (`/llms.txt`)

### Example 3: Audit a Blog Post

**User prompt:** "Check if this article is optimized for AI: https://example.com/blog/how-to-start"

**Expected behavior:**
- Stobo calls `audit_article` with the URL
- Runs 7 SEO checks (title, meta, headings, word count, links, etc.)
- Runs 14 AEO checks (direct answers, FAQ blocks, schema markup, freshness, etc.)
- Returns a score with specific recommendations like "Add a direct answer in the first 60 words" or "Missing FAQ schema markup"
- Claude suggests using `generate_freshness_code` if date markup is missing

### Example 4: Extract Brand Voice

**User prompt:** "Analyze the writing style of https://example.com/blog"

**Expected behavior:**
- Stobo calls `extract_tone` with the blog URL
- Reads up to 10 recent articles from the blog
- Creates a voice profile describing tone (formal/casual), vocabulary patterns, sentence structure, and stylistic traits
- The profile is stored and can be used by `rewrite_article` to maintain brand consistency

### Example 5: Check Credit Balance

**User prompt:** "How many Stobo credits do I have left?"

**Expected behavior:**
- Stobo calls `get_credits`
- Returns the current plan name, credits used, credits remaining, and renewal date
- If no API key is configured, returns an error explaining how to set one up

## Get an API Key

1. Sign up at [trystobo.com](https://trystobo.com)
2. Go to Settings > API Keys
3. Create a new key and add it to your editor config

## Privacy Policy

Stobo processes website URLs and publicly available web content to perform SEO and AEO audits. Here is how data is handled:

- **Data collected:** URLs you submit and the publicly available HTML content at those URLs. For paid tools, your API key is sent to authenticate requests.
- **How it's used:** URLs and HTML are analyzed in real-time to generate audit scores, recommendations, and content. Audit results are cached for up to 24 hours to improve performance.
- **Storage:** Tone profiles and optimization results are stored on Stobo's servers and associated with your account. Audit results are cached temporarily.
- **Third-party sharing:** Stobo uses Anthropic's Claude API for AI-powered analysis (tone extraction, content rewriting). Submitted content is sent to Anthropic for processing. No data is shared with other third parties.
- **Data retention:** Cached audit results expire after 24 hours. Tone profiles and optimization jobs are retained until you delete them or close your account.
- **No tracking:** Stobo does not track browsing behavior, install analytics, or collect personal data beyond what you explicitly submit.

Full privacy policy: [https://trystobo.com/privacy](https://trystobo.com/privacy)

## Support

- Issues: [github.com/stobo-app/stobo-mcp/issues](https://github.com/stobo-app/stobo-mcp/issues)
- Email: hello@trystobo.com

## License

MIT
