# Open questions

> Unresolved decisions. This file exists so that agents **never guess** instead of asking, and so
> a question cannot be lost when an agent session ends.
>
> Rules
> * One row per question, `OQ-###`, never renumbered.
> * Every question names an **owner** and a **blocks** field (what cannot proceed until it is
>   answered). A question blocking a module makes that module `blocked` in
>   `state/modules.yaml`, not `ready`.
> * Escalation needed? Use `docs/workflows/human_in_the_loop.md`. Product questions go to the
>   human (or Discovery Agent); UX questions to the Frontend/UX Agent; technical questions to the
>   Architecture Agent.
> * Answering a question means: record the answer as a `DEC-###` in `docs/project/decisions.md`,
>   update the affected documents in the same session, and close the row here.
> * Agents: **before implementing anything ambiguous**, check this file. If your question is not
>   here, add it and escalate if it is consequential.

## Open question register

| ID | Question | Type | Blocks | Owner | Asked | Status | Answer / decision |
|---|---|---|---|---|---|---|---|
| OQ-001 | Example: does onboarding require an invite code? | product | `AUTH-001`, `UX-002` | human | — | open | — |

Type: `product` · `ux` · `technical` · `process` · `compliance`.
Status: `open` · `answered` · `deferred` · `withdrawn`.

## Detail

### OQ-001 — <question>
- **Asked by:**
- **Context:** <!-- why this matters; what happens either way -->
- **Options:**
  1. <!-- option + consequence -->
  2. <!-- option + consequence -->
- **Recommendation:** `[REC]` <!-- an agent's recommendation is allowed and encouraged; a
  decision is not -->
- **Impact:** <!-- modules, requirements, UX, schedule -->
- **Answer:** <!-- filled when closed, with a link to the DEC-### that recorded it -->
