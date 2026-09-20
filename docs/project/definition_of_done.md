# Definition of done

> Completion is **evidence**, never activity. "Code was written", "tests pass", and "the agent
> said so" are not done. Each level below is a gate; the Orchestrator Agent checks it and the
> Review/Integration Agents verify it.

## Level 1 — Task done (inside a module)

- [ ] The change satisfies a stated requirement or acceptance criterion (cite the ID).
- [ ] Implementation stays inside the module's `allowed_to_modify` paths.
- [ ] Unit tests cover the new behaviour *and its edge cases* from the contract.
- [ ] `python scripts/verify.py` passes locally (typecheck, lint, tests) — output pasted into the PR.
- [ ] No new dependency without an `ADR-###` and human approval.
- [ ] Docs that became stale are updated in the same commit.
- [ ] Commit messages follow the convention and carry the agent trailers.
- [ ] The agent can explain what it changed and why, and what it did **not** do.

## Level 2 — Module done

- [ ] Every acceptance criterion in `modules/<MODULE-ID>.md` has explicit evidence (test name,
      command, screenshot, or recorded manual verification).
- [ ] Every provided interface matches its frozen contract, verified by a contract test.
- [ ] Every consumed interface is used as specified — no reliance on undocumented behaviour.
- [ ] Security requirements from the contract are met (authorization enforced, inputs validated,
      secrets handled correctly).
- [ ] Performance requirements from the contract are measured, not assumed.
- [ ] Review Agent findings are resolved or explicitly accepted as non-blocking by the human.
- [ ] Module docs (`modules/<ID>.md` change log) updated; `state/modules.yaml` status is
      `validated` with `validation: passed`.
- [ ] No known limitation is hidden: they are listed in the PR and in `reports/`.

## Level 3 — Integration done

- [ ] End-to-end workflow for the module's user journeys passes against the integrated system.
- [ ] Cross-module data flows verified (`Integration Agent` report in `reports/`).
- [ ] Frontend ↔ backend contract verified; loading/empty/error states exercised.
- [ ] UI changes validated visually (`docs/ux/visual_validation.md`) and approved by the
      Frontend/UX Agent.
- [ ] Configuration and deployment path work in a clean environment (not just the author's).
- [ ] No unresolved `blocked` module on the integration path.

## Level 4 — Milestone / release done

- [ ] All modules in the milestone are `complete`.
- [ ] Requirements in `requirements.yaml` are `verified` (or explicitly deferred with a `DEC-###`).
- [ ] Security review and dependency audit clean or explicitly accepted.
- [ ] Observability in place: logs/metrics for the new behaviour exist and are checked.
- [ ] Migration/rollback plan exists if data or infrastructure changed.
- [ ] `docs/project/project_state.md` and `state/project.yaml` reflect reality.
- [ ] **Human approval recorded** (`gates.release_approved: true`).

## Explicitly not "done"

| Not done | Why |
|---|---|
| Tests pass but no acceptance criterion was exercised | tests prove code, not behaviour |
| Feature works on the developer's machine only | reproducibility is part of done |
| UI implemented but never rendered/viewed | visual correctness is unverified |
| Docs deferred "to later" | later never comes; stale docs cause wrong agent work |
| Coverage percentage raised | coverage is a signal, not a criterion |
| CI green with required jobs skipped | unverified is not verified |
| Validation claimed without a command + output | claims are not evidence |
