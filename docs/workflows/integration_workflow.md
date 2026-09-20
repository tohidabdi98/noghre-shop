# Integration workflow

Modules are developed by different agents on different branches. Integration is where independent
work is proven to compose — and where failures are attributed to their **true origin** instead of
being patched over.

## 1. When integration happens

| Trigger | Scope | Output |
|---|---|---|
| Two or more modules reach `validated` and depend on each other | first composition check | integration report |
| A milestone's modules are all `validated` | full end-to-end validation of the milestone | milestone verdict, `gates.release_approved` input |
| An interface changed (change request) | re-validate affected edges | re-frozen edge + report |
| Before release | clean-environment validation of the deployment path | release checklist evidence |

## 2. Procedure

1. **Assemble** an integration state: `integration/<milestone>` branch or a dedicated environment.
   Never validate integration on a developer's working tree.
2. **Freeze and verify interfaces.** For each edge in `state/dependencies.yaml`, confirm
   `status: frozen` and that both sides implement the same shape. Contract tests come first: they
   localise most integration failures in minutes.
3. **Exercise data flows** across module boundaries with realistic volumes and shapes (empty, huge,
   unicode, concurrent).
4. **Run end-to-end journeys** from `docs/ux/user_flows.md` on the integrated system, including
   failure paths and state transitions.
5. **Validate configuration**: environment variables, feature flags, migrations applied in order,
   secrets resolved from the environment (not hard-coded), startup ordering, cold start.
6. **Check the deployment path**: build + deploy to a clean environment; validate rollback.
7. **Attribute every failure** (§4) and write the report
   (`docs/agents/templates/validation_report.md`).
8. **Give a milestone verdict**: PASS / PASS WITH FINDINGS / FAIL, with the evidence and any
   conditions.

## 3. What integration must check (beyond "it runs")

| Concern | Examples |
|---|---|
| Interface conformance | field names, types, nullability, error codes, pagination semantics, versioning |
| Data integrity | uniqueness, referential integrity, transaction boundaries, ordering guarantees |
| Concurrency | double submits, race conditions, idempotency keys, retries |
| Failure propagation | timeouts, partial failures, degraded mode, user-visible error states |
| Auth/session flow | token lifetime across modules, permission enforcement end to end |
| Frontend ↔ backend | loading/empty/error/success states with real responses, not mocks |
| Configuration | staging ≠ production differences, env var names, defaults |
| Observability | logs/metrics actually emitted for the integrated flow |

## 4. Failure attribution (the point of this workflow)

| Origin | Signature | Route to |
|---|---|---|
| **Module defect** | contract test fails inside one module; other side behaves correctly | owner module's implementation/debugging agent |
| **Interface/contract problem** | both modules conform to *different* readings of the contract | Architecture/Decomposition Agent → update contract, re-freeze, then fix both |
| **Integration logic** | both conform, composition still wrong (ordering, retries, transaction boundary) | Integration Agent (owns the composition code/tests) |
| **Infrastructure** | environment, configuration, missing service, permissions, resource limits | human / orchestration (infrastructure owner) |
| **Requirements** | the system does what was specified, but the specification is wrong | human → change request |

Rules

- Never fix an integration failure by editing another module's internals. Report and assign.
- Never loosen a contract or a test to make integration pass; that converts a discovery into
  hidden debt.
- Always record the attribution in the report, even when the fix was quick: attribution data is
  what reveals weak decomposition over time.

## 5. Milestone verdict inputs

| Input | Source |
|---|---|
| all modules `validated` | `state/modules.yaml` |
| integration report | `reports/integration-<milestone>-<date>.md` |
| testing reports | `reports/testing-*.md` |
| UX sign-off for UI changes | PRs + `docs/ux/visual_validation.md` |
| security checks | CI security job / manual review |
| known limitations & accepted risks | reports + `docs/project/risks.md` |

## 6. Anti-patterns

| Anti-pattern | Consequence |
|---|---|
| Integrating only at the end of the milestone | failures discovered when fixing is most expensive |
| Validating with mocks and calling it integration | proves nothing about composition |
| Silent monkey-patching of another module to unblock | hides a contract problem; it returns later, bigger |
| Integration on a stale baseline | re-work; always rebase first |
| Treating a green contract test as a green user journey | contract tests do not exercise journeys |
