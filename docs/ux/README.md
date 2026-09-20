# UX specification — how this folder works

> Owned by the **Frontend/UX Agent** (`agents/frontend-ux/STARTER_PROMPT.md`), which is a
> first-class, long-lived role: you can return to it at any point in the project to rethink
> flows, navigation, a screen, or the design system. This folder is the **source of truth for what
> the product must feel like**; `docs/project/requirements.md` owns *what it must do*.

## Files

| File | Owns |
|---|---|
| `ux_requirements.md` | personas, jobs-to-be-done, UX principles, numbered UX requirements (`UX-###`), UX acceptance criteria |
| `user_flows.md` | end-to-end flows and their states, errors, and edge cases |
| `information_architecture.md` | navigation model, hierarchy, naming, URLs, role visibility |
| `screens.md` | screen inventory + a specification per screen |
| `design_system.md` | tokens, typography, colour, spacing, components and their states |
| `interaction_patterns.md` | reusable interaction decisions (forms, modals, destructive actions, shortcuts…) |
| `visual_validation.md` | how rendered UI is verified: screenshots, viewports, a11y, regression |

## Rules

1. **Every UX requirement gets an ID** (`UX-###`) and a measurable acceptance criterion. Module
   contracts must cite the UX requirements they implement (`ux_refs`), so the implementation agent
   receives the relevant UX detail in its context pack — not the whole folder.
2. **UX requirements are behaviour, not decoration.** "The user can undo an accidental delete
   within 10 seconds" is a requirement; "use soft shadows" is a design-system detail.
3. **States are mandatory.** For every screen: default, loading, empty, error, success, and
   permission-denied where applicable. Missing states are the most common source of rework.
4. **Nothing is implemented that is not specified.** If the human asks for something new, the
   agent updates this folder first, then the implementation follows.
5. **Changing your mind is normal.** Discussing and revising the spec *is* the workflow; the
   agent records the revision with an ID-stable change-log entry and updates the affected
   contracts (`docs/workflows/change_management.md`).
6. **Accessibility is not optional and not a phase.** It appears in requirements, screens,
   patterns and validation.
7. **Visual verification is required for UI changes** — passing unit tests never proves UX
   correctness (`visual_validation.md`).
8. **Backend-only projects:** if the project has no user-facing UI (`state/project.yaml →
   profile: backend`), this folder stays as a stub, `gates.ux_approved` is set with a note, and
   the Frontend/UX role is not required.

## Dependency direction

```
docs/project/requirements.md  ──►  docs/ux/*  ──►  modules/<ID>.md (ux_refs)  ──►  implementation
                                    │
                                    └──►  visual validation ──► Frontend/UX review ──► fixes
```

If a UX decision changes something architectural (a new realtime channel, a new API shape, a
different auth flow), the Frontend/UX Agent raises it with the Architecture Agent and records an
`ADR-###` — UX never silently imposes new infrastructure.
