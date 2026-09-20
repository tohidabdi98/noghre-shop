# Documentation map — which document is the source of truth for what

Agents break down when two documents disagree. This file is the contract that prevents it:
**every fact has exactly one home.** If you need a fact elsewhere, link to it — do not copy it.

Enforced by `python scripts/tp.py validate` (link check + contract completeness + prompt sync).

---

## Source-of-truth matrix

| Fact | Source of truth | Maintained by |
|---|---|---|
| What the product must do (behaviour) | `docs/project/requirements.md` | Discovery Agent (approved by human) |
| Requirement IDs, priority, status | `docs/project/requirements.yaml` (index only — no prose) | Discovery Agent |
| What the product must *feel* like, flows, screens, a11y | `docs/ux/*` | Frontend/UX Agent |
| How the system is built (components, data, interfaces, security) | `docs/project/architecture.md` | Architecture Agent |
| Why a significant technical choice was made | `docs/project/decisions.md` (`ADR-###`) | whoever made the decision, published by Architecture Agent |
| What we believe but have not confirmed | `docs/project/assumptions.md` (`ASM-###`) | all roles |
| What we still must decide | `docs/project/open_questions.md` (`OQ-###`) | all roles; resolved by human or owning role |
| What could go wrong | `docs/project/risks.md` (`RISK-###`) | all roles |
| How code is written here | `docs/project/conventions.md` | Architecture Agent (human approves additions to policy) |
| When work is "done" | `docs/project/definition_of_done.md` | Architecture Agent |
| Module boundaries, ownership, acceptance criteria | `modules/<MODULE-ID>.md` | Decomposition Agent; amended by change requests only |
| Module runtime state (status, agent, branch, PR, validation) | `state/modules.yaml` | `scripts/tp.py` + Orchestrator Agent |
| Project identity, stage, gates, milestones | `state/project.yaml` | Orchestrator Agent + human |
| Who is working on what | `state/agents.yaml` | `scripts/tp.py` (start/handoff) + Orchestrator Agent |
| Inter-module dependency edges | `state/dependencies.yaml` | Decomposition Agent |
| Role missions, scopes, escalation duties | `docs/agents/agent_registry.yaml` | template owner (human) |
| Agent process steps and outputs | `agents/<role>/STARTER_PROMPT.md` | template owner (human) |
| Provider-specific agent configuration | `docs/agents/provider_adapters.md` | human |
| Repository/PR/Git rules | `docs/workflows/git_workflow.md` | template owner (human) |
| What must be escalated to the human | `docs/workflows/human_in_the_loop.md` | human |
| Change process | `docs/workflows/change_management.md` | any role via a change request |
| Failure recovery procedures | `docs/workflows/failure_recovery.md` | any role |
| Agent permission and secret rules | `docs/workflows/security.md` | human |

## Representation rules

1. **Markdown owns narrative truth.** Rationale, decisions, criteria, process.
2. **YAML owns identity, state and edges.** IDs, statuses, assignments, dependency edges,
   gates — anything a script must read. YAML files contain no explanatory prose beyond short
   `notes`/`comment` fields.
3. **Never duplicate a fact across representations.** `modules/AUTH-001.md` owns ownership and
   acceptance criteria; `state/modules.yaml` owns only that module's current status. The
   requirement list lives in `requirements.md`; `requirements.yaml` holds IDs and links only.
4. **Supersede, never contradict.** When a fact changes, edit it in place and record the change
   in `docs/project/decisions.md` (or via a change request). Delete or explicitly mark stale
   statements — do not leave two versions in the tree.
5. **Tag every claim.** `[DECISION]`, `[REC]` (recommendation), `[ASSUMPTION]`, `[OPEN]`,
   `[RISK]`, `[CHANGE-REQUEST]`, `[ADR]`. Untagged statements are read as facts and will be
   implemented as such.
6. **IDs are permanent.** `FR-###`, `NFR-###`, `UX-###`, `ADR-###`, `DEC-###`, `ASM-###`,
   `OQ-###`, `RISK-###`, `CR-###`, `MODULE-ID` (`AUTH-001`). Never renumber; retire with a
   status instead.
7. **Requirement headings must contain their ID** (e.g. `### FR-AUTH-1 — Password reset`).
   `tp.py context` extracts module context by ID, so this is what keeps agent context narrow.

## How documentation moves through the lifecycle

```
discovery      requirements.md + assumptions/open_questions/risks/decisions
   ↓ (gate: gates.requirements_approved)
frontend-ux    docs/ux/*
   ↓ (gate: gates.ux_approved — only for projects with a UI)
architecture   architecture.md + ADRs + conventions.md + definition_of_done.md
   ↓ (gate: gates.architecture_approved)
decomposition  modules/<ID>.md + state/dependencies.yaml + state/modules.yaml
   ↓ (gate: gates.decomposition_approved)
implementation module contracts + state + PRs (docs updated in the same PR as code)
   ↓
review/testing integration evidence, reports/, handoffs/
   ↓
human approval gates.release_approved
```

## Folder reference

| Path | Contents |
|---|---|
| `docs/project/` | product and engineering truth: requirements, architecture, decisions, assumptions, open questions, risks, conventions, DoD, change requests |
| `docs/ux/` | the UX specification |
| `docs/modules/` | how to write a module contract + the template |
| `docs/agents/` | role registry, provider adapters, agent-artifact templates |
| `docs/templates/` | artifact templates: requirements, ADR, change request, user flow, screen spec, review report |
| `docs/workflows/` | the twelve operating procedures (dev, git, review, testing, integration, recovery, change, context, memory, parallelism, escalation, security) |
| `modules/` | the real module contracts for this project (one file per module) |
| `state/` | machine-readable project state |
| `handoffs/`, `reports/` | generated agent handoffs and evidence reports |
