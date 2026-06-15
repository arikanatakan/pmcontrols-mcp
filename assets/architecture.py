"""Generate the pmcontrols-mcp architecture figure (academic style).

How an AI agent calls the server, which routes to the validated core and
returns structured results or images.

Run:  python assets/architecture.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5})

INK = "#1f2d3d"
MUT = "#5b6b7b"
NEUT_F, NEUT_E = "#eef1f4", "#9aa7b3"
CORE_F, CORE_E = "#dce8f5", "#2c5f8a"
ANA_F, ANA_E = "#eef3f8", "#3b6ea5"
OPT_F, OPT_E = "#e3f1ec", "#3a8f78"
CONT_F, CONT_E = "#f7f9fb", "#c9d2db"
BAN_F, BAN_E = "#f5f7f9", "#cdd6df"
ARROW = "#7c8a99"

fig, ax = plt.subplots(figsize=(11.5, 6.2))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")


def box(x, y, w, h, text, fill, edge, dashed=False, fs=8.4, bold=False,
        tcol=INK, halign="center"):
    ax.add_patch(FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.35,rounding_size=1.4",
        linewidth=1.25, edgecolor=edge, facecolor=fill,
        linestyle="--" if dashed else "-", zorder=2))
    ax.text(x, y, text, ha=halign, va="center", color=tcol, fontsize=fs,
            fontweight="bold" if bold else "normal", zorder=5)


def arrow(x0, y0, x1, y1, color=ARROW, dashed=False, lw=1.2):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=1,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle="--" if dashed else "-",
                                shrinkA=1, shrinkB=1))


ax.text(3, 96, "pmcontrols-mcp", fontsize=13.5, fontweight="bold", color=INK,
        ha="left")
ax.text(3, 91, "validated project-control tools for AI agents", fontsize=9.5,
        color=MUT, ha="left", fontstyle="italic")

# agent
box(12, 62, 18, 22,
    "AI agent\n\nMCP client\n(Claude Desktop,\nClaude Code, ...)",
    NEUT_F, NEUT_E, fs=8.2)

# server container
ax.add_patch(FancyBboxPatch((27, 33), 44, 50,
             boxstyle="round,pad=0.4,rounding_size=1.6",
             linewidth=1.4, edgecolor=CONT_E, facecolor=CONT_F, zorder=0))
ax.text(49, 79, "pmcontrols-mcp server  (stdio)", ha="center", fontsize=9.5,
        color=MUT, fontweight="bold")
box(49, 65, 40, 16,
    "Analysis tools  (5)\ncritical_path · schedule_risk · crash_schedule\n"
    "earned_value · earned_schedule",
    ANA_F, ANA_E, fs=7.9)
box(49, 45, 40, 16,
    "Chart tools  (5)\ngantt_chart · network_chart · evm_chart\n"
    "criticality_chart · completion_histogram",
    OPT_F, OPT_E, fs=7.9)

# core
box(88, 58, 20, 26,
    "pmcontrols\n\nvalidated\ncomputation\n+ provenance",
    CORE_F, CORE_E, fs=8.6, bold=True)

# forward arrows
arrow(21.2, 62, 26.8, 62)
ax.text(24, 65.5, "call", ha="center", fontsize=7.6, color=MUT)
arrow(69.2, 65, 77.8, 60)
arrow(69.2, 45, 77.8, 56)
ax.text(74, 63.5, "calls", ha="center", fontsize=7.6, color=MUT)

# return lane
arrow(80, 19, 16, 19, color=OPT_E, lw=1.4)
ax.text(48, 22.5, "results to the agent:  structured JSON "
        "(stats · table · alerts · provenance)   or   PNG image",
        ha="center", fontsize=8.0, color="#2e7d6b")
# connectors into the return lane
arrow(88, 45, 88, 19, color=OPT_E, lw=1.2)
arrow(12, 19, 12, 51, color=OPT_E, lw=1.2)

# banner
box(50, 8, 94, 5,
    "the agent interprets   ·   validated code calculates   ·   every result "
    "carries provenance",
    BAN_F, BAN_E, fs=8.2, tcol=MUT)

fig.savefig("assets/architecture.png", dpi=200, bbox_inches="tight",
            facecolor="white")
print("wrote assets/architecture.png")
