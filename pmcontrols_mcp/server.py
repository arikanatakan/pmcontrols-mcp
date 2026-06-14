"""The MCP server: registers the pmcontrols tools and runs over stdio."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import _tools

mcp = FastMCP("pmcontrols")

mcp.tool()(_tools.critical_path)
mcp.tool()(_tools.schedule_risk)
mcp.tool()(_tools.crash_schedule)
mcp.tool()(_tools.earned_value)
mcp.tool()(_tools.earned_schedule)


def main() -> None:
    """Console-script entry point: run the server on stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
