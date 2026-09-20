# Agents — roles, contracts and how to run them

> The framework is provider-agnostic: a **role** is a scope of authority, inputs, outputs and
> escalation duties — not a vendor product. You can run a role by pasting its starter prompt into
> any capable coding agent (see `provider_adapters.md`), or by configuring provider-specific
> sub-agents/rules.

## Files

| File | Purpose |
|---|---|
| `agent_registry.yaml` | **the authority**: mission, inputs, outputs, authority, allowed/forbidden actions, scope, escalation conditions and completion criteria per role |
| `provider_adapters.md` | how to instantiate roles in different coding-agent providers, and how to configure agent identity |
| `templates/agent_contract.md` | the shape of a role contract (for adding new roles) |
| `templates/agent_instance.yaml` | the shape of a role *instance* record (`state/agents.yaml`) |
| `templates/handoff.md` | agent-to-agent handoff record |
| `templates/validation_report.md` | validation report (testing, review, integration, UX) |
| `templates/failure_report.md` | failure/root-cause report |
| `agents/<role>/STARTER_PROMPT.md` | the copy-paste prompt for each role |

## Role taxonomy

| Category | Purpose | Roles | Typical interaction |
|---|---|---|---|
| conversational | turns human intent into specification | discovery, frontend-ux | long dialogues, several sessions, revisitable |
| analytical | turns specification into structure | architecture, decomposition | few, high-leverage sessions with human gates |
| coordination | keeps work flowing | orchestration | periodic, state-driven, short sessions |
| implementation | writes product code and tests | implementation, debugging | one module per session, branch-based |
| validation | proves the work meets the specification | testing, review, integration | per PR / per milestone |

## Roles are not processes

Ten roles do **not** mean ten agents must exist simultaneously.

| Project size | Reasonable setup |
|---|---|
| Tiny (one weekend project) | 2–3 sessions: `discovery+frontend-ux`, `architecture+decomposition`, `implementation+debugging`; validation by the human with the Testing prompt |
| Small | 4–5: separate architecture, separate review, implementation per module |
| Medium / parallel | full roster; orchestration earns its keep once ≥ 3 modules run concurrently |
| Large / long-lived | full roster plus dedicated review and integration agents per milestone |

Rules that always hold:

1. **The validator is never the author** for the final verdict (a module's implementation agent may
   self-review, but review/testing verdicts must come from another instance — see `combinations.forbidden`).
2. **The orchestrator never implements** — it must stay able to see the whole board.
3. **The Frontend/UX role stays available for the project's life** instead of being a one-time phase.
4. **One module, one implementation agent** at a time, always.
5. Combining roles is allowed only per `combinations.allowed` in the registry; combining means one
   context holding two scopes, which is acceptable for a small project and dangerous at scale.

## Identity

Every agent instance has an ID, a role, a module, a branch and a status, recorded in
`state/agents.yaml`:

```yaml
agent_id: impl-auth-001
role: implementation
module_id: AUTH-001
branch: agent/impl-auth-001/AUTH-001
status: active
```

ID pattern: `<role-prefix>-<slug>-<sequence>` — `impl-auth-001`, `ux-002`, `rev-dash-001`.
Prefixes are listed per role in `agent_registry.yaml` (`agent_id_pattern`).

Identity must be visible in: commit trailers (`Agent:`, `Agent-Role:`), PR title and body, the
agent registry and project state. If your provider supports distinct bot identities, configure them
per `provider_adapters.md`; otherwise the trailers are the identity mechanism and they are not
optional.

## Context discipline (why prompts are short)

Agents receive **layered context**, not the repository:

```bash
python scripts/tp.py context --module AUTH-001 --agent impl-auth-001
```

Layers: 1 project identity · 2 relevant requirements · 3 relevant architecture · 4 the module
contract · 5 neighbouring interface contracts · 6 conventions · 7 current task/state ·
8 validation requirements. Details and the "when you need more" discovery path:
`docs/workflows/context_engineering.md`.

## Adding a role

1. Copy `templates/agent_contract.md` into a new entry in `agent_registry.yaml`.
2. Create `agents/<role>/STARTER_PROMPT.md` following the structure of an existing prompt.
3. Add the role to `AGENTS.md` §3 and to the table in `README.md`.
4. Run `python scripts/tp.py validate` — it checks that every registry entry has a prompt and that
   every prompt belongs to a registry entry.
5. Add the role name to the notebook's prompt section (`python scripts/tp.py sync-notebook`).
