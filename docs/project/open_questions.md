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
| OQ-001 | Which domestic payment gateway will v1 use, and can the business obtain it? | product | checkout FRs, payment module, launch date | human | 2026-09-20 | deferred | Knowingly accepted as launch risk at spec approval (DEC-033); owner files application ASAP; FR-PAY-1 blocked until resolved |
| OQ-002 | How are orders delivered, and is cash-on-delivery offered alongside online payment? | product | cart/checkout FRs, order state machine, shipping cost rules | human | 2026-09-20 | answered | Online payment only; no COD — DEC-015 |
| OQ-003 | How are prices set — fixed prices, or prices that track the silver market rate? | product | catalog/pricing FRs, admin workflows | human | 2026-09-20 | answered | weight × daily silver rate + craft fee — DEC-016 |
| OQ-004 | Are product reviews, discount/promo codes, or a blog part of v1? (Not excluded in round 2, not yet agreed.) | product | scope of catalog/product FRs, checkout FRs | human | 2026-09-20 | answered | Promo codes IN; reviews + blog OUT — DEC-018 |
| OQ-005 | What happens when online payment fails mid-checkout? (Round 3 question returned unanswered.) | product | checkout error FRs | human | 2026-09-20 | answered | Retry from checkout; cart preserved — DEC-014 |
| OQ-006 | DEC-012 (email confirmations) needs an email address, but DEC-009 collects only name + phone + address — which gives way? | product | checkout FRs, notification FRs | human | 2026-09-20 | answered | Optional email field at checkout — DEC-017 |
| OQ-007 | Where does the daily silver rate come from — manual owner entry in admin, or an automated source? | product | pricing FRs, pricing engine, admin workflows | human | 2026-09-20 | answered | Manual admin entry in v1, automation-ready — DEC-019 |
| OQ-008 | When is the customer's price locked — at checkout start (with stock reservation), or at payment? | product | checkout FRs, order totals, refund semantics | human | 2026-09-20 | answered | Locked at payment — DEC-020 (UX must re-display total at payment step) |
| OQ-009 | How are product categories defined — a starter taxonomy in the spec, or owner-defined freely? (Round 4 question returned unanswered; re-asked.) | product | catalog FRs, navigation, filters | human | 2026-09-20 | answered | Starter taxonomy (rings/necklaces/earrings/bracelets/sets/other), owner-editable — DEC-023 |
| OQ-010 | What must a promo code do in v1 (type, limits, expiry)? | product | checkout FRs, admin workflows | human | 2026-09-20 | answered | % off + expiry + usage limit — DEC-024 |
| OQ-011 | Uptime expectation for v1 — formal availability target or best-effort fix-fast? (Round 5 question returned unanswered.) | product | NFR availability target, ops scope | human | 2026-09-20 | answered | Best-effort, fix-fast — DEC-031 |
| OQ-012 | Is there a launch deadline? (Round 6–7 question returned unanswered.) | product | milestone planning, orchestration waves | human | 2026-09-20 | answered | No fixed date — DEC-032 |

Type: `product` · `ux` · `technical` · `process` · `compliance`.
Status: `open` · `answered` · `deferred` · `withdrawn`.

## Detail

### OQ-001 — Which domestic payment gateway, and is it obtainable?
- **Asked by:** discovery (round 1 follow-up)
- **Context:** DEC-003 makes online payment the core of v1. Without a gateway account,
  checkout cannot complete and v1 degrades to inquiry/manual payment.
- **Options:**
  1. Owner already has / can promptly obtain a specific gateway account → architecture can
     target its API directly.
  2. Gateway not yet available → decide between waiting, or launching with manual payment
     (supersedes DEC-003 via change request).
- **Recommendation:** `[REC]` owner applies for the gateway **now**, before architecture work;
  the answer also resolves ASM-001.
- **Impact:** checkout/payment FRs, the payment module, launch date.
- **Answer:** — (still open; **owner confirmed 2026-09-20 the application has not been made
  yet** — tracked as RISK-001 with escalation trigger). At spec approval the owner
  **knowingly accepted** this as a launch risk (2026-09-20, **DEC-033**); status set to
  `deferred`. FR-PAY-1 stays blocked until a gateway is named.

### OQ-002 — Delivery method and cash-on-delivery
- **Asked by:** discovery (round 1 follow-up)
- **Context:** "Full online sales" (DEC-003) ends at delivery. Courier vs post, shipping cost
  rules, and whether cash-on-delivery exists change the order state machine and checkout UX.
- **Options:**
  1. Online payment only, courier delivery → simplest order model.
  2. Online payment + cash-on-delivery → extra order state + payment-on-delivery handling.
- **Recommendation:** `[REC]` online payment only for v1 (DEC-003 already chose online
  payment; COD can come later as a change request).
- **Impact:** order state machine, shipping cost rules, checkout FRs.
- **Answer:** Online payment only, no COD in v1 (2026-09-20) — **DEC-015**.

### OQ-003 — Pricing model: fixed vs silver-rate-tracked
- **Asked by:** discovery (round 1 follow-up)
- **Context:** Silver jewelry retail sometimes prices by weight × daily metal rate + craft
  fee, rather than fixed per-item prices. This changes the catalog data model and admin
  workflow fundamentally.
- **Options:**
  1. Fixed per-item prices set by the owner → simplest catalog and admin.
  2. Rate-tracked pricing (weight × daily rate) → needs a rate source and pricing engine.
- **Recommendation:** `[REC]` fixed prices in v1; rate-tracking only if the owner says the
  business cannot operate otherwise.
- **Impact:** catalog data model, pricing FRs, admin workflows.
- **Answer:** The owner chose **weight × daily silver rate + craft fee** (2026-09-20) —
  **DEC-016**. The `[REC]` for fixed prices was **not** accepted; consequences include a rate
  source (`OQ-007`) and a price-lock rule (`OQ-008`).

### OQ-004 — Reviews, promo codes, blog: in v1 or not?
- **Asked by:** discovery (round 2)
- **Context:** Round 2 explicitly excluded only the wishlist. Reviews, discount/promo codes
  and a blog were left unselected — neither excluded nor agreed. They must not silently
  enter scope.
- **Options:**
  1. All three out of v1 → leanest v1, fastest to launch.
  2. Some subset in v1 → each adds a module or meaningful FR surface.
- **Recommendation:** `[REC]` all three out of v1 (launch-fast bias of DEC-003/DEC-008);
  add later via change request if customers ask.
- **Impact:** catalog/product FRs, checkout FRs, content module.
- **Answer:** **Promo codes in; reviews and blog out** (2026-09-20) — **DEC-018**. The
  `[REC]` was partially not accepted (promo codes). Promo capabilities pinned via `OQ-010`.

### OQ-005 — Payment failure mid-checkout
- **Asked by:** discovery (round 3; first ask returned unanswered)
- **Context:** DEC-003's core promise is online payment. The gateway call can fail
  (declined, timeout, user aborts at the gateway). What the software does next shapes the
  checkout FR and the reservation timeout (BR-1/DEC-013).
- **Options:**
  1. Retry from checkout: cart and entered details preserved; customer retries immediately.
  2. Full restart: customer re-enters checkout from the cart.
- **Recommendation:** `[REC]` retry from checkout — standard behaviour, lowest abandonment.
- **Impact:** checkout FR error behaviour, reservation expiry design.
- **Answer:** Retry from checkout; cart and details preserved (2026-09-20) — **DEC-014**.

### OQ-006 — Email confirmations vs minimal checkout fields (contradiction)
- **Asked by:** discovery (round 3 review) — **detected contradiction, escalated per rules**
- **Context:** DEC-012 sends email confirmations; DEC-009 collects no email address. Both
  cannot stand as written.
- **Options:**
  1. Optional email field at checkout → confirmations sent when provided; silent when not.
  2. Required email field → every order gets a confirmation; slightly more friction.
  3. Drop email confirmations → on-site status only; DEC-012 superseded.
- **Recommendation:** `[REC]` option 1 — optional email, on-site always available.
- **Impact:** checkout FRs, notification FRs, DEC-009/DEC-012 amendments.
- **Answer:** Optional email field at checkout (2026-09-20) — **DEC-017**; DEC-009 amended,
  DEC-012 stands.

### OQ-007 — Daily silver rate source
- **Asked by:** discovery (follow-up to DEC-016)
- **Context:** DEC-016 makes every price depend on a daily silver rate. The rate must exist
  every trading day, be trusted, and be auditable when a customer disputes a price.
- **Options:**
  1. Owner enters the rate in the admin panel each day → no external dependency, fully
     auditable, one manual step per day.
  2. Automated feed from a public/exchange source → no daily chore, but an external
     integration with its own failure behaviour.
- **Recommendation:** `[REC]` manual owner entry in v1 (simplest, zero external dependency);
  automation later via change request.
- **Impact:** pricing FRs, admin workflows, pricing engine design.
- **Answer:** Manual admin entry in v1, designed automation-ready (2026-09-20) — **DEC-019**;
  matches the `[REC]`. RISK-002 impact drops (no external dependency in v1).

### OQ-008 — Price-lock moment
- **Asked by:** discovery (follow-up to DEC-016)
- **Context:** With rate-tracked prices, the rate can change between "add to cart",
  checkout start, and payment. The business must know exactly which rate a paid order
  honours, or refunds/disputes become unresolvable.
- **Options:**
  1. Lock at checkout start, together with the stock reservation (BR-1) → one consistent
     snapshot per checkout; rate change mid-checkout never surprises the buyer.
  2. Lock at payment → later rate, but the displayed total can drift from the charged total.
- **Recommendation:** `[REC]` lock at checkout start (option 1) — pairs naturally with the
  reservation and is the least surprising to customers.
- **Impact:** checkout FRs, order totals, refund semantics.
- **Answer:** **Locked at payment** (2026-09-20) — **DEC-020**; the `[REC]` was **not**
  accepted. Stock reservation (DEC-013) and price lock are decoupled; UX must re-display the
  final total at the payment step.

### OQ-009 — Category taxonomy: starter list vs free-form
- **Asked by:** discovery (round 4; question returned unanswered and is re-asked)
- **Context:** DEC-006 needs categories for browsing and filters. A preset list makes
  navigation and filters predictable; free-form lets the owner shape it but can fragment
  navigation.
- **Options:**
  1. Starter taxonomy drafted in this spec (rings, necklaces, earrings, bracelets, sets,
     other), editable by the owner in admin.
  2. Owner defines categories freely from day one.
- **Recommendation:** `[REC]` option 1 — predictable navigation, still owner-editable.
- **Impact:** catalog FRs, navigation, filters.
- **Answer:** —

### OQ-010 — Promo code capabilities in v1
- **Asked by:** discovery (follow-up to DEC-018)
- **Context:** "Promo codes in v1" must be pinned to concrete behaviour so the checkout FRs
  are writable: what a code does, and what limits it has.
- **Options:**
  1. Percentage off the order total, with optional expiry and usage limit — simplest.
  2. Fixed amount off, same limits.
  3. Both types.
- **Recommendation:** `[REC]` percentage off with expiry + usage limit (option 1) for v1.
- **Impact:** checkout FRs, admin workflows, order totals (interacts with DEC-016/DEC-020).
- **Answer:** Percentage off + expiry + usage limit (2026-09-20) — **DEC-024**; matches the
  `[REC]`.

### OQ-011 — Uptime expectation
- **Asked by:** discovery (round 5; question returned unanswered)
- **Context:** Whether v1 carries a formal availability NFR (with monitoring and ops scope)
  or a best-effort, fix-fast posture.
- **Options:**
  1. Best-effort, fix-fast — no formal SLA in v1.
  2. Formal uptime target (99%+) with monitoring.
- **Recommendation:** `[REC]` option 1 for v1; revisit if launch traffic justifies it.
- **Impact:** NFR table, ops/hosting scope.
- **Trigger:** must be resolved before the human approves the requirements spec.
- **Answer:** Best-effort, fix-fast; no formal SLA in v1 (2026-09-20) — **DEC-031**.

### OQ-012 — Launch deadline
- **Asked by:** discovery (rounds 6–7; question returned unanswered)
- **Context:** DEC-008 says the project proceeds regardless; a hard deadline would still
  change milestone planning and wave sizes.
- **Options:**
  1. No fixed date — quality gates decide readiness.
  2. Fixed date (owner supplies it) — becomes a hard constraint.
- **Recommendation:** `[REC]` option 1, consistent with DEC-008.
- **Trigger:** must be resolved before the human approves the requirements spec.
- **Answer:** No fixed date; quality gates decide readiness (2026-09-20) — **DEC-032**.
