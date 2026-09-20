# Decisions — decision log and architecture decision records

> Two things live here, both append-only:
> * **`DEC-###` — decisions.** Any consequential choice made by a human or agent, with rationale.
> * **`ADR-###` — architecture decision records.** Significant, hard-to-reverse technical choices.
>
> Rules
> * Never rewrite history: supersede an old entry by adding a new one and marking the old
>   `superseded by ADR-###`.
> * Every entry names its **decider** (human or agent id) and its **status**:
>   `proposed` · `accepted` · `rejected` · `superseded` · `deprecated`.
> * The Discovery Agent records product decisions; the Architecture Agent publishes ADRs;
>   any role may record a `DEC-###` for a decision inside its scope.
> * A `[REC]` (recommendation) that the human has not answered stays a `[REC]` — agents must not
>   turn a recommendation into a decision silently.

## Decision index

| ID | Title | Type | Status | Decider | Date |
|---|---|---|---|---|---|
| DEC-001 | Instantiate from TemplateProject | process | accepted | human | — |

---

## DEC-001 — Instantiate this project from TemplateProject
- **Status:** accepted · **Decider:** human
- **Context:** Starting a new project with agent-driven development.
- **Decision:** Use the TemplateProject framework: discovery → UX → architecture →
  decomposition → per-module agents → review/testing/integration → human approval.
- **Alternatives considered:** ad-hoc prompting without written specs.
- **Consequences:** documentation and state files are part of the deliverable; agents must obey
  `AGENTS.md`; every module has one owner.

---

## ADR template — copy for each record

### ADR-### — <short title>
- **Status:** proposed · **Date:** — · **Decider:** architecture agent · **Supersedes:** —
- **Context:** <!-- forces at play: requirements, NFRs, constraints, team/agent constraints -->
- **Options considered:**
  1. <!-- option A — pros / cons -->
  2. <!-- option B — pros / cons -->
- **Decision:** <!-- the choice, stated as an instruction an agent can follow -->
- **Rationale:** <!-- why this option beats the others, including agent-parallelism impact -->
- **Consequences:** <!-- what becomes easy, what becomes hard, what must be revisited -->
- **Reversibility:** easy / moderate / hard — and the cost of changing later
- **Affected modules:** `MODULE-ID`s
- **Verification:** <!-- how we will know this decision was right -->
- **References:** requirements `FR-###`, UX `UX-###`, architecture §
