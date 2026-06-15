"""The MCP server: registers the pmcontrols tools and runs over stdio.

All tools are pure, read-only computations, marked with annotations so a
client can present and auto-run them safely.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP, Image
from mcp.types import ToolAnnotations

from . import _tools

mcp = FastMCP("pmcontrols")


def _annotations(title: str, idempotent: bool = True) -> ToolAnnotations:
    return ToolAnnotations(
        title=title,
        readOnlyHint=True,
        idempotentHint=idempotent,
        openWorldHint=False,
    )


mcp.tool(annotations=_annotations("Critical path (CPM)"))(_tools.critical_path)
mcp.tool(
    annotations=_annotations("Schedule risk (PERT + Monte Carlo)", idempotent=False)
)(_tools.schedule_risk)
mcp.tool(annotations=_annotations("Schedule crashing (minimum-cost LP)"))(
    _tools.crash_schedule
)
mcp.tool(annotations=_annotations("Earned value status"))(_tools.earned_value)
mcp.tool(annotations=_annotations("Earned schedule"))(_tools.earned_schedule)


@mcp.tool(annotations=_annotations("Gantt chart (PNG)"))
def gantt_chart(activities: list[_tools.CpmActivity]) -> Image:
    """Render the critical-path schedule as a Gantt chart image (PNG).

    The critical path is highlighted and total float is shown, so the agent
    can present the schedule visually instead of describing it.
    """
    return Image(data=_tools.gantt_png(activities), format="png")


@mcp.tool(annotations=_annotations("Network diagram (PNG)"))
def network_chart(activities: list[_tools.CpmActivity]) -> Image:
    """Render the activity network with the critical path as a PNG image."""
    return Image(data=_tools.network_png(activities), format="png")


@mcp.tool(annotations=_annotations("Earned value S-curve (PNG)"))
def evm_chart(
    periods: list[float], pv: list[float], ev: float, ac: float, at: float
) -> Image:
    """Render the earned value S-curve (PV/EV/AC + forecast) as a PNG image."""
    return Image(data=_tools.evm_png(periods, pv, ev, ac, at), format="png")


@mcp.tool(annotations=_annotations("Criticality chart (PNG)"))
def criticality_chart(activities: list[_tools.PertActivity]) -> Image:
    """Render the Monte Carlo per-activity criticality bars as a PNG image."""
    return Image(data=_tools.criticality_png(activities), format="png")


@mcp.tool(annotations=_annotations("Completion distribution (PNG)"))
def completion_histogram(activities: list[_tools.PertActivity]) -> Image:
    """Render the Monte Carlo completion-time histogram as a PNG image."""
    return Image(data=_tools.histogram_png(activities), format="png")


def main() -> None:
    """Console-script entry point: run the server on stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
