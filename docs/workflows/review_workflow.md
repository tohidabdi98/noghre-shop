# Review workflow

Review answers one question: **does this change satisfy its contract and the project's rules, with
evidence?** Not "do I like it".

## 1. When review happens

| Trigger | Scope | Reviewer |
|---|---|---|
| PR opened for a module | the diff + contract + evidence | review agent (or human) |
| Module moves to `awaiting_review` | acceptance criteria, interfaces, tests, docs | review agent |
| `changes_requested` → new commits | only the delta + previously blocking findings | same reviewer when possible |
| Milestone boundary | the integrated system, DoD level 3 | integration + human |
| Any change to `state/**`, `modules/**`, `docs/project/**` | process integrity | human (CODEOWNERS) |
| Security-relevant change | auth, crypto, permissions, secrets, data deletion | human, mandatory |

**Independence rule:** the agent that implemented a module may self-review before opening a PR, but
the review verdict for that module must come from a different instance (or the human).

## 2. Review inputs

1. `modules/<MODULE-ID>.md` — the contract (acceptance criteria, interfaces, ownership).
2. The PR diff (`git diff <base>...<head>`) and the PR body.
3. `docs/project/requirements.md` — the requirements cited by the contract.
4. `docs/project/architecture.md` — the interfaces it must honour.
5. `docs/ux/*` — only the `ux_refs` in the contract, for UI changes.
6. `docs/project/conventions.md`, `docs/project/definition_of_done.md`.
7. The evidence: test output, CI run, screenshots, `reports/`.
8. `python scripts/tp.py pr-check` output (ownership, conventions, PR completeness).

## 3. Procedure

1. **Re-run the evidence.** `python scripts/verify.py`, `python scripts/tp.py validate`, and the
   module's `validation` commands. Never trust a pasted result you can reproduce cheaply.
2. **Check scope discipline.** Diff ⊆ `allowed_to_modify`, ∩ `forbidden_to_modify` = ∅, no
   unrelated cleanup, no edits to other modules. Two documented allowances exist: `state/**`,
   `handoffs/**` and `reports/**` are framework-managed (every module may write them), and a module may
   write a shared zone it *owns* (`state/project.yaml → shared_zones`). Anything else is a finding.
3. **Walk the acceptance criteria** one by one; each gets PASS / FAIL / NOT VERIFIED + evidence.
4. **Check interfaces**: provided interfaces match the frozen contract; consumed interfaces are used
   as specified (no reliance on undocumented behaviour).
5. **Check tests**: one per criterion, edge cases from the contract, no weakened assertions, no
   skipped tests without a recorded reason.
6. **Check non-functional duties**: authorization, validation, error handling, logs, performance
   targets, accessibility for UI.
7. **Check documentation duties** (conventions §5): the change's docs updated in the same PR.
8. **Classify findings** (§4) and write the report (`docs/agents/templates/validation_report.md`).
9. **Give a verdict** and recommend the state transition.

## 4. Finding taxonomy (use exactly these words)

| Severity | Meaning | Effect |
|---|---|---|
| **Blocking** | contract violated, criteria unverified, security/data problem, ownership breach, evidence missing | PR cannot merge until fixed or explicitly waived by the human |
| **Non-blocking** | real problem, safe to fix after merge | must be filed as an issue/`OQ`/`RISK` before merge |
| **Suggestion** | improvement, no defect | optional; the author may decline without justification |
| **Question** | the reviewer cannot determine intent | must be answered before merge if it affects behaviour |

Every finding states: location, what was observed, what was expected (with the document reference),
the smallest acceptable fix, and an owner. Style opinions not in `conventions.md` are not findings.

## 5. Verdicts

| Verdict | Requirements |
|---|---|
| **PASS** | all criteria verified with evidence; no blocking findings |
| **PASS WITH NON-BLOCKING FINDINGS** | all criteria verified; findings filed with owners |
| **FAIL** | any criterion unverified/failed, or any blocking finding, or evidence unreproducible |

## 6. Anti-patterns

| Anti-pattern | Why it is harmful |
|---|---|
| Approving because CI is green | CI checks code, not acceptance criteria |
| "Looks good" without walking the criteria | the whole point of the contract is skipped |
| Blocking on taste | burns agent budget; use `Suggestion` |
| Silently fixing the code as a reviewer | destroys the authorship/verification boundary — assign the fix instead |
| Reviewing a diff that moved (force-push) | the verdict no longer applies to the reviewed commit |
| Trusting a pasted validation result | the cheapest possible forgery vector, and it happens by accident too |
