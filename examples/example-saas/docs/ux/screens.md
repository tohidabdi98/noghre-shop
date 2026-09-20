# Screens — Example SaaS (abridged)

| Screen | Route | Module | Flow | Status | Visual validation |
|---|---|---|---|---|---|
| SCREEN-01 auth | `/signin`, `/signup`, `/reset` | AUTH-001 | UF-01 | implemented | passed |
| SCREEN-02 dashboard | `/app` | DASH-001 | UF-01, UF-02 | in review | changes requested |
| SCREEN-03 project | `/app/projects/:id` | PROJECT-001 | UF-03 | specified | pending |

## SCREEN-01 — Auth (sign in / sign up / reset)

- **Route:** `/signin`, `/signup`, `/reset` · **Module:** `AUTH-001` · **Flows:** `UF-01`
- **Requirements:** `FR-AUTH-1`, `UX-001`, `UX-002`
- **Primary action:** submit the form · **Secondary:** switch between sign in / sign up, request reset

| Region | Content | Below 768 px |
|---|---|---|
| brand panel | product name, one-line value proposition | hidden (kept as a compact header) |
| form | email, password, submit, inline errors | full width |
| footer | reset link, legal note | same |

### States
| State | Trigger | Appearance | Actions | Accessibility |
|---|---|---|---|---|
| default | — | two fields, disabled submit until valid | submit | labels + autocomplete attributes |
| loading | submit in flight | button shows progress, inputs disabled | cancel after 10 s | `aria-busy` on the form |
| empty | n/a | — | — | — |
| error | invalid credentials / server error | one generic message above the form, fields preserved | retry | `role="alert"`, focus to summary |
| success | valid credentials | redirect to `/app` | — | polite announcement |
| permission-denied | session expired mid-flow | "your session expired, sign in again" | sign in | not styled as an error |

### Responsive / keyboard
Single column below 480 px; targets ≥ 44 px; `Tab` order brand → email → password → submit → reset;
`Enter` submits; focus visible; error summary receives focus on failure.

### Copy
| Element | Copy |
|---|---|
| error | "That email and password don't match. Check them and try again." |
| reset sent | "If that email has an account, a reset link is on its way." |
| expired link | "That reset link has expired or has already been used. Request a new one." |

### Acceptance criteria
- [ ] SCREEN-01-AC1 all applicable states implemented and reachable
- [ ] SCREEN-01-AC2 error copy never reveals whether an account exists
- [ ] SCREEN-01-AC3 keyboard-only completion verified

### Evidence
- [x] screenshots 375 / 768 / 1280 (default, loading, error, success)
- [x] keyboard walkthrough notes
- [x] axe scan clean
- [x] Frontend/UX sign-off — ux-001, 2026-03-08 (`reports/ux-validation-AUTH-001-2026-03-08.md`)

## SCREEN-02 — Dashboard

- **Route:** `/app` · **Module:** `DASH-001` · **Flows:** `UF-01`, `UF-02`
- **Requirements:** `FR-DASH-1`, `UX-005`, `UX-006`
- **Primary action:** create project (header, always visible) · **Secondary:** open attention item, mark notifications read

| Region | Content | Below 1024 px | Below 768 px |
|---|---|---|---|
| header | nav, search, unread count, create | same | bottom bar, unread in header |
| attention | overdue + due ≤ 7 days, urgent first | single column | first section |
| activity | last 10 events | single column | below attention |
| empty | explanation + create action | same | same |

### States
| State | Trigger | Appearance | Actions | Accessibility |
|---|---|---|---|---|
| default | data ready | two columns, attention first | open, create | headings per section; list semantics |
| loading | fetch in flight | skeleton matching final layout, no layout shift | — | `aria-busy`, polite announcement |
| empty | no projects | explanation + exactly one primary action | create | focus on the heading |
| error | query failed | section-level error, other sections still render | retry | `role="alert"` |
| success | creation completed | row inserted, toast with undo on delete | undo (10 s) | polite announcement |
| permission-denied | not a member of any project | explanation + create guidance | create | not styled as an error |

### Responsive / keyboard
≥ 1024 px: 2 columns (attention 2/3, activity 1/3). 768–1023 px: stacked, attention first.
< 768 px: single column, create as a floating action. Keyboard: header → attention items → activity →
create; `n` creates, `Enter` opens the focused item, shortcuts sheet on `?`.

### Copy
| Element | Copy |
|---|---|
| empty | "No projects yet. Create your first one." |
| error | "We couldn't load your projects. Your data is safe — try again." |

### Acceptance criteria
- [ ] SCREEN-02-AC1 attention list is above the fold at 1280×800
- [ ] SCREEN-02-AC2 partial failures degrade only their own section
- [ ] SCREEN-02-AC3 all six states implemented and reachable

### Evidence (review open — `changes_requested`, PR #21)
- [x] screenshots default at 375/768/1280
- [ ] screenshots loading / empty / error / success — **missing**
- [ ] keyboard walkthrough on the attention list — **missing**
- [ ] Frontend/UX sign-off — **pending**
