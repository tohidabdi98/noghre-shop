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
| Layout | `src/<module-slug>/…` for source, `tests/<module-slug>/…` for tests (adjust to your stack and record it here) |
| Module ownership | a module may only write paths granted in its contract (`owns`, `allowed_to_modify`) |
| Shared zones | only the owning module may edit them (`state/project.yaml → shared_zones`) |
| Generated files | never hand-edit; regenerate and commit, or ignore |
| File naming | (your stack's convention) |
| Branching | `docs/workflows/git_workflow.md` |
| Commit messages | `docs/workflows/git_workflow.md` — Conventional Commits with module scope + agent trailers |
| PRs | `.github/pull_request_template.md`, fully filled in |

## 2. Code conventions

| Concern | Rule |
|---|---|
| Formatter | (e.g. prettier / ruff format / gofmt / rustfmt) — *formatting is not a review topic* |
| Linter | (e.g. eslint / ruff / golangci-lint) — warnings that fail CI are listed in `scripts/verify.config.yaml` |
| Type checking | (e.g. tsc --noEmit / mypy --strict / go vet) |
| Naming | (your stack's convention) |
| Error handling | never swallow errors; log with context; user-facing errors are actionable and non-leaking |
| Validation | validate at the boundary; never trust input from outside the boundary |
| Logging | structured, no secrets, no personal data, correlation id per request |
| Comments | explain *why*; never restate the code |
| Dead code | delete it; do not comment it out |
| TODO policy | `TODO(<MODULE-ID>): <what> — <owner>` and referenced from `reports/`; no bare TODOs |
| Line length / file size | keep files reviewable (< ~400 lines soft limit) |

## 3. Testing conventions

| Concern | Rule |
|---|---|
| Test location | `tests/<module-slug>/…`, mirroring the source structure |
| Test naming | describes behaviour: `rejects_expired_reset_token` |
| Required per module | unit tests for each acceptance criterion + contract test for each provided interface |
| Test data | factories/fixtures are owned by the module that defines the entity |
| Isolation | no test may depend on another module's internal state; use the public contract |
| Flakiness | a flaky test is a bug: fix or quarantine with an issue, never retry in silence |
| Coverage | used as a **signal**, never as a target; untested *requirements* are the real gap |
| Running | `python scripts/verify.py` (or your stack's native command, recorded here) |

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
