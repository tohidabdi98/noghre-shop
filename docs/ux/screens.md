# Screens

> Owned by the Frontend/UX Agent. The **screen inventory** plus a specification per screen. A
> screen is specified *before* it is implemented; the implementation agent gets the screens its
> module contract references (`ux_refs`) and nothing else.
>
> Every screen specification **must** cover: default, loading, empty, error, success and
> permission-denied states, responsive behaviour, and the keyboard path.

## 1. Screen inventory

| Screen | Route | Module | Flow | Priority | Status | Visual validation |
|---|---|---|---|---|---|---|
| Sign in | `/signin` | `AUTH-001` | UF-01 | must | specified | pending |

Status: `placeholder` · `specified` · `implemented` · `validated` · `needs-revision`.

## 2. Screen specification format

```text
SCREEN-<id> — <screen name>
  Route:            /app/<path>
  Module:          <MODULE-ID>          (sole owner)
  Flows:           UF-##
  Requirements:    FR-###, UX-###
  Entry points:    how the user gets here
  Exit points:     where they go next
  Primary action:  exactly one
  Secondary actions:
```

### Layout regions

| Region | Content | Behaviour at small widths |
|---|---|---|
| header | | collapses to … |
| primary content | | |
| side panel | | becomes a sheet below 768 px |

### Content and controls

| Element | Type | Data source | Empty behaviour | Error behaviour |
|---|---|---|---|---|

### States

| State | Trigger | Appearance | Actions available | Accessibility |
|---|---|---|---|---|
| default | data loaded | | | |
| loading | request in flight | skeleton matching final layout | cancel where > 10 s | `aria-busy`, polite announcement |
| empty | zero items | explanation + primary call to action | create | announced; focus lands on heading |
| error | failed request | message + retry, input preserved | retry, back | `role="alert"` |
| success | action completed | confirmation, next step | dismiss, continue | announced politely |
| permission-denied | 401/403 | explanation + how to request access | sign in, contact admin | not announced as an error |

### Responsive behaviour

| Breakpoint | Layout | Notes |
|---|---|---|
| ≥ 1280 px | | |
| 768–1279 px | | |
| < 768 px | | |

### Keyboard and focus

- Tab order:
- Shortcuts: (see `interaction_patterns.md`)
- Initial focus:
- Focus trap / return (dialogs, drawers):

### Accessibility requirements

- Landmarks and headings structure:
- Labelling for icon-only controls:
- Contrast requirements for custom colours:
- Target size minimum (≥ 24×24 CSS px; prefer 44×44 for touch):
- Motion / `prefers-reduced-motion`:

### Content copy

| Element | Copy |
|---|---|
| title | |
| empty state | |
| error | |
| success | |

### Acceptance criteria

- [ ] SCREEN-…-AC1 —
- [ ] SCREEN-…-AC2 — all six states implemented and reachable

### Evidence required for validation

- [ ] screenshots at 3 widths (default state)
- [ ] screenshots of loading / empty / error / success
- [ ] keyboard-only walkthrough notes
- [ ] automated accessibility scan result
- [ ] Frontend/UX Agent sign-off recorded in the PR

<!-- Copy per screen. Update the inventory table and the status when a screen changes. -->
