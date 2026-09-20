# NOTIFY-001 — Notifications

```yaml
module_id: NOTIFY-001
name: Notifications
status: planned
priority: should
kind: service
purpose: "Own notification records and delivery: assignment notifications in-app and by email digest, with retries that never block the caller."

requirement_refs: ["FR-NOTIF-1", "NFR-OBS-1"]
ux_refs: ["UX-006"]
architecture_refs:
  - "docs/project/architecture.md#6-interfaces"
  - "docs/project/architecture.md#8-observability"

owns:
  - src/notifications/**
  - tests/notifications/**
allowed_to_modify:
  - src/notifications/**
  - tests/notifications/**
  - db/migrations/0004_notifications.sql
  - modules/NOTIFY-001.md
forbidden_to_modify:
  - src/projects/**
  - src/users/**
  - src/billing/**
  - src/app/routes.ts
  - state/project.yaml

depends_on: ["PROJECT-001", "USER-001"]
blocks: []

interfaces:
  provides:
    - name: IF-NOTIFY-PORT
      kind: event
      contract: docs/project/architecture.md#61-internal-interfaces-module--module
      version: v1
      consumers: ["EV-PROJECT-ASSIGNED subscriber"]
      test: "tests/notifications/notify-port.contract.test.ts"
    - name: IF-NOTIFY-READ
      kind: library
      contract: docs/project/architecture.md#61-internal-interfaces-module--module
      version: v1
      consumers: ["DASH-001"]
      test: "tests/notifications/read.contract.test.ts"
  requires:
    - name: IF-USER-PORT
      from: USER-001
      contract: modules/USER-001.md
      frozen: true
    - name: IF-PROJECT-READ
      from: PROJECT-001
      contract: modules/PROJECT-001.md
      frozen: true

data:
  owns_entities: ["Notification"]
  reads: ["User"]
  migrations: ["db/migrations/0004_notifications.sql"]
  retention: "90 days, then purged by a scheduled job"

security:
  - "a user can only read their own notifications (enforced server-side)"
  - "email content contains no secrets and no data beyond the notification payload"
performance:
  - "notifyAssignment enqueues in < 50 ms; delivery is asynchronous"
  - "markRead p95 < 60 ms"
testing:
  - "unit tests per criterion, including duplicate suppression"
  - "contract tests for both provided interfaces"
  - "retry/backoff test with a failing mail transport stub (no network)"
validation:
  - command: python scripts/verify.py
    expects: exit 0
  - command: python scripts/tp.py validate
    expects: exit 0

acceptance_criteria:
  - id: AC-1
    criterion: "an assignment produces exactly one notification per recipient (AC-FR-NOTIF-1.1)"
    evidence: "tests/notifications/dedupe.test.ts::one_notification_per_event_key"
  - id: AC-2
    criterion: "delivery failure never fails the calling command (AC-FR-NOTIF-1.2)"
    evidence: "tests/notifications/failure.test.ts::command_succeeds_when_mail_transport_fails"
  - id: AC-3
    criterion: "mark-read works and the unread count is accurate (AC-FR-NOTIF-1.3)"
    evidence: "tests/notifications/read.contract.test.ts::unread_count_tracks_mark_read"
  - id: AC-4
    criterion: "retries use backoff and stop after 3 attempts, recording the failure (NFR-OBS-1)"
    evidence: "tests/notifications/retry.test.ts::gives_up_after_three_attempts_and_logs"

definition_of_done:
  - all acceptance criteria evidenced
  - contract tests for IF-NOTIFY-PORT and IF-NOTIFY-READ passing
  - no network access in tests (transport stubbed)
  - notification events appear in the audit log (NFR-OBS-1)
  - reviewed by an instance other than the author

open_questions: []
known_risks: ["RISK-002"]
shared_zones_touched: ["db/migrations/**"]
owner_agent: null
```

## Purpose

Deliver notifications without coupling the rest of the system to a mail provider: other modules state
*what happened*, this module decides *how* the user hears about it.

## Responsibilities

- store notification records with dedupe keys
- deliver in-app (unread count) and by email digest with retries and backoff
- expose read models for the dashboard and an audit trail for observability

## Non-responsibilities

- deciding when an assignment happens → `PROJECT-001` (this module only subscribes to its events)
- the notification centre UI → dashboard/section screens owned by `DASH-001`
- user preferences beyond a simple opt-out flag → deferred (`[OPEN]` if demanded)
- template design for the email itself beyond content rules in `docs/ux/`

## Interfaces

### Provides

`IF-NOTIFY-PORT`: `notifyAssignment({ projectId, assigneeUserId, actorUserId, projectName })` — at most
once per (assignee, project, event key); never throws into the caller. `IF-NOTIFY-READ`:
`listUnread(userId, limit)`, `unreadCount(userId)`, `markRead(userId, notificationId)`.

### Requires

`IF-USER-PORT` (frozen) for recipient email and timezone.

## Data

Owns `Notification`. Invariants: dedupe key unique per user; `readAt` set once; retention 90 days.
Sensitivity: low, but stores user ids and project names.

## Security

Server-side ownership checks on every read and mark-read. Email bodies carry only the notification
payload — no tokens, no links with embedded credentials. The mail API key comes from the environment.

## Performance

`notifyAssignment` enqueues in < 50 ms and never blocks the command path; delivery is asynchronous with
backoff (1 s, 5 s, 30 s) and gives up after 3 attempts, recording the failure for review.

## Testing

Unit tests per criterion, both contract tests, a dedupe test, a retry/backoff test with a stubbed
transport, and a log-capture test asserting no PII in logs.

## Acceptance criteria

| ID | Criterion | Evidence |
|---|---|---|
| AC-1 | exactly one notification per recipient | `tests/notifications/dedupe.test.ts` |
| AC-2 | delivery failure never blocks the caller | `tests/notifications/failure.test.ts` |
| AC-3 | mark-read and unread count accurate | `tests/notifications/read.contract.test.ts` |
| AC-4 | backoff and give-up after 3 attempts | `tests/notifications/retry.test.ts` |

## Definition of done

Per the YAML list, plus the observability requirement (`NFR-OBS-1`): assignment events must appear in
the audit log with a correlation id.

## Example usage

```ts
await notifyPort.notifyAssignment({ projectId, assigneeUserId, actorUserId, projectName });
// never throws: the assignment has already succeeded
```

## Open questions

| ID | Question | Blocks | Owner |
|---|---|---|---|
| OQ-01 | should users be able to opt out of the email digest in v1? | nothing (notification centre already shows in-app) | human |

## Known risks

| ID | Risk | Mitigation |
|---|---|---|
| RISK-002 | email provider latency or outage delays reset/assignment emails | queue + retry; the primary action never depends on delivery |

## Change log

| Date | Change | By | Reference |
|---|---|---|---|
| 2026-03-05 | contract created | decomposition | — |
| 2026-03-11 | `IF-NOTIFY-PORT` shape agreed with PROJECT-001 and frozen | architecture | ADR-001 |
