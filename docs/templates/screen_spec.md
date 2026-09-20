# SCREEN-## — <screen name>

- **Route:** `/app/...`
- **Owner module:** `MODULE-ID` (sole owner)
- **Flows:** `UF-##`
- **Requirements:** `FR-###`, `UX-###`
- **Entry points:** <how the user arrives, including deep links>
- **Exit points:** <where they go next>
- **Primary action:** <exactly one>
- **Secondary actions:** <list>

## Layout regions

| Region | Content | Behaviour at small widths |
|---|---|---|
| header | | |
| primary content | | |
| side panel | | |

## Content and controls

| Element | Type | Data source | Empty behaviour | Error behaviour |
|---|---|---|---|---|

## States

| State | Trigger | Appearance | Actions available | Accessibility |
|---|---|---|---|---|
| default | | | | |
| loading | | skeleton matching final layout | cancel if > 10 s | `aria-busy` |
| empty | | explanation + primary action | create | announced; focus on heading |
| error | | message + retry, input preserved | retry, back | `role="alert"` |
| success | | confirmation + next step | continue, dismiss | polite announcement |
| permission-denied | | explanation + path to access | sign in, request access | not announced as an error |

## Responsive behaviour

| Breakpoint | Layout | Notes |
|---|---|---|
| ≥ 1280 px | | |
| 768–1279 px | | |
| < 768 px | | |

## Keyboard and focus

- Tab order:
- Shortcuts:
- Initial focus:
- Focus trap / return:

## Accessibility requirements

- Landmarks and heading structure:
- Icon-only control labels:
- Contrast requirements:
- Target size minimum:
- Reduced motion:

## Copy

| Element | Copy |
|---|---|
| title | |
| empty | |
| error | |
| success | |

## Acceptance criteria

- [ ] SCREEN-##-AC1 —
- [ ] all specified states implemented and reachable

## Required evidence

- [ ] screenshots at 3 widths (default)
- [ ] screenshots of loading / empty / error / success
- [ ] keyboard-only walkthrough notes
- [ ] accessibility scan result
- [ ] Frontend/UX Agent sign-off in the PR
