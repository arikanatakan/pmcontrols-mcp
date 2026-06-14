# Changelog

## 0.1.0

First public release.

### Added

* MCP server (stdio) exposing pmcontrols as five tools: `critical_path`,
  `schedule_risk`, `crash_schedule`, `earned_value`, and `earned_schedule`.
* `pmcontrols-mcp` console-script entry point.
* Each tool returns the library's JSON-safe `Result` payload with stats,
  table, alerts, and provenance.
