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

## Stack-specific additions (NoghreShop — `ADR-001`…`ADR-010`)

- [ ] TypeScript strict: `npm run typecheck` clean; no new `any`/`@ts-ignore` without a comment naming the reason and an owner.
- [ ] Module boundary intact: imports from other domains only via their `public.ts` barrel; `"use client"` only on interaction islands (lint + review).
- [ ] Data access through the module's own repositories over Prisma; no business logic in route handlers or components.
- [ ] Schema changes arrive as a Prisma migration authored by the `FOUNDATION` owner; destructive or data-moving migrations carry explicit human approval in the PR.
- [ ] Money is integer math through `pricing.compute`; a pricing change updates its rounding property tests.
- [ ] Every boundary input is validated with a zod schema (Server Action, route handler, webhook, env).
- [ ] Persian text renders through `src/lib/fa.ts` helpers (Jalali dates, Persian digits, bidi safety) — no ad-hoc `toLocaleString`/`Intl` calls in components.
- [ ] UI PRs attach the three-width screenshots and axe results for every touched screen (`visual_validation.md` §2.1); storefront pages stay within the JS budget (`NFR-PERF-1`).
- [ ] Theme touching code keeps the rollover colour-only and honours `data-month` resolution (`ADR-007`); the twelve-set contrast test still passes.
- [ ] No card data, no secret, no personal data in logs, fixtures or test snapshots (`NFR-SEC-1`, `NFR-PRIV-1`); the sandbox payment adapter is unreachable in production.
- [ ] Outbox writes commit in the same transaction as the triggering change; a failing send never blocks or reverts the business change.
- [ ] `python scripts/verify.py` passes locally and its output is pasted in the PR (install → typecheck → lint → format → unit/integration → e2e → audit).
