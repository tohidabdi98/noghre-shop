# Change requests

Every significant change to requirements, UX, architecture, or module boundaries goes through
here — including changes requested by the human mid-project.

- **Template:** `docs/templates/change_request.md`
- **Process:** `docs/workflows/change_management.md`
- **Naming:** `CR-###-short-slug.md` (one file per change request; never renumber)
- **State:** `proposed → analysing → approved | rejected → implemented → verified`
- **Who approves:** the human usually; the owning agent when the change is purely mechanical
  (e.g. a typo in a contract that changes no behaviour).

A change request is **not** a bug report. Bugs follow `docs/workflows/failure_recovery.md` unless
the fix requires changing an approved requirement or contract.

After a CR is approved, the following must be updated in one coherent pass before implementation
restarts:

```
docs/project/requirements.md (+ requirements.yaml)
docs/ux/*                      (if UX is affected)
docs/project/architecture.md   (if interfaces or components are affected)
docs/project/decisions.md      (ADR-### or DEC-###)
modules/<ID>.md                (affected contracts, with change-log entries)
state/dependencies.yaml        (re-freeze affected edges)
state/modules.yaml             (re-open affected modules)
```
