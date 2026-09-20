# Requirements — Example SaaS

> **Status:** approved · **Approved by:** human · **Last updated:** 2026-03-04
> Abridged reference: the important thing is the shape — IDs, observable criteria, explicit
> out-of-scope.

## 1. Product

### 1.1 Problem statement
Freelancers and small teams track projects in scattered notes and spreadsheets. They lose track of
what changed, who owns what, and what needs attention next.

### 1.2 Vision
A calm dashboard where a solo operator can see every project, what needs attention, and what
happened recently — without configuration.

### 1.3 Target users
| Persona | Who they are | Primary goal |
|---|---|---|
| P1 | solo freelancer managing 3–15 projects | know what to do next in under 30 seconds |
| P2 | team member on a shared project | see assignments and recent activity |

### 1.4 Core use cases
| ID | Use case | Actor | Outcome | `[DECISION]` |
|---|---|---|---|---|
| UC-1 | create an account and sign in | P1 | authenticated session | yes |
| UC-2 | create and manage projects | P1 | projects with status and dates | yes |
| UC-3 | see what needs attention | P1 | dashboard with recent activity and due items | yes |
| UC-4 | get notified when something is assigned | P2 | notification in-app and by email | yes |

### 1.5 Success criteria
| ID | Criterion | Measurement | Target |
|---|---|---|---|
| SC-1 | time to first project | instrumented onboarding event | < 3 minutes |
| SC-2 | dashboard usefulness | weekly returning users | ≥ 40 % of signups |

### 1.6 Scope (in)
- email/password authentication with password reset
- projects CRUD with status and due date
- dashboard: recent activity, attention list
- notifications for assignment (`[DECISION]` in-app first, email second)

### 1.7 Out of scope (explicitly not built)
- billing and subscriptions `[DECISION]`
- realtime collaborative editing `[DECISION]`
- native mobile apps `[DECISION]`
- file attachments and comments `[DECISION]`

### 1.8 Business rules
| ID | Rule |
|---|---|
| BR-1 | a project belongs to exactly one owner; members are collaborators |
| BR-2 | only the owner may delete a project |
| BR-3 | a due date in the past is shown as overdue, never hidden |

### 1.9 Constraints and assumptions
- `[ASSUMPTION] ASM-01` users have a modern evergreen browser
- `[ASSUMPTION] ASM-02` email delivery is acceptable within ~1 minute (`[RISK] RISK-02` if not)
- `[OPEN] OQ-01` invite codes for signup: deferred until after M1

---

## 2. Functional requirements

### FR-AUTH-1 — Sign up, sign in and reset a password `[DECISION]`
- **Status:** approved · **Priority:** must
- **Actor:** P1
- **Description:** a visitor creates an account with email and password, signs in, and can reset a
  forgotten password via a single-use expiring link.
- **Acceptance criteria:**
  - [ ] AC-FR-AUTH-1.1 — invalid credentials reject with a non-enumerating error message
  - [ ] AC-FR-AUTH-1.2 — a reset link works once and expires after 30 minutes
  - [ ] AC-FR-AUTH-1.3 — sessions survive a page reload and expire after 30 days of inactivity
- **Permissions:** anonymous users may sign up, sign in and request a reset
- **State transitions:** anonymous → authenticated → anonymous (sign out, session expiry)
- **Edge cases:** unknown email on reset (no user enumeration), reused/expired token, concurrent sign-ins
- **Error behaviour:** field-level validation messages; server errors are actionable, never leaking internals
- **Related UX:** `UX-001`, `UX-002`

### FR-USER-1 — Profile and collaborators
- **Status:** approved · **Priority:** must
- **Description:** a user has a profile (display name, email, timezone) and can be added to a project
  as a collaborator with a role.
- **Acceptance criteria:**
  - [ ] AC-FR-USER-1.1 — profile changes persist and are visible to collaborators
  - [ ] AC-FR-USER-1.2 — a collaborator cannot modify or delete a project they do not own
- **Permissions:** self-service profile; owner manages collaborators
- **Edge cases:** removing yourself from a project, duplicate email invitation
- **Error behaviour:** permission failures return 403 with an explanatory message, never a stack trace
- **Related UX:** `UX-003`

### FR-PROJ-1 — Project lifecycle
- **Status:** approved · **Priority:** must
- **Description:** create, edit, archive and delete projects with name, status, due date and owner.
- **Acceptance criteria:**
  - [ ] AC-FR-PROJ-1.1 — creating a project with a name is possible in one step
  - [ ] AC-FR-PROJ-1.2 — deleting requires confirmation and is recoverable for 10 seconds
  - [ ] AC-FR-PROJ-1.3 — archiving hides a project from the active list without deleting data
- **Permissions:** owner may delete; collaborators may edit
- **State transitions:** active → archived → active; active → deleted (recoverable window)
- **Edge cases:** duplicate names allowed, empty name rejected, due date in the past allowed
- **Related UX:** `UX-004`

### FR-DASH-1 — Dashboard
- **Status:** approved · **Priority:** must
- **Description:** the dashboard shows the projects that need attention (overdue or due soon), the
  most recent activity, and a shortcut to create a project.
- **Acceptance criteria:**
  - [ ] AC-FR-DASH-1.1 — the attention list shows overdue and due-within-7-days projects, ordered by urgency
  - [ ] AC-FR-DASH-1.2 — recent activity shows the last 10 events with actor and time
  - [ ] AC-FR-DASH-1.3 — an account with no projects sees the empty state with a create action
- **Data scope:** only projects the user owns or collaborates on
- **Edge cases:** no activity yet, 200 projects, clock skew between client and server
- **Related UX:** `UX-005`, `UX-006`

### FR-NOTIF-1 — Assignment notifications
- **Status:** approved · **Priority:** should
- **Description:** when a user is assigned to a project, they receive an in-app notification and an
  email digest entry.
- **Acceptance criteria:**
  - [ ] AC-FR-NOTIF-1.1 — assignment produces exactly one notification per recipient
  - [ ] AC-FR-NOTIF-1.2 — notification delivery failure never blocks the assignment itself
  - [ ] AC-FR-NOTIF-1.3 — a user can mark notifications read; unread count is accurate
- **Failure behaviour:** the notification port retries with backoff; after 3 failures it is recorded
  for review rather than retried forever
- **Related UX:** `UX-006`

---

## 3. Non-functional requirements

| ID | Category | Requirement | Target | Verification |
|---|---|---|---|---|
| NFR-PERF-1 | performance | dashboard interactive for 200 projects | p95 < 400 ms server, LCP < 2.0 s | load test + browser trace |
| NFR-PERF-2 | performance | project list query | p95 < 150 ms at 1 000 rows | query benchmark in CI |
| NFR-SEC-1 | security | passwords hashed with argon2id; sessions in httpOnly cookies | no plaintext, no token in localStorage | code review + test |
| NFR-SEC-2 | security | authorization enforced server-side on every project route | 100 % of routes covered by an authz test | route matrix test |
| NFR-A11Y-1 | accessibility | WCAG 2.2 AA on all screens | zero blocking audit findings | axe + manual sweep (`docs/ux/screens.md`) |
| NFR-OBS-1 | observability | request logs with correlation id; assignment events counted | every mutation produces a log line | review of log output |
| NFR-MAINT-1 | maintainability | module boundaries enforced in CI | no cross-module imports | dependency check |

---

## 4. Data

| Entity | Owning module | Sensitivity | Retention |
|---|---|---|---|
| User | USER-001 | personal data (email, name) | until deletion request + 30 days |
| Session / reset token | AUTH-001 | secret material (hashed) | session 30 days idle; reset token 30 min |
| Project | PROJECT-001 | low | until deleted (soft delete 10 s) |
| Notification | NOTIFY-001 | low | 90 days |

## 5. Integrations
| Service | Purpose | Auth model | Failure behaviour |
|---|---|---|---|
| transactional email | password reset + assignment digest | API key in environment | queue and retry; never block the primary action |

## 6. Engineering requirements
Testing per `docs/project/definition_of_done.md`; conventions in `docs/project/conventions.md`.

## 7. Open items
`[OPEN] OQ-01` invite codes (deferred) · `[ASSUMPTION] ASM-01`, `ASM-02` · `[RISK] RISK-02` email latency.
