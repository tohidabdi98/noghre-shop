---
name: Change request (post-approval)
about: A significant change to approved requirements, UX, architecture or module boundaries.
title: "[CR] "
labels: ["change-request", "needs-human"]
---

<!--
  Use this when the project has already passed a gate and the truth must change. For a small,
  impact-free edit, record a DEC-### in docs/project/decisions.md in the same PR instead.
  Full process: docs/workflows/change_management.md · Template: docs/templates/change_request.md
-->

## 1. Summary

<!-- One paragraph: what changes and why (trigger: user feedback, performance, security, cost). -->

## 2. Type

- [ ] requirement
- [ ] ux
- [ ] architecture
- [ ] module boundary / ownership
- [ ] scope / milestone
- [ ] compliance / security
- [ ] infrastructure

## 3. Requested change (be precise)

<!-- New requirement text, new interface shape, new boundary. Ambiguity here becomes agent rework. -->

## 4. Impact analysis

| Area | Affected items | Impact | Action |
|---|---|---|---|
| Requirements | `FR-###`, `NFR-###` | | update text + `requirements.yaml` status |
| UX | `UX-###`, screens | | update `docs/ux/*` |
| Architecture | interfaces, components | | `ADR-###` |
| Data | entities, migrations | | migration + rollback |
| Modules | `MODULE-ID`s | | contract updates, reopen, re-freeze |
| Dependencies | `state/dependencies.yaml` | | re-freeze affected edges |
| In-flight work | branches, PRs, agents | | rebase / close / hand off |
| Tests | now-obsolete assertions | | update or delete with reason |
| CI / infra | | | |
| Cost / schedule | | | |

## 5. Decisions required

| Question | Options | Recommendation | Decision |
|---|---|---|---|
| | | | |

## 6. Migration / rollback

- Migration steps:
- Data implications:
- Rollback plan:
- Feature flag / rollout:

## 7. Validation plan

| What proves it worked | How | Evidence |
|---|---|---|
| | | |

## 8. Approval

- [ ] Approved by `<human>` on `<date>` — `CR-###` recorded in `docs/project/change_requests/`
- [ ] Documents updated before implementation restarts
- [ ] Affected modules reopened in `state/modules.yaml`
- [ ] Interfaces re-frozen before parallel work resumes
