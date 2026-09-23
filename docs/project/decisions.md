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
| DEC-035 | Visual identity created in-project; direction: modern minimal | ux | accepted | human | 2026-09-20 |
| DEC-036 | James Avery storefront adopted as the UX reference to adapt | ux | accepted | human | 2026-09-20 |
| DEC-037 | Storefront mobile-first; admin desktop-first | ux | accepted | human | 2026-09-20 |
| DEC-038 | v1 catalog: silver jewelry including silver bars (شمش) | product | accepted | human | 2026-09-20 |
| DEC-039 | Homepage composition accepted; small public rate display on home | ux | accepted | human | 2026-09-20 |
| DEC-040 | Storefront navigation: header + drawer, no bottom bar; search = results page | ux | accepted | human (delegated to frontend-ux) | 2026-09-20 |
| DEC-041 | Cart as drawer everywhere; checkout is a single page | ux | accepted | human (REC fallback) | 2026-09-20 |
| DEC-042 | Admin shell in Farsi with sidebar sections | ux | accepted | human (REC fallback) | 2026-09-20 |
| DEC-043 | "Design of the Month" featured slot adopted from James Avery | ux | accepted | human | 2026-09-20 |
| DEC-044 | Brand mark: Persian wordmark + geometric motif | ux | accepted | human (defaults delegated) | 2026-09-20 |
| DEC-045 | Palette: monochrome silver base + deep-green accent | ux | superseded (accent only) by DEC-050 | human (defaults delegated) | 2026-09-20 |
| DEC-046 | Storefront copy tone: warm-polite Persian («شما») | ux | accepted | human (defaults delegated) | 2026-09-20 |
| DEC-047 | Hero content owner-editable with tasteful default | ux | accepted | human (defaults delegated) | 2026-09-20 |
| DEC-048 | Trust row uses generic payment wording until OQ-001 resolves | ux | accepted | human (defaults delegated) | 2026-09-20 |
| DEC-049 | Homepage product row: new arrivals until paid-order data exists, then bestsellers | ux | accepted | human (defaults delegated) | 2026-09-20 |
| DEC-050 | Accent = the stone of the month (birthstone), replacing the deep-green accent | ux | superseded (calendar only) by DEC-053 | human | 2026-09-21 |
| DEC-051 | Moonstone (ماه‌سنگ) specialization: homepage band + first-class stone value | product | superseded (band only) by DEC-052 | human | 2026-09-21 |
| DEC-052 | Homepage stone section: the twelve-stone album (replaces the moonstone band) | product | accepted | human | 2026-09-21 |
| DEC-053 | Stone of the month follows the Gregorian calendar (accent + album keyed by Gregorian month) | product | accepted | human | 2026-09-21 |
| DEC-054 | UX specification approved — `gates.ux_approved` set on `reports/ux-gate-review-2026-09-21.md` | process | accepted | human | 2026-09-21 |
| ADR-001 | Modular monolith: TypeScript end-to-end on Next.js (App Router), one deployable | architecture | accepted | human (delegated to architecture) | 2026-09-21 |
| ADR-002 | PostgreSQL 16 as the single data store; Prisma for schema and ordered migrations | architecture | accepted | human (delegated to architecture) | 2026-09-21 |
| ADR-003 | Deployment: one domestic VPS, Docker Compose (edge + web + worker + db), Caddy TLS | architecture | accepted | human | 2026-09-21 |
| ADR-004 | Payment boundary: internal `PaymentProvider` port with a sandbox adapter; no card data | architecture | accepted | human | 2026-09-21 |
| ADR-005 | Auth: guest-first signed cookie session; optional phone+password accounts; separate admin session | architecture | accepted | human | 2026-09-21 |
| ADR-006 | Cart and checkout state live server-side (signed cookie + DB row), never in localStorage | architecture | accepted | human (delegated to architecture) | 2026-09-21 |
| ADR-007 | Monthly theme resolved server-side into `data-month` + CSS custom properties | architecture | accepted | human (delegated to architecture) | 2026-09-21 |
| ADR-008 | Notifications through a DB-backed outbox consumed by the worker (email in v1) | architecture | accepted | human (delegated to architecture) | 2026-09-21 |
| ADR-009 | Observability: structured logs + admin failure surface; no paid APM in v1 | architecture | accepted | human (delegated to architecture) | 2026-09-21 |
| ADR-010 | Testing architecture: Vitest + real Postgres in a container + Playwright visual/a11y evidence | architecture | accepted | human (delegated to architecture) | 2026-09-21 |

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

## DEC-035 — Visual identity is created in-project; direction: modern minimal
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** UX round 1 — the business has no existing logo, colours or visual identity
  (no Instagram kit, no printed material to inherit).
- **Decision:** The Frontend/UX Agent creates the visual identity during the UX phase
  (logo/wordmark, palette, type ramp in `design_system.md`). The direction is **modern
  minimal**: whitespace, restrained palette, photos and prices carry the page (PRIN-3).
- **Alternatives considered:** classic/luxurious (jewel tones, serif feel); warm/traditional
  Persian craft motifs.
- **Consequences:** design tokens stay few and cheap (DEC-030); identity work is part of
  `gates.ux_approved`; the owner reviews and approves the visual identity before screens are
  validated against it.

---

## DEC-036 — James Avery storefront adopted as the UX reference
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** UX round 1 — the human named jamesavery.com as the site to take ideas from.
- **Decision:** Storefront patterns are adapted from James Avery: category tiles, seasonal
  hero, product cards (name · price · material), a trust row, and a brand-story block.
- **Consequences:** patterns are re-derived for RTL/Farsi (DEC-004) and rate-tracked pricing
  (DEC-016) — nothing is copied verbatim; JA features that NoghreShop excludes (engraving,
  store pickup, wishlists) are not carried over.

---

## DEC-037 — Storefront mobile-first; admin desktop-first
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** UX round 1 — platform priorities (DEC-025 mobile-heavy social traffic;
  NFR-MAINT-1 owner's daily workspace).
- **Decision:** The storefront is specified and optimised mobile-first; the admin is
  specified desktop-first and usable on tablet.
- **Consequences:** UX-006 governs storefront performance; UX-007 governs admin ergonomics;
  admin-on-phone is an open minor question (see `ux_requirements.md` §7).

---

## DEC-038 — v1 catalog: silver jewelry including silver bars
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** UX round 2 — the owner clarified the business scope: "we will only sell silver
  jewelry, including silver bars".
- **Decision:** The catalog sells the owner's silver products **including silver bars
  (شمش نقره)**. The category seed gains «شمش نقره» alongside the DEC-023 starter list
  (owner-editable per DEC-023). Product presentation for bars emphasises weight and purity
  rather than stone/wear attributes; craft fee may be zero for bars (BR-4 unchanged).
- **Consequences:** filters like stone/no-stone simply do not apply to bar items; photo style
  guide (OQ-014) includes a bar setup (hallmark visible, neutral background); requirements.md
  wording ("silver jewelry") is understood to include bars — no FR changes required.

---

## DEC-039 — Homepage composition accepted; small public rate display
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** UX round 2 — homepage blocks proposal and rate transparency.
- **Decision:** Homepage order: hero → category tiles → new/bestselling products → trust row →
  craft story. A **small** silver-rate display (rate + date) appears on the homepage in
  addition to per-product rate dating (UX-001).
- **Consequences:** rate chip is secondary-styled, never competes with products (PRIN-3);
  shows last-known rate + date when stale, hidden when no rate was ever entered (PRIN-5);
  a new UX-010 records it.

---

## DEC-040 — Storefront navigation pattern (delegated choice)
- **Status:** accepted · **Decider:** frontend-ux (human delegated: "chose yourself") · **Date:** 2026-09-20
- **Context:** UX round 2 — mobile navigation pattern.
- **Decision:** Header categories + hamburger drawer on mobile; **no sticky bottom bar**.
  Search is a dedicated results page (no typeahead dropdown in v1).
- **Rationale:** jewelry shopping is browse-heavy; drawers keep screen space for imagery;
  typeahead adds complexity without clear value at 50–200 items (DEC-008).
- **Consequences:** cart icon persistent with count; track order + account in drawer + footer.

---

## DEC-041 — Cart drawer everywhere; single-page checkout
- **Status:** accepted · **Decider:** human (frontend-ux `[REC]` unanswered → fallback applied) · **Date:** 2026-09-20
- **Context:** UX round 2 — cart and checkout shape.
- **Decision:** The cart is a slide-in drawer on all widths (full `/cart` page exists as the
  keyboard/shareable path). Checkout is **one compact page** with sections (contact → address
  → review & pay); the gateway redirect remains the single irreversible step (UX-009).
- **Consequences:** fewer taps on mobile (PRIN-1/UX-002); promo field lives in checkout as a
  labelled collapsible; failure paths return to the same page (DEC-014).

---

## DEC-042 — Admin shell in Farsi with sidebar sections
- **Status:** accepted · **Decider:** human (frontend-ux `[REC]` unanswered → fallback applied) · **Date:** 2026-09-20
- **Context:** UX round 2 — admin language and structure (NFR-MAINT-1).
- **Decision:** Admin UI is **Farsi** (RTL). Sidebar sections: Overview · Orders · Catalog ·
  Daily rate · Promotions · Pages · Featured design.
- **Consequences:** matches PRIN-6; the Featured-design section is the DEC-043 admin surface;
  decomposition seeds these sections as the admin module map.

---

## DEC-043 — "Design of the Month" featured slot (from James Avery)
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-20
- **Context:** UX round 2 — human explicitly wants James Avery's "Design of the Month".
- **Decision:** The homepage carries a featured-design slot. The owner picks one product (and
  an optional short note) in `/admin/featured`; the slot shows that product; **hidden when
  nothing is selected** (never an empty placeholder on the storefront).
- **Consequences:** extends the admin surface by one small screen (DEC-042) — decomposition
  must include it; no scheduling automation in v1 (manual monthly pick).

---

## DEC-044 — Brand mark: Persian wordmark + geometric motif
- **Status:** accepted · **Decider:** human (defaults delegated) · **Date:** 2026-09-20
- **Decision:** The logo is a clean Persian **wordmark** «نقره‌شاپ» with a subtle geometric
  ingot/ring motif; no separate pictorial logo. Specifications in `design_system.md`.

## DEC-045 — Palette: monochrome silver base + deep-green accent
- **Status:** superseded (accent clause only) by `DEC-050` · **Decider:** human (defaults delegated) · **Date:** 2026-09-20
- **Amendment (2026-09-21):** the silver base palette stands unchanged; the fixed deep-green accent
  is replaced by the stone-of-the-month accent — see `DEC-050` and `design_system.md` §2.1.
- **Decision:** Near-white surfaces, near-black text, silver grays; **one** accent — deep
  green (#0E5F4B family) — reserved for primary actions and positive states. Full token set
  in `design_system.md`.

## DEC-046 — Storefront copy tone: warm-polite Persian
- **Status:** accepted · **Decider:** human (defaults delegated) · **Date:** 2026-09-20
- **Decision:** Storefront copy uses warm-polite Persian: always «شما», short plain
  sentences, no stiff bureaucratic register and no over-familiarity. Admin copy stays plain
  and functional (PRIN-6). Copy rules live in `interaction_patterns.md`.

## DEC-047 — Hero content owner-editable with default
- **Status:** accepted · **Decider:** human (defaults delegated) · **Date:** 2026-09-20
- **Decision:** The homepage hero (image + one line) is owner-editable in admin, reusing the
  FR-PAGE-1 content machinery; an elegant default renders when unset. Extends the content
  module's scope — decomposition must include it.

## DEC-048 — Trust row wording generic until the gateway is named
- **Status:** accepted · **Decider:** human (defaults delegated) · **Date:** 2026-09-20
- **Decision:** Trust row: «ارسال به سراسر کشور» · «ضمانت بازگشت» · «پرداخت امن آنلاین» —
  the payment line names no provider until OQ-001 resolves; policy wording stays
  owner-provided (FR-PAGE-1).

## DEC-049 — Homepage product row: new arrivals until real data
- **Status:** accepted · **Decider:** human (defaults delegated) · **Date:** 2026-09-20
- **Decision:** The homepage product row shows **newest items** at launch; once real paid
  orders exist it switches to bestsellers (by paid-order count). No owner setting in v1.

---

## DEC-050 — Storefront accent: the stone of the month (birthstone)
- **Status:** superseded (calendar clause) by `DEC-053` · **Decider:** human · **Date:** 2026-09-21 · **Supersedes:** `DEC-045` (accent clause only)
- **Context:** the owner asked for the accent to carry the business instead of a fixed deep green:
  the theme should follow **the stone of the month (سنگ ماه تولد)**, so the storefront's accent
  changes with the calendar and the moonstone season states itself. The list used is the
  Persian/Iranian birthstone convention that pairs each **Jalali** month with the birthstone of its
  dominant Gregorian month (فروردین ≈ آوریل = الماس، اردیبهشت ≈ مه = زمرد، …، خرداد ≈ ژوئن =
  مروارید و ماه‌سنگ، …, اسفند ≈ مارس = آکوامارین).
- **Decision:** `color.accent.*` is derived from the current Jalali month's stone. Twelve accent
  sets (`accent` / `hover` / `subtle`, plus a decorative `accent.stone` swatch) are declared in
  `design_system.md` §2.1 and selected at render time by `<html data-month="1…12">`; the raw stone
  colour is decorative only. Every set keeps ≥ 4.5:1 against white with `#FFFFFF` text (actual
  minimum 5.8:1). Semantic states (`success`, `warning`, `danger`) are fixed and never follow the
  accent.
- **Rationale:** one accent at a time still satisfies PRIN-3 (quiet chrome), while a monthly cycle
  gives the shop a reason to be revisited and makes the moonstone offering legible without adding
  chrome. Contrast-checked token values keep WCAG AA independent of the owner's taste in stones.
- **Consequences:** the token file (shared zone) gains twelve accent sets and a month resolver;
  storefront-only — admin stays neutral; visual baselines become month-dependent, so the
  theme-integrity check pins a month via `theme.monthPreview`; rollover must be colour-only (no
  layout shift) and cache keys must not freeze a stale month. `OQ-015` keeps open whether the accent
  follows the calendar month (default) or the individual visitor's own birth month. **The calendar
  clause alone is superseded by `DEC-053`**: the theme now runs on the Gregorian calendar, so stone
  and month are the same month (the twelve accent values are unchanged).

---

## DEC-051 — Moonstone (ماه‌سنگ) specialization: homepage band + first-class stone value
- **Status:** superseded (band clause) by `DEC-052` · **Decider:** human · **Date:** 2026-09-21
- **Context:** the owner sells moonstone-set silver as a speciality and wants it visible on the
  homepage ("a section dedicated to exploring moonstones"), with the monthly accent reinforcing it
  (`DEC-050`).
- **Decision:**
  (a) `SCR-001` gains an **evergreen** «کاوش ماه‌سنگ» band between the product row and the trust row:
  short education (۲–۳ lines), an optional owner photo, and a CTA to the moonstone-filtered results;
  (b) the product attribute «سنگ» gains a **type** when «دارد» is chosen, with «ماه‌سنگ» as the v1
  value, so the band's CTA is a real shareable URL (`/search?stone=moonstone`) and the stone filter
  gains a «ماه‌سنگ» option;
  (c) خرداد — the month whose birthstone is مروارید/ماه‌سنگ — is the anchor of the accent cycle, but
  the band itself does not depend on the month.
- **Consequences:** `FR-CAT-2` and `FR-ADM-1` each need one added value (one filter option, one
  product field) — recorded here because the requirement text is owned by the Discovery Agent; with
  zero tagged items the band renders in education-only mode (no CTA, never a dead link); `OQ-016`
  decides how far the stone taxonomy and any dedicated landing page go. **Clause (a) is superseded by
  `DEC-052`** — the homepage stone section is now the twelve-stone album, without the band, its
  education copy or its CTA; **clause (b) stands** (the «ماه‌سنگ» product value and filter option).

---

## DEC-052 — Homepage stone section: the twelve-stone album (replaces the moonstone band)
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-21 · **Supersedes:** `DEC-051` (clause a only)
- **Context:** the owner reviewed the band and asked that *this part* show **the twelve stones
  correlated to months** (`DEC-050`) — "just the twelve month stones, not ماه‌سنگ", with the current
  month highlighted, the other months selectable, and nothing long. A moonstone block tells one
  month's story, while the accent already visits twelve stones a year and the birthstone list is the
  only homepage content that is evergreen, free and inherently seasonal.
- **Decision:**
  (a) the homepage stone section is a **compact album of the twelve month stones** between the
  product row and the trust row: each tile carries the Gregorian month (Farsi + Latin, `DEC-053`)
  and the stone's Farsi + Latin name; the current month's tile is highlighted (border + the text «این ماه»); no
  education paragraph, no photo, no CTA, and no care/«در نقره» lines on the homepage;
  (b) the album **replaces** the «کاوش ماه‌سنگ» band. `DEC-051` clause (b) stands: «ماه‌سنگ» stays a
  product value and a stone-filter option, so the speciality is reached through category and search
  rather than a homepage CTA;
  (c) content comes from `design_system.md` §2.2 — the stone names shown on the homepage are the
  short half of that table; the correlation, «در نقره» and care lines stay in the reference table for
  the chip, the admin field and any future per-stone surface (they are not rendered in the album).
  In the storefront the album is **static and non-interactive**: no data call, no new route, no filter
  behind a tile. Selecting a tile is a **review-build affordance**: in `style_tile.html` it applies
  that month's accent so the twelve sets can be compared side by side;
  (d) the album sits inside the accepted composition, so the homepage order and the six-block
  structure are unchanged (`UX-010`) — the block that was the band is now the album.
- **Rationale:** the album is the smallest thing that makes the monthly accent legible — twelve
  months at a glance, two short lines each, no copy to maintain and no dependency on a catalogue that
  is still being filled. Keeping ماه‌سنگ as *a stone in the list* (خرداد) stays honest and keeps the
  speciality's real product paths (stone filter, product attribute) instead of promoting it in chrome.
- **Consequences:** `UX-012` and `SCR-001` are rewritten to the album (band, education copy and CTA
  removed); `SCR-002`/`SCR-003`/`SCR-021` keep the «ماه‌سنگ» value unchanged; the homepage no longer
  has a story slot for the speciality, so the stone filter and product copy carry it — `OQ-016` still
  decides a dedicated landing page or a wider taxonomy, and tiles become genuinely actionable in the
  storefront only if such a taxonomy arrives.

---

## DEC-053 — The stone of the month follows the Gregorian calendar
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-21 · **Supersedes:** `DEC-050` (calendar clause only) · **Amends:** `DEC-052` (month basis of the album)
- **Context:** `DEC-050` resolved the month from the **Jalali** calendar and then *derived* the stone
  by pairing each Jalali month with the birthstone of its dominant Gregorian month. That mapping
  shifted every stone by up to three weeks (۱–۲۰ فروردین wore الماس although those days are مارس),
  needed a rule to explain, and could disagree with the birthstone chart a visitor is holding. The
  owner asked for the stones to be shown on the **Gregorian** calendar — the calendar the birthstone
  convention itself is defined in.
- **Decision:**
  (a) both the accent and the homepage album are keyed by the **Gregorian month**:
  `data-month="1…12"` on `<html>` is ژانویه…دسامبر, resolved from the shop's date (`Asia/Tehran`),
  and `theme.monthSource` defaults to `gregorian` (`design_system.md` §7);
  (b) **stone values and accent tokens are unchanged** — ژانویه گارنت، فوریه آمیتیست، مارس آکوامارین،
  آوریل الماس، مه زمرد، ژوئن مروارید و ماه‌سنگ، ژوئیه یاقوت سرخ، اوت زبرجد، سپتامبر یاقوت کبود،
  اکتبر اوپال، نوامبر توپاز، دسامبر فیروزه — the twelve `accent`/`hover`/`subtle` sets of §2.1 are
  reused verbatim, so the contrast guarantee carries over (re-verified: white on accent ≥ 5.85:1);
  (c) the `:root` fallback becomes the ژانویه/گارنت set (month `1`); the chip, the album tiles and
  every stone label print the **Gregorian** month in Farsi + Latin («سپتامبر · September»), with a
  Jalali equivalent allowed only as secondary reference text;
  (d) the album of `DEC-052` keeps its shape — its twelve tiles are the Gregorian months.
- **Rationale:** one calendar, one answer: no derived mapping to explain or get wrong, and the month
  on the tile is the month a birthstone chart would give the visitor. Keeping the token values means
  zero new contrast work, and a Gregorian month changes on the 1st — easier to explain than a switch
  in the middle of a Jalali month.
- **Consequences:** the accent can now change **mid-Jalali-month** (الماس arrives ۱ آوریل, not
  ۱۲ فروردین), so the chip always names the Gregorian month to keep the change explained; the Jalali
  date display elsewhere on the storefront (`design_system.md` §6, `interaction_patterns.md`) is
  unaffected; `OQ-015` still asks whether a visitor's own birth month may override the calendar; any
  Iranian-friendly «≈ شهریور» hint is display sugar, never the source of the theme.

---

## DEC-054 — UX specification approved (`gates.ux_approved`)
- **Status:** accepted · **Decider:** human · **Date:** 2026-09-21
- **Context:** the frontend-ux role submitted the completed UX specification for review
  (`reports/ux-gate-review-2026-09-21.md`), including the spec-completeness audit against its own
  completion criteria. The owner reviewed the direction — the stone-of-the-month accent on the
  Gregorian calendar, the twelve-stone homepage album, and the birth-month prototype as an open
  question — in the review build `docs/ux/style_tile.html`.
- **Decision:** the UX specification in `docs/ux/**` is approved as the binding visual/behavioural
  contract for implementation; `state/project.yaml → gates.ux_approved: true`; the project moves to
  the architecture stage. `OQ-013` (font candidate), `OQ-014` (photography), `OQ-015` (birth month)
  and `OQ-016` (ماه‌سنگ scope) stay open and are explicitly **not** part of this approval.
- **Rationale:** the review found no blocking defect (five non-blocking findings, two of them fixed
  during the review); the specification is complete enough to design and size modules against, and
  deferring it would block the architecture phase on cosmetic questions.
- **Consequences:** module contracts must cite the `UX-###` IDs they implement; the first module
  that renders UI owes the per-screen visual evidence of `docs/ux/visual_validation.md` §2.1 (no
  screenshots exist yet — recorded as finding NB-3); any later UX change follows
  `docs/workflows/change_management.md` rather than editing an approved requirement in place.
- **References:** `reports/ux-gate-review-2026-09-21.md`, `docs/ux/README.md`, `DEC-034`

---

## ADR-001 — Modular monolith: TypeScript end-to-end on Next.js (App Router)
- **Status:** accepted · **Date:** 2026-09-21 · **Decider:** human (chose between the alternatives
  below and the Python/Django option presented in the architecture kick-off)
- **Context:** one small storefront + one admin surface, 50–200 products, 100–1,000 visitors/day with
  ×5 social spikes (`NFR-SCALE-1`), a non-technical owner who must run it alone (`NFR-MAINT-1`),
  domestic Iranian hosting with minimal cost (`DEC-027`, `DEC-030`), and a framework whose decisive
  quality attribute is **agent-parallelism**. The UX spec demands server-rendered RTL pages, no
  layout shift on load, a server-resolved monthly theme (`DEC-053`) and WCAG-AA-minded accessibility.
- **Options considered:**
  1. **Next.js (App Router) modular monolith, TypeScript** — one language and one deployable for
     storefront + admin; SSR/RSC gives first-paint correctness (needed for the theme and CLS rules)
     with no client data-fetch waterfall; route handlers/server actions cover the few dynamic
     islands.
  2. **Next.js frontend + separate Node API service** — cleaner runtime boundary, but two builds, two
     deployments, an extra network hop per render, and an internal API to version — cost with no
     benefit at this scale.
  3. **Python/Django with server-rendered templates + HTMX** — batteries-included admin and ORM,
     permissive licence; rejected as the second-best fit rather than as a good/bad call: it splits the
     codebase into two ecosystems for the token/theme work the UX spec requires in CSS, and gives the
     owner two skill surfaces to maintain.
- **Decision:** build one TypeScript monorepo-deployable on Next.js (App Router, React Server
  Components) with: feature modules under `src/<domain>/`, each exposing a single `public.ts` barrel;
  a pure domain layer with repository interfaces; Server Actions / route handlers for mutations;
  no client-side data fetching for first paint. Node 22 LTS (`.nvmrc`), npm with a committed
  `package-lock.json`.
- **Rationale:** every UX hard requirement (SSR HTML, `data-month` before paint, zero-CLS, form posts
  that work without JS) is the default behaviour of this shape rather than something to engineer.
  One deployable keeps operations inside `DEC-030`; the module/barrel discipline keeps the
  agent-parallelism property that a service split would have provided anyway.
- **Consequences:** the app is a single failure domain (mitigated by the worker being a separate
  process, ADR-008); a future extraction of any module into a service is possible because domain
  modules talk through interfaces, not through HTTP; server-component discipline must be enforced in
  review (a client component that fetches data on mount violates this ADR).
- **Reversibility:** moderate — the runtime boundary can be added later (extract one module behind an
  HTTP port); the language choice is effectively permanent for v1.
- **Affected modules:** every module; the boundary rules land in `conventions.md` §2.
- **Verification:** first wave modules build and pass contract tests without importing another
  module's internals (lint rule + review); Lighthouse budget on `SCR-001`/`SCR-004`.
- **References:** `NFR-SCALE-1`, `NFR-MAINT-1`, `DEC-027`, `DEC-030`, `UX-G-007`, architecture §1–§3

---

## ADR-002 — PostgreSQL 16 + Prisma for schema and ordered migrations
- **Status:** accepted · **Date:** 2026-09-21 · **Decider:** human (delegated to architecture)
- **Context:** the data is small but *relational and money-bearing*: products priced from a daily rate
  (`DEC-016`, `BR-4`), orders whose price basis must be reproducible forever (`DEC-020`), stock
  reservations with an expiry, promo usage counters, an audit trail for owner actions. Multiple
  modules (catalog, cart, checkout, orders, admin) read the same entities, so the schema is a shared
  zone and its migration order matters.
- **Options considered:**
  1. **PostgreSQL + Prisma Migrate** — real transactions and constraints (unique order codes, unique
     rate-per-date, forward-only status), typed client, SQL migration files that a reviewer can read.
  2. **SQLite file** — simplest operations, but single-writer limits, weaker concurrent checkout
     behaviour and a painful migration path later.
  3. **MongoDB/document store** — flexible, but the pricing/stock invariants above want transactions
     and foreign keys.
- **Decision:** PostgreSQL 16 in Docker Compose; Prisma as the only data-access layer; schema and
  migrations owned by one module (`prisma/schema.prisma`, `prisma/migrations/**` in shared zones).
  Business invariants that guard money (order code uniqueness, one rate per date, status transitions)
  are enforced in the database where possible and in the domain layer always.
- **Rationale:** money correctness is the one place where the simplest-to-reason-about store wins;
  Postgres also gives the owner a boring, well-documented backup/restore story (`pg_dump`).
- **Consequences:** every environment needs a Postgres instance (compose services `db` and `db-test`);
  migrations become a coordination point (one author per wave, expand→migrate→contract for anything
  destructive); Prisma's generated client is a build artefact, never committed.
- **Reversibility:** hard for the schema itself, moderate for the access layer (the repository
  interfaces are the seam if Prisma is swapped).
- **Affected modules:** `FOUNDATION` (owns schema/migrations), all domain modules (via repositories).
- **Verification:** integration tests run against a real Postgres container; a migration test applies
  the full chain to an empty database and asserts the expected tables.
- **References:** `FR-RATE-1`, `FR-ORD-1`, `DEC-016`, `DEC-019`, `DEC-020`, architecture §5

---

## ADR-003 — Deployment: one domestic VPS, Docker Compose, Caddy with automatic TLS
- **Status:** accepted · **Date:** 2026-09-21 · **Decider:** human (cost + hosting implication)
- **Context:** hosting must be domestic (`DEC-027`), cheap and owner-operable (`DEC-030`,
  `NFR-MAINT-1`), with HTTPS for checkout (`NFR-SEC-1`) and room for a nightly database backup. Traffic
  is a few hundred visitors a day with short spikes (`ASM-004`). No managed platform in the target
  market offers this stack, and cross-border container platforms are out of scope for a domestic,
  Iran-only shop.
- **Options considered:**
  1. **Single VPS (2 vCPU / 4 GB / domestic provider) with Docker Compose**: `edge` (Caddy) → `web`
     (Next.js) + `worker` + `db` (Postgres), images built in CI or on the box.
  2. **Two VPS (app + db separately)** — better isolation, double cost and double ops.
  3. **Managed/PaaS hosting** — unavailable or non-compliant for the requirement, and it hides the
     part the owner must be able to restore.
- **Decision:** option 1. One compose file, one image with two entrypoints (`web`, `worker`), Postgres
  data on a named volume, uploads on a separate volume, Caddy terminating TLS and serving uploaded
  files; secrets in a `.env` file readable only by root on the server (never in git); deploy =
  `docker compose pull && docker compose up -d`, rollback = previous image tag; nightly `pg_dump`
  retained 14 days plus a volume snapshot before each deploy. The exact plan and price are the owner's
  to approve (`OQ-017` records the registry/CI reachability question that goes with it).
- **Rationale:** the smallest topology that still separates the web process, the background worker and
  the database, with no vendor lock-in and a restore procedure the owner can run.
- **Consequences:** the VPS is a single point of failure (accepted at this scale; the backup is the
  mitigation, and its restore must be rehearsed once — see DoD level 4); TLS and DNS live at a domestic
  provider (`OQ-021`); CI credentials are scoped to the deploy job only.
- **Reversibility:** easy-to-moderate — the compose file moves to a bigger box or a second host without
  code changes; moving the database is the only real work.
- **Affected modules:** `OPS` (compose/Dockerfile/Caddyfile), `FOUNDATION` (CI workflows).
- **Verification:** a clean-host rehearsal: clone → `.env` → `docker compose up -d` → smoke check
  `/healthz` and one end-to-end order in sandbox payment mode; restore drill from the previous dump.
- **References:** `DEC-027`, `DEC-030`, `NFR-MAINT-1`, `NFR-SEC-1`, architecture §10

---

## ADR-004 — Payment boundary: internal `PaymentProvider` port with a sandbox adapter
- **Status:** accepted · **Date:** 2026-09-21 · **Decider:** human (security model + vendor decision)
- **Context:** `OQ-001`/`RISK-001` — the owner has not yet been approved for a domestic gateway, so the
  provider is unknown while checkout, order status and notifications must still be built. `FR-PAY-1`
  requires online payment; `NFR-SEC-1` forbids card data touching the store; `DEC-020` requires the
  price to be locked when payment succeeds.
- **Options considered:**
  1. **Port + adapters**: an internal interface (`createPayment`, `verifyPayment`, `refund` where the
     provider supports it) with a **sandbox adapter** now and one thin adapter per real gateway later.
  2. **Code directly against one named gateway** — faster, but blocks wave 1 on an unresolved vendor and
     hard-codes its quirks into checkout.
  3. **No online payment in v1** — contradicts an approved requirement.
- **Decision:** option 1. Checkout calls the port; the sandbox adapter simulates success/failure/cancel
  paths deterministically (it is what the automated tests use). A real adapter is added when the
   gateway is named, behind the same interface, with: server-side verification of the provider's
  response before an order becomes `paid`, idempotency key per attempt, no card fields in any form,
  and only non-sensitive provider references stored. Callback/IPN endpoints are the only public
  payment surface and are rate-limited and validated.
- **Rationale:** the unresolved vendor is a *launch* risk, not a *design* risk; the port keeps the
  payment module testable in isolation and makes the vendor decision reversible — the exact reason the
  sandbox adapter exists.
- **Consequences:** one extra interface and adapter to maintain; the sandbox adapter must never be
  reachable in production (config guard + a test); the gateway's reconciliation/refund semantics will
  need their own ADR when the vendor is known.
- **Reversibility:** easy for the boundary, hard-free for adapters — adding or replacing a provider is
  one file plus its contract test.
- **Affected modules:** `PAYMENT` (owner of the port), `CHECKOUT`, `ORDERS`, `OPS` (secrets/config).
- **Verification:** provider-conformance test suite runs against the sandbox adapter (success, failure,
  cancel, duplicate callback, tampered callback); a payment can never mark an order paid without
  server-side verification.
- **References:** `FR-PAY-1`, `OQ-001`, `RISK-001`, `DEC-020`, `NFR-SEC-1`, architecture §6.2 and §9

---

## ADR-005 — Auth: guest-first cookies, optional phone+password accounts, separate admin session
- **Status:** accepted · **Date:** 2026-09-21 · **Decider:** human (security model)
- **Context:** v1 is guest checkout with optional accounts (`DEC-005`); the buyer identifies an order by
  code + phone (`DEC-021`, `FR-ORD-3`); personal data is minimal (`NFR-PRIV-1`); the owner needs a
  protected admin area (`FR-ADM-1`). Passwords vs OTP was left open in the UX spec as an architecture
  decision (`SCR-012` note).
- **Options considered:**
  1. **Password accounts, guest-first**: no account needed to buy; optional phone + password account
     (argon2id); admin uses a separate credential and session namespace; sessions are signed httpOnly
     cookies in the database, revocable.
  2. **OTP/SMS login only** — no passwords to manage, but every login costs an SMS (`DEC-030`) and
     depends on an SMS provider that is not chosen (`OQ-019`).
  3. **Magic-link email login** — cheap, but email reliability in the target market is the weakest link
     (`OQ-018`) and it adds a round trip to a flow that must stay unblocked.
- **Decision:** option 1. Guests receive a signed httpOnly session cookie holding a cart/session id;
  accounts add phone (unique, validated) + argon2id password; the admin is a separate principal with
  its own session cookie, its own login screen and optional TOTP (recommended on at launch). All
  authorization is enforced server-side in the owning module — the UI is never the boundary.
  Password reset via email if an address exists, else owner-assisted (documented, rare).
- **Rationale:** keeps checkout unblocked by third parties, keeps cost at zero, and keeps the owner's
  surface small enough to secure properly (`NFR-MAINT-1`).
- **Consequences:** a small password-reset path exists to maintain; SMS/OTP can be added later behind
  the same session model; rate limiting and lockout on both login screens is mandatory.
- **Reversibility:** moderate — the session layer is provider-agnostic, so adding OTP later changes the
  login step, not the model.
- **Affected modules:** `IDENTITY` (owner), `CART`, `ORDERS`, `ADMIN`, `OPS`.
- **Verification:** integration tests for session fixation/renewal, revoked sessions, lockout, and for
  "a guest can complete checkout without creating an account" (`UX-AC-002.1`).
- **References:** `DEC-005`, `DEC-009`, `DEC-017`, `DEC-021`, `NFR-PRIV-1`, `SCR-012`, architecture §7

---

## ADR-006 — Cart and checkout state live server-side
- **Status:** accepted · **Date:** 2026-09-21 · **Decider:** human (delegated to architecture)
- **Context:** `UF-02-AC4` requires that abandoning checkout loses nothing the user entered, the cart
  drawer appears on every screen (`DEC-041`), prices must be recomputed against the current rate on
  every visit (`BR-4`), stock is reserved during checkout, and the storefront must work without
  JavaScript for the buying path.
- **Options considered:**
  1. **Server-side cart** (DB row keyed by the signed session cookie) with server-rendered drawer and
     form posts — survives reloads, browser restarts and no-JS; one source of truth for pricing.
  2. **localStorage cart** — no server state, but a client-first waterfall, pricing computed in the
     browser (the rate would have to be shipped to the client), and a broken no-JS path.
  3. **Cookie-only cart payload** — no DB row, but a tamper/price surface and a size limit for the
     drawer contents.
- **Decision:** option 1 — a cart row per session with line items referencing products; prices are
  always recomputed server-side from the current rate; the reservation row is created when checkout
  starts and released by the worker when it expires; the anonymous cart is merged into the account cart
  on login.
- **Rationale:** pricing authority stays on the server (the only way `BR-4`/`DEC-020` are provable), and
  the cart becomes testable without a browser.
- **Consequences:** every cart interaction is a server round trip (acceptable at this scale, and the
  drawer is server-rendered); a session-scoped cleanup job is required; anonymous carts are abandoned
  data that must be purged on a schedule.
- **Reversibility:** moderate — the drawer UI could later hold a client-side optimistic copy, but the
  server stays the authority.
- **Affected modules:** `CART`, `CHECKOUT`, `CATALOG` (pricing), `OPS` (cleanup job).
- **Verification:** integration tests for price change between visits, reservation expiry, cart merge on
  login, and a no-JS e2e run of `UF-02`.
- **References:** `UF-02`, `UF-02-AC4`, `DEC-041`, `BR-4`, `UX-005`, architecture §6.3

---

## ADR-007 — Monthly theme resolved server-side into `data-month` + CSS custom properties
- **Status:** accepted · **Date:** 2026-09-21 · **Decider:** human (delegated to architecture)
- **Context:** `DEC-050`/`DEC-053` theme the storefront with the current **Gregorian** month's stone;
  `UX-AC-012.2` forbids layout shift at rollover, `UX-G-007` forbids shift on load, and the birth-month
  prototype (`OQ-015`, `design_system.md` §2.1 rule 10) is explicitly **not** approved yet.
- **Options considered:**
  1. **Server-resolved month** rendered as `data-month` on `<html>` with the twelve token sets in CSS;
     correct on first paint, cacheable, works without JS, and rollover stays colour-only.
  2. **Client-resolved month** (pre-paint inline script always) — one cached HTML for all months, but it
     makes the theme JS-dependent for no gain once the month is known server-side.
  3. **Build-time month** — bakes the theme into the artefact; a deploy per month, rejected outright.
- **Decision:** year-round: the month is computed on the server (Asia/Tehran) and rendered as
  `data-month="1…12"`; `src/styles/tokens.css` owns the twelve sets; the fallback in `:root` is the
  ژانویه set, so a page without the attribute is still correct. `theme.monthPreview` (query parameter,
  admin/owner only) pins a month for previews and screenshot tests. The visitor birth-month override is
  **not implemented**: when `OQ-015` is answered it arrives as the pre-paint script of
  `design_system.md` §2.1 rule 10, layered over this resolution, with the album marker still following
  the calendar.
- **Rationale:** the server already knows the month, and the CSS-only delivery is what makes the CLS and
  no-JS guarantees cheap.
- **Consequences:** HTML is month-dependent — caches must key on the month (or revalidate at the day
  boundary); the token file is a shared zone with a single writer; the theme-integrity check
  (contrast for all twelve sets, month resolution, no drift from the stone reference) becomes a test.
- **Reversibility:** easy — adding the client override later touches one script and the chip copy.
- **Affected modules:** `SHELL` (layout + tokens), all screens; `TESTS` for the integrity check.
- **Verification:** a unit test over the twelve sets (contrast ≥ 4.5:1 with white, minimum recorded), a
  snapshot asserting `data-month` matches the pinned month, and a CLS check in the e2e suite.
- **References:** `DEC-050`, `DEC-053`, `UX-AC-012.*`, `design_system.md` §2.1, `OQ-015`, architecture §6.3

---

## ADR-008 — Notifications through a database-backed outbox consumed by the worker
- **Status:** accepted · **Date:** 2026-09-21 · **Decider:** human (delegated to architecture)
- **Context:** `DEC-021` requires order events to reach the buyer by email where an address exists and
  always on-site; `NFR-OBS-1` requires failures to be visible rather than silent; `UF-04-AC4` requires an
  email failure not to block the owner's status change; SMS is not chosen and costs money (`DEC-030`).
- **Options considered:**
  1. **Outbox table + worker** — every notification is a row written in the same transaction as the
     triggering change, then attempted with retries and per-attempt logging; failures surface in admin.
  2. **Send inline during the request** — simplest, but a slow or failing SMTP server delays checkout and
     status changes, and failures are invisible after the response.
  3. **External queue/broker** — overkill for this scale and one more thing to operate.
- **Decision:** option 1, with the worker running as a separate compose process (`ADR-003`) sharing the
  image: it drains the outbox, runs reservation expiry, purges abandoned anonymous carts, generates
  image derivatives and writes the daily backup marker. Email uses plain SMTP (provider chosen at launch,
  `OQ-018`); SMS is deferred behind the same enqueue interface (`OQ-019`).
- **Rationale:** dual-write safety (order change + notification intent commit together), decoupled from
  buyer latency, and a failure surface the owner can actually see.
- **Consequences:** the worker is a second process to monitor; retry/backoff policy and a dead-letter view
  in admin are required; duplicate-email suppression keyed by (order, event) is required.
- **Reversibility:** easy — the outbox is an internal table; the transport behind it can change freely.
- **Affected modules:** `NOTIFY` (owner), `ORDERS`, `ADMIN`, `OPS`.
- **Verification:** integration test asserts a status change commits the outbox row in the same
  transaction; worker test asserts retry with backoff and a visible failed state; a failed send never
  changes order status (`UF-04-AC4`).
- **References:** `DEC-021`, `FR-ORD-1`, `UF-04-AC4`, `NFR-OBS-1`, architecture §3 and §8

---

## ADR-009 — Observability: structured logs plus an admin failure surface; no paid APM in v1
- **Status:** accepted · **Date:** 2026-09-21 · **Decider:** human (delegated to architecture)
- **Context:** `NFR-OBS-1` says the owner must see failures — orders, payments, email — without a
  developer; `DEC-030` keeps recurring costs minimal; the audience that reads logs is one owner plus
  agents.
- **Options considered:**
  1. **JSON logs to stdout (rotated) + `/healthz` + an admin "failures" panel** fed by outbox failures,
     payment verification failures and worker errors; optional domestic uptime monitor on `/healthz`.
  2. **Hosted APM/Sentry** — best-in-class error tracking, recurring cost, and cross-border data flow
     that fits neither the budget nor the privacy posture.
  3. **Database-backed event log only** — queryable, but loses process-level context and makes production
     debugging blind.
- **Decision:** option 1. Correlation id per request (`x-request-id`), structured logs with no personal
  data (`NFR-PRIV-1`), log rotation with 30-day retention on the box, health endpoints, and an admin
  panel listing unresolved failures with a retry action. Failure counts also feed the daily owner summary
  line in admin.
- **Rationale:** the failure modes that matter here (payment not verified, email not sent, job stuck) are
  *business* failures and are best surfaced where the owner already is — the admin — with logs as the
  fallback for a developer.
- **Consequences:** no automatic exception grouping (accepted); the admin panel becomes a required
  module surface; logs must be scrubbed of PII by construction, which is a review item.
- **Reversibility:** easy — adding Sentry later is an adapter plus config.
- **Affected modules:** `SHELL`/`OPS` (logging setup), `ADMIN` (panel), `PAYMENT`, `NOTIFY`, `WORKER`.
- **Verification:** failure drill — force a payment verification failure and a failed email, then confirm
  both appear in admin with a retry action and in logs with a correlation id.
- **References:** `NFR-OBS-1`, `NFR-PRIV-1`, `DEC-030`, `FR-ADM-2`, architecture §8

---

## ADR-010 — Testing architecture: Vitest, a real Postgres container, Playwright for UI evidence
- **Status:** accepted · **Date:** 2026-09-21 · **Decider:** human (delegated to architecture)
- **Context:** framework rule — independent module development requires that each module is testable
  without the whole system; the UX spec additionally requires rendered UI evidence (`visual_validation.md`
  §2.1: three widths, states, keyboard walkthrough, a11y scan) and the payment boundary must be provable
  against a fake provider (`ADR-004`).
- **Options considered:**
  1. **Vitest (unit + integration) + real Postgres in a container + Playwright (e2e, screenshots, axe)** —
     one runner for TS, the same database engine as production, and browser evidence in the same toolchain.
  2. **Jest + Testing Library + Cypress** — heavier, slower, less ergonomic with the App Router, no
     material advantage here.
  3. **Unit tests only, manual UI checks** — fails the framework's isolation requirement and the UX
     evidence rule.
- **Decision:** option 1. Layers: pure unit tests for domain logic and adapters (no DB, fakes allowed);
  integration tests against a disposable Postgres (`db-test` service, migrations applied, tables truncated
  per test); contract tests per provided interface plus a payment-provider conformance suite; Playwright
  e2e for `UF-01`…`UF-04` including payment failure, the no-JS buying path, RTL keyboard walkthrough and
  screenshots at 320/768/1280 for the screens a PR touches. CI runs install → typecheck → lint → format
  → unit/integration → e2e → dependency audit (`scripts/verify.config.yaml`).
- **Rationale:** the seams that make the architecture parallel-friendly (repository interfaces, the
  payment port, pure pricing) are exactly the seams these layers test; browser evidence lives where the
  UX review already looks.
- **Consequences:** every module must expose its domain logic without a browser and without another
  module's internals; e2e needs a seeded fixture set (no production data — `NFR-PRIV-1`); screenshots are
  attached to PRs, never committed.
- **Reversibility:** easy — layers are independent; Playwright or Vitest could be swapped without
  touching production code.
- **Affected modules:** `TESTS`/`FOUNDATION` (harness, fixtures), every module (its own tests).
- **Verification:** the first wave proves it — a module PR whose evidence is one unit test per acceptance
  criterion, one contract test per interface, and Playwright screenshots for its screen.
- **References:** `docs/workflows/testing_workflow.md`, `docs/ux/visual_validation.md`, `NFR-A11Y-1`,
  architecture §11, `scripts/verify.config.yaml`

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
