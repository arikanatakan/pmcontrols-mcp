def test_server_imports_and_wires():
    from pmcontrols_mcp import server

    assert server.mcp is not None
    assert callable(server.main)


def test_all_tools_registered():
    import asyncio

    from pmcontrols_mcp import server

    names = {tool.name for tool in asyncio.run(server.mcp.list_tools())}
    expected = {
        "critical_path", "schedule_risk", "crash_schedule", "earned_value",
        "earned_schedule", "gantt_chart", "network_chart", "evm_chart",
        "criticality_chart", "completion_histogram",
    }
    assert expected <= names
