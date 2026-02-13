"""Verify MCP tools are registered correctly."""

from stobo_mcp.server import mcp


def test_tool_count():
    """All 11 tools should be registered."""
    tools = mcp._tool_manager._tools
    assert len(tools) == 11, f"Expected 11 tools, got {len(tools)}: {list(tools.keys())}"


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
        "rewrite_article",
        "extract_tone",
        "audit_freshness",
        "get_credits",
        "check_connection",
    }
    extra = names - expected
    assert not extra, f"Unexpected tools: {extra}"
