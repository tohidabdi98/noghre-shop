<!--
  Every field below is required unless marked optional. Keep it truthful: the review agent re-runs
  what you claim. `python scripts/tp.py pr-check` fails the PR when required sections are missing.
-->

## Module

- **Module ID:** `MODULE-001`
- **Contract:** `modules/MODULE-001.md`
- **Acceptance criteria addressed:** `AC-1`, `AC-2` (list them, do not say "all")

## Agent

- **Agent ID:** `impl-xxx-001`
- **Role:** implementation | debugging | integration | frontend-ux | other
- **Branch:** `agent/impl-xxx-001/MODULE-001`
- **Replaces (if any):** `impl-xxx-000` + link to `handoffs/…`
- **Human sponsor (if any):**

## Summary

<!-- What this PR does, in 3–6 lines, in behavioural terms. No implementation narration. -->

## Implementation details

<!-- The decisions a reviewer needs: structure, trade-offs, anything surprising. Link ADRs. -->

## Acceptance criteria

| Criterion | Status | Evidence |
|---|---|---|
| AC-1 | met / partially / not met | test name, command, or screenshot path |
| AC-2 | | |

## Tests executed

```text
# exact commands and results, pasted — not summarised
python scripts/verify.py         -> exit 0 (41 tests)
python scripts/tp.py validate    -> exit 0
```

## Validation results

| Check | Command | Result |
|---|---|---|
| state + contracts | `python scripts/tp.py validate` | exit 0 |
| project pipeline | `python scripts/verify.py` | exit 0 |
| ownership + conventions | `python scripts/tp.py pr-check --base main` | exit 0 |
| contract/conformance tests | | |
| end-to-end (if applicable) | | |

## Known limitations

<!-- Anything not done, not verified, or verified only in a specific environment. Honest gaps are
     cheap; discovered gaps are expensive. -->

## Potential risks

<!-- What could break, who is affected, what the rollback is. Link RISK-### or create one. -->

## Dependencies

- [ ] No new runtime dependency
- [ ] New runtime dependency → ADR: `ADR-###`, approved by: `<human name>`

## Interface changes

- [ ] No interface change
- [ ] Interface change → contract + `docs/project/architecture.md` + `state/dependencies.yaml` updated, edge re-frozen

## Data / configuration

- [ ] No data or configuration change
- [ ] Migration included and reversible: `<path>`
- [ ] New environment variable(s): `<names>` (documented in `.env.example`)

## Screenshots (required for UI changes)

| Screen | State | Widths | Notes |
|---|---|---|---|
| | default / loading / empty / error / success | 375 / 768 / 1280 | |

**UX validation:** `UX validation: passed|failed — <what was seen, one line>` (required when UI changed;
see `docs/ux/visual_validation.md`)

## Checklist

- [ ] Diff is inside the module's `allowed_to_modify` (framework-managed paths `state/**`, `handoffs/**`,
      `reports/**` and any owned shared zone excepted); nothing from `forbidden_to_modify`
- [ ] One module only (no cross-module edits)
- [ ] Tests added/updated for each criterion, including edge cases
- [ ] Documentation updated in the same PR (conventions §5)
- [ ] Contract change log updated; `state/modules.yaml` reflects the real status
- [ ] Commit messages carry `Agent:` / `Agent-Role:` / `Module:` / `Validated-With:` trailers
- [ ] I did not merge my own PR
- [ ] Known limitations and risks above are complete and honest

## Reviewer notes (optional)

<!-- Where should the reviewer look first? What worries you? -->
