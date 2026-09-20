# Requirements — NoghreShop

> **Status:** **approved** · **Approved by:** owner (human) · **Approved:** 2026-09-20 · **Last updated:** 2026-09-20
>
> **How to use this file.** The Discovery Agent owns it. It is written *after* the discovery
> interview, never before: the agent interviews the human, then records what was actually
> agreed. It is the **source of truth for what the product must do**.
>
> Rules
> * Tag every statement: `[DECISION]`, `[REC]`, `[ASSUMPTION] ASM-###`, `[OPEN] OQ-###`, `[RISK] RISK-###`.
> * Number requirements: `FR-###` (functional), `NFR-###` (non-functional), `UX-###` (UX, owned
>   by `docs/ux/`). Never renumber; retire with `status: retired` in `requirements.yaml`.
> * Every heading for a requirement must contain its ID so `scripts/tp.py context` can extract
>   exactly the requirements a module needs (e.g. `### FR-AUTH-1 — Password reset`).
> * Anything not agreed here is **not** a requirement. Agents may not invent requirements.
> * The human approval gate is `state/project.yaml → gates.requirements_approved`.
>
> Approval checklist (human): scope is honest · out-of-scope is explicit · success criteria are
> measurable · no requirement contradicts another · every `[OPEN]` item is either resolved or
> knowingly accepted as a risk.

---

## 1. Product

### 1.1 Problem statement
`[DECISION]` NoghreShop is the owner's own silver jewelry business, which today has **no online sales channel at all** (round 1: "not selling yet"). Customers who might buy silver jewelry from this business have no way to discover the catalog, order, or pay online. The business loses sales it could make and depends entirely on offline contact.

### 1.2 Vision (one paragraph)
`[DECISION]` NoghreShop v1 is a Farsi-language (RTL) online store where domestic retail customers browse the silver jewelry catalog, add items to a cart, pay online, and have orders delivered — and where the owner can manage products and orders without technical help. It is the business's **first** sales channel, not a replacement for an existing one.

### 1.3 Target users
<!-- Personas at product level. Persona *UX* detail lives in docs/ux/ux_requirements.md. -->
| Persona | Who they are | Primary goal | Notes |
|---|---|---|---|
| Domestic retail buyer | Persian-speaking consumer in the domestic market | find and buy silver jewelry online with confidence | the only customer type in v1 `[DECISION]` |
| Owner (store admin) | the business owner, non-technical | manage the catalog, see and fulfil orders | number of admin users TBD `[OPEN]` |

### 1.4 Core use cases
| ID | Use case | Actor | Trigger | Outcome |
|---|---|---|---|---|
| UC-1 | Browse the silver jewelry catalog | domestic retail buyer | wants to see what is available | views products with photos, prices and availability (detail level: rounds 3–4) |
| UC-2 | Buy a product end-to-end | domestic retail buyer | wants to purchase | adds to cart, pays online, receives order confirmation; on payment failure retries from checkout (`OQ-001` gateway TBD) |
| UC-3 | Manage catalog and orders | owner | stock changes / a new order arrives | products added or updated; orders seen and progressed (workflow detail: rounds 3–4) |

### 1.5 Success criteria
<!-- Measurable. If you cannot measure it, it is a hope, not a criterion. -->
| ID | Criterion | Measurement | Target |
|---|---|---|---|
| SC-1 | First orders complete **end-to-end without owner rescue** (browse → online payment → delivery) | order records: paid orders fulfilled with no manual payment step | ≥ 1 order in the first month; expected steady state of a few orders/day by day 90 `[DECISION]` DEC-025 |
| SC-2 | Launch catalog **fully listed** | catalog audit: every launch product has photo(s), weight, craft fee, category | 100% of the 50–200 launch items within 90 days of launch `[DECISION]` DEC-025 |

### 1.6 Scope (in)
- `[DECISION]` Farsi-only storefront, right-to-left layout
- `[DECISION]` Catalog of silver jewelry products with photos, prices and availability
- `[DECISION]` Shopping cart and checkout ending in **online payment** (gateway: `OQ-001`)
- `[DECISION]` Order placement with confirmation for the customer
- `[DECISION]` Owner-side administration of products and orders
- `[DECISION]` Guest checkout: anyone can buy without registering; **accounts are optional**
  and add order history / faster repeat buying
- `[DECISION]` Product discovery: category browsing **plus free-text search plus filters**
  (price range, weight, stone/no-stone)
- `[DECISION]` Catalog size at launch: 50–200 items (medium — pagination and good admin
  ergonomics required; no bulk-import tooling in v1)
- `[DECISION]` Checkout data: name, phone number, delivery address — nothing more required
- `[DECISION]` Order lifecycle visible to the customer: **Paid → Shipped → Delivered**
- `[DECISION]` Admin capabilities: product CRUD with photos, stock/availability control,
  order view + status advancement, basic sales overview (counts/totals)
- `[DECISION]` Notifications: email confirmations + on-site order status; **no SMS in v1**
  (optional email field at checkout — DEC-017)
- `[DECISION]` Delivery is for **online-paid orders only**; no cash-on-delivery (DEC-015)
- `[DECISION]` Pricing model: product price = **weight × daily silver rate + craft fee**
  (DEC-016); rate entered manually in admin, automation-ready (DEC-019); price locked at
  payment (DEC-020)
- `[DECISION]` **Promo/discount codes at checkout** (DEC-018; capabilities: `OQ-010`)
- `[DECISION]` Guest order status: on-site lookup by **order code + phone** plus an email
  link when an email was provided (DEC-021)
- `[DECISION]` Products carry a **multi-photo gallery** (DEC-022)
- `[DECISION]` Starter category taxonomy: rings, necklaces, earrings, bracelets, sets,
  other — owner-editable in admin (DEC-023)
- `[DECISION]` Promo code = **percentage off** the order total, with owner-set expiry date
  and maximum usage count (DEC-024)
- `[DECISION]` Policy pages: shipping, returns/refund, contact — owner-provided wording,
  editable in admin (DEC-026)

### 1.7 Out of scope (explicitly not built)
- `[DECISION]` International sales / cross-border shipping — v1 serves the domestic market only
- `[DECISION]` English or bilingual UI — Farsi only in v1
- `[DECISION]` Multi-vendor marketplace — single owner's business only
- `[DECISION]` Wishlist / favorites — explicitly excluded from v1
- `[DECISION]` Product reviews & ratings — out of v1 (DEC-018)
- `[DECISION]` Blog / content pages — out of v1 (DEC-018)

### 1.8 Business rules
| ID | Rule | Applies to | Notes |
|---|---|---|---|
| BR-1 | Stock is reserved the moment a customer's checkout starts; others see "out of stock" | checkout, catalog | `[DECISION]` no overselling (round 3) |
| BR-2 | An order moves only forward: Paid → Shipped → Delivered | orders | `[DECISION]` (round 3) |
| BR-3 | The buyer receives an email confirmation at order placement and on every status change, **when an email was provided** (optional at checkout) | orders, notifications | `[DECISION]` DEC-012 + DEC-017 |
| BR-4 | A product's price = weight × daily silver rate + craft fee; the rate is a first-class, auditable input | catalog, pricing, checkout | `[DECISION]` DEC-016; manual admin entry (DEC-019); locked at payment (DEC-020) |

### 1.9 Constraints and assumptions
**Constraints** (fixed boundaries):
- `[DECISION]` Storefront language: Farsi only, RTL layout
- `[DECISION]` Market: domestic retail buyers only (v1)
- `[DECISION]` Online payment only — every order is paid before fulfilment (DEC-015)
- `[DECISION]` Hosting preference: domestic (DEC-027); running costs minimal (DEC-030)
- `[DECISION]` No existing product data — the catalog is built from scratch in admin (DEC-029)
- `[DECISION]` No fixed launch deadline (DEC-032)
- Single owner-operator runs the store; admin tooling must be usable by a non-technical person

- `[DECISION]` No postponement/cancellation triggers: the store is built regardless of
  budget or timeline overrun (round 2)

**Assumptions** (mirrored into `assumptions.md`): ASM-001, ASM-002, ASM-003 (confirmed),
ASM-004.

---

## 2. Functional requirements

> Detail per requirement: behaviour, inputs, outputs, state transitions, permissions, error
> behaviour, edge cases. Behaviour belongs here; visual/flow detail belongs in `docs/ux/`.

> Every FR below derives from a recorded human decision (referenced per block). Priorities:
> `must` = v1 cannot ship without it; `should` = agreed for v1, deferrable by change request.

### FR-CAT-1 — Category browsing `[DECISION]`
- **Status:** approved · **Priority:** must (DEC-023)
- **Actor:** domestic retail buyer; owner (admin)
- **Description:** The storefront groups products by category. v1 launches with the starter
  taxonomy: rings, necklaces, earrings, bracelets, sets, other. The owner can rename,
  regroup, add, and retire categories in admin.
- **Acceptance criteria:**
  - [ ] AC-FR-CAT-1.1 — a visitor can open any starter category and see only its products
  - [ ] AC-FR-CAT-1.2 — the owner can add a new category and assign a product to it; the
        change is visible on the storefront without a deploy
- **Permissions / roles:** browse = public; manage = owner only
- **State transitions:** category: active ↔ retired (retired hides it, products keep data)
- **Edge cases:** empty category renders an empty-state view; product in retired category
  still reachable via direct link/search
- **Error behaviour:** unknown category ID → 404-equivalent Farsi page
- **Related UX:** navigation IA, category page (Frontend/UX Agent)

### FR-CAT-2 — Search and filters `[DECISION]`
- **Status:** approved · **Priority:** must (DEC-006)
- **Actor:** domestic retail buyer
- **Description:** Free-text search over product names/descriptions; filters for price range
  (computed price, BR-4), weight, and stone/no-stone; combinable with category browsing.
- **Acceptance criteria:**
  - [ ] AC-FR-CAT-2.1 — searching a word from a product's Farsi name returns that product
  - [ ] AC-FR-CAT-2.2 — applying price range + weight + stone filters returns only matching
        products; the result set updates without a full page reload
  - [ ] AC-FR-CAT-2.3 — filters combine with category selection (AND semantics)
- **Permissions / roles:** public
- **State transitions:** —
- **Edge cases:** no results → helpful Farsi empty state; price filter bounds operate on the
  current daily computed price (rate changes can move a product in/out of a range)
- **Error behaviour:** empty search query → all products (paginated)
- **Related UX:** search bar, filter panel (RTL) (Frontend/UX Agent)

### FR-PROD-1 — Product page with multi-photo gallery `[DECISION]`
- **Status:** approved · **Priority:** must (DEC-022)
- **Actor:** domestic retail buyer
- **Description:** Each product shows: photo gallery (several images, swipeable), name,
  description, category, weight, stone presence, availability, and the current computed
  price (weight × daily rate + craft fee, BR-4) with the rate's date.
- **Acceptance criteria:**
  - [ ] AC-FR-PROD-1.1 — the gallery shows all uploaded photos with swipe/arrow navigation
  - [ ] AC-FR-PROD-1.2 — the displayed price equals weight × current daily rate + craft fee
        and shows the rate's date
  - [ ] AC-FR-PROD-1.3 — an out-of-stock product is viewable but cannot be added to the cart
- **Permissions / roles:** public
- **State transitions:** product availability: in stock / out of stock (owner-controlled)
- **Edge cases:** rate not entered for today (RISK-002) → last-known rate shown with its
  date and an owner-facing staleness warning
- **Error behaviour:** unknown product → Farsi 404-equivalent
- **Related UX:** product page layout, gallery (RTL) (Frontend/UX Agent)

### FR-RATE-1 — Daily silver rate and price computation `[DECISION]`
- **Status:** approved · **Priority:** must (DEC-016, DEC-019)
- **Actor:** owner
- **Description:** The owner enters the day's silver rate in admin (manual entry in v1,
  automation-ready per DEC-019). Every product price is computed as weight × rate + craft
  fee (BR-4). Rate history is retained and auditable. Admin shows a staleness warning when
  no rate exists for the current trading day.
- **Acceptance criteria:**
  - [ ] AC-FR-RATE-1.1 — after the owner enters today's rate, all storefront prices reflect
        it; the price shows the rate's date
  - [ ] AC-FR-RATE-1.2 — rate history is retained; past order totals are NOT recomputed
        retroactively
  - [ ] AC-FR-RATE-1.3 — with no rate for today, admin shows a staleness warning and the
        storefront falls back to the last-known rate with its date
- **Permissions / roles:** manage = owner only
- **State transitions:** rate entry per date: none → entered (editable same day)
- **Edge cases:** multiple entries same day → latest wins and is audited; negative/zero rate
  rejected
- **Error behaviour:** invalid input → Farsi validation message, previous value kept
- **Related UX:** admin rate screen (Frontend/UX Agent)

### FR-CART-1 — Shopping cart `[DECISION]`
- **Status:** approved · **Priority:** must (DEC-003)
- **Actor:** domestic retail buyer
- **Description:** Visitors add available products to a cart, change quantities, remove
  items, and see the running total (computed prices, BR-4). The cart works for guests and
  account holders and persists across visits (at least per browser).
- **Acceptance criteria:**
  - [ ] AC-FR-CART-1.1 — an anonymous visitor can add, update, and remove items; the total
        updates correctly
  - [ ] AC-FR-CART-1.2 — the cart persists across a page reload and repeat visits in the
        same browser
  - [ ] AC-FR-CART-1.3 — an item that went out of stock while in the cart is flagged at
        cart view and cannot proceed to checkout
- **Permissions / roles:** public
- **State transitions:** item: added → in checkout → ordered / removed
- **Edge cases:** adding an out-of-stock item is blocked with a Farsi message; rate change
  while in cart → total reflects the current rate (locked only at payment, DEC-020)
- **Error behaviour:** stale cart item (deleted product) → item removed with notice
- **Related UX:** cart page/drawer (RTL) (Frontend/UX Agent)

### FR-CHK-1 — Checkout with stock reservation `[DECISION]`
- **Status:** approved · **Priority:** must (DEC-009, DEC-013, DEC-017, DEC-014)
- **Actor:** domestic retail buyer (guest or logged-in)
- **Description:** Checkout collects name, phone, delivery address, and an **optional**
  email. Starting checkout **reserves stock** for all cart items (BR-1): other buyers then
  see out-of-stock. The reservation expires if the checkout is abandoned (timeout defined
  at decomposition). Payment failure returns the buyer to checkout with cart and details
  intact for immediate retry (DEC-014).
- **Acceptance criteria:**
  - [ ] AC-FR-CHK-1.1 — a guest completes checkout with only name, phone, address; email is
        optional and clearly marked
  - [ ] AC-FR-CHK-1.2 — when checkout starts, the reserved item shows out-of-stock to other
        visitors
  - [ ] AC-FR-CHK-1.3 — after an abandoned checkout (reservation expiry), stock is released
        and the item is buyable again
  - [ ] AC-FR-CHK-1.4 — after a failed payment, the buyer returns to checkout with the cart
        and entered details intact and can retry immediately
- **Permissions / roles:** public (guest or account)
- **State transitions:** checkout: active → paid / expired / failed-payment(retryable)
- **Edge cases:** required fields missing → Farsi inline validation; phone format validated
  for the domestic market
- **Error behaviour:** reservation expired mid-checkout → buyer is told stock was released
  and can re-checkout if available
- **Related UX:** checkout form (RTL), error and expiry messaging (Frontend/UX Agent)

### FR-PAY-1 — Online payment via domestic gateway `[DECISION]`
- **Status:** approved · **Priority:** must (DEC-003, DEC-015, DEC-020) — **blocked by
  `OQ-001`**
- **Actor:** domestic retail buyer; gateway (external)
- **Description:** Checkout ends at the domestic payment gateway (provider TBD, `OQ-001`).
  No card data touches the store (NFR-SEC-1). The order's authoritative total is the price
  at the moment payment completes (DEC-020); the final total is re-displayed at the payment
  step. On success the order is Paid.
- **Acceptance criteria:**
  - [ ] AC-FR-PAY-1.1 — a successful gateway payment transitions the order to Paid and the
        buyer sees the confirmation
  - [ ] AC-FR-PAY-1.2 — the final total (rate at payment, minus promo if applied) is shown
        before the buyer is sent to the gateway
  - [ ] AC-FR-PAY-1.3 — no card numbers or card secrets are stored in the store's database
        or logs
- **Permissions / roles:** public; gateway credentials owner-only
- **State transitions:** order: checkout → Paid (via gateway callback)
- **Edge cases:** gateway callback arrives twice → idempotent (one Paid order); callback
  never arrives → order stays unpaid and reservation expires (reconcile manually)
- **Error behaviour:** gateway unreachable → Farsi error, retry per FR-CHK-1; payment
  cancelled by user → back to checkout, cart intact
- **Related UX:** payment step, gateway redirect flow (Frontend/UX Agent)
- **Note:** the Architecture Agent must isolate the provider behind one integration boundary
  (RISK-001).

### FR-ORD-1 — Order lifecycle and tracking `[DECISION]`
- **Status:** approved · **Priority:** must (DEC-010, DEC-021)
- **Actor:** buyer; owner
- **Description:** Orders move forward-only: Paid → Shipped → Delivered (BR-2). Every order
  gets a code. Status is visible on-site (order code + phone lookup — works for guests
  without email) and via the confirmation-email link when an email exists.
- **Acceptance criteria:**
  - [ ] AC-FR-ORD-1.1 — the buyer sees the current status of their order on-site using the
        order code + the phone number used at checkout
  - [ ] AC-FR-ORD-1.2 — the owner can advance an order Paid → Shipped → Delivered; backward
        moves are impossible
  - [ ] AC-FR-ORD-1.3 — lookup with a wrong phone for a valid code fails; codes are not
        guessable-enumerable
- **Permissions / roles:** buyer = own order (via code+phone or account); owner = all orders
- **State transitions:** Paid → Shipped → Delivered (forward-only)
- **Edge cases:** refund/cancellation is manual and outside v1 scope (DEC-010) but the paid
  amount stays authoritative (DEC-020)
- **Error behaviour:** unknown code or wrong phone → Farsi not-found message (no data leak)
- **Related UX:** order status page, confirmation content (Frontend/UX Agent)

### FR-NOT-1 — Email confirmations `[DECISION]`
- **Status:** approved · **Priority:** must (DEC-012, DEC-017)
- **Actor:** system; email service (external)
- **Description:** When the buyer provided an email, the system sends a Farsi confirmation
  at order placement and on every status change (Shipped, Delivered). Email is never
  load-bearing: failures are logged and retried without blocking the order.
- **Acceptance criteria:**
  - [ ] AC-FR-NOT-1.1 — an order placed with an email triggers a Farsi confirmation email
        containing the order code and total
  - [ ] AC-FR-NOT-1.2 — each status change triggers the corresponding Farsi email
  - [ ] AC-FR-NOT-1.3 — an order placed without an email produces no email attempt and no
        error
  - [ ] AC-FR-NOT-1.4 — email service downtime does not block checkout or status changes;
        failures are visible in admin/logs (NFR-OBS-1)
- **Permissions / roles:** system-only
- **State transitions:** notification: queued → sent / failed(retried)
- **Edge cases:** bounce → logged, no retry loop
- **Error behaviour:** provider error → retry with backoff, then surfaced in admin
- **Related UX:** email templates (Farsi, RTL) (Frontend/UX Agent)

### FR-ADM-1 — Catalog admin `[DECISION]`
- **Status:** approved · **Priority:** must (DEC-011, DEC-022, DEC-023, DEC-029)
- **Actor:** owner
- **Description:** The owner manages products: create/edit/retire, upload multi-photo
  galleries, set weight, craft fee, stone presence, description, category, and toggle
  stock/availability. All without technical help (NFR-MAINT-1). Built for 50–200 items
  (pagination, search in admin).
- **Acceptance criteria:**
  - [ ] AC-FR-ADM-1.1 — the owner creates a product with ≥ 3 photos, weight, craft fee, and
        category; it appears on the storefront immediately
  - [ ] AC-FR-ADM-1.2 — the owner toggles availability; the product shows out-of-stock
        storefront-wide
  - [ ] AC-FR-ADM-1.3 — the owner finds any product in a 200-item catalog within seconds
        via admin search/pagination
- **Permissions / roles:** owner only
- **State transitions:** product: draft → active ↔ retired
- **Edge cases:** photo upload failure → clear error, partial state not saved silently;
  product in a cart when retired → cart flags it (FR-CART-1.3)
- **Error behaviour:** invalid weight/fee → Farsi validation, nothing lost
- **Related UX:** admin catalog screens (RTL) (Frontend/UX Agent)

### FR-ADM-2 — Order admin and sales overview `[DECISION]`
- **Status:** approved · **Priority:** must (DEC-011)
- **Actor:** owner
- **Description:** The owner sees incoming orders with buyer contact info and ordered items,
  advances their status (FR-ORD-1), and sees a basic sales overview (order counts, revenue
  totals) — list-level, no reporting engine.
- **Acceptance criteria:**
  - [ ] AC-FR-ADM-2.1 — new Paid orders are visible in admin with full buyer contact and
        items
  - [ ] AC-FR-ADM-2.2 — the overview shows order count and revenue for a chosen period
        matching the order records
- **Permissions / roles:** owner only
- **State transitions:** mirrors FR-ORD-1
- **Edge cases:** concurrent status updates by the single owner — last write wins (single
  operator, DEC-002)
- **Error behaviour:** —
- **Related UX:** admin orders + overview screens (RTL) (Frontend/UX Agent)

### FR-PROMO-1 — Promo codes `[DECISION]`
- **Status:** approved · **Priority:** must (DEC-018, DEC-024)
- **Actor:** buyer; owner
- **Description:** The owner creates promo codes: percentage off the order total, expiry
  date, maximum usage count. The buyer can apply a valid code at checkout; the discount
  applies on top of the computed total and is part of the payment-locked amount.
- **Acceptance criteria:**
  - [ ] AC-FR-PROMO-1.1 — a valid, unexpired, under-limit code reduces the checkout total by
        its percentage
  - [ ] AC-FR-PROMO-1.2 — an expired or exhausted code is rejected with a clear Farsi
        message and the total is unchanged
  - [ ] AC-FR-PROMO-1.3 — the owner creates a code with percent, expiry, and max uses; usage
        count increments exactly once per paid order
- **Permissions / roles:** manage = owner; apply = any buyer
- **State transitions:** code: active → expired/exhausted (automatic)
- **Edge cases:** code applied then payment fails → usage count only counts **paid** orders
  (AC-FR-PROMO-1.3); rate change between apply and pay recalculates the discounted total
- **Error behaviour:** unknown code → Farsi not-found message
- **Related UX:** checkout promo field, admin promo screens (RTL) (Frontend/UX Agent)

### FR-ACC-1 — Optional customer accounts `[DECISION]`
- **Status:** approved · **Priority:** should (DEC-005)
- **Actor:** domestic retail buyer
- **Description:** Buyers may register (phone-based, with the domestic market in mind) and
  log in to see their order history and repeat checkout with saved details. Accounts are
  never required to buy (DEC-005).
- **Acceptance criteria:**
  - [ ] AC-FR-ACC-1.1 — a registered, logged-in buyer sees their past orders and their
        current statuses
  - [ ] AC-FR-ACC-1.2 — a buyer can complete checkout without any account
  - [ ] AC-FR-ACC-1.3 — account data is deletable on request (NFR-PRIV-1)
- **Permissions / roles:** own account only
- **State transitions:** account: active → deleted (on request)
- **Edge cases:** guest order later associated with an account? — **not** in v1 (manual)
- **Error behaviour:** login failure → standard Farsi message, no user enumeration
- **Related UX:** register/login (RTL) (Frontend/UX Agent)

### FR-PAGE-1 — Policy and contact pages `[DECISION]`
- **Status:** approved · **Priority:** must (DEC-026)
- **Actor:** owner; buyer
- **Description:** Shipping, returns/refund, and contact pages render owner-provided Farsi
  wording, editable in admin without a deploy. The refund policy covers online-paid orders
  (DEC-015).
- **Acceptance criteria:**
  - [ ] AC-FR-PAGE-1.1 — all three pages are reachable from the storefront footer (or
        equivalent navigation)
  - [ ] AC-FR-PAGE-1.2 — the owner edits a page's content in admin; the change is live
        without a deploy
- **Permissions / roles:** browse = public; edit = owner
- **State transitions:** page: draft → published
- **Edge cases:** unpublished/missing page → Farsi not-found
- **Error behaviour:** —
- **Related UX:** static page layout (RTL) (Frontend/UX Agent)

---

## 3. Non-functional requirements

> Each NFR must state how it is verified, otherwise it will be ignored.

| ID | Category | Requirement | Target | Verification |
|---|---|---|---|---|
> Targets below were approved by the human with this specification (2026-09-20).
> Availability posture: **best-effort, fix-fast** — no formal SLA NFR in v1 (DEC-031).

| ID | Category | Requirement | Target | Verification |
|---|---|---|---|---|
| NFR-PERF-1 | performance | Storefront usable on mobile under social-traffic spikes (traffic is mobile-heavy per DEC-025) | core pages interactive < 3 s on a mid-range mobile connection `[REC]` | Lighthouse/performance budget check |
| NFR-SEC-1 | security | No card data ever touches the store — payment happens at the gateway; no plaintext secrets | zero stored card data `[REC]` | code review per `docs/workflows/security.md` |
| NFR-SCALE-1 | scalability | Handle expected launch traffic with spikes | 100–1,000 visitors/day, ×5 spike without degradation `[DECISION]` DEC-025 basis | load test at spike profile |
| NFR-A11Y-1 | accessibility | Full RTL correctness; baseline accessibility | WCAG 2.1 AA-minded basics `[REC]` | `docs/ux/visual_validation.md` |
| NFR-OBS-1 | observability | The owner can see failures (orders, payments, email) | failures visible in admin/logs, not silent `[REC]` | failure drill |
| NFR-MAINT-1 | maintainability | Non-technical owner runs the store alone | every v1 admin task doable without developer help `[DECISION]` §1.9 | task walkthrough with owner |
| NFR-PRIV-1 | privacy/compliance | Minimal personal data only, deletable on request | collect only name/phone/address/optional email `[DECISION]` DEC-009/DEC-017 | data inventory review |

---

## 4. Data

### 4.1 Entities and ownership
Owning modules are assigned at decomposition; listed here to bound the data.

| Entity | Owning module | Sensitivity | Retention |
|---|---|---|---|
| Product (weight, craft fee, photos, category, availability) | catalog module (TBD) | business data | while the item is sold/listed |
| Category (seed taxonomy per DEC-023) | catalog module (TBD) | business data | while used |
| DailyRate (date, rate, entered-by) | pricing module (TBD) | business data, auditable | permanent history (BR-4) |
| Reservation (product, checkout, expiry) | checkout module (TBD) | transient | until checkout completes or expires (DEC-013) |
| Order + OrderItem (contact info, totals, status, promo) | orders module (TBD) | **personal data** | per owner policy (returns window) |
| Customer account (optional, per FR-ACC-1) | accounts module (TBD) | **personal data** | deletable on request (NFR-PRIV-1) |
| PromoCode (percent, expiry, max uses, used count) | promo module (TBD) | business data | while active + audit |
| ContentPage (policy wording per DEC-026) | content module (TBD) | business data | while published |

### 4.2 Data flows
- Customer contact data (name/phone/address/optional email) flows: checkout → order record
  → owner's admin; email address (when given) also flows to the email service (FR-NOT-1).
- Order + payment result flow: checkout ↔ payment gateway (`OQ-001`); **no card data ever
  enters the store** (NFR-SEC-1).
- Daily silver rate: owner → admin → pricing (FR-RATE-1); no external flow in v1 (DEC-019).

### 4.3 Privacy and compliance
- Personal data collected is exactly: name, phone, delivery address, optional email
  (`[DECISION]` DEC-009/DEC-017) — nothing more (NFR-PRIV-1).
- Owner sees order contact data in admin to fulfil orders; it is not shared further.
- Customer accounts (when created) and their data are deletable on request (NFR-PRIV-1).
- No analytics/tracking beyond basic traffic measurement is agreed for v1 `[OPEN]` — confirm
  at spec review if the owner wants any.

---

## 5. Integrations and external services

| Service | Purpose | Auth model | Failure behaviour | Cost |
|---|---|---|---|---|
| Domestic payment gateway (`OQ-001` — **not applied yet**) | online payment (DEC-003/015) | per-gateway; owner account | payment failure → retry from checkout (DEC-014); gateway outage → checkout blocked, visible error | per-transaction fees |
| Email sending service (Architecture Agent picks; DEC-012) | order + status confirmations | API key in `.env` | send failure logged, retried; order remains valid (email is not load-bearing) | minimal (DEC-030) |
| Silver-rate feed | **NOT in v1** (manual entry, DEC-019); future automation must not re-architect pricing | — | — | — |

---

## 6. Engineering requirements

| Area | Requirement |
|---|---|
| Testing | every FR has observable ACs; `python scripts/verify.py` runs typecheck/lint/test; browser/visual validation for UI (`docs/ux/visual_validation.md`) |
| CI/CD | GitHub Actions via `.github/`; `tp.py pr-check` ownership gate on every PR |
| Coding conventions | see `docs/project/conventions.md` |
| Dependency policy | see `docs/project/conventions.md`; new runtime deps need an ADR (DEC-030 bias: few) |
| Documentation | owned docs updated in the same PR as code (AGENTS.md rule 8) |
| Definition of done | see `docs/project/definition_of_done.md` |

---

## 7. Open items

Unresolved items are tracked in `docs/project/open_questions.md`; do not bury them here.

| Type | ID | Summary |
|---|---|---|
| OPEN | OQ-001 | Payment gateway — **knowingly accepted as launch risk** (DEC-033); blocks FR-PAY-1 only |
| OPEN | OQ-011 | — closed (DEC-031) |
| OPEN | OQ-012 | — closed (DEC-032) |
| ASSUMPTION | ASM-001 | Gateway obtainable before launch — **owner has not applied** |
| ASSUMPTION | ASM-004 | Demand band: few orders/day, 100–1,000 visitors/day |
| RISK | RISK-001 | Gateway unobtainable in time — score 15, owner action required |

---

## 8. Change log

| Date | Change | By | Reference |
|---|---|---|---|
| | initial draft | discovery | — |
