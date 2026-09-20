# PROJECT-001 — Project lifecycle

```yaml
module_id: PROJECT-001
name: Project lifecycle
status: validated
priority: must
kind: library
purpose: "Own projects end to end: creation, editing, archiving, reversible deletion, attention rules and membership, exposed as read models and commands."

requirement_refs: ["FR-PROJ-1", "FR-DASH-1", "NFR-PERF-2"]
ux_refs: ["UX-004"]
architecture_refs:
  - "docs/project/architecture.md#6-interfaces"
  - "ADR-001"

owns:
  - src/projects/**
  - tests/projects/**
allowed_to_modify:
  - src/projects/**
  - tests/projects/**
  - db/migrations/0003_projects.sql
  - modules/PROJECT-001.md
forbidden_to_modify:
  - src/auth/**
  - src/users/**
  - src/billing/**
  - state/project.yaml

depends_on: ["USER-001"]
blocks: ["DASH-001", "NOTIFY-001"]

interfaces:
  provides:
    - name: IF-PROJECT-READ
      kind: library
      contract: docs/project/architecture.md#6-interfaces
      version: v1
      consumers: ["DASH-001"]
      test: "tests/projects/project-read.contract.test.ts"
    - name: IF-PROJECT-COMMAND
      kind: library
      contract: docs/project/architecture.md#6-interfaces
      version: v1
      consumers: ["DASH-001"]
      test: "tests/projects/project-command.contract.test.ts"
    - name: EV-PROJECT-ASSIGNED
      kind: event
      contract: docs/project/architecture.md#6-interfaces
      version: v1
      consumers: ["NOTIFY-001"]
      test: "tests/projects/events.contract.test.ts"
  requires:
    - name: IF-USER-PORT
      from: USER-001
      contract: modules/USER-001.md
      frozen: true

data:
  owns_entities: ["Project", "Membership (roles)"]
  reads: ["User"]
  migrations: ["db/migrations/0003_projects.sql"]
  retention: "soft delete with a 10 second recovery window, then hard delete"
security:
  - "every read and command calls requireProjectAccess(userId, projectId, action)"
  - "ownership rule BR-1/BR-2 enforced here, never in the UI"
performance:
  - "listProjectsForUser p95 < 120 ms at 1000 projects (NFR-PERF-2)"
  - "listAttentionItems p95 < 150 ms for 200 projects"
testing:
  - "unit tests per criterion, including the urgency ordering rule"
  - "contract tests for IF-PROJECT-READ and IF-PROJECT-COMMAND"
  - "authz matrix test covering every route action"
validation:
  - command: python scripts/verify.py
    expects: exit 0
  - command: python scripts/tp.py validate
    expects: exit 0

acceptance_criteria:
  - id: AC-1
    criterion: "creating a project with only a name succeeds in one step (AC-FR-PROJ-1.1)"
    evidence: "tests/projects/create.test.ts::creates_with_name_only"
  - id: AC-2
    criterion: "deletion is confirmed and recoverable for 10 seconds (AC-FR-PROJ-1.2)"
    evidence: "tests/projects/delete.test.ts::undo_window_restores_project"
  - id: AC-3
    criterion: "archiving hides a project without deleting data (AC-FR-PROJ-1.3)"
    evidence: "tests/projects/archive.test.ts::archive_preserves_rows"
  - id: AC-4
    criterion: "attention ordering is overdue-first then due within 7 days (AC-FR-DASH-1.1)"
    evidence: "tests/projects/attention.test.ts::orders_by_urgency"

definition_of_done:
  - all acceptance criteria evidenced
  - both contract tests passing
  - authz matrix test green
  - migration reversible and reviewed
  - reviewed by a different agent instance than the author

open_questions: []
known_risks: ["RISK-003"]
shared_zones_touched: ["db/migrations/**"]
owner_agent: impl-project-001
```

## Purpose

Own the project as a domain object: its lifecycle, its attention semantics and who may do what. This
is the module that decides "what needs attention", which the dashboard merely presents.

## Responsibilities

- create, edit, archive, restore and delete projects
- membership and role assignment for projects (using user data from `USER-001`)
- attention rules: overdue first, then due within a configurable window
- emitting `EV-PROJECT-ASSIGNED` on assignment (an event, not an import — no dependency on NOTIFY-001)
- exposing membership roles for authorization decisions

## Non-responsibilities

- presenting attention items → `DASH-001` (read model consumer)
- notification storage and delivery → `NOTIFY-001` (subscriber to `EV-PROJECT-ASSIGNED`)
- identity, sessions and credentials → `AUTH-001`, `USER-001`
- the projects UI screens beyond data contracts → `DASH-001`

## Interfaces

### Provides

`IF-PROJECT-READ`: `listProjectsForUser`, `listAttentionItems`, `listRecentActivity` — pure read
models, never throwing on empty results. `IF-PROJECT-COMMAND`: `createProject`, `updateProject`,
`archiveProject`, `deleteProject`, `restoreProject`. Both frozen before implementation.

### Requires

`IF-USER-PORT` (frozen) for actor/assignee data. Deliberately **no** import of `NOTIFY-001`: assignment
emits `EV-PROJECT-ASSIGNED`, which `NOTIFY-001` subscribes to (wired by the app shell). This keeps the
dependency one-way and guarantees a notification failure can never fail the command
(`AC-FR-NOTIF-1.2`).

## Data

Owns `Project` and the membership role table; reads `User` through the port. Invariants: a project has
exactly one owner; archived projects keep their rows; soft-deleted projects are recoverable for 10
seconds.

## Security

Authorization is enforced server-side for every read and command through
`requireProjectAccess`; BR-2 (only the owner deletes) is enforced there and covered by the authz matrix
test. Input validation happens at the HTTP boundary.

## Performance

`listProjectsForUser` p95 < 120 ms at 1 000 projects using a covering index on (owner_id, archived_at,
due_date); attention queries avoid N+1 by joining memberships once. Measured in CI with the benchmark
factory.

## Testing

Unit tests per criterion, contract tests for both ports, an authz matrix test over every route action,
migration up/down, and a determinism check that injects the clock for due-date logic.

## Acceptance criteria

| ID | Criterion | Evidence |
|---|---|---|
| AC-1 | one-step creation | `tests/projects/create.test.ts` |
| AC-2 | 10 s undo window | `tests/projects/delete.test.ts` |
| AC-3 | archive preserves rows | `tests/projects/archive.test.ts` |
| AC-4 | urgency ordering | `tests/projects/attention.test.ts` |

## Definition of done

Per the YAML list. The review must be performed by an instance other than `impl-project-001`.

## Example usage

```ts
const attention = await projectRead.listAttentionItems(session.userId, 7);
const project = await projectCommand.createProject({ ownerId: session.userId, name: "Launch site" });
```

## Open questions

| ID | Question | Blocks | Owner |
|---|---|---|---|
| — | none | — | — |

## Known risks

| ID | Risk | Mitigation |
|---|---|---|
| RISK-003 | timezone handling around due dates | store UTC, render in the user's timezone, inject the clock in tests |

## Change log

| Date | Change | By | Reference |
|---|---|---|---|
| 2026-03-05 | contract created | decomposition | — |
| 2026-03-10 | implemented, under review | impl-project-001 | PR #18 |
| 2026-03-11 | validated after review fixes | rev-project-001 | PR #18 |
