# CR-### — <change title>

- **Status:** proposed | analysing | approved | rejected | implemented | verified
- **Requested by:** <human name | agent-id>
- **Date:** YYYY-MM-DD
- **Approver:** <human name> (or "mechanical — owned by <agent-id>")
- **Type:** requirement | ux | architecture | module-boundary | scope | compliance | infrastructure

## 1. Summary

<!-- One paragraph: what is changing and why. Include the trigger (user feedback, discovery,
     performance finding, security issue, cost, regulation). -->

## 2. Motivation

- Current behaviour / specification:
- Why it is no longer right:
- Cost of not changing:

## 3. Requested change

<!-- Precise. If it changes a requirement, give the new text. If it changes an interface, give the
     new shape. Ambiguous change requests are the main cause of agent rework. -->

## 4. Impact analysis

| Area | Affected items | Impact | Action |
|---|---|---|---|
| Requirements | `FR-###`, `NFR-###` | | update text + `requirements.yaml` status |
| UX | `UX-###`, `UF-##`, screens | | update `docs/ux/*` |
| Architecture | components, interfaces | | `ADR-###` |
| Data | entities, migrations | | migration + rollback plan |
| Modules | `MODULE-ID`s | | contract updates, re-open, re-freeze |
| Dependencies | `state/dependencies.yaml` edges | | re-freeze affected edges |
| Agents / PRs | open branches, in-flight PRs | | rebase / close / hand off |
| Tests | existing coverage now wrong | | update or delete with reason |
| CI / infra | | | |
| Docs | | | |
| Cost / schedule | | | |

## 5. Decisions required

| Question | Options | Recommendation `[REC]` | Decision `[DECISION]` |
|---|---|---|---|
| | | | |

## 6. Migration / rollback

- Migration steps:
- Data implications:
- Rollback plan:
- Feature flag / gradual rollout:

## 7. Validation plan

| What proves the change worked | How | Evidence |
|---|---|---|

## 8. Sequence of work after approval

1. <!-- documents first -->
2. <!-- contracts/state second -->
3. <!-- implementation waves -->
4. <!-- validation and human approval -->

## 9. Outcome

- **Approved by / date:**
- **Implemented in:** PRs / commits
- **Verified by:**
- **Notes / follow-ups:**
