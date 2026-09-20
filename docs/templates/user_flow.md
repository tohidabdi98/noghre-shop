# UF-## — <flow name>

- **Owner:** frontend-ux
- **Persona:** P#
- **Goal:** <what "done" means for the user>
- **Trigger:** <what starts the flow>
- **Preconditions:** <required system/data state>
- **Success:** <observable end state>
- **Abandonment points:** <where users realistically drop out, and what the design does about it>
- **Related:** `FR-###`, `UX-###`, screens `<screen-ids>`
- **Modules touched:** `MODULE-ID`s

## Steps (happy path)

| # | User action | System response | Screen / state | Latency budget | Notes |
|---|---|---|---|---|---|
| 1 | | | | | |

## Alternative paths

| Branch | Condition | Divergence | Returns to step |
|---|---|---|---|
| A1 | | | |

## Failure paths

| Failure | Detection | User sees | Recovery | Logged |
|---|---|---|---|---|
| | | | | |

## States

| State | Where | What the user sees | Accessibility |
|---|---|---|---|
| loading | | | announced politely |
| empty | | | |
| error | | | `role="alert"` |
| success | | | |
| permission-denied | | | |

## Data touched

| Data | Read | Written | Sensitivity | Validation |
|---|---|---|---|---|

## Responsive behaviour

| Breakpoint | Behaviour |
|---|---|
| ≥ 1280 px | |
| 768–1279 px | |
| < 768 px | |

## Accessibility notes

- Keyboard path:
- Focus order / focus return:
- Announcements:
- Target sizes:

## Acceptance criteria

- [ ] UF-##-AC1 —
- [ ] UF-##-AC2 —

## Verification evidence

| Check | How | Evidence |
|---|---|---|
| happy path | browser walkthrough | screenshots |
| failure paths | forced errors | screenshots + notes |
| responsive | viewport sweep | screenshots ×3 widths |
| keyboard | keyboard-only run | notes |
