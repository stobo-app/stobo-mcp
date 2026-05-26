"""Stobo MCP Server — retired. The Stobo SEO/AEO audit service has been shut down."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

_RETIRED_MESSAGE = (
    "Stobo has been retired. The Stobo SEO/AEO audit service was shut down in May 2026 "
    "and its API is no longer available. This MCP server no longer performs audits. "
    "Thank you to everyone who used it."
)

mcp = FastMCP(
    "Stobo (retired)",
    instructions=_RETIRED_MESSAGE,
)


@mcp.tool()
def stobo_status() -> str:
    """Stobo has been retired and no longer performs SEO/AEO audits."""
    return _RETIRED_MESSAGE


def main():
    mcp.run()


if __name__ == "__main__":
    main()
