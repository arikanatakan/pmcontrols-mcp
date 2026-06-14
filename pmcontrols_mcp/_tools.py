"""Tool functions, kept free of the MCP SDK so they can be tested directly.

Each function takes plain JSON-friendly arguments, calls pmcontrols, and
returns the analysis as a JSON-safe dict (``Result.to_dict()``), which
carries stats, a tidy table, structured alerts, and provenance.
"""

from __future__ import annotations

import pmcontrols as pm


def critical_path(activities: list[dict], duration: str = "duration") -> dict:
    """Critical path analysis (CPM) of an activity-on-node network.

    Each activity is a mapping with ``id``, ``predecessors`` (a list of ids
    or a comma-separated string), and a duration field. Returns the
    earliest/latest start and finish, total slack, and the zero-float
    critical path.
    """
    return pm.cpm(activities, duration=duration).to_dict()


def schedule_risk(
    activities: list[dict],
    optimistic: str = "a",
    most_likely: str = "m",
    pessimistic: str = "b",
    n_sim: int = 20000,
    seed: int | None = 0,
) -> dict:
    """PERT three-point analysis with a Monte Carlo schedule-risk simulation.

    Each activity carries optimistic/most-likely/pessimistic estimates.
    Returns the analytic expected duration and standard deviation, the
    simulated completion distribution (p50/p80/p95), and a per-activity
    criticality index.
    """
    return pm.pert(
        activities,
        optimistic=optimistic,
        most_likely=most_likely,
        pessimistic=pessimistic,
        n_sim=n_sim,
        seed=seed,
    ).to_dict()


def crash_schedule(
    activities: list[dict],
    target: float,
    duration: str = "duration",
    crash_duration: str = "crash_duration",
    cost_per_period: str = "crash_cost",
) -> dict:
    """Minimum-cost schedule compression to a target completion time.

    Each activity needs a normal duration, a fully-crashed duration, and a
    linear crash cost per period. Returns the globally optimal crash amounts,
    the resulting schedule, and the total crash cost (solved as a linear
    program, not by greedy marginal-cost crashing).
    """
    return pm.crash(
        activities,
        target=target,
        duration=duration,
        crash_duration=crash_duration,
        cost_per_period=cost_per_period,
    ).to_dict()


def earned_value(
    periods: list[float],
    pv: list[float],
    ev: float,
    ac: float,
    at: float,
    thresholds: dict | None = None,
) -> dict:
    """Earned value status against a time-phased planned-value baseline.

    ``periods`` and ``pv`` define the cumulative planned-value curve (the
    Performance Measurement Baseline). Given earned value ``ev``, actual cost
    ``ac`` and actual time ``at``, returns the full indicator set (CV, SV,
    CPI, SPI, the EAC family, TCPI, VAC) plus Lipke's earned schedule (ES,
    SPI(t), IEAC(t)) and any threshold alerts.
    """
    pmb = pm.plan(periods, pv)
    return pm.evm(pmb, ev=ev, ac=ac, at=at, thresholds=thresholds).to_dict()


def earned_schedule(periods: list[float], pv: list[float], ev: float) -> dict:
    """Lipke earned schedule ES for a given earned value.

    ``periods`` and ``pv`` define the cumulative planned-value curve. Returns
    the time at which the plan had earned what has now been earned, by linear
    interpolation on the curve.
    """
    pmb = pm.plan(periods, pv)
    return {"es": pm.earned_schedule(pmb, ev)}
