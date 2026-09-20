<!-- PROJECT-BANNER -->
# NoghreShop

- **Project ID:** `noghre-shop`
- **Owner:** —
- **Profile:** `fullstack`
- **Stage:** `discovery` · gates and state in `state/project.yaml`

> How this project is developed: [`HOW_TO_USE.ipynb`](HOW_TO_USE.ipynb).
> The template documentation below describes the framework this project is built on — keep it,
> it is the operating manual for every agent that works here.

---

# Template documentation (framework reference)

A copy-and-use project template that operationalizes **agent-driven software development**:
you supply intent and make the consequential decisions, agents do as much of the engineering
work as can be done safely, and the repository itself — docs, state files, contracts, Git
history — carries the project's memory across agent sessions, failures and model changes.

This is the template *root*. Copy the whole folder to start a new project.

> **Read first:** [`HOW_TO_USE.ipynb`](HOW_TO_USE.ipynb) is the primary, step-by-step guide.
> This README is the orientation; the notebook is the instructions.

---

## Core philosophy

1. **Human intent is the source of product truth.** Agents may recommend; product decisions are explicit.
2. **Written specifications are the source of engineering truth.** Never rely on chat history alone.
3. **Narrow agent responsibilities.** Specialized roles with explicit scopes beat one generalist.
4. **One module, one owner.** Two implementation agents never edit the same module at once.
5. **Git is part of the coordination system.** Branches, commits, PRs and reviews are workflow primitives.
6. **Verification is mandatory.** "Code was written" is not completion; evidence is.
7. **Prefer reversible decisions** unless there is a reason not to.
8. **Escalate important ambiguity** — agents never invent consequential requirements.
9. **Optimize for useful parallelism**, not maximum agent count.
10. **Preserve project knowledge** so any new agent can join without another agent's memory.

## How the pieces fit

```
                     HUMAN  ── intent, gates, escalations
                       │
                       ▼
        Discovery ─► Requirements ─┬─► Frontend/UX ──► UX spec
                                   └─► Architecture ─► ADRs + interfaces
                                              │
                                              ▼
                                      Decomposition ─► module contracts
                                              │
                                              ▼
                                       Orchestrator ─► waves, assignments
                                              │
        ┌─────────────────────────────────────┼─────────────────────────────────────┐
        ▼                                     ▼                                     ▼
  impl agent A                          impl agent B                          impl agent C
  branch + commits + PR                 branch + commits + PR                 branch + commits + PR
        └─────────────────────────────────────┼─────────────────────────────────────┘
                                              ▼
                            Review ─► Testing ─► Integration ─► HUMAN approval
```

Each arrow is a **documented artifact**, not a conversation: requirements, UX specs,
ADRs, module contracts, state transitions, PRs, validation reports.

## Agent roles

| Role | Kind | Owns | Starter prompt |
|---|---|---|---|
| Discovery | conversational | requirements, assumptions, open questions, decisions, risks | [`agents/discovery`](agents/discovery/STARTER_PROMPT.md) |
| Frontend / UX | conversational | the UX specification, design system, UX acceptance criteria | [`agents/frontend-ux`](agents/frontend-ux/STARTER_PROMPT.md) |
| Architecture | analytical | architecture, ADRs, interfaces, testing/deployment architecture | [`agents/architecture`](agents/architecture/STARTER_PROMPT.md) |
| Module decomposition | analytical | module contracts + dependency graph | [`agents/decomposition`](agents/decomposition/STARTER_PROMPT.md) |
| Orchestrator | coordination | readiness, assignment, blockers, routing, escalation | [`agents/orchestration`](agents/orchestration/STARTER_PROMPT.md) |
| Implementation | implementation | exactly one module | [`agents/implementation`](agents/implementation/STARTER_PROMPT.md) |
| Testing | validation | requirement-based verification evidence | [`agents/testing`](agents/testing/STARTER_PROMPT.md) |
| Review | validation | PR/contract conformance findings | [`agents/review`](agents/review/STARTER_PROMPT.md) |
| Integration | validation | cross-module and end-to-end behavior | [`agents/integration`](agents/integration/STARTER_PROMPT.md) |
| Debugging / Fix | implementation | smallest correct fix + regression coverage | [`agents/debugging`](agents/debugging/STARTER_PROMPT.md) |

Machine-readable contracts for all ten roles live in
[`docs/agents/agent_registry.yaml`](docs/agents/agent_registry.yaml).

## Directory structure

```
TemplateProject/
├── README.md                  ← you are here
├── HOW_TO_USE.ipynb           ← primary guide: start here
├── AGENTS.md                  ← entry point every coding agent reads first
├── docs/
│   ├── README.md              source-of-truth map (which document wins for what)
│   ├── project/               requirements, architecture, decisions, assumptions, open questions, risks
│   ├── ux/                    UX specification (flows, IA, screens, design system, patterns)
│   ├── modules/               module-contract format + template (contracts live in modules/)
│   ├── agents/                role registry, provider adapters, agent-artifact templates
│   ├── templates/             artifact templates (ADR, change request, screen spec, …)
│   └── workflows/             12 workflow guides (dev, git, review, testing, recovery, security, …)
├── agents/<role>/STARTER_PROMPT.md     copy-paste prompts for each of the ten roles
├── modules/<MODULE-ID>.md             one contract per module (created during decomposition)
├── state/                     structured project state: project, modules, agents, dependencies
├── handoffs/                  generated agent-to-agent handoff records
├── reports/                   generated validation / review / failure reports
├── scripts/                   zero-dependency Python tools (tp.py, verify.py) + tests
├── examples/example-saas/     filled-in golden reference (delete when you know the shape)
└── .github/                   PR + issue templates, CI and agent-PR checks
```

## Quick start

```bash
# 1. create the project from the template (copies the tree, fills in placeholders, git-inits)
python TemplateProject/scripts/tp.py bootstrap my-project \
  --name "My Project" --id my-project --profile fullstack --init-git --adopt-env
cd my-project

# 2. verify the tooling works in your environment
python scripts/tp.py validate --strict && python scripts/tp.py status

# 3. open HOW_TO_USE.ipynb and start the Discovery Agent (paste the prompt from
#    agents/discovery/STARTER_PROMPT.md) — discovery happens before any code.
```

Already copied the directory yourself? The same command works in place (drop the destination path):

```bash
cd my-project && python scripts/tp.py bootstrap --name "My Project" --id my-project --profile fullstack
```

Requirements: Python ≥ 3.9 (stdlib only — no packages to install), Git ≥ 2.30, and a coding
agent of your choice. The framework is deliberately provider-agnostic.

## Git workflow in one screen

| Thing | Convention |
|---|---|
| Agent branch | `agent/<agent-id>/<MODULE-ID>` — e.g. `agent/impl-auth-001/AUTH-001` |
| Human branch | `human/<name>/<topic>` |
| Integration / release | `integration/<milestone>`, `release/<version>` |
| Commit | `<type>(<MODULE-ID>): <subject>` + `Agent:` / `Module:` / `Refs:` trailers |
| PR title | `[AUTH-001] feat: password reset — agent impl-auth-001` |
| Module states | `planned → ready → assigned → in_progress → awaiting_review → validated → complete` (+ `blocked`, `failed`, `changes_requested`, `cancelled`) |
| Ownership | enforced mechanically by `python scripts/tp.py pr-check` in CI |

Full detail: [`docs/workflows/git_workflow.md`](docs/workflows/git_workflow.md).

## Project lifecycle

1. **Discovery** — an interview; produces an approved requirements specification.
2. **UX** — flows, IA, screens, design system; a living spec you can revisit any time.
3. **Architecture** — components, data model, interfaces, security, deployment, ADRs.
4. **Decomposition** — modules with contracts, ownership boundaries and a dependency graph.
5. **Orchestration** — the orchestrator plans waves and assigns one agent per module.
6. **Implementation** — one branch, one module, own tests, PR with evidence.
7. **Review / Testing / Integration** — blocking vs non-blocking findings, verification, cross-module validation.
8. **Human approval** — you accept the milestone; then ship.

Changes are handled the same way as initial work: change request → impact analysis →
affected requirements/UX/architecture/modules → updated contracts → implementation → validation.

## Where to read what

| Question | Read |
|---|---|
| How do I start? What do I do at each step? | [`HOW_TO_USE.ipynb`](HOW_TO_USE.ipynb) |
| What is the source of truth for X? | [`docs/README.md`](docs/README.md) |
| How do agents behave, and what are they allowed to do? | [`AGENTS.md`](AGENTS.md), [`docs/agents/`](docs/agents/README.md) |
| How do I write a module contract? | [`docs/modules/template.md`](docs/modules/template.md) |
| How do I recover from a failed/stale agent? | [`docs/workflows/failure_recovery.md`](docs/workflows/failure_recovery.md) |
| What must an agent escalate to me? | [`docs/workflows/human_in_the_loop.md`](docs/workflows/human_in_the_loop.md) |
| What are the security rules for agents? | [`docs/workflows/security.md`](docs/workflows/security.md) |

## Tooling

```bash
python scripts/tp.py validate            # state, contracts, placeholders, doc links, prompt sync
python scripts/tp.py status              # board: states, blockers, open questions, next actions
python scripts/tp.py ready               # dependency waves + shared-zone conflict warnings
python scripts/tp.py new-module --id AUTH-001 --name Authentication
python scripts/tp.py context --module AUTH-001 --agent impl-auth-001   # layered context pack
python scripts/tp.py start --module AUTH-001 --agent impl-auth-001     # branch + state transition
python scripts/tp.py handoff --module AUTH-001 --from impl-auth-001 --to impl-auth-002 --reason "context stale"
python scripts/tp.py pr-check --base main                              # CI ownership + convention gate
python scripts/tp.py sync-notebook       # keep notebook prompts in sync with agents/*/STARTER_PROMPT.md
python scripts/verify.py                 # typecheck / lint / test (stack auto-detect)
python -m unittest discover -s scripts/tests -t .
```

## License / attribution

No license is imposed by this template. Add your own `LICENSE` when you start a project.
