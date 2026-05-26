"""EOL: the retired MCP server exposes only a single status tool."""

from stobo_mcp.server import mcp, stobo_status


def test_only_status_tool():
    """After retirement, stobo_status is the sole registered tool."""
    tools = mcp._tool_manager._tools
    assert set(tools.keys()) == {"stobo_status"}, f"Unexpected tools: {list(tools.keys())}"


def test_status_reports_retirement():
    """The status tool reports that Stobo has been retired."""
    msg = stobo_status()
    assert "retired" in msg.lower()
    assert "no longer" in msg.lower()
