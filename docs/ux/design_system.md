# Design system

> Owned by the Frontend/UX Agent. Design-system decisions are **specified here first** and then
> implemented in the module that owns the design-system files. Implementation agents use these
> tokens and components; they do not invent colours, spacings or one-off components.
>
> Rule of thumb: if a value or a component appears twice, it belongs here; if it appears once, it
> belongs in the screen specification.

## 1. Principles

| # | Principle | Consequence for implementation |
|---|---|---|
| 1 | Consistency beats local cleverness | never style a control locally if a component exists |
| 2 | Hierarchy through spacing and weight before colour | fewer colour tokens, clearer layout |
| 3 | Colour is never the only signal | pair with icon/text/pattern (`UX-G-006`) |
| 4 | Motion explains, never entertains | short, interruptible, reducible |
| 5 | Accessible by default | AA contrast and keyboard support are part of the component's definition |

## 2. Tokens

> Tokens are the only sanctioned way to express these values. Implementation happens in the
> module owning the token file (declare it as a **shared zone** in `state/project.yaml`).

### Colour

| Token | Purpose | Light | Dark | Contrast pair |
|---|---|---|---|---|
| `color.bg.canvas` | page background | | | with `color.text.primary` |
| `color.bg.surface` | cards/panels | | | |
| `color.text.primary` | body text | | | ≥ 4.5:1 on canvas |
| `color.text.muted` | secondary text | | | ≥ 4.5:1 where informational |
| `color.border.default` | separators | | | ≥ 3:1 against adjacent colours |
| `color.accent.default` | primary action | | | ≥ 3:1 for UI, 4.5:1 for text |
| `color.state.success` / `warning` / `danger` / `info` | status | | | never sole carrier of meaning |

### Typography

| Token | Size / line-height | Weight | Use |
|---|---|---|---|
| `text.display` | | | page titles |
| `text.title` | | | section headings |
| `text.body` | | | default |
| `text.label` | | | control labels |
| `text.caption` | | | helper text, metadata |
| `text.mono` | | | identifiers, code |

### Space, radius, elevation, motion

| Scale | Values |
|---|---|
| `space` | 4 / 8 / 12 / 16 / 24 / 32 / 48 px (multiples of 4 only) |
| `radius` | sm / md / lg / pill |
| `elevation` | flat / raised / overlay — used sparingly, never for decoration |
| `motion.duration` | fast 120 ms · base 200 ms · slow 320 ms |
| `motion.easing` | standard = ease-out; entrance = decelerate; exit = accelerate |

## 3. Components

| Component | Purpose | Variants | States to implement | Owner module | A11y notes |
|---|---|---|---|---|---|
| Button | trigger an action | primary / secondary / ghost / danger | default, hover, focus, active, loading, disabled | | keyboard, ≥ 24 px target |
| Input | single-line entry | text / number / search | default, focus, filled, invalid, disabled, readonly | | label association, error text linked |
| Select | choose one of many | native / custom | as Input + open | | keyboard model |
| Checkbox / Radio | binary / exclusive choice | — | default, checked, indeterminate, invalid | | label click target |
| Table / List | show collections | table, card list | default, loading, empty, error, selected | | header semantics, row keyboard access |
| Dialog | focused subtask | modal, drawer, sheet | open, loading, error, closing | | focus trap + restore, Esc |
| Toast / Banner | transient/blocking messages | info, success, warning, danger | enter, persist, dismiss | | polite vs assertive announcement |
| Tabs | switch views in place | underline, segmented | default, active, disabled | | roving tabindex |
| Navigation | move between areas | sidebar, top bar, bottom bar | default, active, collapsed | | landmarks, current page |
| Empty state | explain absence of data | inline, full-page | — | | heading + single action |

**Component definition of done:** variants and states implemented · keyboard operable · focus
visible · labelled for assistive tech · contrast verified · documented in the component catalogue
· used (not re-implemented) elsewhere.

## 4. Icons and imagery

| Concern | Decision |
|---|---|
| Icon set | |
| Sizing | |
| Decorative vs meaningful | decorative icons `aria-hidden`; meaningful icons always carry a text label |
| Imagery rules | |

## 5. Content and tone

| Concern | Rule |
|---|---|
| Voice | |
| Action labels | verb + object, sentence case |
| Error copy formula | what happened → what to do → how to recover |
| Numbers/dates/currency | one documented format per locale |
| Localisation readiness | no concatenated strings; text never baked into images |

## 6. Theming and platform

| Concern | Decision |
|---|---|
| Dark mode | required / optional / not now — and which tokens differ |
| Density | |
| Platform differences | |
| Design-tool source of truth | where the human's designs live (Figma file, etc.) |

## 7. Governance

- **Changing a token or component** is a UX decision: the Frontend/UX Agent records it, updates
  this file, and lists affected modules. If it changes an interface other modules consume, it goes
  through `docs/workflows/change_management.md`.
- **Adding a component** requires: a use case, a screen reference, its states table, and a11y notes.
- **Design-system version** is tracked in `state/project.yaml` (milestone) and follows the release
  version; breaking token renames are recorded as `ADR-###` when they force module changes.

## 8. Change log

| Date | Change | By | Affected modules |
|---|---|---|---|
| | initial draft | frontend-ux | — |
