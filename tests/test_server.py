"""Verify MCP tools are registered correctly."""

import json

from stobo_mcp.server import _trim_site_audit, mcp


def test_tool_count():
    """All 12 tools should be registered."""
    tools = mcp._tool_manager._tools
    assert len(tools) == 12, f"Expected 12 tools, got {len(tools)}: {list(tools.keys())}"


def test_required_tools_present():
    """Core tools must exist."""
    tools = mcp._tool_manager._tools
    names = set(tools.keys())
    expected = {
        "audit_site",
        "audit_article",
        "generate_llms_txt",
        "generate_robots_txt",
        "generate_sitemap",
        "generate_freshness_code",
        "generate_fix_brief",
        "rewrite_article",
        "extract_tone",
        "audit_freshness",
        "get_credits",
        "check_connection",
    }
    missing = expected - names
    assert not missing, f"Missing tools: {missing}"


def test_no_extra_tools():
    """No unexpected tools registered."""
    tools = mcp._tool_manager._tools
    names = set(tools.keys())
    expected = {
        "audit_site",
        "audit_article",
        "generate_llms_txt",
        "generate_robots_txt",
        "generate_sitemap",
        "generate_freshness_code",
        "generate_fix_brief",
        "rewrite_article",
        "extract_tone",
        "audit_freshness",
        "get_credits",
        "check_connection",
    }
    extra = names - expected
    assert not extra, f"Unexpected tools: {extra}"


# ── _trim_site_audit tests ──────────────────────────────────────────


_FAKE_AUDIT = {
    "url": "https://example.com",
    "domain": "example.com",
    "cached": True,
    "combined_percentage": 72,
    "pages_analyzed": 5,
    "page_results": [{"url": "https://example.com", "html": "<html>..." * 1000}],
    "business_context": {"industry": "tech", "description": "A company"},
    "seo_audit": {
        "id": "abc-123",
        "grade": "B",
        "overall_score": 280,
        "total_points": 280,
        "max_points": 380,
        "category_scores": {"content": 80, "links": 50},
        "checks": {str(i): {"status": "pass", "details": "x" * 500} for i in range(30)},
        "recommendations": [
            {"check": f"check_{i}", "message": f"Fix {i}", "fix_type": "quick", "extra": "data"}
            for i in range(15)
        ],
    },
    "aeo_audit": {
        "score": 5,
        "max_points": 7,
        "percentage": 71,
        "checks": {
            "robots_ai": {"status": "pass", "score": 1, "max_points": 1, "message": "OK", "details": {"raw": "long"}},
            "llms_txt": {"status": "fail", "score": 0, "max_points": 1, "message": "Missing", "details": {"raw": "long"}},
        },
    },
    "eeat_audit": {
        "grade": "B",
        "composite_percentage": 65,
        "checks": {"authority": {"score": 3, "details": "lots of data"}},
    },
    "blog_detection": {"has_blog": True, "blog_url": "/blog"},
    "sitemap_discovery": {
        "total_urls": 120,
        "blog_article_count": 30,
        "categories": [
            {"name": "Blog", "slug": "blog", "count": 30, "urls": [f"https://example.com/blog/{i}" for i in range(30)]},
        ],
    },
    "seo_error": None,
    "aeo_error": None,
    "eeat_error": None,
}


def test_trim_site_audit():
    """Trimmed result keeps critical fields, strips heavy ones, stays under 8KB."""
    trimmed = _trim_site_audit(_FAKE_AUDIT)

    # Critical fields preserved
    assert trimmed["domain"] == "example.com"
    assert trimmed["combined_percentage"] == 72
    assert trimmed["seo_audit"]["id"] == "abc-123"
    assert trimmed["seo_audit"]["grade"] == "B"
    assert trimmed["seo_audit"]["category_scores"] == {"content": 80, "links": 50}
    assert trimmed["aeo_audit"]["percentage"] == 71
    assert trimmed["aeo_audit"]["checks"]["robots_ai"]["status"] == "pass"
    assert trimmed["eeat_audit"]["grade"] == "B"
    assert trimmed["blog_detection"]["has_blog"] is True
    assert trimmed["sitemap_discovery"]["total_urls"] == 120

    # Heavy fields stripped
    assert "page_results" not in trimmed
    assert "business_context" not in trimmed
    assert "checks" not in trimmed["seo_audit"]  # raw checks removed
    assert "details" not in trimmed["aeo_audit"]["checks"]["robots_ai"]
    assert "checks" not in trimmed["eeat_audit"]

    # Recommendations capped at 10, only slim keys
    assert len(trimmed["seo_audit"]["recommendations"]) == 10
    assert "extra" not in trimmed["seo_audit"]["recommendations"][0]

    # Sitemap categories have no URL lists
    assert "urls" not in trimmed["sitemap_discovery"]["categories"][0]

    # Next step hint
    assert "_next_step" in trimmed
    assert "abc-123" in trimmed["_next_step"]
    assert "fix brief" in trimmed["_next_step"]

    # Size check
    size = len(json.dumps(trimmed))
    assert size < 8192, f"Trimmed response is {size} bytes, expected < 8KB"


def test_trim_site_audit_handles_none():
    """Null/missing sections don't crash."""
    data = {
        "url": "https://example.com",
        "domain": "example.com",
        "seo_audit": None,
        "aeo_audit": None,
        "eeat_audit": None,
        "sitemap_discovery": None,
    }
    trimmed = _trim_site_audit(data)
    assert trimmed["domain"] == "example.com"
    assert "seo_audit" not in trimmed
    assert "aeo_audit" not in trimmed


def test_trim_site_audit_empty_recommendations():
    """Empty recommendations list handled gracefully."""
    data = {
        "domain": "example.com",
        "seo_audit": {
            "id": "abc",
            "grade": "A",
            "overall_score": 350,
            "max_points": 380,
            "recommendations": [],
        },
    }
    trimmed = _trim_site_audit(data)
    assert trimmed["seo_audit"]["recommendations"] == []
