"""Tool functions and their input schemas, kept free of the MCP SDK so they
can be tested directly.

Each activity type is a typed model, so the server advertises exactly which
fields an agent must supply. Each tool calls pmcontrols and returns the
analysis as a JSON-safe dict (``Result.to_dict()``) with stats, a tidy
table, structured alerts, and provenance.
"""

from __future__ import annotations

import pmcontrols as pm
from pydantic import BaseModel, Field


class CpmActivity(BaseModel):
    """One activity in a deterministic schedule network."""

    id: str = Field(description="Unique activity identifier.")
    predecessors: list[str] = Field(
        default_factory=list,
        description="Ids of the immediate predecessor activities; empty to start.",
    )
    duration: float = Field(description="Activity duration in consistent time units.")


class PertActivity(BaseModel):
    """One activity with a three-point (optimistic/likely/pessimistic) estimate."""

    id: str = Field(description="Unique activity identifier.")
    predecessors: list[str] = Field(
        default_factory=list,
        description="Ids of the immediate predecessor activities; empty to start.",
    )
    a: float = Field(description="Optimistic duration.")
    m: float = Field(description="Most likely duration.")
    b: float = Field(description="Pessimistic duration.")


class CrashActivity(BaseModel):
    """One activity with normal and fully-crashed durations and a crash cost."""

    id: str = Field(description="Unique activity identifier.")
    predecessors: list[str] = Field(
        default_factory=list,
        description="Ids of the immediate predecessor activities; empty to start.",
    )
    duration: float = Field(description="Normal duration.")
    crash_duration: float = Field(description="Fully-crashed (minimum) duration.")
    crash_cost: float = Field(description="Crash cost per period of compression.")


def _as_dicts(items: list) -> list[dict]:
    """Accept either pydantic models (from the MCP layer) or plain dicts."""
    return [i if isinstance(i, dict) else i.model_dump() for i in items]


def critical_path(activities: list[CpmActivity]) -> dict:
    """Critical path analysis (CPM) of an activity-on-node network.

    Runs the forward and backward pass and returns earliest/latest start and
    finish, total slack, and the zero-float critical path.
    """
    return pm.cpm(_as_dicts(activities)).to_dict()


def schedule_risk(
    activities: list[PertActivity],
    n_sim: int = 20000,
    seed: int | None = 0,
) -> dict:
    """PERT three-point analysis with a Monte Carlo schedule-risk simulation.

    Returns the analytic expected duration and standard deviation, the
    simulated completion distribution (p50/p80/p95), and a per-activity
    criticality index. Pass ``seed=null`` for a fresh random draw.
    """
    return pm.pert(_as_dicts(activities), n_sim=n_sim, seed=seed).to_dict()


def crash_schedule(activities: list[CrashActivity], target: float) -> dict:
    """Minimum-cost schedule compression to a target completion time.

    Returns the globally optimal crash amount per activity, the resulting
    schedule, and the total crash cost, solved as a linear program rather
    than by greedy marginal-cost crashing.
    """
    return pm.crash(_as_dicts(activities), target=target).to_dict()


def earned_value(
    periods: list[float],
    pv: list[float],
    ev: float,
    ac: float,
    at: float,
    thresholds: dict[str, float] | None = None,
) -> dict:
    """Earned value status against a time-phased planned-value baseline.

    ``periods`` and ``pv`` define the cumulative planned-value curve. Given
    earned value ``ev``, actual cost ``ac`` and actual time ``at``, returns
    the full indicator set (CV, SV, CPI, SPI, the EAC family, TCPI, VAC) plus
    Lipke's earned schedule (ES, SPI(t), IEAC(t)) and any threshold alerts.
    """
    pmb = pm.plan(periods, pv)
    return pm.evm(pmb, ev=ev, ac=ac, at=at, thresholds=thresholds).to_dict()


def earned_schedule(periods: list[float], pv: list[float], ev: float) -> dict:
    """Lipke earned schedule (ES) for a given earned value.

    ``periods`` and ``pv`` define the cumulative planned-value curve. Returns
    the time at which the plan had earned what has now been earned, by linear
    interpolation on the curve.
    """
    pmb = pm.plan(periods, pv)
    return {"es": pm.earned_schedule(pmb, ev)}


def _use_agg() -> None:
    """Select a headless matplotlib backend before any pyplot import."""
    import matplotlib

    matplotlib.use("Agg")


def _render_png(fig) -> bytes:
    import io

    import matplotlib.pyplot as plt

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    return buffer.getvalue()


def gantt_png(activities: list[CpmActivity]) -> bytes:
    """Render the critical-path schedule (CPM) as a Gantt chart PNG."""
    _use_agg()
    fig, _ = pm.gantt(pm.cpm(_as_dicts(activities)))
    return _render_png(fig)


def network_png(activities: list[CpmActivity]) -> bytes:
    """Render the activity network (critical path highlighted) as a PNG."""
    _use_agg()
    fig, _ = pm.network_diagram(pm.cpm(_as_dicts(activities)))
    return _render_png(fig)


def evm_png(
    periods: list[float], pv: list[float], ev: float, ac: float, at: float
) -> bytes:
    """Render the earned value S-curve (PV/EV/AC + forecast) as a PNG."""
    _use_agg()
    pmb = pm.plan(periods, pv)
    fig, _ = pm.evm_curve(pmb, pm.evm(pmb, ev=ev, ac=ac, at=at))
    return _render_png(fig)


def criticality_png(activities: list[PertActivity]) -> bytes:
    """Render the Monte Carlo criticality bars as a PNG."""
    _use_agg()
    fig, _ = pm.criticality(pm.pert(_as_dicts(activities)))
    return _render_png(fig)


def histogram_png(activities: list[PertActivity]) -> bytes:
    """Render the Monte Carlo completion-time histogram as a PNG."""
    _use_agg()
    fig, _ = pm.mc_distribution(pm.pert(_as_dicts(activities), keep_samples=True))
    return _render_png(fig)
