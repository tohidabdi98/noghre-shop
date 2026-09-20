# Context engineering

Agent quality is mostly context quality: the right information, in the right amount, at the right
time. This file defines the layers, how they are assembled, and what must **never** be dumped into
an agent's context.

## 1. The eight layers

| Layer | Content | Source | Why it is included |
|---|---|---|---|
| 1 — Project identity | project id, name, stage, profile, gates, default branch | `state/project.yaml` + `AGENTS.md` rules | so the agent knows what project it is in and what rules bind it |
| 2 — Relevant requirements | only the requirements this module cites | `docs/project/requirements.md` sections whose heading contains the module's `requirement_refs` | product truth, without unrelated features |
| 3 — Relevant architecture | the interfaces and decisions this module touches | `docs/project/architecture.md` sections + the `ADR-###` it cites | constraints and interface shapes |
| 4 — Module contract | the whole contract | `modules/<MODULE-ID>.md` | the agent's task definition, ownership and criteria |
| 5 — Neighbouring interface contracts | only the interface blocks of the modules it depends on / blocks | their contract YAML `interfaces` | integration without cross-module context bloat |
| 6 — Conventions | how code and docs are written here | `docs/project/conventions.md`, `docs/workflows/git_workflow.md`, `docs/project/definition_of_done.md` | consistency and process compliance |
| 7 — Current task & state | module status, agent identity, branch, blockers, open questions that affect it | `state/modules.yaml`, `state/agents.yaml`, `docs/project/open_questions.md` | situational awareness, no re-doing finished work |
| 8 — Validation requirements | the commands and criteria that prove completion | contract `validation`/`acceptance_criteria` + `scripts/verify.config.yaml` | evidence, not opinion |
| ↳ plus | the UX slice, **only** if the contract has `ux_refs` | `docs/ux/*` sections containing those IDs | UI detail without the whole UX spec |

Assemble all of it in one command:

```bash
python scripts/tp.py context --module AUTH-001 --agent impl-auth-001          # markdown pack
python scripts/tp.py context --module AUTH-001 --format json --out state/.cache/context/AUTH-001.json
```

## 2. Rules

1. **Never paste the whole repository.** If a layer is too large, the extraction is wrong — fix the
   IDs and headings, not the agent.
2. **Extraction is by ID.** Requirement headings must contain their IDs; UX headings likewise. This
   is what makes narrow context possible.
3. **One pack per session, regenerated after any change.** A stale pack is worse than no pack:
   `tp.py context` is cheap, re-derive it.
4. **Conversation is not context.** Anything the agent must know lives in a file. If you explain
   something in chat that matters, write it down first.
5. **Bounded packs.** If a pack exceeds roughly 4,000–6,000 lines, the module is too big or the
   requirements are not properly ID-linked — treat as a decomposition smell.
6. **The agent must know how to discover more.** Every pack ends with the discovery index (§4) so
   the agent can fetch a specific extra file instead of guessing.

## 3. Choosing the right context by role

| Role | Primary layers | Explicitly excluded |
|---|---|---|
| discovery | 1, 2 + the registers | architecture, module contracts, code |
| frontend-ux | 1, 2, UX files, 6 | module implementation details |
| architecture | 1, 2, UX spec, 6, existing architecture | module-level implementation history |
| decomposition | 1, 2, 3, 6, `docs/modules/*` | code, PRs |
| orchestration | 1, 4 (summaries), 7, state, reports | full contracts, code |
| implementation | 1–8 (+ UX slice) | other modules' internals, other PRs, requirement sections it does not cite |
| testing | 1, 2, 4, 6, 8, the PR | unrelated modules |
| review | 1, 2, 3, 4, 6, 8, the diff | unrelated modules |
| integration | 1, 3, 5, UX flows, 8 | module internals |
| debugging | 1, 4 (owning module), 6, 7, 8, failure report, recent Git history for the paths | everything else |

## 4. Discovery index (what an agent should read when it needs more)

| Need | Read |
|---|---|
| "What exactly must this do?" | `docs/project/requirements.md` § the cited IDs |
| "How must this behave visually?" | `docs/ux/` the cited `UX-###` |
| "Why is it built this way?" | `docs/project/decisions.md` (tail) + the ADR cited |
| "What did the other side promise?" | `modules/<OTHER-ID>.md` `interfaces:` |
| "Am I allowed to touch this file?" | own contract `allowed_to_modify` / `forbidden_to_modify` |
| "How do I write/commit this?" | `docs/project/conventions.md`, `docs/workflows/git_workflow.md` |
| "When is it done?" | contract criteria + `docs/project/definition_of_done.md` |
| "What is already known to be wrong?" | `docs/project/open_questions.md`, `docs/project/risks.md`, `reports/` |
| "Has this been tried before?" | `handoffs/`, `git log -- <path>` |

## 5. Anti-patterns

| Anti-pattern | Effect |
|---|---|
| Dumping the entire `docs/` tree | the agent loses the signal; instructions get diluted |
| Pasting an old context pack after a change | the agent implements superseded behaviour |
| Relying on the previous chat session's memory | breaks on agent replacement; the repository is the memory |
| Summarising the contract in chat instead of reading it | details (criteria, ownership) get lost |
| Letting the agent explore the repo freely to find context | wasted budget, inconsistent reads — give it the pack |
| Including other modules' internals "just in case" | tempts cross-module edits and copies internal assumptions |
