"""Tests for the tool functions (no MCP client needed).

The numbers are the General Foundry network and a linear PMB, the same
reference cases pmcontrols itself validates against.
"""

import pmcontrols_mcp._tools as t

FOUNDRY = [
    {"id": "A", "predecessors": [], "duration": 2},
    {"id": "B", "predecessors": [], "duration": 3},
    {"id": "C", "predecessors": ["A"], "duration": 2},
    {"id": "D", "predecessors": ["B"], "duration": 4},
    {"id": "E", "predecessors": ["C"], "duration": 4},
    {"id": "F", "predecessors": ["C"], "duration": 3},
    {"id": "G", "predecessors": ["D", "E"], "duration": 5},
    {"id": "H", "predecessors": ["F", "G"], "duration": 2},
]

CRASH = [
    {"id": "A", "predecessors": [], "duration": 2, "crash_duration": 1, "crash_cost": 1000},
    {"id": "B", "predecessors": [], "duration": 3, "crash_duration": 1, "crash_cost": 2000},
    {"id": "C", "predecessors": ["A"], "duration": 2, "crash_duration": 1, "crash_cost": 1000},
    {"id": "D", "predecessors": ["B"], "duration": 4, "crash_duration": 3, "crash_cost": 1000},
    {"id": "E", "predecessors": ["C"], "duration": 4, "crash_duration": 2, "crash_cost": 1000},
    {"id": "F", "predecessors": ["C"], "duration": 3, "crash_duration": 2, "crash_cost": 500},
    {"id": "G", "predecessors": ["D", "E"], "duration": 5, "crash_duration": 2, "crash_cost": 2000},
    {"id": "H", "predecessors": ["F", "G"], "duration": 2, "crash_duration": 1, "crash_cost": 3000},
]

PERIODS = list(range(11))
PV = [i * 10000 for i in PERIODS]


def test_critical_path():
    d = t.critical_path(FOUNDRY)
    assert d["method"] == "cpm"
    assert d["stats"]["project_duration"] == 15.0
    assert d["meta"]["critical_activities"] == ["A", "C", "E", "G", "H"]


def test_schedule_risk():
    tp = [
        {"id": a["id"], "predecessors": a["predecessors"],
         "a": a["duration"] * 0.8, "m": a["duration"], "b": a["duration"] * 1.3}
        for a in FOUNDRY
    ]
    d = t.schedule_risk(tp, n_sim=2000, seed=1)
    assert d["method"] == "pert"
    assert "mc_p80" in d["stats"]
    assert "criticality_index" in d["table"]


def test_crash_schedule():
    d = t.crash_schedule(CRASH, target=13)
    assert d["method"] == "crash"
    assert d["stats"]["total_crash_cost"] == 3000.0


def test_earned_value():
    d = t.earned_value(PERIODS, PV, ev=30000, ac=35000, at=4)
    assert d["method"] == "evm"
    assert round(d["stats"]["cpi"], 4) == 0.8571
    assert {a["indicator"] for a in d["alerts"]} == {"cpi", "spi_t"}


def test_earned_schedule():
    d = t.earned_schedule(PERIODS, PV, ev=34000)
    assert d["es"] == 3.4


def _png_ok(data):
    return isinstance(data, (bytes, bytearray)) and data[:8] == b"\x89PNG\r\n\x1a\n"


_THREE_POINT = [
    {"id": a["id"], "predecessors": a["predecessors"],
     "a": a["duration"] * 0.8, "m": a["duration"], "b": a["duration"] * 1.3}
    for a in FOUNDRY
]


def test_gantt_png_returns_png_bytes():
    assert _png_ok(t.gantt_png(FOUNDRY))


def test_network_png():
    assert _png_ok(t.network_png(FOUNDRY))


def test_evm_png():
    assert _png_ok(t.evm_png(PERIODS, PV, 30000, 35000, 4))


def test_criticality_png():
    assert _png_ok(t.criticality_png(_THREE_POINT))


def test_completion_histogram_png():
    assert _png_ok(t.histogram_png(_THREE_POINT))
