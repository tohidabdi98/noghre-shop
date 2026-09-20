# Validation report — <MODULE-ID> (<testing | review | integration | ux-validation>)

- **Agent:** `<agent-id>` (`<role>`)
- **Date:** YYYY-MM-DD
- **Artifact validated:** branch `agent/<agent-id>/<MODULE-ID>`, commits `<sha>..<sha>`, PR #`<n>`
- **Baseline:** `<default-branch>` @ `<sha>`
- **Verdict:** PASS | PASS WITH FINDINGS | FAIL

## 1. Method (what was actually executed)

| # | Command / action | Purpose | Result |
|---|---|---|---|
| 1 | `python scripts/tp.py validate` | state and contract integrity | exit 0 |
| 2 | `python scripts/verify.py` | typecheck / lint / tests | exit 0 |
| 3 | | | |

Raw output: attach or link (`reports/…`, CI run URL). **No verdict without a command.**

## 2. Requirement and criterion coverage

| Requirement | Acceptance criterion | Verdict | Evidence |
|---|---|---|---|
| `FR-###` | AC-1 | PASS / FAIL / NOT VERIFIED | test name, file:line |

## 3. Interface / contract conformance

| Interface | Direction | Conformance | Notes |
|---|---|---|---|
| | provided / consumed | pass / fail | |

## 4. Findings

| # | Severity | Area | Finding | Expected | Fix | Owner | State |
|---|---|---|---|---|---|---|---|
| 1 | blocking / non-blocking / suggestion / question | | | | | | open |

## 5. Gaps in coverage (requirement-driven)

| Unverified requirement | Why automated verification is impossible | Proposed manual check | Who performs it |
|---|---|---|---|

## 6. Non-functional checks

| Area | Check | Result |
|---|---|---|
| Security | authorization enforced, inputs validated, no secret exposure, dependency audit | |
| Performance | contract targets measured (numbers, not adjectives) | |
| Accessibility | scan + keyboard walkthrough (UI changes) | |
| Observability | logs/metrics exist for the new behaviour | |
| Reproducibility | validated in a clean environment, not only the author's machine | |

## 7. Evidence inventory

| Evidence | Location |
|---|---|
| test output | |
| screenshots | |
| CI run | |
| logs / traces | |

## 8. Verdict and next state

- **Mergeable:** yes | no | after fixes
- **Required before merge:** <list>
- **Recommended state transition:** `awaiting_review` → `validated` | `changes_requested`
- **Follow-ups filed:** <issue links, `OQ-###`, `RISK-###`>
