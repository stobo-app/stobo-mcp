<!-- mcp-name: io.github.stobo-app/seo-audit -->
<!-- docs: https://docs.trystobo.com -->

# Stobo MCP Server

**Docs:** [docs.trystobo.com](https://docs.trystobo.com)

Audit any site for SEO, AEO, and E-E-A-T from Claude Desktop. Get a structured fix brief your developer can drop straight into Claude Code, Cursor, or VS Code and start shipping.

```
You: stobo this site: example.com

Claude: I just received a complete audit for example.com. SEO, AEO, EEAT,
per-page breakdowns, 30+ checks with scores and details.

Want me to generate a fix brief you can download and drop into
Claude Code, Cursor, or hand off to your developer?
```

---

## Why not just use web_fetch?

Fetching every page manually costs ~386,000 tokens across 16+ calls. It still misses Core Web Vitals, TTFB, and Flesch-Kincaid. Those metrics require server-side computation. Stobo runs everything in one call.

| | Manual (web_fetch) | Stobo MCP |
|---|---|---|
| `audit_site` | 71,000 tk · 6 fetches | 20,000 tk · 1 call |
| `audit_freshness` | 60,000 tk · 20 fetches | 3,000 tk · 1 call |
| `generate_llms_txt` | 35,000 tk · 6 fetches | 3,000 tk · 1 call |
| `extract_tone` | 35,000 tk · 10 fetches | 5,000 tk · 1 call |
| **Full suite** | **264,500 tk · 56 fetches** | **47,000 tk · 9 calls** |

82% fewer tokens. And you get metrics Claude cannot compute from raw HTML alone.

---

## What happens after an audit

Claude receives 30+ scored checks across SEO, AEO, and E-E-A-T. It then offers a fix brief: structured markdown with every failing check, prioritized by impact, with specific fix instructions. Paste it into Claude Code, Cursor, or VS Code and start shipping.

Claude also offers generators for quick wins. Failing robots.txt? Claude generates one. Same for llms.txt, sitemap, and freshness code. The audit-to-fix loop runs in a single conversation.

---

## Tools

### Free — no API key required

| Say to Claude | What it does | Tool |
|---|---|---|
| "Stobo this site: example.com" | 30 SEO + 7 AEO checks + E-E-A-T + blog detection across your whole site | `audit_site` |
| "Audit this article: example.com/blog/post" | 7 SEO + 14 AEO checks on a single article | `audit_article` |
| "Generate a fix brief" | Structured markdown fix brief from a completed audit. Numbered tasks, priority order, fix instructions. IDE-ready. | `generate_fix_brief` |
| "Check freshness across example.com/sitemap.xml" | Scan your sitemap for datePublished and dateModified coverage | `audit_freshness` |
| "Generate a robots.txt for example.com" | AI-crawler-friendly robots.txt. All 21 major bots covered. | `generate_robots_txt` |
| "Generate a sitemap for example.com" | BFS-crawl up to 200 URLs and return a sitemap.xml | `generate_sitemap` |
| "Generate freshness code for example.com/blog/post" | JSON-LD snippet with datePublished and dateModified | `generate_freshness_code` |
| "Check connection" | Diagnostic ping. Also tells you if a newer MCP version is available. | `check_connection` |

### Premium — coming soon

| Say to Claude | What it does | Tool |
|---|---|---|
| "Generate llms.txt for example.com" | Crawl your site and return a spec-compliant llms.txt | `generate_llms_txt` |
| "Extract brand voice from example.com/blog" | Analyze up to 10 articles and create a persistent voice profile | `extract_tone` |
| "Rewrite this article: example.com/blog/post" | Audit + tone match + full rewrite in one pipeline | `rewrite_article` |
| "Audit the UX of example.com" | 50+ UX checks across accessibility, forms, typography, and navigation | `audit_ux` |
| "How many credits do I have?" | Credit balance and usage breakdown | `get_credits` |

---

## Routing

- Domain or homepage → `audit_site`
- Blog post or article URL → `audit_article`
- After any audit → Claude offers `generate_fix_brief` automatically

---

## Install

```bash
pip install stobo-mcp
```

No install with `uvx`:

```bash
uvx stobo-mcp
```

---

## Setup

Add to your Claude Desktop config.

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

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

`STOBO_API_KEY` is optional. Every audit and fix brief tool works without one. API key support for premium tools is coming soon.

Full setup guide at [docs.trystobo.com](https://docs.trystobo.com).

---

## Upgrades

```bash
pip install --upgrade stobo-mcp
```

Run `check_connection`. Claude tells you if a newer version is available.

---

## What's new in v0.5.0

- `generate_fix_brief`: structured fix brief from any completed audit. Free, instant, no LLM.
- Claude now offers a fix brief automatically after every `audit_site` or `audit_article` run.
- `check_connection` reports when a newer version is available.
- Version strings are now consistent across server, client, and package.

---

## License

MIT
