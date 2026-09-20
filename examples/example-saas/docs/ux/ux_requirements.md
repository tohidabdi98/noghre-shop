# UX requirements — Example SaaS (abridged reference)

> Owner: Frontend/UX Agent (ux-001) · Approved by human 2026-03-04

## 1. Personas
| Persona | Context | Devices | Accessibility |
|---|---|---|---|
| P1 solo operator | "what needs attention right now?" | laptop first, phone in the evening | keyboard-heavy user |
| P2 collaborator | "what changed and what is mine?" | laptop | screen-reader user |

## 2. UX principles
| ID | Principle | Test in review |
|---|---|---|
| PRIN-1 | attention over inventory: the first screen answers "what next?" | dashboard shows attention items above everything else |
| PRIN-2 | no configuration before value | first project creatable without settings |
| PRIN-3 | reversible by default | destructive actions offer recovery |

## 3. UX requirements

### UX-001 — Sign in is one screen with inline errors `[DECISION]`
- **Persona:** P1 · **Statement:** a returning user signs in with email + password on a single screen,
  with inline, non-enumerating errors.
- **States:** default · loading · error · success · (empty/permission not applicable)
- **Responsive:** single column, full width below 480 px; ≥ 44 px targets
- **Accessibility:** error summary announced, focus moves to the first invalid field, visible focus
- **Acceptance criteria:** [ ] UX-AC-001.1 invalid credentials show one generic error within 1 s
  [ ] UX-AC-001.2 the form is completable by keyboard only
- **Related requirement:** `FR-AUTH-1` · **Screens:** `screens.md#screen-01` · **Status:** implemented

### UX-002 — Password reset explains itself and survives failure
- **Persona:** P1 · **Statement:** the reset flow tells the user what happened at each step, without
  revealing whether an account exists.
- **States:** default · loading · error (expired/used link) · success · permission-denied (used link)
- **Accessibility:** step changes announce politely; the resend action is reachable by keyboard
- **Acceptance criteria:** [ ] UX-AC-002.1 expired/used links show recovery copy plus a resend action
- **Related requirement:** `FR-AUTH-1` · **Status:** implemented

### UX-003 — Profile and collaborators are editable in place
- **Persona:** P2 · **Statement:** a collaborator sees their role and can leave; an owner manages
  roles without leaving the project screen.
- **States:** default · loading · empty (no collaborators) · error · success · permission-denied
- **Accessibility:** role selector is a native-accessible control with visible labels
- **Acceptance criteria:** [ ] UX-AC-003.1 permission-denied is explanatory, not an error state
- **Related requirement:** `FR-USER-1` · **Status:** implemented

### UX-004 — Project creation takes one step and one field
- **Persona:** P1 · **Statement:** a project is created with only a name; status and due date are
  optional with sensible defaults.
- **States:** default · loading · error (duplicate/empty name) · success (opens the project) · empty
- **Interaction:** optimistic list insert with a 10 s undo on delete (`FR-PROJ-1` AC-1.2)
- **Accessibility:** dialog traps focus and returns it to the trigger; `Esc` closes
- **Acceptance criteria:** [ ] UX-AC-004.1 creation completes in one step from the dashboard
  [ ] UX-AC-004.2 deletion offers undo for 10 seconds
- **Related requirement:** `FR-PROJ-1` · **Status:** validated

### UX-005 — The dashboard leads with what needs attention
- **Persona:** P1 · **Statement:** the first thing on the dashboard is the attention list (overdue,
  then due within 7 days), followed by recent activity; a create action is always visible.
- **States:** default · loading (skeleton) · empty (no projects) · error (retry) · success · permission-denied
- **Responsive:** two columns ≥ 1024 px; single column with attention first below 768 px
- **Accessibility:** attention items are a list with headings; overdue is conveyed by text, not colour
  alone; loading announces politely
- **Acceptance criteria:** [ ] UX-AC-005.1 an operator can identify the next action in < 30 s
  [ ] UX-AC-005.2 empty state offers exactly one primary action
  [ ] UX-AC-005.3 all six states implemented and reachable
- **Related requirement:** `FR-DASH-1` · **Screens:** `screens.md#screen-02` · **Status:** in review

### UX-006 — Assignments surface without interrupting
- **Persona:** P2 · **Statement:** an assignment appears as an unread count in the header and as an
  item in the dashboard activity; no modal interruption.
- **States:** default · loading · empty (nothing unread) · error · success (marked read)
- **Accessibility:** unread count announced on change; list reachable by keyboard
- **Acceptance criteria:** [ ] UX-AC-006.1 nothing interrupts an in-progress form
  [ ] UX-AC-006.2 marking read updates the count within 200 ms
- **Related requirement:** `FR-NOTIF-1` · **Status:** specified

## 4. Global UX requirements
| ID | Requirement | Verification |
|---|---|---|
| UX-G-001 | every interactive element keyboard-reachable in a logical order | keyboard walkthrough |
| UX-G-002 | destructive actions confirm and offer recovery | interaction review |
| UX-G-003 | errors say what happened and what to do next | error-state sweep |
| UX-G-004 | loading > 300 ms shows progress; > 10 s offers cancel | throttled test |
| UX-G-005 | 320 px width and 200 % zoom keep every function | viewport sweep |

## 5. Accessibility targets
WCAG 2.2 AA · keyboard completeness · visible focus · ≤ 24 px minimum target size (44 px preferred for
touch) · `prefers-reduced-motion` respected · verified per `docs/ux/screens.md`.
