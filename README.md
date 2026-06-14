# pmcontrols-mcp

[![CI](https://github.com/arikanatakan/pmcontrols-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/arikanatakan/pmcontrols-mcp/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/github/license/arikanatakan/pmcontrols-mcp)](LICENSE)

An MCP server that exposes [pmcontrols](https://github.com/arikanatakan/pmcontrols),
the validated project scheduling and earned value library, as tools for AI
agents.

Agents asked to plan a project or report its status tend to generate the
arithmetic themselves: a backward pass done by eye, an earned-value index
inverted, an earned schedule confused with schedule variance. Generated
project metrics fail silently. This server routes the work through a
validated, versioned library instead, so the agent picks the analysis and
explains the verdict while checked code does the math.

## Tools

| Tool | What it does |
| ---- | ------------ |
| `critical_path` | CPM forward/backward pass: ES, EF, LS, LF, slack, critical path |
| `schedule_risk` | PERT three-point analysis with Monte Carlo completion distribution and criticality indices |
| `crash_schedule` | minimum-cost schedule compression to a deadline (linear program) |
| `earned_value` | full EVM indicator set plus Lipke earned schedule against a planned-value baseline |
| `earned_schedule` | the earned schedule ES for a given earned value |

Every tool returns the same structured payload as the library: named
statistics, a tidy table, structured alerts, and provenance (library
version, input hash, timestamp).

## Install

```
pip install pmcontrols-mcp
```

## Use with Claude Desktop

Add the server to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pmcontrols": {
      "command": "pmcontrols-mcp"
    }
  }
}
```

Restart Claude Desktop and the five tools appear. The same command works
with any MCP client; the server speaks MCP over stdio.

## Why

See [Project control is not a language task](https://arikanatakan.github.io/pmcontrols/agents/),
the design note behind pmcontrols: the agent interprets, validated code
calculates.

## License

MIT. Written and maintained by [Atakan Arikan](https://github.com/arikanatakan),
MSc Student at Tsinghua University and Politecnico di Milano.
