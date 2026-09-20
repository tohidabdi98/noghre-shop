# Requirements template — the shape, and why it has this shape

> The live file is `docs/project/requirements.md`. This document records the **required structure**
> so the Discovery Agent writes something that agents can consume, and so a human can check the
> result quickly. Copy the section list into the live file; do not fork the content.

## Required sections

1. **Product** — problem, vision, personas (product level), use cases, success criteria, scope,
   explicit out-of-scope, business rules, constraints and assumptions.
2. **Functional requirements** — one block per `FR-###` with: actor, description, acceptance
   criteria, permissions, state transitions, edge cases, error behaviour, related UX IDs.
3. **Non-functional requirements** — table with category, target and **verification method**.
4. **Data** — entities with owning module, sensitivity, retention; flows; privacy/compliance.
5. **Integrations** — service, purpose, auth model, failure behaviour, cost.
6. **Engineering requirements** — testing, CI/CD, conventions (link), dependency policy (link),
   documentation duties, definition of done (link).
7. **Open items** — pointers to `open_questions.md`, `assumptions.md`, `risks.md` (never inline).
8. **Change log** — dates, changes, authors.

## Rules that make requirements agent-usable

| Rule | Why it matters |
|---|---|
| Every requirement has an ID and its **heading contains that ID** | `tp.py context` extracts exactly the requirements a module needs |
| Every requirement states acceptance criteria that are observable | the module contract must cite them, and review checks them |
| Behaviour here, look-and-feel in `docs/ux/` | two sources of truth otherwise diverge immediately |
| Out-of-scope is explicit | the cheapest way to stop an agent from building something unwanted |
| NFRs name their verification | unmeasured NFRs are ignored by definition |
| Uncertainties are `[ASSUMPTION]`/`[OPEN]`, not silent prose | false certainty is the most expensive documentation bug |
| Nothing appears twice | `docs/README.md` rule 3 |

## Quality gate before the human approves

- [ ] every `FR-###` has ≥ 1 acceptance criterion that a test or a screenshot can prove
- [ ] every `NFR-###` has a target **and** a verification method
- [ ] scope and out-of-scope agree (nothing in-scope contradicts an out-of-scope statement)
- [ ] every integration names a failure behaviour
- [ ] every uncertainty is tagged and mirrored into the assumptions/open-questions registers
- [ ] `python scripts/tp.py validate` passes (IDs referenced, heading conventions, links)
- [ ] `state/project.yaml → gates.requirements_approved: true` set by the human, with a date
