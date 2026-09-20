# User flows — Example SaaS (abridged)

| ID | Flow | Persona | Entry | Screens | Modules | Priority |
|---|---|---|---|---|---|---|
| UF-01 | Sign up, then create a first project | P1 | landing page | `signup`, `dashboard` | AUTH-001, PROJECT-001, DASH-001 | must |
| UF-02 | Check what needs attention | P1 | bookmark / app root | `dashboard` | DASH-001, PROJECT-001 | must |
| UF-03 | Assign a collaborator and notify them | P1/P2 | project screen | `project`, `dashboard` | PROJECT-001, NOTIFY-001, USER-001 | should |

## UF-01 — Sign up, then create a first project

**Actor:** P1 · **Goal:** be inside a project with a name in under 3 minutes · **Trigger:** landing page CTA
**Preconditions:** none · **Success:** project visible on the dashboard, onboarding not repeated

| # | User action | System response | Screen / state |
|---|---|---|---|
| 1 | submits email + password | validates, creates user + session | signup / loading → success |
| 2 | (no email verification in v1) | lands on empty dashboard | dashboard / empty |
| 3 | clicks "Create project" | dialog with a single field | modal / default |
| 4 | enters a name, submits | project created, dialog closes, list updated optimistically | dashboard / success |
| 5 | — | row appears in attention list if a due date is set | dashboard / default |

**Failure paths**

| Failure | Detection | User sees | Recovery |
|---|---|---|---|
| email already registered | server 409 | "that email already has an account" + sign-in link | sign in |
| weak password | client + server validation | inline rule list, input preserved | correct |
| submit fails (network) | timeout | banner + retry, input preserved | retry |

**States:** loading (skeleton rows) · empty (one primary action) · error (banner + retry) ·
success (row + confirmation) · permission-denied (not applicable)

**Acceptance criteria**
- [ ] UF-01-AC1 signup → project created in ≤ 3 actions after the CTA
- [ ] UF-01-AC2 onboarding is not shown again on the next visit
- [ ] UF-01-AC3 every failure path preserves input

**Verification:** browser walkthrough (screenshots at 375/768/1280) · keyboard-only run · axe scan clean

## UF-02 — Check what needs attention

**Actor:** P1 · **Goal:** know the next action in under 30 seconds · **Trigger:** opening the app
**Success:** the attention list is visible without scrolling on a 1280×800 viewport

| # | User action | System response | Screen / state |
|---|---|---|---|
| 1 | opens the app | session resolved; attention + activity fetched | dashboard / loading → default |
| 2 | scans the attention list | overdue first, then due within 7 days | dashboard / default |
| 3 | clicks an item | opens the project | project / default |

**Failure paths**

| Failure | User sees | Recovery |
|---|---|---|
| attention query fails | section-level error, activity still shown | retry button |
| slow query (> 1 s) | skeleton retained, no layout jump | auto-resolve |

**Acceptance criteria**
- [ ] UF-02-AC1 attention list is above the fold at 1280×800
- [ ] UF-02-AC2 overdue is indicated by text, not colour alone
- [ ] UF-02-AC3 partial failure degrades only its own section

**Verification:** browser walkthrough · throttled network test · screenshots ×3 widths

## UF-03 — Assign a collaborator and notify them

| # | User action | System response |
|---|---|---|
| 1 | opens project → collaborators | list with roles |
| 2 | adds a collaborator by email | membership created, role applied |
| 3 | — | assignment notifies the collaborator (in-app + digest entry) |
| 4 | collaborator opens the app | unread count and dashboard activity item |

**Failure path:** notification delivery fails → the assignment still succeeds (AC-FR-NOTIF-1.2),
the failure is logged and retried, and the user is never blocked.
