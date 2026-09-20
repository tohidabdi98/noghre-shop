# Assumptions

> Beliefs the project depends on that have **not** been confirmed. Each assumption is a latent
> risk: if it is false, work changes. Every role may add one; the Discovery Agent owns the file.
>
> Rules
> * One row per assumption, `ASM-###`, never renumbered.
> * State the **impact if wrong** and **how it will be confirmed** with a trigger
>   (date, milestone, or event). An assumption with no confirmation plan is a risk — mirror it
>   into `docs/project/risks.md`.
> * When an assumption is confirmed, set `status: confirmed` and record the evidence.
>   When falsified, set `status: falsified`, raise a change request
>   (`docs/workflows/change_management.md`) and fix the affected documents.
> * Implementation agents **must not** silently build on an assumption that affects behaviour —
>   if your module depends on an `ASM-###` marked `open`, ask the human.

## Assumption register

| ID | Assumption | Why we believe it | Impact if wrong | Confirmation plan | Status | Owner |
|---|---|---|---|---|---|---|
| ASM-001 | Example: users have a modern evergreen browser | target audience is SaaS knowledge workers | would need legacy support + polyfills | analytics at M2 | open | frontend-ux |

Status values: `open` · `confirming` · `confirmed` · `falsified` · `retired`.

## Details

### ASM-001 — <assumption title>
- **Statement:**
- **Basis:**
- **Affects:** `FR-###`, `UX-###`, `MODULE-ID`s
- **Verification:** <!-- command, metric, interview, experiment -->
- **Decision if falsified:** <!-- what changes, and who decides -->
- **Status:** open
