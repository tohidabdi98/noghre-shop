---
name: Module proposal / tasking
about: Propose a module boundary, or task an implementation agent with an existing module.
title: "[MODULE-001] "
labels: ["module"]
---

<!--
  Two uses:
   1) Decomposition: propose a new module boundary (the Decomposition Agent writes the contract).
   2) Tasking: hand a ready module to an implementation agent, including its context pack.
  A module may not start until it passes the readiness test in docs/workflows/parallelism.md §1.
-->

## Purpose

<!-- One sentence: what this module is for, for whom. -->

## Boundary

- **Module ID:** `MODULE-001`
- **Kind:** library | service | ui | job | config | infra
- **Owns (paths):**
- **Allowed to modify:**
- **Forbidden to modify:** (list the tempting neighbours explicitly)
- **Shared zones touched:** (each must already have an owner in `state/project.yaml`)

## Dependencies

| Direction | Module | Type | Interface | Frozen? |
|---|---|---|---|---|
| depends on | | contract / data / runtime / build / ui | | yes/no |
| consumed by | | | | |

## Traceability

- **Requirements:** `FR-###`, `NFR-###`
- **UX:** `UX-###` (required when the module has a UI)
- **Architecture:** `docs/project/architecture.md#…`, `ADR-###`

## Acceptance criteria

| ID | Criterion | Evidence expected |
|---|---|---|
| AC-1 | | test / command / screenshot |

## Validation commands

```bash
python scripts/verify.py         # expected: exit 0
python scripts/tp.py validate    # expected: exit 0
```

## Readiness checklist (orchestrator)

- [ ] contract exists and passes `python scripts/tp.py validate`
- [ ] all dependencies are `validated` / `complete`
- [ ] consumed interfaces are `frozen` in `state/dependencies.yaml`
- [ ] no open question blocks it
- [ ] ownership does not intersect an in-progress module
- [ ] a reviewer is available

## Tasking (when starting)

- **Agent:** `impl-module-001`
- **Branch:** `agent/impl-module-001/MODULE-001`
- **Context pack:** `python scripts/tp.py context --module MODULE-001 --agent impl-module-001`
- **Started with:** `python scripts/tp.py start --module MODULE-001 --agent impl-module-001`
- **Reviewer:** `<review agent id or human>`
