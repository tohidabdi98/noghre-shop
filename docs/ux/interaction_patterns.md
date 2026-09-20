# Interaction patterns

> Owned by the Frontend/UX Agent. Reusable answers to recurring interaction questions, so that
> implementation agents do not each invent their own. Each pattern states the **default** and when
> it is *not* appropriate. Deviating requires a UX decision recorded here.

## 1. Feedback

| Situation | Pattern | Notes |
|---|---|---|
| action < 300 ms | no indicator | avoid flicker |
| action 300 ms – 10 s | inline progress on the control that triggered it | keep the button's size stable |
| action > 10 s | progress with label + cancel/retry | never an indefinite spinner |
| background operation | optimistic UI + status chip + notification if it fails | must be recoverable |
| destructive success | confirmation referencing the object ("Project X deleted") + undo when feasible | never a bare "Done" |

## 2. Forms

| Concern | Default |
|---|---|
| Validation timing | validate on blur; re-validate on change once the field is invalid; never on first focus |
| Error placement | inline next to the field, plus an error summary at the top for ≥ 3 errors |
| Error copy | "what happened → what to do" (no codes, no jargon) |
| Required fields | marked, with rationale, and only when truly required |
| Preservation | never clear user input on failure |
| Submit | disabled only while in flight; never disabled as validation theatre — show the error instead |
| Long forms | saved as draft / resumable when they exceed one screen |
| Autofill/paste | must work; never block paste |

## 3. Navigation and layout

| Concern | Default |
|---|---|
| Page transitions | no full-page blocking spinner; keep chrome stable, skeleton the content |
| Back/forward | always predictable; filter/pagination state in the URL |
| Unsaved changes | confirm before leaving, with "stay / discard / save" |
| Scroll restoration | restore position when returning to a list |
| Modals vs pages | modal = one focused decision ≤ 3 fields; anything bigger gets a page |

## 4. Destructive and irreversible actions

| Item | Default |
|---|---|
| Confirmation | required, naming the object and the consequence |
| Confirmation strength | typed confirmation only for data loss with no undo |
| Undo window | 10 s where feasible (soft delete) |
| Recovery | state the retention/restore path in the confirmation |
| Agent rule | destructive UX changes require human approval (`docs/workflows/human_in_the_loop.md`) |

## 5. Keyboard

| Pattern | Default |
|---|---|
| Global shortcuts | documented in an in-app shortcuts sheet; avoid overriding browser/OS keys |
| Primary action | `Enter` submits a form; `Ctrl/Cmd+Enter` submits multi-line contexts |
| Cancel | `Esc` closes the top-most layer only |
| Lists | arrow keys move, `Enter` activates, `Space` selects for multi-select |
| Shortcut discoverability | `?` opens the sheet; every shortcut has a visible equivalent |
| Focus | never move focus silently except on navigation, dialog open/close, and error summary |

## 6. Notifications and messaging

| Kind | Channel | Persistence | Use |
|---|---|---|---|
| inline | next to the trigger | transient | action feedback |
| banner | top of the page | until resolved | degraded mode, expiring session |
| toast | bottom-right / top-center on mobile | auto-dismiss 5 s, pausable on hover/focus | non-critical completion |
| notification centre | `/app/notifications` | persistent | things the user must not miss |

## 7. Lists, search and filtering

| Concern | Default |
|---|---|
| Pagination | cursor/infinite for feeds; explicit page controls for tabular admin data |
| Filter state | in the URL; empty results say which filter excluded everything |
| Bulk actions | appear only when ≥ 1 row is selected; state the count in the action label |
| Sorting | one default sort documented per list; last-used sort is not silently remembered |

## 8. Data display

| Concern | Default |
|---|---|
| Empty vs zero | distinguish "no data yet" from "no results for this filter" |
| Long values | truncate with a way to reveal, never mid-identifier |
| Dates/times | locale-formatted, absolute for precision, relative for recency, tooltip with the other |
| Numbers | right-aligned in tables; consistent units |
| Loading graphs/charts | skeleton with axis placeholders; never a fake data curve |

## 9. Errors and degraded states

| Kind | Presentation | Must include |
|---|---|---|
| field error | inline + summary | cause, correction, preserved input |
| request failure | section-level error with retry | retry, what was lost, safe fallback |
| permission | explanatory, non-judgemental | why, who to ask, alternate path |
| offline | global banner, queue writes when safe | what is queued, what is not saved |
| unexpected | friendly message + reference id | copyable correlation id for support |

## 10. Onboarding and empty starts

| Concern | Default |
|---|---|
| First run | resumable, ≤ 4 steps, skippable, with a visible progress indicator |
| Sample content | optional and clearly marked as sample; one click to remove |
| Empty states | teach the next action, never a dead end |
| Returning user | never repeat onboarding; deep links land where intended |

## 11. Change log

| Date | Pattern | Change | By |
|---|---|---|---|
| | initial draft | — | frontend-ux |
