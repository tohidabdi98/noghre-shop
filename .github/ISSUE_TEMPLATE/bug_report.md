---
name: Bug report
about: Something behaves incorrectly. Use this when the specification is right and the code is wrong.
title: "[bug] "
labels: ["bug"]
---

<!--
  A bug means: the documents say X, the system does Y. If the specification is wrong instead, use
  the "Change request" template — it takes a different route (docs/workflows/change_management.md).
  Defects that block a module should also be recorded in the module's status (blocked_reasons).
-->

## What happened

<!-- Observable behaviour, including the exact wording of any error message. -->

## What should happen

- **Requirement / criterion:** `FR-###` / `AC-…` / `UX-###`
- **Expected behaviour:**

## Reproduction

```bash
# exact steps or commands, from a clean checkout
```

- **Environment:** commit/branch, OS, runtime version, browser (if UI)
- **Reproducible:** always / intermittent (n of m) / once

## Evidence

- Server output / stack trace:
- Screenshot or recording (UI):
- Correlation id:

## Impact

- **Severity:** S1 blocks everything · S2 blocks a module · S3 degrades work · S4 annoyance
- **Affected modules:** `MODULE-ID`s
- **Data impact:** none / possible corruption / loss (stop and escalate if loss is possible)
- **Security impact:** yes/no (if yes, see `docs/workflows/security.md` §8)

## Suspected origin (optional)

- [ ] module defect
- [ ] contract/interface ambiguity
- [ ] integration logic
- [ ] infrastructure/configuration
- [ ] requirements (this is really a change request)
