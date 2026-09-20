# Repository and coding conventions — Example SaaS

> Owner: Architecture Agent · Stack decisions are binding for every module agent.

## 1. Repository
| Concern | Rule |
|---|---|
| Layout | `src/<module-slug>/…`, `tests/<module-slug>/…` |
| Ownership | only the module contract's `allowed_to_modify` paths may be written |
| Shared zones | `src/app/routes.ts`, `package.json`, `db/migrations/**`, `src/app/design-tokens.css` (owners in architecture §4.1) |
| Generated files | never hand-edit; regenerate |
| Imports | a module may import another module **only** through its declared port |

## 2. Code
| Concern | Rule |
|---|---|
| Formatter | prettier (checked in CI: `format_check`) |
| Linter | eslint with the repository config; warnings fail CI |
| Types | TypeScript strict; `any` requires a comment explaining why |
| Errors | never swallow; throw typed errors at boundaries; no stack traces to users |
| Validation | at the HTTP boundary; never trust client input |
| Logging | structured JSON with correlation id; no PII, no secrets |
| TODOs | `TODO(<MODULE-ID>): …` with an owner |

## 3. Testing
| Concern | Rule |
|---|---|
| Location | `tests/<module-slug>/…` |
| Naming | describes behaviour (`rejects_expired_reset_token`) |
| Required | one test per acceptance criterion + a contract test per provided port |
| Isolation | module tests use in-memory repositories; no network |
| Determinism | inject the clock and the random source |
| Coverage | a signal, never a target |

## 4. Dependencies
Standard library and existing dependencies first. A new **runtime** dependency requires an `ADR-###`
and human approval; dev-only tooling needs a note in the PR. Lockfile is committed.

## 5. Documentation duties
Change | Update
|---|---|
| behaviour | `docs/project/requirements.md` |
| UI | `docs/ux/*` |
| interface | module contract + architecture §6 + `state/dependencies.yaml` (re-freeze) |
| architectural choice | `ADR-###` |
