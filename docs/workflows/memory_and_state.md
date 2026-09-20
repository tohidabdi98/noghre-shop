# Persistent memory and state

The framework must survive: agent sessions ending, agents being replaced, model changes, weeks of
development, and changes of mind. Therefore **nothing important lives only in a conversation.**

## 1. Where knowledge belongs

| Kind of knowledge | Home | Why there |
|---|---|---|
| Product intent and agreed behaviour | `docs/project/requirements.md` (+ `requirements.yaml` index) | reviewed, versioned, citable by ID |
| Why a choice was made | `docs/project/decisions.md` (`DEC`/`ADR`) | prevents relitigating decisions; shows reversibility |
| Design intent for the UI | `docs/ux/*` | persistent UX memory the human can revisit |
| System structure and interfaces | `docs/project/architecture.md` | the contract between modules |
| Task definition and ownership | `modules/<MODULE-ID>.md` | one source of truth per module |
| **Live status** (what is happening now) | `state/*.yaml` | machine-readable, script-validated, small diffs |
| History of what actually happened | **Git** (commits, branches, diffs, tags) | immutable, cheap, standard, survives everything |
| Review/validation evidence | `reports/`, PR bodies, CI runs | auditable claims; who proved what, when |
| Agent-to-agent continuity | `handoffs/` | replacement without reconstruction |
| Role rules and permissions | `docs/agents/agent_registry.yaml` + `agents/*/STARTER_PROMPT.md` | stable across sessions and providers |
| Configuration/credentials | environment + secret manager (never Git) | security (`security.md`) |
| Ephemeral session state | context packs in `state/.cache/` (gitignored) | regenerable, not worth versioning |
| Conversation | nowhere | it is a means, not a record |

## 2. The state files

| File | Owns | Updated by |
|---|---|---|
| `state/project.yaml` | project id/name, `initialised`, profile, stage, milestone, version, spec status, gates, shared zones | orchestrator + human (gates) |
| `state/modules.yaml` | per-module runtime status, assigned agent, branch, PR, validation result | `tp.py start/handoff`, orchestrator, agents at clear transitions |
| `state/agents.yaml` | agent instances: role, module, branch, status, task, authority, history | `tp.py start/handoff`, orchestrator |
| `state/dependencies.yaml` | dependency edges: `from` **depends on** `to`, type, interface, freeze status | decomposition; re-frozen by architecture/integration |

Rules

1. **Small and inspectable.** YAML, comments allowed, no prose essays.
2. **Validated.** `python scripts/tp.py validate` checks schema, IDs, references, cycles.
3. **Git-friendly.** One line per status change; no generated noise; no timestamps in bulk.
4. **Never a source of truth for *meaning*.** A status field says *where* work is, never *what* the
   behaviour should be.
5. **No duplication.** Ownership lives in the contract; status lives here (`docs/README.md` rule 3).

## 3. Session protocol (how an agent starts and ends)

**Start**
1. Read `AGENTS.md` → role prompt → context pack (`tp.py context`).
2. Check `state/*` for the current truth, including blockers affecting your module.
3. Confirm your branch and that your module state matches the task.

**During**
4. Commit early and often with conventional messages and trailers — commits are your durable memory.
5. Write decisions/questions into the documents as they arise, not at the end.

**End** (even if the work is unfinished or failed)
6. Update the module status honestly (`awaiting_review`, `blocked`, `failed`, `in_progress`).
7. Write the report (`reports/…`) — including failures.
8. If you are handing off, write the handoff (`handoffs/…`) with the "warnings" section filled.
9. Commit the documentation changes in the same branch so the next session starts from truth.

## 4. Continuity scenarios

| Scenario | What carries the project |
|---|---|
| New session, same agent | documents + state + branch (+ a regenerated context pack) |
| Agent replaced | handoff record + branch history + module contract |
| Model/provider changed | documents; the framework assumes no model-specific memory |
| Human returns after two weeks | `docs/project/project_state.md` + `tp.py status` |
| Decomposition revised | contracts + ADR + change request, all in Git |
| Repository moved/renamed | everything is relative and provider-agnostic |

## 5. Anti-patterns

| Anti-pattern | Failure it causes |
|---|---|
| "The agent remembers" | replacement loses weeks of context |
| Status only in a chat thread | nobody can plan the next wave |
| Requirements in an issue tracker only | agents cannot read them; IDs cannot be referenced |
| State duplicated in a spreadsheet | two truths, drift, stale planning |
| Huge state files with prose | merge conflicts and unreadable diffs |
| Reports skipped when work fails | the next agent repeats the same failure |
