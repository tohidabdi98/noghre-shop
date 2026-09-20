# UX requirements — NoghreShop

> **Status:** draft · **Owner:** Frontend/UX Agent · **Approved by:** — (gate `gates.ux_approved`)
>
> Personas, user goals and numbered UX requirements. Requirements here are **behavioural and
> measurable**; visual detail lives in `design_system.md`, flows in `user_flows.md`.

## 1. Personas

| Persona | Role | Context of use | Devices | Frequency | Skill / accessibility needs |
|---|---|---|---|---|---|
| P1 | | | | | |

### P1 — <persona name>
- **Job to be done:**
- **Pain today:**
- **Definition of success for them:**
- **Where they work from** (desktop, phone, shared device, offline, low bandwidth):
- **Accessibility considerations:**

## 2. UX principles

<!-- 3–6 principles that settle arguments. Each must be checkable in review. -->

| ID | Principle | Means | Test in review |
|---|---|---|---|
| PRIN-1 | Example: the user is never blocked by a required decision they cannot make yet | defaults are pre-filled and editable | a new user can complete onboarding without external information |

## 3. UX requirements

> `UX-###` IDs are referenced by module contracts (`ux_refs`). Never renumber.

### UX-001 — <name> `[DECISION]`
- **Persona:**
- **Statement:** <!-- what the user can do, in observable terms -->
- **Trigger / entry point:**
- **States:** default · loading · empty · error · success · permission-denied
- **Responsive behaviour:** desktop / tablet / mobile
- **Accessibility:** keyboard path, focus behaviour, screen-reader announcement, contrast, target size
- **Acceptance criteria:**
  - [ ] UX-AC-001.1 — measurable and verifiable by observation
  - [ ] UX-AC-001.2 —
- **Related requirement:** `FR-###`
- **Screens:** `screens.md#<screen>`
- **Flows:** `user_flows.md#<flow>`
- **Status:** proposed · **Wave:** —

<!-- Copy the block per requirement. -->

## 4. Global UX requirements

| ID | Requirement | Applies to | Verification |
|---|---|---|---|
| UX-G-001 | Every interactive element is keyboard reachable in a logical order | all screens | keyboard walkthrough |
| UX-G-002 | Every destructive action is confirmable and recoverable where feasible | all destructive controls | interaction review |
| UX-G-003 | User-visible errors state what happened and what to do next, without technical jargon | all error states | error-state sweep |
| UX-G-004 | Loading beyond ~300 ms shows progress; beyond ~10 s offers cancel/retry | all async actions | throttle test |
| UX-G-005 | Layout survives 320 px width and 200 % zoom without loss of function | all screens | viewport sweep |
| UX-G-006 | Colour is never the only carrier of meaning | all status indicators | contrast/vision check |
| UX-G-007 | No layout shift on font/image load | all screens | performance trace |

## 5. Accessibility targets

| Concern | Target | Verified by |
|---|---|---|
| Standard | WCAG 2.2 AA (or the level the human approved) | automated + manual sweep |
| Keyboard | every action reachable and operable | `visual_validation.md` §keyboard |
| Focus | visible focus indicator; focus moves predictably on navigation and dialogs | manual |
| Screen reader | names, roles, values, live-region announcements on async change | manual + axe |
| Motion | `prefers-reduced-motion` respected | automated |
| Zoom/text | usable at 200 % zoom; no clipped text | manual |
| Forms | labels, error association, error summary | manual |

## 6. UX constraints

| Constraint | Source | Consequence |
|---|---|---|
| e.g. no native mobile app in v1 | scope | responsive web only → `UX-G-005` matters more |

## 7. Open UX questions

Tracked in `docs/project/open_questions.md` with type `ux`.

| ID | Question | Blocks |
|---|---|---|
| | | |

## 8. Change log

| Date | Change | By | Reason |
|---|---|---|---|
| | initial draft | frontend-ux | — |
