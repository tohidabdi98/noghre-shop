# Testing workflow

Testing exists to answer: **is each requirement actually satisfied, and what would break if it
regressed?** Coverage percentages do not answer either question.

## 1. Levels and what each level must prove

| Level | Scope | Must prove | Owner | Required in CI |
|---|---|---|---|---|
| Unit | one module, internals allowed | each acceptance criterion's logic, edge cases, error paths | module agent | yes |
| Contract | a module's provided interfaces | the interface behaves exactly as the frozen contract says (shape, errors, versioning) | module agent | yes |
| Property/fuzz (where valuable) | parsers, validators, money/time logic | invariants hold over generated input | module agent | per project |
| Integration | module ↔ module through real interfaces | data flows, ordering, failure propagation, retries | integration agent | yes |
| End-to-end | user journeys from `docs/ux/user_flows.md` | the journey completes; states are reachable | integration agent | yes (smoke) |
| Visual/UX | rendered UI | screens match the specification in every state | frontend-ux | for UI changes (`docs/ux/visual_validation.md`) |
| Performance | NFR targets | the numbers promised are met | architecture/testing | on demand + before release |
| Security | authz, input handling, dependencies | unauthorized access fails; no known vulnerable deps | testing + human | scheduled + on auth changes |
| Regression | previously fixed defects | the defect stays fixed | debugging agent | yes |

## 2. Requirement-driven coverage (the important part)

1. Build the matrix **before writing tests**:

| Requirement | Criterion | Level | Test | Status |
|---|---|---|---|---|
| `FR-AUTH-1` | AC-FR-AUTH-1.1 | unit | `tests/auth/test_reset.py::test_expires_after_use` | pass |
| `FR-AUTH-1` | AC-FR-AUTH-1.2 | e2e | `tests/e2e/test_reset_flow.py` | pass |

2. Any requirement without a test is either **tested now**, **listed as unverified with a reason**,
   or **promoted to a human-verified manual check**. Unverified requirements are a finding, not a
   footnote.
3. Delete or rewrite tests whose requirement was removed by a change request — a test asserting
   obsolete behaviour is worse than no test.

## 3. Test quality rules

| Rule | Why |
|---|---|
| A test name describes behaviour (`rejects_expired_token`), never implementation (`test_fn_3`) | reviewers need intent |
| One behaviour per test; failures must localise | debugging speed |
| Tests must be deterministic: control time, randomness, network, ordering | flakiness destroys trust in the whole suite |
| No test depends on another module's internals | breaks independent development |
| Fixtures/factories are owned by the entity's module and used through public contracts | prevents duplicated domain rules |
| Assert on outcomes, not on logs or internal call order | brittle otherwise |
| No `skip`/`xfail` without a linked issue and an owner | silent gaps |
| Test data is synthetic; never production data | privacy/security |

## 4. Running and evidence

```bash
python scripts/verify.py              # the project's typecheck/lint/test pipeline
python scripts/verify.py --list       # what it will run (and what is not configured yet)
python scripts/tp.py validate         # state + contract + docs integrity
```

Paste results into the PR (`## Tests executed`, `## Validation results`) — command **and** outcome.
A verdict without a command is not evidence.

## 5. Flaky tests

1. Quarantine immediately (mark + issue) so the suite stays trustworthy.
2. Fix or delete within the milestone; a test that fails randomly is worse than a missing test.
3. Never "retry until green" in CI as a permanent state.

## 6. Gaps that must be reported, not hidden

- requirements that cannot be verified automatically (report + propose a manual check)
- environment-dependent behaviour (integration/E2E) that the agent cannot run (report as a known
  limitation with exact steps for the human)
- UI states that were never rendered (report; do not mark validated)
- performance claims that were never measured (report as unverified)

## 7. CI expectations

| Job | Fails the build when |
|---|---|
| `ci / state-and-contracts` | state inconsistent, contract incomplete, broken doc link, notebook prompt out of sync, unreplaced placeholder |
| `ci / verify` | typecheck, lint, formatting or tests fail |
| `ci / security` (opt-in) | secret detected, vulnerable dependency, when enabled |
| `agent-pr-check` | branch/commit convention violated, ownership breach, PR body incomplete |

A red CI on a fresh copy before `bootstrap` is expected and intentional: it is the reminder that
setup is unfinished.
