# Repository and coding conventions

> **Status:** draft · **Owner:** Architecture Agent · **Approved by:** human for policy changes
>
> The Architecture Agent fills in the stack-specific sections during the architecture phase and
> keeps them current. Implementation agents read this file as **context layer 6** — it is binding.
> Anything not specified here is a free choice *inside your own module*, but if you make a choice
> other agents should copy, add it here (`[DECISION]`).

## 1. Repository conventions

| Concern | Rule |
|---|---|
| Layout | Next.js App Router: `src/app/(storefront|admin|api)/…` for routes; feature code in `src/<domain>/` (one module per domain, e.g. `src/catalog/`, `src/orders/`); tests mirror in `tests/<domain>/…` |
| Module ownership | a module may only write paths granted in its contract (`owns`, `allowed_to_modify`) |
| Module boundaries | each module exposes exactly one barrel `src/<domain>/public.ts`; **no deep imports** into another module (`eslint no-restricted-imports` enforces this; the rule is a shared zone owned by `FOUNDATION`) |
| Server/client split | default to React Server Components; `"use client"` only for interaction islands (drawer, dialogs, qty steppers). A client component that fetches first-paint data is a review finding (`ADR-001`) |
| Shared zones | only the owning module may edit them (`state/project.yaml → shared_zones`) |
| Generated files | Prisma client is generated, never committed or hand-edited; regenerate with `npm run prisma:generate` |
| File naming | components `kebab-case.tsx`, domain modules `src/<domain>/`, tests `*.test.ts` next to nothing — always under `tests/` |
| Branching | `docs/workflows/git_workflow.md` |
| Commit messages | `docs/workflows/git_workflow.md` — Conventional Commits with module scope + agent trailers |
| PRs | `.github/pull_request_template.md`, fully filled in |

## 2. Code conventions

| Concern | Rule |
|---|---|
| Language | TypeScript **strict** everywhere; `any` is a review finding; boundary data is `unknown` until validated |
| Formatter | Prettier (`.prettierrc` from `FOUNDATION`) — *formatting is not a review topic* |
| Linter | ESLint (flat config `eslint.config.mjs`): `typescript-eslint` recommended + `no-restricted-imports` module rule; warnings that fail CI are listed in `scripts/verify.config.yaml` |
| Type checking | `tsc --noEmit` on every PR (`verify.config.yaml`) |
| Naming | files `kebab-case`; types/components `PascalCase`; functions/vars `camelCase`; DB columns `snake_case` (Prisma `@map`) |
| Validation | zod schemas at every boundary (Server Action input, route handler, webhook, `.env` via a typed config module); never trust client data |
| Money | integers only (Toman/Rial), never floats; rounding helpers live in `src/catalog/pricing.ts` — never inline `Math.round` on money |
| Dates | store UTC `timestamptz`; format for humans via `src/lib/fa.ts` (Jalali display, Persian digits, bidi-safe mixing, `UX-G-009`); never `toLocaleString` ad hoc |
| Error handling | never swallow errors; typed result unions for expected failures; unexpected failures logged with correlation id and re-thrown; user-facing errors are actionable Farsi (`UX-G-003`), never leaking internals |
| Logging | structured JSON via the `SHELL` logger; no secrets, no personal data (`NFR-PRIV-1`); correlation id per request |
| Comments | explain *why*; never restate the code |
| Dead code | delete it; do not comment it out |
| TODO policy | `TODO(<MODULE-ID>): <what> — <owner>` and referenced from `reports/`; no bare TODOs |
| Line length / file size | keep files reviewable (< ~400 lines soft limit) |

## 3. Testing conventions

| Concern | Rule |
|---|---|
| Test location | `tests/<domain>/…`, mirroring `src/<domain>/` |
| Runners | Vitest (unit + integration + contract), Playwright (e2e + visual evidence) — `ADR-010` |
| Database in tests | real PostgreSQL from the `db-test` compose service; migrations applied, tables truncated per test — never mock the DB to fake success |
| Test naming | describes behaviour: `rejects_expired_reset_token`, `advances_paid_to_shipped_only` |
| Required per module | unit tests for each acceptance criterion + contract test for each provided interface (`architecture.md` §6.1) |
| UI evidence | Playwright screenshots at 320/768/1280 for every screen a PR touches, attached to the PR (`docs/ux/visual_validation.md` §2.1); never committed to the repo |
| A11y | axe scan on changed screens as part of the Playwright pass; `UX-AC-012.1` contrast/theme integrity is a Vitest unit test |
| Payment | provider conformance suite runs against the sandbox adapter; the sandbox adapter must never be enabled in production (config guard + test) |
| Test data | factories/fixtures owned by the module that defines the entity; e2e seed script in `tests/fixtures/`; **no production data in tests** (`NFR-PRIV-1`) |
| Isolation | no test may depend on another module's internal state; use the public barrel/contract |
| Flakiness | a flaky test is a bug: fix or quarantine with an issue, never retry in silence |
| Coverage | used as a **signal**, never as a target; untested *requirements* are the real gap |
| Running | `python scripts/verify.py` (wraps `npm run verify` sections — see `scripts/verify.config.yaml`) |

## 4. Dependency policy

1. **Prefer the standard library / existing dependencies.** A new runtime dependency needs a
   justification, not a preference.
2. **New runtime dependency ⇒ `ADR-###` + human approval.** New dev-only tooling ⇒ PR
   description note; the Architecture Agent may record it as a `DEC-###`.
3. **Pin and lock.** Lockfiles are committed. Upgrades arrive through Dependabot PRs or a
   scheduled task, never as a side effect of a feature PR.
4. **No unmaintained packages.** Check maintenance status, license, install size and transitive
   count before adding.
5. **One dependency manager per ecosystem.** Do not mix npm+pnp, pip+poetry+cargo, etc.
6. **Security.** Known-vulnerable dependencies fail the security job. No post-install scripts
   from unknown publishers.
7. **Agent rule:** you may not add a dependency to satisfy a test, and you may not vendor code
   without an ADR.

## 5. Documentation requirements

| Change | Documentation you must update in the same PR |
|---|---|
| Behaviour change | `docs/project/requirements.md` (+ `requirements.yaml`) |
| UX change | `docs/ux/*` |
| Interface change | module contract + `docs/project/architecture.md` + `state/dependencies.yaml` (re-freeze) |
| Architectural choice | `ADR-###` in `docs/project/decisions.md` |
| New module / boundary change | `modules/<ID>.md` + `state/modules.yaml` + `state/dependencies.yaml` |
| New open question | `docs/project/open_questions.md` |
| New assumption | `docs/project/assumptions.md` |
| Any of the above | nothing else in the repo may contradict it (`docs/README.md` rule 4) |

## 6. Security conventions

- Secrets: only via environment/secret manager; `.env` is gitignored; never log secrets.
- Authorization is enforced server-side at the module that owns the resource.
- Input validation at the boundary; output encoding at the render site.
- Destructive operations require human approval (`docs/workflows/human_in_the_loop.md`).
- Agent permissions follow least privilege (`docs/workflows/security.md`).

## 7. Definition of ready (before an agent starts)

A module may start only when: contract exists and is complete · dependencies are
`validated`/`complete` · interfaces it consumes are `frozen` · no open question blocks it ·
shared zones it needs have an owner and an agreed change mechanism · its branch name is reserved.
