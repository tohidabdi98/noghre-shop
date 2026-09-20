# AGENTS.md — entry point for every coding agent

This repository is developed by AI agents under human direction. **Whatever agent, tool or
model you are, read this file first.** It tells you where the truth lives, what you may do,
and what you must escalate.

> Human: paste the relevant `agents/<role>/STARTER_PROMPT.md` file into your coding agent as
> the first message of a session. That prompt already follows this contract; this file is the
> shared rulebook it refers to.

---

## 1. Read order

Read only what your role needs. Do not load the whole repository into context.

1. `AGENTS.md` (this file) — global rules.
2. `state/project.yaml` — project identity, stage, gates.
3. `docs/README.md` — which document is the source of truth for what.
4. Your role contract in `docs/agents/agent_registry.yaml` — mission, scope, escalation.
5. Your role's starter prompt `agents/<role>/STARTER_PROMPT.md` — process and outputs.
6. Then the role-specific context described in `docs/workflows/context_engineering.md`.

A generated context pack already contains layers 1–8 for a specific module or task:

```bash
python scripts/tp.py context --module AUTH-001 --agent impl-auth-001
```

## 2. Hard rules

1. **Discovery before implementation.** No agent writes product code until
   `docs/project/requirements.md` is approved by the human (`state/project.yaml → gates.requirements_approved: true`).
2. **Specifications are the source of truth.** If the documents do not say it and it matters,
   it is an open question — not something to invent. Never silently invent product requirements.
3. **Stay inside your scope.** Modify only paths granted by your role and your module contract
   (`owns`, `allowed_to_modify`). Never touch `forbidden_to_modify`. `forbidden` beats `allowed`.
4. **One module, one owner.** Never edit another module's files as a side effect of your task.
   Cross-module changes require an explicit contract permission or escalation.
5. **Verification is mandatory.** Completion requires evidence: commands run, results, and the
   module's acceptance criteria satisfied. Tests passing is not the same as the feature working.
6. **Frontend work is not done until it is seen.** UI changes require browser/visual validation
   as described in `docs/ux/visual_validation.md`, not only unit tests.
7. **Escalate, don't guess** (see §4). Escalation means: stop, write the question into the right
   document, and ask the human.
8. **Update the documents you own** in the same PR as your code. Stale docs are defects.
9. **No secrets in the repository.** No credentials, tokens or production data — ever.
10. **Small, reversible steps.** One coherent change per commit; no unrelated cleanup.
11. **No destructive Git operations.** Never force-push, never rewrite shared history, never
    delete another agent's branch, never commit directly to the default branch.
12. **Identify yourself.** Every commit and PR must name the agent (see §5).

## 3. Roles

| Role | Category | Prompt |
|---|---|---|
| discovery | conversational | `agents/discovery/STARTER_PROMPT.md` |
| frontend-ux | conversational | `agents/frontend-ux/STARTER_PROMPT.md` |
| architecture | analytical | `agents/architecture/STARTER_PROMPT.md` |
| decomposition | analytical | `agents/decomposition/STARTER_PROMPT.md` |
| orchestration | coordination | `agents/orchestration/STARTER_PROMPT.md` |
| implementation | implementation | `agents/implementation/STARTER_PROMPT.md` |
| testing | validation | `agents/testing/STARTER_PROMPT.md` |
| review | validation | `agents/review/STARTER_PROMPT.md` |
| integration | validation | `agents/integration/STARTER_PROMPT.md` |
| debugging | implementation | `agents/debugging/STARTER_PROMPT.md` |

If you have not been assigned a role, ask which one you are. A role is not a personality: it is
a scope of authority, inputs, outputs and escalation duties. Your contract in
`docs/agents/agent_registry.yaml` is binding.

## 4. Escalation to the human (mandatory)

Stop and ask when any of these apply:

- ambiguous or conflicting product requirements
- a major architectural trade-off with more than one defensible option
- security-sensitive decisions (auth model, secrets, crypto, PII, permissions)
- destructive or irreversible data/infrastructure changes
- breaking public API changes
- scope changes (new module, changed milestone, new external service, anything billable)
- materially different UX direction affecting primary flows or navigation
- changing established product behavior
- you cannot satisfy two acceptance criteria at once
- you need to modify files outside your allowed scope beyond a trivial, documented fix

Low-risk decisions inside your scope (names, internal structure, tests, formatting, refactors in
your own module) do **not** need approval: make the call, then record it as a `[DECISION]` or
`[REC]` entry. Full policy: `docs/workflows/human_in_the_loop.md`.

## 5. Identity, Git and evidence

- Branch: `agent/<agent-id>/<MODULE-ID>` (create with `python scripts/tp.py start …`).
- Commit: `<type>(<MODULE-ID>): <subject>` plus trailers:
  ```
  Agent: impl-auth-001
  Agent-Role: implementation
  Module: AUTH-001
  Refs: #12
  Validated-With: python scripts/verify.py (exit 0)
  ```
- PR title: `[AUTH-001] feat: password reset — agent impl-auth-001`; fill in
  `.github/pull_request_template.md` completely, and never claim validation you did not run.
- Never `git push --force`, never merge your own PR, never commit to the default branch.

## 6. Where to write things

| Artifact | Location |
|---|---|
| Requirements, assumptions, open questions, decisions, risks | `docs/project/` |
| UX specification | `docs/ux/` |
| Architecture, ADRs | `docs/project/architecture.md`, `docs/project/decisions.md` |
| Module contract | `modules/<MODULE-ID>.md` |
| Project/module/agent/dependency state | `state/*.yaml` |
| Handoff record | `handoffs/` |
| Validation, review, failure reports | `reports/` |
| Change requests | `docs/project/change_requests/` |

Documentation rules: keep one source of truth per fact (`docs/README.md`), tag claims as
`[DECISION]`, `[REC]`, `[ASSUMPTION]`, `[OPEN]`, `[RISK]`, and never leave contradictory
statements in place — supersede them explicitly.
