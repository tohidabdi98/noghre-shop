# Failure report — <MODULE-ID or area>

- **Reported by:** `<agent-id | human>`
- **Date:** YYYY-MM-DD
- **Severity:** S1 blocks everything · S2 blocks a module · S3 degrades work · S4 annoyance
- **Failure type:** agent_crash | bad_implementation | wrong_assumption | test_failure | ci_failure |
  merge_conflict | contract_break | architecture_change | requirement_change | stale_context |
  bad_decomposition | partial_work | integration_failure | environment
- **Owner of the fix:** `<agent-id | human>`
- **Status:** open | mitigating | fixed | verified | accepted-as-risk

## 1. What happened

<!-- Observable facts only: what was run, what was expected, what occurred, when. No blame, no
     speculation in this section. -->

## 2. Reproduction

```bash
# exact commands, from a clean checkout
```

- Reproducible: always | intermittent (< n > of < m > runs) | once (with trace/time)
- Environment: branch/commit, OS, runtime version, relevant env vars (never secrets)

## 3. Evidence

| Evidence | Location |
|---|---|
| logs / stack trace | |
| failing command output | |
| CI run | |
| screenshots | |

## 4. Root cause

<!-- The real cause, not the symptom. If it is not certain, say "hypothesis" and describe the
     experiment that would confirm it. -->

- **Cause:**
- **Ownership:** module / contract / integration logic / infrastructure / requirements / process
- **Why it was not caught earlier:**
- **Blast radius:** which modules, data, users, or states are affected

## 5. Fix

- **Smallest correct fix:**
- **Files changed** (must stay inside the owning module's allowed paths):
- **Workaround applied?** yes/no — if yes, record it in `docs/project/risks.md`
- **Regression coverage added:** test name + proof it fails before the fix
- **Validation after fix:**

| Command | Result |
|---|---|
| | |

## 6. Prevention

| Action | Owner | Where recorded |
|---|---|---|
| e.g. contract clarification | decomposition | `modules/<ID>.md` |
| e.g. test added to CI | testing | `.github/workflows/ci.yml` |
| e.g. process change | orchestrator | `docs/workflows/failure_recovery.md` |

## 7. State and schedule impact

| Item | Before | After |
|---|---|---|
| Module state | | |
| Agent assigned | | |
| Milestone impact | | |
| Requirement impact (`FR-###`) | | |

## 8. Follow-ups

| Item | Type | Owner |
|---|---|---|
| | `OQ-###` / `RISK-###` / `CR-###` / issue | |
