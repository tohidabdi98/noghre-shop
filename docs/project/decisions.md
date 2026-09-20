# Decisions — decision log and architecture decision records

> Two things live here, both append-only:
> * **`DEC-###` — decisions.** Any consequential choice made by a human or agent, with rationale.
> * **`ADR-###` — architecture decision records.** Significant, hard-to-reverse technical choices.
>
> Rules
> * Never rewrite history: supersede an old entry by adding a new one and marking the old
>   `superseded by ADR-###`.
> * Every entry names its **decider** (human or agent id) and its **status**:
>   `proposed` · `accepted` · `rejected` · `superseded` · `deprecated`.
> * The Discovery Agent records product decisions; the Architecture Agent publishes ADRs;
>   any role may record a `DEC-###` for a decision inside its scope.
> * A `[REC]` (recommendation) that the human has not answered stays a `[REC]` — agents must not
>   turn a recommendation into a decision silently.

## Decision index

| ID | Title | Type | Status | Decider | Date |
|---|---|---|---|---|---|
| DEC-001 | Instantiate from TemplateProject | process | accepted | human | — |
| DEC-002 | NoghreShop is the owner's own single-vendor silver business | product | accepted | human | 2026-09-20 |
| DEC-003 | v1 = full online sales (browse → cart → pay online → order) | product | accepted | human | 2026-09-20 |
| DEC-004 | Domestic retail market only; Farsi-only RTL storefront | product | accepted | human | 2026-09-20 |
| DEC-005 | Guest checkout + optional accounts in v1 | product | accepted | human | 2026-09-20 |
| DEC-006 | Discovery = categories + search + filters | product | accepted | human | 2026-09-20 |
| DEC-007 | Wishlist/favorites out of scope for v1 | product | accepted | human | 2026-09-20 |
| DEC-008 | Catalog 50–200 items; no postponement triggers | product | accepted | human | 2026-09-20 |
| DEC-009 | Checkout collects name + phone + address only | product | accepted | human | 2026-09-20 |
| DEC-010 | Customer-visible order lifecycle: Paid → Shipped → Delivered | product | accepted | human | 2026-09-20 |
| DEC-011 | Admin v1: product CRUD + stock + orders + basic sales overview | product | accepted | human | 2026-09-20 |
| DEC-012 | Notifications: email + on-site; no SMS in v1 | product | accepted | human | 2026-09-20 |
| DEC-013 | Stock reserved at checkout start; no overselling | product | accepted | human | 2026-09-20 |
| DEC-014 | Payment failure → retry from checkout, cart preserved | product | accepted | human | 2026-09-20 |
| DEC-015 | Delivery with online payment only; no COD in v1 | product | accepted | human | 2026-09-20 |
| DEC-016 | Pricing = weight × daily silver rate + craft fee | product | accepted | human | 2026-09-20 |
| DEC-017 | Optional email field at checkout (amends DEC-009) | product | accepted | human | 2026-09-20 |
| DEC-018 | Promo codes IN for v1; reviews and blog OUT | product | accepted | human | 2026-09-20 |
| DEC-019 | Daily rate: manual admin entry in v1, automation-ready design | product | accepted | human | 2026-09-20 |
| DEC-020 | Price locked at payment (not at checkout start) | product | accepted | human | 2026-09-20 |
| DEC-021 | Guest order tracking: order code + phone lookup AND email link | product | accepted | human | 2026-09-20 |
| DEC-022 | Products carry a multi-photo gallery | product | accepted | human | 2026-09-20 |
| DEC-023 | Starter category taxonomy in the spec, owner-editable | product | accepted | human | 2026-09-20 |
| DEC-024 | Promo codes: % off + expiry + usage limit | product | accepted | human | 2026-09-20 |
| DEC-025 | v1 success: first end-to-end orders + fully listed catalog; volume/traffic expectations accepted as planning basis | product | accepted | human | 2026-09-20 |
| DEC-026 | Policy pages (shipping, returns/refund, contact) in v1 | product | accepted | human | 2026-09-20 |
| DEC-027 | Domestic hosting/cloud preferred | product | accepted | human | 2026-09-20 |
| DEC-028 | No stack preference — Architecture Agent decides | product | accepted | human | 2026-09-20 |
| DEC-029 | No existing product data — catalog built from scratch in admin | product | accepted | human | 2026-09-20 |
| DEC-030 | Minimal running-cost posture | product | accepted | human | 2026-09-20 |
| DEC-031 | Availability posture: best-effort, fix-fast (no formal SLA) | product | accepted | human | 2026-09-20 |
| DEC-032 | No fixed launch deadline | product | accepted | human | 2026-09-20 |
| DEC-033 | OQ-001 (payment gateway) knowingly accepted as launch risk | product | accepted | human | 2026-09-20 |
| DEC-034 | Requirements specification approved | process | accepted | human | 2026-09-20 |

---

## DEC-001 — Instantiate this project from TemplateProject
- **Status:** accepted · **Decider:** human
- **Context:** Starting a new project with agent-driven development.
- **Decision:** Use the TemplateProject framework: discovery → UX → architecture →
  decomposition → per-module agents → review/testing/integration → human approval.
- **Alternatives considered:** ad-hoc prompting without written specs.
- **Consequences:** documentation and state files are part of the deliverable; agents must obey
  `AGENTS.md`; every module has one owner.

---

## DEC-002 — Single-vendor, owner-operated silver jewelry business
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Discovery round 1 — whose business the store is.
- **Decision:** NoghreShop sells the owner's own silver jewelry. Not a marketplace, not a
  client project; one seller.
- **Consequences:** no vendor onboarding/split-payment machinery; admin is single-operator
  (user count still open); catalog is homogeneous (silver jewelry).

---

## DEC-003 — v1 delivers full online sales
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Round 1 — the #1 thing v1 must do; alternatives were showcase + manual
  inquiry ordering, or "recommend for me".
- **Decision:** v1 supports the complete purchase flow: browse → cart → **online payment** →
  order confirmation. Not an inquiry/showcase site.
- **Consequences:** a domestic payment gateway must be obtainable before launch (ASM-001,
  `OQ-001`); order state tracking becomes a requirement; manual-payment fallback is not the
  primary flow but may exist as error behaviour.

---

## DEC-004 — Domestic retail only; Farsi-only RTL
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Round 1 — target customers and storefront language.
- **Decision:** v1 serves domestic retail buyers; interface is Farsi only, right-to-left.
  No international sales, no English UI, no bilingual switcher in v1.
- **Consequences:** no multi-currency or i18n machinery in v1; RTL correctness is a first-class
  quality bar (input to Frontend/UX Agent); cross-border expansion later would be a change
  request.

---

## DEC-005 — Guest checkout with optional accounts
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Round 2 — what v1 requires of a buyer.
- **Decision:** Anyone can complete checkout as a guest. Registration is optional and exists
  to add order history and faster repeat buying.
- **Consequences:** orders must work without an account (contact info identifies the order);
  account module cannot be a hard dependency of checkout; auth scope shrinks for v1.

---

## DEC-006 — Product discovery: categories + search + filters
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Round 2 — how customers find products; alternatives were categories only or
  categories + search.
- **Decision:** v1 ships category browsing, free-text search, and filters (price range,
  weight, stone/no-stone).
- **Consequences:** product data model must carry weight and stone-presence attributes;
  filter UI is input to the Frontend/UX Agent; search backend needed for 50–200 items
  (simple, not enterprise search).

---

## DEC-007 — Wishlist/favorites excluded from v1
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Round 2 — explicit exclusions.
- **Decision:** No wishlist/favorites feature in v1.
- **Consequences:** none beyond scope clarity; revisit via change request if demanded.

---

## DEC-008 — Catalog 50–200 items; project proceeds regardless
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Round 2 — catalog size and postpone triggers.
- **Decision:** Launch catalog is 50–200 items. There are no postpone/cancel triggers: the
  store is built regardless of budget or timeline overrun.
- **Consequences:** ASM-003 confirmed (manual catalog management, no bulk tooling);
  pagination and admin ergonomics become quality requirements; schedule pressure is accepted
  by the human.

---

## DEC-009 — Minimal checkout data
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Round 3 — what a buyer must provide to place an order.
- **Decision:** Name, phone number, delivery address. Nothing else is required.
- **Consequences:** least purchase friction; email is NOT collected by default — conflicts
  with DEC-012 (email confirmations), resolved via `OQ-006`.

---

## DEC-010 — Three-state order lifecycle
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Round 3 — post-payment order states.
- **Decision:** Paid → Shipped → Delivered, forward-only (BR-2). No self-cancellation
  window in v1.
- **Consequences:** refunds/cancellations handled manually by the owner outside v1 scope;
  simplest order state machine.

---

## DEC-011 — Admin capabilities for v1
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Round 3 — owner's tooling.
- **Decision:** All four selected: product CRUD with photo upload, stock/availability
  control, order view + status advancement, basic sales overview (counts/totals).
- **Consequences:** photo upload/storage is a v1 requirement; reporting stays list-level.

---

## DEC-012 — Email + on-site notifications; no SMS in v1
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Round 3 — customer notifications; SMS was offered as recommendation and
  **not** selected by the human.
- **Decision:** Order confirmation and status changes reach the customer by **email** and
  are always visible **on-site**. No SMS in v1.
- **Consequences:** an email sending service is a v1 integration; contradicts DEC-009's
  field list (no email collected) — must be resolved via `OQ-006` before checkout FRs are
  written.

---

## DEC-013 — Reserve stock at checkout start
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Round 3 — two customers want the last item (BR-1).
- **Decision:** Stock is reserved when checkout starts; the other buyer then sees "out of
  stock". No overselling.
- **Consequences:** reservations need expiry (abandoned checkouts must release stock —
  timeout to be specified in the checkout FR); simplest guarantee that never lies to a
  paying customer.

---

## DEC-014 — Payment failure: retry from checkout
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** OQ-005 (first ask returned unanswered; re-asked) — what happens when the
  gateway call fails mid-checkout.
- **Decision:** Cart and entered details are preserved; the customer retries the payment
  immediately from checkout.
- **Consequences:** checkout state must survive a failed payment round-trip; reservation
  (DEC-013) must outlive a failed attempt and expire on true abandonment.

---

## DEC-015 — Online payment only; no cash-on-delivery in v1
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** OQ-002 — delivery and COD.
- **Decision:** v1 sells exclusively via online payment (DEC-003). No cash-on-delivery.
- **Consequences:** simplest order state machine (DEC-010); no payment-on-delivery handling;
  COD can return later via change request.

---

## DEC-016 — Rate-tracked pricing: weight × daily silver rate + craft fee
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** OQ-003 — fixed vs market-tracked prices. The discovery `[REC]` was fixed
  prices; the human chose rate-tracking instead (the business cannot operate otherwise).
- **Decision:** A product's price is computed as **weight × daily silver rate + craft fee**.
  The daily silver rate is a first-class input; owner enters weight and craft fee per item.
- **Consequences:** a daily-rate source is required (new integration or manual admin entry,
  `OQ-007`); the customer-facing price must be **locked at a defined moment** (`OQ-008`) or
  payments and shipments can disagree; price-range filters operate over computed prices
  (architecture implication); product admin stores weight + craft fee, not a price.

---

## DEC-017 — Optional email field at checkout (amends DEC-009)
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** OQ-006 — contradiction between DEC-012 (email confirmations) and DEC-009
  (name + phone + address only).
- **Decision:** Checkout collects an **optional** email in addition to name, phone, address.
  Confirmation email is sent when provided; on-site order status is always available.
- **Consequences:** DEC-009's field list gains one optional field; DEC-012 stands; guests
  without email rely on on-site tracking (mechanism to be specified in round 4).

---

## DEC-018 — Promo codes in v1; reviews and blog out
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** OQ-004 — round 2 left reviews/promo codes/blog undecided.
- **Decision:** v1 includes **discount/promo codes** at checkout. Product reviews/ratings
  and a blog are explicitly **out** of v1.
- **Consequences:** promo application interacts with DEC-016 computed prices (a code applies
  on top of the rate-computed total); owner needs promo management in admin (extends
  DEC-011 — capabilities pinned via `OQ-010`); no moderation or content tooling in v1.

---

## DEC-019 — Daily silver rate: manual entry in v1, automation-ready
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** OQ-007 — rate source for DEC-016.
- **Decision:** v1 ships **manual rate entry in the admin panel** as the default mechanism,
  designed so an automated feed can be plugged in later (change request, no re-architecture).
- **Consequences:** no external rate integration in v1 (removes a failure mode, RISK-002
  impact drops); admin gains a "daily rate" screen with history; staleness must be visible
  to the owner (a trading day without a rate must be obvious).

---

## DEC-020 — Price locked at payment
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** OQ-008 — with rate-tracked prices (DEC-016), the rate can change between
  checkout start and payment. The discovery `[REC]` was locking at checkout start; the human
  chose **payment** as the lock moment.
- **Decision:** The order's authoritative total is the price computed from the rate at the
  moment payment completes.
- **Consequences:** the displayed total may change between checkout start and payment — the
  Frontend/UX Agent must design for this (re-display of the final total at the payment
  step; no silent drift); the charged amount is always the authoritative one; refund
  semantics reference the paid amount. Stock remains reserved at checkout start (DEC-013) —
  reservation and price lock are deliberately decoupled.

---

## DEC-021 — Guest order tracking: code + phone AND email link
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Round 4 — how a guest checks order status on-site.
- **Decision:** Every order gets a code; status is queryable on-site with **order code +
  phone number** (works with no email), and additionally via the link in the confirmation
  email when an email was provided (DEC-017).
- **Consequences:** the order-lookup flow needs anti-enumeration care (code must be
  unguessable enough paired with phone) — note for the Architecture Agent.

---

## DEC-022 — Multi-photo product gallery
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Round 4 — product photography for jewelry.
- **Decision:** Products carry a multi-photo gallery (upload several images per product in
  admin; swipeable gallery on the storefront).
- **Consequences:** photo upload/storage handles sets per product; gallery UI is input to
  the Frontend/UX Agent; image optimisation matters for mobile users.

---

## DEC-023 — Starter category taxonomy, owner-editable
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** OQ-009 (re-asked after being skipped in round 4).
- **Decision:** v1 launches with the starter taxonomy **rings, necklaces, earrings,
  bracelets, sets, other**, editable by the owner in admin (rename, regroup, add).
- **Consequences:** navigation and filters are predictable from day one; taxonomy lives in
  the spec and in admin seed data, not hard-coded.

---

## DEC-024 — Promo code capabilities
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** OQ-010 — pinning DEC-018 to concrete behaviour.
- **Decision:** A promo code gives a **percentage off the order total**, with owner-set
  **expiry date** and **maximum usage count**. No fixed-amount codes in v1.
- **Consequences:** checkout applies the code before payment; with DEC-016/DEC-020 the code
  applies on top of the rate-computed, payment-locked total; admin gains code CRUD (extends
  DEC-011).

---

## DEC-025 — Success criteria and planning expectations
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Round 5 — measurable success and expected volume.
- **Decision:** 90-day success = (1) first orders completed **end-to-end without owner
  rescue**, (2) launch catalog **fully listed** (photos, weight, craft fee, category).
  Planning basis: **a few orders per day**, **100–1,000 visitors/day** (social-traffic
  spikes, mobile-heavy). Revenue targets and repeat-customer metrics are *not* v1 success
  criteria.
- **Consequences:** SC-1/SC-2 defined in `requirements.md` §1.5; ASM-004 records the volume
  expectations; NFR scale/perf targets derive from these numbers ([REC]-tagged until spec
  approval).

---

## DEC-026 — Policy pages in v1
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Rounds 6–7 — online-payment-only orders (DEC-015) need a stated refund path;
  domestic e-commerce norm is visible policies.
- **Decision:** v1 ships shipping, returns/refund, and contact pages; the owner provides the
  wording, editable in admin (FR-PAGE-1).
- **Consequences:** refunds follow the owner's published policy (manual, outside the order
  state machine per DEC-010); content is seed data, not hard-coded.

---

## DEC-027 — Domestic hosting/cloud preferred
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Rounds 6–7 — hosting preference; trade-offs are the Architecture Agent's.
- **Decision:** Preference for domestic hosting (market latency, payment-gateway fit).
- **Consequences:** an ADR must weigh domestic vs international providers against NFR-PERF-1,
  NFR-SCALE-1, DEC-030, and `OQ-001` gateway constraints.

---

## DEC-028 — No stack preference
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Rounds 6–7 — technology preferences.
- **Decision:** No language/framework/CMS preference. The Architecture Agent recommends a
  maintainable stack fitting the NFRs, RTL needs, and DEC-030.
- **Consequences:** stack choice lands in an ADR; RTL/`NFR-A11Y-1` competence is a selection
  criterion.

---

## DEC-029 — No existing product data
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Rounds 6–7 — starting material for the catalog.
- **Decision:** No spreadsheet or existing listing; the 50–200 launch items are entered
  manually through the admin (DEC-008, ASM-003 confirmed this is workable).
- **Consequences:** no import tooling in v1; admin entry ergonomics matter for SC-2.

---

## DEC-030 — Minimal running costs
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Rounds 6–7 — budget posture for hosting/services.
- **Decision:** Minimal spend: cheap hosting, free tiers where sensible; scale up only when
  traffic (ASM-004) demands.
- **Consequences:** architecture favours low fixed cost over managed convenience; revisit at
  a spike via change request.

---

## DEC-031 — Best-effort availability
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** OQ-011 (skipped in round 5, resolved at review).
- **Decision:** No formal uptime SLA in v1; issues fixed promptly.
- **Consequences:** no availability NFR or monitoring added to v1 scope; revisited if launch
  traffic justifies.

---

## DEC-032 — No fixed launch deadline
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** OQ-012 (skipped in rounds 6–7, resolved at review).
- **Decision:** No fixed date; quality gates decide readiness.
- **Consequences:** consistent with DEC-008; milestone targets stay soft.

---

## DEC-033 — Payment gateway knowingly accepted as launch risk
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** OQ-001 is unresolved (no gateway application filed). The approval checklist
  allows open items that are **knowingly accepted as risks**.
- **Decision:** The requirements specification is approved with OQ-001 open, knowingly
  accepted as RISK-001 (score 15). The owner commits to filing the gateway application
  immediately.
- **Consequences:** checkout/payment implementation cannot start until OQ-001 resolves; the
  payment module will be `blocked` at decomposition if it is still open; RISK-001 stays
  owner-owned with escalation at every milestone.

---

## DEC-034 — Requirements specification approved
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** Discovery interview rounds 1–10 complete; all completion criteria verified
  (FRs with ACs, NFRs with verification, scope/out-of-scope explicit, uncertainties tagged,
  `tp.py validate` green).
- **Decision:** The human approves the requirements specification as written
  (`docs/project/requirements.md`, 14 FRs, 7 NFRs, 4 business rules, data, integrations).
  `state/project.yaml → gates.requirements_approved = true`, `spec_status: approved`.
- **Consequences:** discovery is complete; the Frontend/UX Agent and Architecture Agent are
  unblocked; implementation still requires UX → architecture → decomposition gates.

---

## ADR template — copy for each record

### ADR-### — <short title>
- **Status:** proposed · **Date:** — · **Decider:** architecture agent · **Supersedes:** —
- **Context:** <!-- forces at play: requirements, NFRs, constraints, team/agent constraints -->
- **Options considered:**
  1. <!-- option A — pros / cons -->
  2. <!-- option B — pros / cons -->
- **Decision:** <!-- the choice, stated as an instruction an agent can follow -->
- **Rationale:** <!-- why this option beats the others, including agent-parallelism impact -->
- **Consequences:** <!-- what becomes easy, what becomes hard, what must be revisited -->
- **Reversibility:** easy / moderate / hard — and the cost of changing later
- **Affected modules:** `MODULE-ID`s
- **Verification:** <!-- how we will know this decision was right -->
- **References:** requirements `FR-###`, UX `UX-###`, architecture §
