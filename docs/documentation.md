# Stobo MCP

Learn how to connect AI assistants to Stobo for website SEO and AI visibility audits.

Use [Stobo](https://trystobo.com) from your AI editor through the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction), an open standard that lets AI assistants audit, fix, and optimize your website for search engines and AI discovery.

## What is Stobo MCP?

Stobo MCP is an MCP server that gives AI tools direct access to Stobo's SEO and AEO audit engine. It works with Claude Desktop, Claude Code, Cursor, VS Code, Windsurf, and any MCP-compatible client.

### Why use Stobo MCP?

* **No manual fetching** — One tool call replaces dozens of web fetches and hundreds of thousands of tokens of raw HTML parsing
* **Full SEO + AEO audit** — 34 SEO checks across 7 categories (380 pts), plus 7 AEO checks for AI discoverability
* **Instant fix generation** — Generate llms.txt, robots.txt, sitemap.xml, and date markup files ready to deploy
* **Brand-aware rewrites** — Extract your writing style from existing content and rewrite articles to match
* **Server-side metrics** — Core Web Vitals, TTFB, HTTP status codes, and readability scores that can't be computed from raw HTML
* **Free to start** — Audits and most generators work without an API key or account

### What can you do with Stobo MCP?

* **Website audits** — Run a full 34-check SEO + 7-check AEO audit on any website, get a combined score, and see exactly what's failing
* **Article audits** — Deep-dive a specific blog post with 7 SEO and 14 AEO checks, optionally targeting a keyword
* **Fix failing checks** — Generate llms.txt, robots.txt, sitemap.xml, and date markup to fix issues found in the audit
* **Content freshness** — Scan your sitemap and find which blog posts are missing date markup that AI assistants look for
* **Brand voice extraction** — Analyze up to 10 blog posts to build a tone profile of your writing style
* **Article rewriting** — Rewrite an article to improve SEO and AI visibility while keeping your brand voice

---

## Getting Started

### Prerequisites

Before connecting Stobo MCP, ensure you have:

1. An MCP-compatible AI client (Claude Desktop, Claude Code, Cursor, VS Code, Windsurf, etc.)
2. `uv` installed (`pip install uv` or `brew install uv`) — for the `uvx` runtime
3. (Optional) A Stobo API key from [trystobo.com](https://trystobo.com) — only needed for paid tools

### Connecting to Stobo MCP

Add the following config to your AI editor. No OAuth — just paste the config and go.

#### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "stobo": {
      "command": "uvx",
      "args": ["--native-tls", "stobo-mcp"],
      "env": {
        "STOBO_API_KEY": "your-api-key"
      }
    }
  }
}
```

#### Claude Code (CLI)

```bash
claude mcp add stobo -- uvx --native-tls stobo-mcp
```

Then export your key in your shell:

```bash
export STOBO_API_KEY="your-api-key"
```

#### Cursor

Open **Settings > MCP Servers > Add Server**, then paste:

```json
{
  "stobo": {
    "command": "uvx",
    "args": ["--native-tls", "stobo-mcp"],
    "env": {
      "STOBO_API_KEY": "your-api-key"
    }
  }
}
```

#### VS Code (Copilot)

Add to `.vscode/mcp.json` in your project:

```json
{
  "servers": {
    "stobo": {
      "command": "uvx",
      "args": ["--native-tls", "stobo-mcp"],
      "env": {
        "STOBO_API_KEY": "your-api-key"
      }
    }
  }
}
```

#### Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "stobo": {
      "command": "uvx",
      "args": ["--native-tls", "stobo-mcp"],
      "env": {
        "STOBO_API_KEY": "your-api-key"
      }
    }
  }
}
```

> **Note:** `STOBO_API_KEY` is optional. Remove the `env` block entirely to use free tools without an account.

---

## Supported Tools

Stobo MCP exposes 11 tools. Most are free. Their real power comes from combining them — audit a site, then fix every failing check in the same conversation.

### Audits

| Tool | Description | Example Prompts |
|------|-------------|-----------------|
| `audit_site` | Full website audit: 34 SEO checks (380 pts) + 7 AEO checks, blog detection, sitemap discovery. **Default tool — use for any website or homepage.** Results cached 24h. | "Audit phantombuster.com"<br/>"Check the SEO of https://example.com"<br/>"How does my site score for AI visibility?" |
| `audit_article` | Article-level audit: 7 SEO + 14 AEO checks. Use for specific blog post URLs. Optionally target a keyword. | "Audit https://example.com/blog/my-post"<br/>"Check this article targeting 'content marketing'" |
| `audit_freshness` | Scan your sitemap and report which pages are missing date markup that AI assistants look for. | "Check freshness across my blog"<br/>"Which posts are missing date markup?" |

### Fix Generators

| Tool | Description | Example Prompts |
|------|-------------|-----------------|
| `generate_llms_txt` | Create an llms.txt file so AI assistants understand your website. Returns ready-to-deploy content. | "Generate an llms.txt for https://example.com"<br/>"My llms.txt check failed — fix it" |
| `generate_robots_txt` | Create a robots.txt that welcomes AI crawlers (GPTBot, ClaudeBot, PerplexityBot, etc.). | "Create a robots.txt that allows AI crawlers"<br/>"Fix my blocked AI bots" |
| `generate_sitemap` | Crawl your website and create a sitemap.xml. Scans up to 200 URLs by default. | "Generate a sitemap for https://example.com"<br/>"My sitemap is missing — create one" |
| `generate_freshness_code` | Create a date markup code snippet with publish and update dates for a page. | "Generate date markup for this page"<br/>"Add freshness signals to my blog post" |

### Content Optimization

| Tool | Description | Example Prompts |
|------|-------------|-----------------|
| `extract_tone` | Analyze your brand's writing style from up to 10 blog posts. Creates a voice profile. | "Extract the brand voice from https://example.com/blog"<br/>"What's my writing style?" |
| `rewrite_article` | Rewrite an article to improve SEO and AI visibility while keeping your brand voice. Audits first, then rewrites. | "Rewrite this article for better AI visibility"<br/>"Optimize https://example.com/blog/guide" |

### Account & Diagnostics

| Tool | Description | Example Prompts |
|------|-------------|-----------------|
| `get_credits` | Check your plan, credit usage, and remaining balance. | "How many credits do I have left?"<br/>"Check my balance" |
| `check_connection` | Verify the Stobo API is reachable. Use to diagnose connection issues. | "Check if Stobo is working"<br/>"Test the connection" |

---

## Sample Prompts

### Full Website Audit

| Prompt | What it does |
|--------|-------------|
| "Audit phantombuster.com" | Runs a full 34 SEO + 7 AEO audit on the site |
| "Check https://example.com for AI visibility" | Same audit, framed around AEO |
| "What's failing on my site?" | Runs audit and highlights failing checks |

### Fix Failing Checks

| Prompt | What it does |
|--------|-------------|
| "My llms.txt is missing — generate one" | Creates a ready-to-deploy llms.txt file |
| "AI crawlers are blocked — fix my robots.txt" | Generates an AI-friendly robots.txt |
| "Generate a sitemap for my site" | Crawls up to 200 pages and builds sitemap.xml |
| "Add date markup to this page" | Creates a freshness code snippet |

### Blog Content Optimization

| Prompt | What it does |
|--------|-------------|
| "Audit https://example.com/blog/my-post" | Runs article-level audit with 14 AEO checks |
| "Extract my brand voice from my blog" | Analyzes 10 posts and builds a tone profile |
| "Rewrite this article for better SEO" | Audits, then rewrites keeping your voice |

### Content Freshness

| Prompt | What it does |
|--------|-------------|
| "Check freshness across my sitemap" | Scans sitemap for missing date markup |
| "Which blog posts need date markup?" | Same — surfaces pages without freshness signals |

---

## Typical Workflows

These tools work best when combined. Here are the most common patterns:

### Audit → Fix

1. **"Audit https://example.com"** — Get your combined SEO + AEO score
2. Review failing checks
3. Fix each one:
   - llms.txt missing → **"Generate an llms.txt"**
   - AI crawlers blocked → **"Generate a robots.txt"**
   - Sitemap missing → **"Generate a sitemap"**
   - Freshness missing → **"Generate date markup"**

### Blog Optimization

1. **"Audit my blog post https://example.com/blog/guide"** — Article-level deep dive
2. **"Extract my brand voice from https://example.com/blog"** — Build tone profile
3. **"Rewrite https://example.com/blog/guide"** — Optimized rewrite in your voice

### Content Freshness Sweep

1. **"Check freshness across my blog at https://example.com/sitemap.xml"** — Find gaps
2. For each page missing dates → **"Generate date markup for [url]"**

---

## Pricing & Credits

| Tool | Cost |
|------|------|
| `audit_site`, `audit_article`, `audit_freshness` | Free |
| `generate_robots_txt`, `generate_sitemap`, `generate_freshness_code` | Free |
| `check_connection` | Free |
| `generate_llms_txt` | 500 credits |
| `extract_tone` | 500 credits |
| `rewrite_article` | 1,000 credits |
| `get_credits` | Requires API key |

Free tools work without an account or API key. Get credits at [trystobo.com](https://trystobo.com).

---

## Why MCP Instead of web_fetch?

Without Stobo, auditing a site means fetching every page with `web_fetch`, pasting raw HTML into context, and asking the AI to parse it.

| | Manual (web_fetch) | Stobo MCP |
|---|---|---|
| Full site audit (34 checks) | ~71,000 tokens / 6 fetches | ~20,000 tokens / 1 call |
| Freshness audit | ~60,000 tokens / 20 fetches | ~3,000 tokens / 1 call |
| llms.txt generation | ~35,000 tokens / 6 fetches | ~3,000 tokens / 1 call |
| Tone extraction | ~35,000 tokens / 10 fetches | ~5,000 tokens / 1 call |
| **All tools combined** | **~264,500 tokens / 56 fetches** | **~47,000 tokens / 9 calls** |

That's **82% fewer tokens** and **84% fewer network calls**. Plus, Stobo computes metrics the AI can't get from raw HTML: Core Web Vitals (via Playwright), TTFB timing, HTTP status codes for all links, and Flesch-Kincaid readability scoring.

---

## Troubleshooting

### "No API key configured"

Free tools work without a key. If you're calling a paid tool:

1. Sign up at [trystobo.com](https://trystobo.com)
2. Go to **Settings > API Keys**
3. Add `STOBO_API_KEY` to your editor config
4. Restart your editor

### "Your API key is invalid or expired"

Log in at [trystobo.com](https://trystobo.com), generate a new key, and update your config.

### "You've run out of credits"

Top up at [trystobo.com](https://trystobo.com). Free tools still work without credits.

### "Rate limit reached"

Wait a moment and try again. Rate limits reset quickly. Normal conversational use stays well within limits.

### Connection issues

Ask your AI assistant to run `check_connection`. Common fixes:

- Check your internet connection
- Make sure `STOBO_BASE_URL` is not set (it defaults to the right value)
- Try again in a few minutes if the API is temporarily down

### Tool not showing up in your editor

- Save your config file and **restart** the editor
- Verify `uvx` is installed: run `uvx --version` in your terminal
- Test manually: `uvx --native-tls stobo-mcp` — it should start without errors

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `STOBO_API_KEY` | No | _(empty)_ | Your API key from trystobo.com. Free tools work without it. |
| `STOBO_BASE_URL` | No | `https://api.trystobo.com` | API endpoint. Only change this if told to by Stobo support. |

---

## What's Next

* [Stobo Website](https://trystobo.com) — Sign up, get an API key, and manage your credits
* [GitHub Repository](https://github.com/stobo-app/stobo-mcp) — Source code, issues, and contributions
* [PyPI Package](https://pypi.org/project/stobo-mcp/) — Package details and version history
* [Stobo CLI](https://pypi.org/project/stobo/) — Command-line interface for Stobo (same tools, terminal-first)
