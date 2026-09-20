# USER-001 — Users and collaborators

```yaml
module_id: USER-001
name: Users and collaborators
status: complete
priority: must
kind: library
purpose: "Own user profiles and project membership: identity data, display preferences and collaborator roles, exposed through a read port."

requirement_refs: ["FR-USER-1", "NFR-SEC-2"]
ux_refs: ["UX-003"]
architecture_refs:
  - "docs/project/architecture.md#5-data-model"
  - "docs/project/architecture.md#6-interfaces"

owns:
  - src/users/**
  - tests/users/**
allowed_to_modify:
  - src/users/**
  - tests/users/**
  - modules/USER-001.md
forbidden_to_modify:
  - src/auth/**
  - src/billing/**
  - src/projects/**
  - state/project.yaml

depends_on: ["AUTH-001"]
blocks: ["PROJECT-001", "DASH-001", "NOTIFY-001"]

interfaces:
  provides:
    - name: IF-USER-PORT
      kind: library
      contract: docs/project/architecture.md#61-internal-interfaces-module--module
      version: v1
      consumers: ["AUTH-001", "PROJECT-001", "NOTIFY-001", "DASH-001"]
      test: "tests/users/user-port.contract.test.ts"
  requires: []

data:
  owns_entities: ["User", "Membership"]
  reads: []
  migrations: ["db/migrations/0001_users_and_memberships.sql"]
  retention: "profile data is deleted 30 days after an account deletion request"

security:
  - "email uniqueness enforced case-insensitively at the database level"
  - "no password or token material stored here (that belongs to AUTH-001)"
  - "role checks are exposed for callers; enforcement happens in the owning module"
performance:
  - "getUserByEmail p95 < 20 ms with the unique index"
testing:
  - "unit tests per acceptance criterion"
  - "contract test for IF-USER-PORT (null for missing user, no throwing)"
validation:
  - command: python scripts/verify.py
    expects: exit 0
  - command: python scripts/tp.py validate
    expects: exit 0

acceptance_criteria:
  - id: AC-1
    criterion: "profile changes persist and are visible to collaborators (AC-FR-USER-1.1)"
    evidence: "tests/users/profile.test.ts::updates_display_name_and_timezone"
  - id: AC-2
    criterion: "a collaborator cannot modify or delete a project they do not own (AC-FR-USER-1.2)"
    evidence: "tests/users/roles.test.ts::collaborator_cannot_delete_owned_project"
  - id: AC-3
    criterion: "role changes are reflected in IF-USER-PORT results without restart"
    evidence: "tests/users/user-port.contract.test.ts::role_changes_are_visible"

definition_of_done:
  - all acceptance criteria evidenced
  - IF-USER-PORT contract test passing
  - migration reviewed and reversible
  - state and docs updated in the same PR

open_questions: []
known_risks: []
shared_zones_touched: []
owner_agent: impl-user-001
```

## Purpose

Own the person behind a session: profile data, timezone, and which projects they can reach and with
what role. Other modules ask this module; they never query user tables themselves.

## Responsibilities

- user profile storage and updates (display name, email, timezone)
- membership records and roles per project
- exposing `IF-USER-PORT` with predictable `null` semantics

## Non-responsibilities

- credentials, sessions and password reset → `AUTH-001`
- authorization decisions on project actions → `PROJECT-001` (using roles read here)
- notification preferences and delivery → `NOTIFY-001`
- profile UI composition → `DASH-001`/`PROJECT-001` screens

## Interfaces

### Provides

`IF-USER-PORT`: `getUser(userId)`, `getUserByEmail(email)`; returns `null` when absent, throws only on
infrastructure failure. Frozen before implementation; consumers (`AUTH-001`, `PROJECT-001`,
`NOTIFY-001`, `DASH-001`) must not assume non-null.

### Requires

None. This is the base of the dependency graph for data (`AUTH-001` is a build-order dependency only
for shared error types).

## Data

Owns `User` and `Membership`. Invariants: email unique (case-insensitive); a membership is unique per
(project, user); deleting a user cascades to memberships. Sensitivity: personal data (`NFR-PRIV-1`).

## Security

No credential material. Authorization checks are exposed as helpers but enforced by the owning module.
Deletion requests cascade and are audited.

## Performance

`getUser` p95 < 15 ms; `getUserByEmail` p95 < 20 ms with the unique index. No N+1 in list endpoints.

## Testing

Unit tests per criterion, contract test for `IF-USER-PORT`, migration up/down test, and a test that
personal data does not appear in logs.

## Acceptance criteria

| ID | Criterion | Evidence |
|---|---|---|
| AC-1 | profile changes persist and are visible | `tests/users/profile.test.ts` |
| AC-2 | collaborator cannot modify/delete a non-owned project | `tests/users/roles.test.ts` |
| AC-3 | role changes visible through the port | `tests/users/user-port.contract.test.ts` |

## Definition of done

Per the YAML list, plus: migration reviewed by the review agent and reversible, and no PII in logs
verified by a log-capture test.

## Example usage

```ts
const user = await userPort.getUser(session.userId);
if (!user) return unauthorized("user_missing");
```

## Open questions

| ID | Question | Blocks | Owner |
|---|---|---|---|
| — | none | — | — |

## Known risks

| ID | Risk | Mitigation |
|---|---|---|
| — | none recorded | — |

## Change log

| Date | Change | By | Reference |
|---|---|---|---|
| 2026-03-05 | contract created | decomposition | — |
| 2026-03-08 | implemented and validated | impl-user-001 | PR #15 |
