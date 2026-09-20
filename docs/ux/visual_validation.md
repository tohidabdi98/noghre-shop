# Visual validation — proving the UI actually works

> **Passing unit tests never proves the UX is correct.** A styled component can render, a test can
> pass, and the screen can still be unusable. This file defines how rendered UI is verified, by the
> Frontend/UX Agent, before UX work is accepted.
>
> Tool-agnostic by design: pick the adapters your stack supports (table at the end) and record the
> choice in `docs/project/conventions.md`.

```
UX decision → UX specification → implementation → browser/visual validation
    → Frontend/UX review → feedback → implementation changes → validation again
```

## 1. What must be validated

Any change that affects what a user sees or how they interact:

- new or changed screens, components, states
- responsive behaviour changes
- accessibility-relevant changes (focus, keyboard, labels, contrast)
- anything touching tokens, typography, or the design system
- user-visible copy and error messages

Backend-only changes are out of scope for this file (see
`docs/workflows/testing_workflow.md`).

## 2. Validation procedure

### Step 1 — the implementation agent captures raw evidence

1. Run the app locally (or in a preview environment) with the module's real data path.
2. Walk the flow from the specification, including **every state**:
   default · loading (throttled) · empty · error (forced) · success · permission-denied.
3. Capture screenshots at three widths: **320/375 px**, **768 px**, **1280+ px** (and 200 % zoom
   on the primary flow).
4. Record the commands/URLs used, so the evidence is reproducible.
5. Attach screenshots to the PR under `## Screenshots` and note anything you know is unfinished.

### Step 2 — the Frontend/UX Agent reviews against the spec

Review each screen against its specification in `screens.md`, not against taste:

| Check | Pass condition |
|---|---|
| Layout | matches the specified regions and hierarchy at all three widths |
| Hierarchy | primary action is unmistakable on first glance |
| States | all six states specified are actually implemented and reachable |
| Empty/error copy | actionable, matches the specification's copy |
| Responsive | no clipping, no horizontal scroll, no lost function at 320 px |
| Keyboard | the flow is completable with the keyboard alone, focus visible and ordered |
| Accessibility | scan clean for the changed screens; manual checks below performed |
| Design system | tokens/components used; no one-off colours, spacings or controls |
| Consistency | matches neighbouring screens and the established patterns |
| Cumulative layout shift | no visible jump on load |

### Step 3 — findings become requirements, not opinions

Findings are written as `Blocking` / `Non-blocking` / `Suggestion` / `Question` (same taxonomy as
`docs/workflows/review_workflow.md`), each with: screen, state, what was observed, what the
specification says, and the smallest change that fixes it. Blocking findings are either fixed or
the specification is amended by the Frontend/UX Agent — never silently ignored.

### Step 4 — re-validate and record sign-off

The agent re-captures the affected screenshots and the Frontend/UX Agent records sign-off in the
PR: `UX validation: passed — screenshots attached, keyboard walkthrough performed, scan clean`.
The module may not move to `validated` without this line when UI changed.

## 3. Manual checks that automated tools cannot do

- **Keyboard-only walkthrough** — Tab/Shift+Tab/Enter/Space/Esc/arrows; focus never lost or trapped
  outside dialogs; shortcut sheet accurate.
- **Screen reader sanity pass** (VoiceOver / NVDA / Orca / TalkBack) — headings, labels, live
  announcements on async change, dialog announcements.
- **Zoom / text scaling** — 200 % browser zoom, and 150 % base font size.
- **Reduced motion** — `prefers-reduced-motion: reduce` removes non-essential motion.
- **Colour independence** — grayscale filter still conveys status.
- **Copy read-aloud** — the error/success text makes sense to a non-engineer.
- **Real data shape** — very long names, many items, zero items, unicode/emoji, RTL if in scope.

## 4. Evidence and storage

| Evidence | Where | Naming |
|---|---|---|
| screenshots | PR body (required) and `reports/` for milestone-level reviews | `<screen>-<state>-<width>.png` |
| baseline images (visual regression) | repo's chosen snapshot directory, committed | tool-managed |
| walkthrough notes | PR body, under `## Validation results` | — |
| a11y scan output | PR body (summary) + `reports/` (full) | `<screen>-a11y.txt` |

Never commit large binary artefacts. Never claim a visual check you did not perform — that is the
single most damaging false signal in frontend work.

## 5. Tool adapters (choose and record)

| Need | Common options | Notes |
|---|---|---|
| Browser automation + screenshots | Playwright, Cypress, Puppeteer, Selenium | Playwright covers screenshots, viewports, a11y, traces in one tool |
| Component catalogue | Storybook, Ladle, Histoire | makes state coverage reviewable per component |
| Visual regression | Playwright snapshots, Percy, Chromatic, reg-suit | baseline review must be done by the Frontend/UX Agent, not blindly approved |
| Accessibility scanning | axe-core (via Playwright/Cypress), Pa11y, Lighthouse | automated scans catch ~30–40 % of issues — manual checks remain mandatory |
| Manual/exploratory | the browser + screenshots pasted into the PR | always available, always acceptable |
| Design comparison | Figma/design files side by side with the build | if a design file is the source of truth |

If your environment cannot run a browser (e.g. a headless agent sandbox), the Frontend/UX review
happens on the human's machine: the agent prepares the checklist and the exact URLs/flows, the
human captures the screenshots, and the agent records the outcome. **Unverified UI is not
validated UI** — it is recorded as a known limitation, not as passing.

## 6. Definition of done for UI work

- [ ] every specified state implemented and reachable
- [ ] screenshots at three widths attached to the PR
- [ ] keyboard walkthrough performed and noted
- [ ] accessibility scan run on changed screens; findings triaged
- [ ] responsive behaviour matches `screens.md`
- [ ] design tokens/components used; no local one-offs
- [ ] copy matches the specification
- [ ] Frontend/UX Agent sign-off recorded
