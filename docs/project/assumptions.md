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
| ASM-001 | The business can obtain a domestic online payment gateway account before launch | DEC-003 requires online payment; this is standard for domestic e-commerce | checkout cannot complete online → v1 degrades to inquiry/manual payment (major scope change) | owner applies for the gateway before architecture is final; answer recorded in `OQ-001` — **as of 2026-09-20 the owner has NOT applied yet** (see RISK-001) | open | human |
| ASM-002 | Farsi-only UI is acceptable to effectively all target customers | DEC-004; the domestic retail market is Persian-speaking | some customers excluded → bilingual support needed (change request + real scope) | owner judges from customer base; revisit if international demand appears | open | human |
| ASM-003 | Product catalog is small enough for owner-side manual management (tens, not thousands, of items) | single-owner silver jewelry business | needs bulk import/CSV tooling and richer catalog admin | owner stated 50–200 items at launch (round 2, DEC-008) | confirmed | discovery |
| ASM-004 | Launch demand lands in the stated band: a few orders/day, 100–1,000 visitors/day with social spikes | owner expectation (round 5, DEC-025) | wrong band → overspent perf/scale work, or a launch that falls over on a spike | post-launch analytics in the first month | open | discovery |

Status values: `open` · `confirming` · `confirmed` · `falsified` · `retired`.

## Details

### ASM-001 — Domestic payment gateway is obtainable before launch
- **Statement:** The business can secure and integrate a domestic online payment gateway in
  time for v1 launch.
- **Basis:** DEC-003 (full online sales); standard practice for domestic e-commerce.
- **Affects:** checkout `FR-###`s, `OQ-001`, the payment module (not yet decomposed).
- **Verification:** owner completes the gateway application; result recorded in `OQ-001`.
- **Decision if falsified:** v1 falls back to inquiry/manual payment (DEC-003 partially
  superseded); owner decides via a change request.
- **Status:** open

### ASM-002 — Farsi-only UI reaches effectively all target customers
- **Statement:** Persian-only, RTL UI loses no meaningful share of the v1 audience.
- **Basis:** DEC-004; domestic retail market.
- **Affects:** all storefront `UX-###`, no i18n in v1 architecture.
- **Verification:** owner judgement from existing customer base; revisited at first
  international inquiry.
- **Decision if falsified:** bilingual support becomes a change request (scope + cost).
- **Status:** open

### ASM-003 — Catalog is small (tens, not thousands, of items)
- **Statement:** Owner-side manual catalog management is sufficient; no bulk tooling needed.
- **Basis:** single-owner silver jewelry business.
- **Affects:** catalog/admin `FR-###`s, admin module scope.
- **Verification:** owner states expected catalog size during rounds 2–4.
- **Decision if falsified:** bulk import/CSV tooling enters scope via change request.
- **Status:** **confirmed** (2026-09-20) — owner stated 50–200 items at launch (DEC-008);
  manual management with pagination and good admin ergonomics is sufficient.

### ASM-004 — Launch demand band: a few orders/day, 100–1,000 visitors/day
- **Statement:** Post-launch demand lands in the band the owner stated in round 5.
- **Basis:** owner expectation (DEC-025); no prior online channel exists to measure.
- **Affects:** NFR-SCALE-1, NFR-PERF-1, hosting sizing (architecture input).
- **Verification:** post-launch analytics in the first month; adjust capacity if the band
  is wrong by an order of magnitude.
- **Decision if falsified:** capacity/perf targets revisited via change request; owner
  decides with the Architecture Agent.
- **Status:** open
