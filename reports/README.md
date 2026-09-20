# reports/ — evidence

Reports are the written proof that a claim about the project is true: validation runs, reviews,
integration results, UX validation, failure analyses and orchestration boards. They are committed to
Git so a human or a later agent can audit **what was proven, by whom, when**.

## Naming

```
reports/<kind>-<MODULE-ID>-<YYYY-MM-DD>.md     per-module reports
reports/<kind>-<milestone>-<YYYY-MM-DD>.md     milestone-level reports
reports/orchestration-<YYYY-MM-DD>.md          board snapshots
```

| Kind | Written by | Required for |
|---|---|---|
| `validation` | implementation agent | every module PR (evidence of the contract's validation commands) |
| `testing` | testing agent | every module before `validated` |
| `review` | review agent | every module before `validated` |
| `ux-validation` | frontend-ux agent | every PR that changes UI |
| `integration` | integration agent | every milestone and every interface change |
| `failure` | debugging/fix agent | every failure, crash or abandoned attempt |
| `orchestration` | orchestrator | each planning session / milestone boundary |

## Rules

1. **A command and its result, or it is not evidence.** Every report contains an executed-commands
   table with real output (`exit 0`, test counts, CI run links).
2. **Reproduce, do not trust.** Reviewers re-run the reported commands; that is the point of the report.
3. **Reports are written even when the outcome is bad** — especially then. An invisible failure is how
   parallel agent work goes wrong.
4. **No secrets, no personal data, no production data** in reports. Redact; use correlation ids.
5. **Large artefacts stay out of Git** (screenshots, traces, coverage HTML): link them from the report
   (PR attachment, CI artefact) instead of committing them.
6. Templates: `docs/agents/templates/validation_report.md`, `.../failure_report.md`,
   `docs/templates/review_report.md`. Examples: `examples/example-saas/reports/`.

## Relationship to PRs

Every report referenced by a PR must also be summarised in the PR body's `Validation results` section.
The report is the detail; the PR is the summary; CI checks that required sections exist
(`python scripts/tp.py pr-check`).
