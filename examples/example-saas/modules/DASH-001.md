# DASH-001 — Dashboard

```yaml
module_id: DASH-001
name: Dashboard
status: changes_requested
priority: must
kind: ui
purpose: "Compose and present the dashboard: attention list, recent activity, create action and unread notifications, with all specified states."

requirement_refs: ["FR-DASH-1", "NFR-A11Y-1", "NFR-PERF-1"]
ux_refs: ["UX-005", "UX-006"]
architecture_refs:
  - "docs/project/architecture.md#6-interfaces"
  - "docs/project/architecture.md#62-frontend--backend"

owns:
  - src/dashboard/**
  - tests/dashboard/**
allowed_to_modify:
  - src/dashboard/**
  - tests/dashboard/**
  - modules/DASH-001.md
forbidden_to_modify:
  - src/projects/**
  - src/users/**
  - src/app/routes.ts
  - state/project.yaml

depends_on: ["USER-001", "PROJECT-001"]
blocks: []

interfaces:
  provides: []
    # This module is a leaf: it consumes read models and renders them.
  requires:
    - name: IF-PROJECT-READ
      from: PROJECT-001
      contract: modules/PROJECT-001.md
      frozen: true
    - name: IF-USER-PORT
      from: USER-001
      contract: modules/USER-001.md
      frozen: true

data:
  owns_entities: []
  reads: ["Project", "User", "Notification"]
  migrations: []
  retention: "no persistence — read models only"
security:
  - "renders only data the server already authorized; never widens visibility client-side"
  - "no session token in JavaScript (httpOnly cookie only, NFR-SEC-1)"
performance:
  - "LCP < 2.0 s and no layout shift on load for 200 projects (NFR-PERF-1)"
  - "skeleton rendered within 100 ms of navigation"
testing:
  - "component tests per state (default, loading, empty, error, success, permission-denied)"
  - "keyboard navigation test for the attention list"
  - "partial-failure test: activity section fails while attention still renders"
validation:
  - command: python scripts/verify.py
    expects: exit 0
  - command: python scripts/tp.py validate
    expects: exit 0

acceptance_criteria:
  - id: AC-1
    criterion: "attention list above the fold at 1280×800 with overdue first (AC-FR-DASH-1.1, UX-AC-005.1)"
    evidence: "tests/dashboard/layout.test.tsx + screenshots 1280"
  - id: AC-2
    criterion: "recent activity shows the last 10 events with actor and time (AC-FR-DASH-1.2)"
    evidence: "tests/dashboard/activity.test.tsx"
  - id: AC-3
    criterion: "empty account sees the empty state with exactly one primary action (AC-FR-DASH-1.3)"
    evidence: "tests/dashboard/empty.test.tsx + screenshot"
  - id: AC-4
    criterion: "all six states implemented and reachable per screens.md#screen-02 (UX-AC-005.3)"
    evidence: "BLOCKED — screenshots for loading/empty/error/success missing (review finding B1)"
  - id: AC-5
    criterion: "keyboard-only navigation works on the attention list (NFR-A11Y-1)"
    evidence: "BLOCKED — keyboard walkthrough not performed (review finding B2)"

definition_of_done:
  - all acceptance criteria evidenced
  - screenshots for all six states at 375/768/1280 attached to the PR
  - keyboard walkthrough notes in the PR
  - axe scan clean on the dashboard route
  - Frontend/UX sign-off recorded
  - NFR-PERF-1 measured with a browser trace

open_questions: []
known_risks: ["RISK-004"]
shared_zones_touched: []
owner_agent: impl-dashboard-003
```

## Purpose

Answer "what needs attention right now?" in under 30 seconds. `DASH-001` is presentation and
composition: it turns read models into a calm, ordered surface and never owns domain rules.

## Responsibilities

- compose attention, activity and create affordances on one screen
- implement all specified states, responsive behaviour and keyboard path
- keep the dashboard fast and layout-stable

## Non-responsibilities

- deciding *what* needs attention → `PROJECT-001` (`listAttentionItems`)
- mutation logic (create/update/delete) → `PROJECT-001` commands
- notification storage and unread counts → `NOTIFY-001`
- adding routes to the app shell → `APP-001` (shared zone)

## Interfaces

### Provides

None (leaf module).

### Requires

`IF-PROJECT-READ` and `IF-USER-PORT` (both frozen). The dashboard must handle `null` users, empty
results and partial failures gracefully.

## Data

No persistence. Reads project summaries, attention items, activity events and unread counts. Never
caches authorization decisions client-side.

## Security

Renders only what the server authorized. No token handling in JavaScript. Errors never echo raw server
messages to the user.

## Performance

LCP < 2.0 s for 200 projects, skeleton within 100 ms, no layout shift (skeletons match final layout
dimensions). Measured with a browser trace recorded in `reports/`.

## Testing

Component tests for every state, a partial-failure test, a keyboard navigation test, and screenshot
evidence at three widths. Visual correctness is validated per `docs/ux/screens.md#screen-02`.

## Acceptance criteria

| ID | Criterion | Evidence | Status |
|---|---|---|---|
| AC-1 | attention above the fold at 1280×800 | `tests/dashboard/layout.test.tsx` + screenshot | met |
| AC-2 | last 10 events with actor and time | `tests/dashboard/activity.test.tsx` | met |
| AC-3 | empty state with one primary action | `tests/dashboard/empty.test.tsx` | met |
| AC-4 | six states reachable | screenshots | **blocked** (finding B1) |
| AC-5 | keyboard path works | walkthrough notes | **blocked** (finding B2) |

## Definition of done

Per the YAML list. AC-4 and AC-5 remain outstanding after the first review (`changes_requested`,
PR #21) — the implementation agent must attach the missing evidence, not merely assert the states exist.

## Example usage

```tsx
const attention = await projectRead.listAttentionItems(session.userId, 7);
return <Dashboard attention={attention} activity={activity} unread={unread} />;
```

## Open questions

| ID | Question | Blocks | Owner |
|---|---|---|---|
| — | none | — | — |

## Known risks

| ID | Risk | Mitigation |
|---|---|---|
| RISK-004 | dashboard becomes a coupling magnet ("just fetch it here") | any new read model goes through `PROJECT-001`'s interfaces, never direct table access |

## Change log

| Date | Change | By | Reference |
|---|---|---|---|
| 2026-03-05 | contract created | decomposition | — |
| 2026-03-11 | first implementation attempt abandoned (agent context exhaustion) | impl-dashboard-002 | handoff to impl-dashboard-003 |
| 2026-03-12 | review returned changes_requested: missing state screenshots and keyboard walkthrough | rev-dash-001 | PR #21 |
