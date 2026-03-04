"""Stobo MCP Server — exposes Stobo API as tools for Claude Desktop."""

from __future__ import annotations

import json
import os

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from stobo.client import AuthError, RateLimitError, StoboAPIError, StoboClient

# ── Annotations ─────────────────────────────────────────────────────

READ_ONLY = ToolAnnotations(
    readOnlyHint=True, destructiveHint=False, openWorldHint=True
)
WRITE = ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True)

mcp = FastMCP(
    "Stobo",
    instructions="""Stobo helps websites get discovered by AI assistants (ChatGPT, Perplexity, Claude, etc.) and search engines.

WHICH TOOL TO USE:
- "audit my site" / any domain / homepage → audit_site (DEFAULT — always use this unless told otherwise)
- "audit this article" / specific blog post URL → audit_article
- When in doubt, use audit_site.

EXAMPLES:
- "audit phantombuster.com" → audit_site
- "check https://example.com" → audit_site
- "audit https://example.com/blog/my-post" → audit_article

HOW TO PRESENT AUDIT_SITE RESULTS:

Lead with the combined score, then break down SEO and AEO:

  ## {domain} — {combined_percentage}% (SEO + AEO)
  SEO: {grade} ({overall_score}/{max_points})
  AEO: {percentage}% ({score}/{max_points})

Then show:
1. SEO category breakdown (7 categories) as a table — Content, Links, Technical, Performance, Security, Social, Accessibility
2. AEO checklist (7 checks) — robots_ai, llms_txt, freshness, faqs, faq_schema, direct_answer, sitemap — as pass/fail
3. Blog detection — if found, suggest audit_freshness or audit_article as next steps
4. Sitemap discovery — summary of pages found and how they're classified
5. Top 3-5 recommendations from the failing checks

Only show failing/critical checks in detail. Don't dump all 30 checks.
Mention if results are cached ("Results from cache, less than 24h old").

PROACTIVE FIX SUGGESTIONS:
After showing audit results, offer to fix any failing AEO checks:
- llms.txt missing/failing → "Want me to generate an llms.txt file?"
- robots.txt blocking AI → "Want me to generate an AI-friendly robots.txt?"
- sitemap missing → "Want me to generate a sitemap.xml?"
- freshness missing → "Want me to generate date markup for this page?"

These generators are free and produce ready-to-deploy files.

FIX BRIEF — DEVELOPER HANDOFF:
After showing audit results and proactive fix suggestions, ALWAYS offer:
"Want me to generate a fix brief you can download and drop straight into Claude Code, Cursor, or hand off to your developer?"
When the user accepts, call generate_fix_brief with the audit_id from seo_audit.id.

TOOL LIST FORMAT — MANDATORY:
When the user asks what tools/commands are available, you MUST use EXACTLY this format with these two groups. Do NOT invent your own categories. Do NOT show parameter names. Copy this structure verbatim:

**Free — no setup needed**

`audit_site` — Analyze a website's SEO and AI visibility
`audit_article` — Analyze a single blog post or article
`audit_freshness` — Check date markup across your blog posts
`generate_robots_txt` — Create a robots.txt that welcomes AI crawlers
`generate_sitemap` — Create a sitemap.xml for your website
`generate_freshness_code` — Create date markup for a page
`generate_fix_brief` — Generate a developer fix brief from an audit

**Requires API key**

`generate_llms_txt` — Create an llms.txt so AI assistants understand your site
`extract_tone` — Analyze your brand's writing style
`rewrite_article` — Rewrite an article for better SEO and AI visibility
`get_credits` — Check your remaining credits""",
)


def _get_client() -> StoboClient:
    api_key = os.environ.get("STOBO_API_KEY", "")
    base_url = os.environ.get("STOBO_BASE_URL", "https://api.trystobo.com")
    return StoboClient(
        base_url=base_url, api_key=api_key, user_agent="stobo-mcp/0.5.1", source="mcp"
    )


def _call(fn, *args, transform=None, **kwargs) -> str:
    """Call a client method and return JSON string, handling errors."""
    try:
        result = fn(*args, **kwargs)
        if transform is not None:
            result = transform(result)
        return json.dumps(result, indent=2, default=str)
    except AuthError as e:
        has_key = bool(os.environ.get("STOBO_API_KEY", ""))
        if not has_key:
            msg = (
                "No API key configured. "
                "Get your free API key at https://trystobo.com — "
                "then add STOBO_API_KEY to your MCP server config."
            )
        else:
            msg = (
                "Your API key is invalid or expired. "
                "Log in at https://trystobo.com to get a new one, "
                "then update STOBO_API_KEY in your MCP server config."
            )
        return json.dumps({"error": msg, "status_code": e.status_code})
    except RateLimitError as e:
        return json.dumps(
            {
                "error": "Rate limit reached. Please wait a moment and try again.",
                "status_code": e.status_code,
            }
        )
    except StoboAPIError as e:
        if e.status_code == 402:
            msg = (
                "You've run out of credits. "
                "Top up at https://trystobo.com to continue using premium tools."
            )
            return json.dumps({"error": msg, "status_code": 402})
        return json.dumps({"error": e.detail, "status_code": e.status_code})
    except Exception as e:
        return json.dumps({"error": str(e)})


def _trim_site_audit(data: dict) -> dict:
    """Strip a site audit response to essentials (~5KB instead of ~249KB)."""
    if not isinstance(data, dict):
        return data

    out: dict = {}

    # Top-level scalars
    for key in ("url", "domain", "cached", "combined_percentage", "pages_analyzed"):
        if key in data:
            out[key] = data[key]

    # SEO audit — keep scores + top 10 recommendations (slim)
    seo = data.get("seo_audit")
    if seo and isinstance(seo, dict):
        trimmed_seo: dict = {}
        for key in (
            "id",
            "grade",
            "overall_score",
            "total_points",
            "max_points",
            "category_scores",
        ):
            if key in seo:
                trimmed_seo[key] = seo[key]
        recs = seo.get("recommendations") or []
        trimmed_seo["recommendations"] = [
            {k: r[k] for k in ("check", "message", "fix_type") if k in r}
            for r in recs[:10]
        ]
        out["seo_audit"] = trimmed_seo

    # AEO audit — keep scores + check summaries (no details)
    aeo = data.get("aeo_audit")
    if aeo and isinstance(aeo, dict):
        trimmed_aeo: dict = {}
        for key in ("score", "max_points", "percentage"):
            if key in aeo:
                trimmed_aeo[key] = aeo[key]
        checks = aeo.get("checks")
        if checks and isinstance(checks, dict):
            trimmed_aeo["checks"] = {
                name: {
                    k: v
                    for k, v in check.items()
                    if k in ("status", "score", "max_points", "message")
                }
                for name, check in checks.items()
            }
        out["aeo_audit"] = trimmed_aeo

    # EEAT audit — just grade + composite
    eeat = data.get("eeat_audit")
    if eeat and isinstance(eeat, dict):
        out["eeat_audit"] = {
            k: eeat[k] for k in ("grade", "composite_percentage") if k in eeat
        }

    # Blog detection — as-is (tiny)
    if "blog_detection" in data:
        out["blog_detection"] = data["blog_detection"]

    # Sitemap discovery — strip URL lists from categories
    sitemap = data.get("sitemap_discovery")
    if sitemap and isinstance(sitemap, dict):
        trimmed_sitemap: dict = {}
        for key in ("total_urls", "blog_article_count"):
            if key in sitemap:
                trimmed_sitemap[key] = sitemap[key]
        cats = sitemap.get("categories")
        if cats and isinstance(cats, list):
            trimmed_sitemap["categories"] = [
                {k: c[k] for k in ("name", "slug", "count") if k in c} for c in cats
            ]
        out["sitemap_discovery"] = trimmed_sitemap

    # Error fields — pass through
    for key in ("seo_error", "aeo_error", "eeat_error"):
        if key in data:
            out[key] = data[key]

    # Hint for Claude to offer full details
    audit_id = (seo or {}).get("id")
    if audit_id:
        out["_next_step"] = (
            f"Want me to generate a fix brief you can download and drop into "
            f"Claude Code, Cursor, or hand off to your developer? "
            f"Call generate_fix_brief with audit_id '{audit_id}'."
        )

    return out


# ── Audits ───────────────────────────────────────────────────────────


@mcp.tool(annotations=READ_ONLY)
def audit_site(url: str) -> str:
    """Analyze a website's SEO performance and AI visibility. Runs 30 SEO checks, 7 AEO checks, detects your blog, and maps your sitemap. This is the main tool — use it for any website or homepage. Results are cached for 24 hours."""
    client = _get_client()
    return _call(client.audit_site, url, transform=_trim_site_audit)


@mcp.tool(annotations=READ_ONLY)
def audit_article(
    url: str,
    keyword: str | None = None,
    use_playwright: bool = False,
) -> str:
    """Analyze a single blog post or article for SEO and AI readability. Runs 7 SEO and 14 AEO checks. Only use this for specific article URLs (e.g. /blog/my-post), not homepages."""
    client = _get_client()
    return _call(
        client.audit_article, url, keyword=keyword, use_playwright=use_playwright
    )


# ── Fix generators ───────────────────────────────────────────────────


@mcp.tool(annotations=WRITE)
def generate_llms_txt(url: str) -> str:
    """Create an llms.txt file to help AI assistants understand your website. Use when the audit shows your llms.txt is missing or incomplete. Returns ready-to-deploy content for your domain root."""
    client = _get_client()
    return _call(client.generate_llms_txt, url)


@mcp.tool(annotations=READ_ONLY)
def generate_robots_txt(url: str) -> str:
    """Create a robots.txt that welcomes AI crawlers (GPTBot, ClaudeBot, PerplexityBot, etc.). Use when the audit shows AI crawlers are being blocked. Free, instant."""
    client = _get_client()
    return _call(client.generate_robots_txt, url)


@mcp.tool(annotations=READ_ONLY)
def generate_sitemap(url: str, max_urls: int = 200) -> str:
    """Create a sitemap.xml by crawling your website's pages. Use when the audit shows your sitemap is missing or incomplete. Free."""
    client = _get_client()
    return _call(client.generate_sitemap, url, max_urls=max_urls)


@mcp.tool(annotations=READ_ONLY)
def generate_freshness_code(url: str) -> str:
    """Create date markup so AI knows your content is up to date. Generates a ready-to-use code snippet with publish and update dates. Use when the audit shows missing freshness signals. Free, instant."""
    client = _get_client()
    return _call(client.generate_freshness_code, url)


@mcp.tool(annotations=READ_ONLY)
def generate_fix_brief(audit_id: str) -> str:
    """Generate a structured fix brief from a completed audit. Returns markdown
    with all failing checks prioritized by impact, with fix instructions.
    Ready to paste into Claude Code, Cursor, or any AI coding assistant.
    Free, instant.

    The audit_id comes from the seo_audit.id field in audit_site results."""
    client = _get_client()
    try:
        result = client.generate_fix_brief(audit_id)
        return result["markdown"]
    except StoboAPIError as e:
        return json.dumps({"error": e.detail, "status_code": e.status_code})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ── Content optimization ─────────────────────────────────────────────


@mcp.tool(annotations=WRITE)
def rewrite_article(
    url: str,
    customer_id: str | None = None,
) -> str:
    """Rewrite an existing article to improve its SEO and AI visibility while keeping your brand voice. Audits the article first, then rewrites it with targeted fixes. Returns the improved version."""
    client = _get_client()
    return _call(client.optimize, url, customer_id=customer_id, sync=True)


@mcp.tool(annotations=WRITE)
def extract_tone(
    blog_url: str,
    customer_id: str | None = None,
    max_articles: int = 10,
) -> str:
    """Analyze your brand's writing style from blog posts. Reads up to 10 articles and creates a voice profile describing your tone, vocabulary, and style patterns."""
    client = _get_client()
    return _call(
        client.extract_tone,
        blog_url,
        customer_id=customer_id,
        max_articles=max_articles,
    )


# ── Freshness audit ──────────────────────────────────────────────────


@mcp.tool(annotations=READ_ONLY)
def audit_freshness(sitemap_url: str, limit: int = 50) -> str:
    """Check how many of your blog posts have proper date markup. Scans your sitemap and reports which pages are missing freshness signals that AI assistants look for."""
    client = _get_client()
    return _call(client.freshness_audit, sitemap_url, limit=limit)


# ── Credits ──────────────────────────────────────────────────────────


@mcp.tool(annotations=READ_ONLY)
def get_credits() -> str:
    """Check how many credits you have left. Shows your plan, usage, and remaining balance."""
    client = _get_client()
    return _call(client.get_credits)


# ── Diagnostics ─────────────────────────────────────────────────────


@mcp.tool(annotations=READ_ONLY)
def check_connection() -> str:
    """Check if the Stobo API is reachable. Use this to diagnose connection issues before running audits."""
    import importlib.metadata

    import httpx
    from packaging.version import Version

    base_url = os.environ.get("STOBO_BASE_URL", "https://api.trystobo.com")
    api_key = os.environ.get("STOBO_API_KEY", "")
    result = {
        "base_url": base_url,
        "has_api_key": bool(api_key),
    }

    try:
        resp = httpx.get(f"{base_url}/api/v1/health", timeout=10)
        result["status"] = "ok" if resp.status_code == 200 else "error"
        result["http_code"] = resp.status_code

        # Check for MCP version upgrade
        if resp.status_code == 200:
            try:
                body = resp.json()
                installed = importlib.metadata.version("stobo-mcp")
                latest = body.get("latest_mcp_version")
                if latest and Version(installed) < Version(latest):
                    result["update_available"] = {
                        "installed": installed,
                        "latest": latest,
                        "upgrade": "pip install --upgrade stobo-mcp",
                        "changelog": body.get("changelog_url", ""),
                    }
            except Exception:
                pass
    except httpx.ConnectError as e:
        result["status"] = "connection_refused"
        result["error"] = str(e)
        result["fix"] = (
            "The API server is unreachable. Check your network or try again later."
        )
    except httpx.TimeoutException:
        result["status"] = "timeout"
        result["error"] = "Request timed out after 10 seconds"
        result["fix"] = "The API server is slow or unreachable. Check your network."
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return json.dumps(result, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
