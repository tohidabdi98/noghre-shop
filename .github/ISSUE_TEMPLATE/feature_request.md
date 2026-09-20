---
name: Feature request
about: New capability or behaviour change. This is a change request, not a bug.
title: "[feature] "
labels: ["feature", "needs-triage"]
---

<!--
  Anything that changes agreed behaviour goes through docs/workflows/change_management.md:
  change request → impact analysis → decision → documents → contracts → implementation.
  Discovery produced the approved requirements; this template is how they change.
-->

## What you want

<!-- The capability or behaviour, described from the user's point of view. -->

## Why

- **Problem it solves:**
- **Who benefits:** persona / role
- **What happens today:**
- **Cost of not doing it:**

## Where it fits

- **Affected requirements:** add/modify `FR-###` / `NFR-###`
- **Affected UX:** `UX-###`, screens, flows
- **Affected modules:** `MODULE-ID`s
- **Milestone:** which milestone should carry this, and what it displaces

## Scope

- **Minimum useful version:**
- **Explicitly out of scope for now:**
- **New external services / dependencies:** (each one needs an ADR + human approval)

## Impact analysis (filled by the orchestrator / architecture agent)

| Area | Impact |
|---|---|
| Requirements | |
| UX | |
| Architecture / interfaces | |
| Data / migrations | |
| Modules (new, reopened) | |
| In-flight PRs | |
| Cost / schedule | |

## Decision

- [ ] Approved — change request: `CR-###`
- [ ] Deferred until `<event>`
- [ ] Rejected — reason:

## Definition of done for this request

- [ ] documents updated first (requirements → UX → architecture → contracts)
- [ ] affected modules re-planned and re-assigned
- [ ] implementation merged with evidence
- [ ] validation + integration re-run
- [ ] `requirements.yaml` status updated
