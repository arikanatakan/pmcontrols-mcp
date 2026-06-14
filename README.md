# pmcontrols-mcp

[![CI](https://github.com/arikanatakan/pmcontrols-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/arikanatakan/pmcontrols-mcp/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/github/license/arikanatakan/pmcontrols-mcp)](LICENSE)

An MCP server that exposes [pmcontrols](https://github.com/arikanatakan/pmcontrols),
the validated project scheduling and earned value library for Python, as tools
for AI agents.

Agents asked to plan a project or report its status tend to generate the
arithmetic themselves: a backward pass done by eye, an earned-value index
inverted, an earned schedule mistaken for schedule variance. Generated project
metrics fail silently. The calculation belongs in a deterministic, versioned,
validated library that the agent calls, which leaves the agent to choose the
analysis and explain the result.

## Tools

| Tool | Purpose |
| ---- | ------- |
| `critical_path` | CPM forward and backward pass: ES, EF, LS, LF, slack, critical path |
| `schedule_risk` | PERT three-point analysis with a Monte Carlo completion distribution and criticality indices |
| `crash_schedule` | minimum-cost schedule compression to a deadline, solved as a linear program |
| `earned_value` | the full EVM indicator set with Lipke earned schedule, against a planned-value baseline |
| `earned_schedule` | the earned schedule for a given earned value |

Each tool returns the library's structured payload: named statistics, a tidy
table, structured alerts, and provenance (library version, input hash,
timestamp).

## Installation

```
pip install pmcontrols-mcp
```

## Configuration

Add the server to your MCP client's configuration:

```json
{
  "mcpServers": {
    "pmcontrols": {
      "command": "pmcontrols-mcp"
    }
  }
}
```

The server communicates over stdio and works with any MCP-compatible client.

## Design

The reasoning behind routing project-control arithmetic through a validated
tool, rather than letting a model generate it, is set out in
[Project control is not a language task](https://arikanatakan.github.io/pmcontrols/agents/).

## License

MIT. Written and maintained by [Atakan Arikan](https://github.com/arikanatakan),
MSc Student at Tsinghua University and Politecnico di Milano.
