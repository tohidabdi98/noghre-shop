# handoffs/ — agent-to-agent continuity

Every time work moves from one agent instance to another (replacement, rotation, a module handed to a
specialist), a handoff record is written **here** and committed. It is what makes an agent replaceable
without losing weeks of context.

## Naming

```
handoffs/<YYYY-MM-DD>-<from-agent-id>-to-<to-agent-id>-<MODULE-ID>.md
handoffs/2026-03-11-impl-dashboard-002-to-impl-dashboard-003-DASH-001.md
```

Generate the skeleton from real state rather than writing it by hand:

```bash
python scripts/tp.py handoff --module DASH-001 \
  --from impl-dashboard-002 --to impl-dashboard-003 \
  --reason "context exhausted mid-module"
```

That command also updates `state/agents.yaml` (old instance → `replaced`, new instance → `active` with
`parent_agent` set) and reopens the module if it was `failed`/`blocked`.

## Rules

1. **Write it before the new agent starts** — not as a post-mortem.
2. **Fill in the narrative sections** (state of the work, decisions, assumptions, known issues,
   warnings, remaining criteria). The skeleton's table is generated; the judgement is not.
3. **Section 6 (warnings) is the most valuable** — dead ends already explored, approaches that failed,
   environment quirks. Skipping it is how the next agent repeats the same failure.
4. **The receiving agent re-runs the claimed validation** and ticks the acknowledgement box. A failed
   agent's "tests pass" is a hypothesis, not evidence.
5. **Never delete a handoff** — it is part of the audit trail (`docs/workflows/failure_recovery.md`).
6. Template: `docs/agents/templates/handoff.md`. Example:
   `examples/example-saas/handoffs/2026-03-11-impl-dashboard-002-to-impl-dashboard-003-DASH-001.md`.
