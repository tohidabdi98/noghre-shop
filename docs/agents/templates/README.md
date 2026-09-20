# Agent artifact templates

| Template | Purpose | Written to |
|---|---|---|
| `agent_contract.md` | the shape of a role contract — copy into `docs/agents/agent_registry.yaml` when adding a role | `docs/agents/agent_registry.yaml` |
| `agent_instance.yaml` | the shape of a role instance record | `state/agents.yaml` |
| `handoff.md` | transfer of work between agents (including replacing a failed agent) | `handoffs/<date>-<from>-to-<to>-<MODULE-ID>.md` |
| `validation_report.md` | testing / review / integration / UX-validation evidence | `reports/validation-<MODULE-ID>-<date>.md` |
| `failure_report.md` | root cause + smallest fix + blast radius | `reports/failure-<MODULE-ID>-<date>.md` |

Rules

- One artifact per file, one purpose per artifact, always dated and attributed to an `agent-id`.
- Evidence means a command and its result, a test name, or a screenshot path — never a claim.
- Reports are written even when the outcome is bad, especially then. An unwritten failure is an
  invisible failure, and invisible failures are how parallel agent work goes wrong.
- Handoffs and reports are committed to Git so they survive agent replacement
  (`docs/workflows/failure_recovery.md`).
