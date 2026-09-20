# Development workflow

The operating manual for the whole project. Every stage has: an owner, required inputs, a
produced artifact, a gate, and a next stage. Nothing skips a gate, and **discovery precedes code
always**.

## 1. Stage map

| # | Stage | Owner role | Inputs | Outputs (artifacts) | Gate |
|---|---|---|---|---|---|
| 0 | Bootstrap | human | the template | `state/project.yaml` filled, repo created, CI green | — |
| 1 | Discovery | discovery | human intent, `docs/project/*` | `requirements.md`, `requirements.yaml`, assumptions, open questions, decisions, risks | `gates.requirements_approved` (human) |
| 2 | UX specification | frontend-ux | approved requirements | `docs/ux/*`, UX IDs, flows, screens, design system | `gates.ux_approved` (human) |
| 3 | Architecture | architecture | requirements + UX | `architecture.md`, `ADR-###`, conventions, DoD, interfaces, testing architecture | `gates.architecture_approved` (human) |
| 4 | Decomposition | decomposition | architecture | `modules/<ID>.md`, `state/modules.yaml`, `state/dependencies.yaml` | `gates.decomposition_approved` (human) |
| 5 | Orchestration | orchestration | contracts + dependency graph | waves, agent assignments, `state/agents.yaml`, handoffs | none (plan review by human, optional) |
| 6 | Implementation | implementation (one per module) | context pack + contract | code, tests, docs, PR with evidence | PR review |
| 7 | Review | review | PR + contract | `reports/review-*.md`, classified findings | `awaiting_review → validated/changes_requested` |
| 8 | Testing | testing | PR + requirements | `reports/testing-*.md`, gap list | validation result |
| 9 | Integration | integration | validated modules | `reports/integration-*.md`, e2e evidence | milestone verdict |
| 10 | Human approval | human | integration report, project state | `gates.release_approved` | release |
| 11 | Release / ship | human (+ orchestration) | approved milestone | version tag, release notes, deploy | — |
| 12 | Maintenance | debugging (+ others) | defects, change requests | fixes, reports | per change |

## 2. Rules that hold at every stage

1. **Written artifacts, not conversations.** If it is not in the repository, it did not happen.
2. **One source of truth per fact** (`docs/README.md`). Link, do not copy.
3. **Gates are explicit and human-owned** except the technical ones (review/testing/integration
   verdicts), which are agent-owned with evidence.
4. **Every stage updates state.** `state/project.yaml` → `stage` and the relevant status fields must
   reflect reality before the next stage begins.
5. **Escalate early.** A question asked at step 4 costs minutes; the same question discovered at
   step 9 costs a rewrite (`docs/workflows/human_in_the_loop.md`).
6. **Change after approval goes through a change request** (`change_management.md`) — never a
   silent edit of an approved document.
7. **Evidence over assertion.** Paste commands and results; never claim verification you did not run.

## 3. Stage detail

### Stage 0 — Bootstrap
Human: create the project from the template
(`python TemplateProject/scripts/tp.py bootstrap my-project --name … --id … --profile … --init-git`),
create the remote, set branch protection, and confirm `python scripts/tp.py validate --strict` passes.
The command copies the tree, replaces the placeholders, flips `initialised: true` and makes the first
commit — so a leftover placeholder becomes a build failure instead of a surprise later.

### Stages 1–4 — Specification chain
Each stage may send work back to the previous one. Discovery repeatedly asks the human rather than
guessing. UX may raise architectural implications; architecture may find a requirement impossible;
decomposition may find the architecture undecomposable — all of these produce a change to the
earlier artifact **before** implementation starts.

### Stage 5 — Planning
The orchestrator computes waves from `state/dependencies.yaml`, caps concurrency by review
capacity, and assigns one agent per module. Planning is cheap to redo; implement it wrong and you
pay in merge conflicts (`parallelism.md`).

### Stage 6 — Implementation
One agent, one module, one branch (`agent/<agent-id>/<MODULE-ID>`), context from `tp.py context`,
tests for every acceptance criterion, PR with evidence. The agent stops when criteria are met — not
when it runs out of ideas, and not when the code compiles.

### Stages 7–9 — Validation
Review checks conformance to contract/requirements/conventions. Testing checks behaviour against
requirements and reports unverified gaps. Integration checks that the modules work together and
attributes failures to their true origin. All three produce written reports; none may silently edit.

### Stage 10–12 — Acceptance, release, maintenance
The human accepts the milestone against the DoD. Release notes come from the decisions and PRs in
the milestone. Maintenance uses the same machinery: a defect is a failure report, a behaviour change
is a change request.

## 4. What "the project is in good shape" looks like

- `python scripts/tp.py validate` passes; no unreplaced placeholders.
- `python scripts/tp.py status` shows no module `blocked` without a recorded blocker and owner.
- Every open question has an owner; nothing material is missing an `[OPEN]`/`[ASSUMPTION]` tag.
- Every merged PR has evidence; no module is `complete` without review + testing verdicts.
- `docs/project/project_state.md` agrees with `state/*.yaml`.
