# User flows

> Owned by the Frontend/UX Agent. A flow is the end-to-end path a user takes to accomplish one
> goal: happy path **plus** the states and failures around it. Implementation agents receive only
> the flows their module touches (via `ux_refs` in the module contract).
>
> Modules are `TBD` until decomposition; contracts will cite these flows by ID.

## Flow index

| ID | Flow | Persona | Entry points | Screens | Modules | Priority |
|---|---|---|---|---|---|---|
| UF-01 | Discover and choose a product | P1 | home, search, social links, category tiles | home, category, search, product | TBD (catalog/search) | must |
| UF-02 | Buy end-to-end as a guest | P1 | product page | product, cart (drawer), checkout, payment, confirmation | TBD (cart/checkout/payment) | must |
| UF-03 | Track an order (guest-safe) | P1 | header/footer, confirmation page, email link | track, confirmation | TBD (orders) | must |
| UF-04 | Owner daily operations | P2 | `/admin` | admin rate, admin orders, admin order detail | TBD (admin) | must |

## Flow format

Each flow answers, in order: who, why, from where, what happens step by step, what can go wrong,
where the user can leave and come back, and how we know it worked.

---

## UF-01 — Discover and choose a product

**Actor:** P1 · **Goal:** find a piece she trusts and understand its price ·
**Trigger:** social post, shared link, or organic visit · **Preconditions:** none (public) ·
**Success:** product page open with price + rate date understood ·
**Related requirements:** `FR-CAT-1`, `FR-CAT-2`, `FR-PROD-1`, `UX-001`, `UX-006`, `UX-012`, `DEC-050`, `DEC-051`, `DEC-052`, `DEC-053`

### Steps (happy path)

| # | User action | System response | Screen / state | Notes |
|---|---|---|---|---|
| 1 | lands on home | hero, category tiles, rate chip (small) + سنگ این ماه chip, featured design, product row, سنگ ماه album (دوازده ماه میلادی), trust row, story | home / default | `DEC-039` composition; the accent is this Gregorian month's stone (`DEC-050`, `DEC-053`); the album names all twelve Gregorian months' stones with the current one marked (`DEC-052`) |
| 2 | taps a category tile | category grid with product cards (name · price · rate date · photo) | category / default | starter taxonomy + شمش (`DEC-038`) |
| 3 | applies filters (price / weight / stone) or uses search | filtered results, URL reflects state | category or search / default | combinable (AND), `FR-CAT-2` |
| 4 | taps a product card | product page: gallery, price + rate date, weight, stone, availability | product / default | `FR-PROD-1` |

### Alternative paths

| Branch | Condition | Divergence | Returns to step |
|---|---|---|---|
| A1 | arrives from a shared/social product link | skips 1–3, lands on product page | 4 |
| A2 | search has no results | helpful Farsi empty state + suggested categories | 3 |
| A3 | taps the small homepage rate chip | sees today's rate + date (informational) | 1 |
| A4 | wants the shop's ماه‌سنگ pieces | picks the «ماه‌سنگ» stone filter on a category or search page (shareable URL) — the homepage no longer carries a moonstone CTA (`DEC-052`) | 3 |
| A5 | reads the سنگ ماه album without clicking anything | sees all twelve **Gregorian** months (Farsi + Latin) with their stone; the current month is marked «این ماه» — it is static reading | 1 |
| A6 | her own birth month's stone is not the current one | she finds her month in the album — no personalisation in v1, so the accent stays the current Gregorian month's (`OQ-015`) | 1 |

### Failure paths

| Failure | Detection | User sees | Recovery | Logged |
|---|---|---|---|---|
| stale rate (RISK-002) | rate date ≠ today | price with last-known rate + its date + unobtrusive note | shopping continues (`UX-001`) | yes |
| slow connection | > 300 ms | layout-matching skeleton (`UX-G-004`) | automatic | no |
| unknown category/product URL | 404-equivalent | Farsi not-found page with paths to home/categories | navigate away | yes |

### States around the flow

| State | Where | What the user sees |
|---|---|---|
| loading | home/category/search/product | skeleton matching final layout |
| empty | category with no products, empty search | explanation + links to other categories |
| error | data fetch fails | message + retry, page frame intact |
| success | — | n/a (browsing has no terminal success state) |
| permission-denied | — | n/a (public) |

### Data touched

| Data | Read | Written | Sensitivity | Validation |
|---|---|---|---|---|
| products, categories, daily rate | yes | no | business data | — |

### Responsive behaviour

| Breakpoint | Behaviour |
|---|---|
| ≥ 1280 px | 4-up product grid, filters in a side rail |
| 768–1279 px | 3-up grid, filters collapsible rail |
| < 768 px | 2-up grid, filters in a bottom sheet, horizontal category chip row |

### Accessibility notes

- Keyboard path: skip-link → nav → filters → product grid; every card focusable and operable.
- Focus order and focus return: bottom-sheet filters return focus to their trigger on close.
- Announcements: result-count changes announced politely after filtering.
- Target sizes: ≥ 44 px cards/controls (`UX-G-010`).

### Acceptance criteria

- [ ] UF-01-AC1 — from home, any starter category is reachable in 1 tap
- [ ] UF-01-AC2 — price + rate date are visible on every product card and the product page (`UX-AC-001.1`)
- [ ] UF-01-AC3 — filters combine with category and are reflected in a shareable URL
- [ ] UF-01-AC4 — every failure path above preserves the page frame (no dead ends)
- [ ] UF-01-AC5 — the ماه‌سنگ filter option reaches the moonstone-tagged result set in ≤ 2 taps from home and the URL is shareable (`DEC-051` clause b)
- [ ] UF-01-AC6 — the سنگ ماه album is readable without a single interaction and needs no data call; the current Gregorian month is identifiable from text alone (`UX-AC-012.6`, `DEC-053`)
- [ ] UF-01-AC7 — the album contains no link and no control, so it can never become a dead end (`DEC-052`)

### Verification

| Check | How | Evidence |
|---|---|---|
| happy path | browser walkthrough | screenshots |
| failure paths | stale-rate simulation, 404 URL, network offline | screenshots + notes |
| responsive | viewport sweep | screenshots at 3 widths |
| keyboard | keyboard-only walkthrough | notes |

---

## UF-02 — Buy end-to-end as a guest

**Actor:** P1 · **Goal:** buy a piece without an account and get proof of order ·
**Trigger:** "add to cart" on a product page · **Preconditions:** product in stock; a rate
exists for today (or last-known fallback per `UX-001`) · **Success:** Paid order +
confirmation with order code · **Related requirements:** `FR-CART-1`, `FR-CHK-1`, `FR-PAY-1`,
`FR-PROMO-1`, `UX-002`, `UX-008`, `UX-009`

### Steps (happy path)

| # | User action | System response | Screen / state | Notes |
|---|---|---|---|---|
| 1 | adds product to cart | cart drawer opens with line + total (+ rate date) | cart drawer / default | guest, no account prompt (`PRIN-2`) |
| 2 | continues shopping or taps "checkout" | checkout page (single page, sections) | checkout / default | `DEC-041` |
| 3 | enters name, phone, address; optional email | inline validation, fields labelled in Farsi | checkout / default | `FR-CHK-1`; **stock reserved at step start** (`BR-1`) |
| 4 | optionally applies promo code | total updates or code rejected with reason | checkout / default | `FR-PROMO-1` |
| 5 | taps "pay" | payment step: final total (rate at payment, promo applied) + security note + gateway redirect | payment / default | irreversible-step confirmation (`UX-009`, `DEC-020`) |
| 6 | pays at the gateway | returns to confirmation: order code prominent, status timeline, track-order explainer | confirmation / success | `FR-ORD-1`; email if provided (`FR-NOT-1`) |

### Alternative paths

| Branch | Condition | Divergence | Returns to step |
|---|---|---|---|
| A1 | item went out of stock while in cart | cart flags the item; checkout blocked with named reason (`UX-AC-008.2`) | 1–2 |
| A2 | buyer cancels at the gateway | back to checkout, cart and details intact (`UX-AC-009.3`) | 5 |
| A3 | buyer has an account and is logged in | contact details pre-filled, still editable | 3 |

### Failure paths

| Failure | Detection | User sees | Recovery | Logged |
|---|---|---|---|---|
| gateway failure / timeout | gateway callback error | returned to intact checkout + clear Farsi reason + retry (`DEC-014`) | retry immediately | yes |
| reservation expired mid-checkout | expiry check | explanation that stock was released; re-checkout if available (`UX-AC-008.3`) | re-checkout | yes |
| required field missing / bad phone | inline validation | field error + summary, nothing lost | correct and resubmit | no |
| promo code expired/exhausted | validation | code rejected with reason; total unchanged (`AC-FR-PROMO-1.2`) | remove code or retry | no |
| price changed since checkout start | rate at payment | payment step shows the **new** final total explicitly (`DEC-020`) — never silent drift | accept and pay, or abandon | yes |

### States around the flow

| State | Where | What the user sees |
|---|---|---|
| loading | payment redirect | progress + "do not close the page" note |
| empty | empty cart → checkout blocked | explanation + continue shopping |
| error | gateway failure | intact checkout + reason + retry |
| success | confirmation | order code, status timeline, track-order explainer, (soft) account offer |
| permission-denied | — | n/a (guests by design) |

### Data touched

| Data | Read | Written | Sensitivity | Validation |
|---|---|---|---|---|
| cart items, computed prices | yes | no | business data | — |
| reservation | created at step 3 | transient | — | expiry per `FR-CHK-1` |
| contact info (name/phone/address/optional email) | — | written at order | **personal data** (NFR-PRIV-1) | phone format (domestic) |
| order + payment result | — | written | personal data | gateway callback idempotent |
| promo usage | read/increment | paid orders only (`AC-FR-PROMO-1.3`) | business data | — |

### Responsive behaviour

| Breakpoint | Behaviour |
|---|---|
| ≥ 1280 px | drawer cart; checkout single page, two-column (form / summary) |
| 768–1279 px | drawer cart; checkout single column with sticky summary |
| < 768 px | drawer cart; checkout single column, summary above the pay button |

### Accessibility notes

- Keyboard path: drawer focus-trapped; checkout fields in logical order; pay button reachable.
- Focus order and focus return: drawer close returns focus to its trigger; errors move focus to summary.
- Announcements: total changes announced politely; gateway redirect state announced.
- Target sizes: pay button ≥ 44 px height; promo field labelled (never placeholder-only).

### Acceptance criteria

- [ ] UF-02-AC1 — first-time guest completes purchase with zero account interactions (`UX-AC-002.1`)
- [ ] UF-02-AC2 — every failure path returns the buyer to an intact checkout (`DEC-014`)
- [ ] UF-02-AC3 — the total shown at the payment step equals the charged amount, with basis visible (`UX-AC-009.1`)
- [ ] UF-02-AC4 — abandoning at any step before payment loses nothing the user entered (cart persists per browser)

### Verification

| Check | How | Evidence |
|---|---|---|
| happy path | browser walkthrough with test gateway | screenshots |
| failure paths | forced gateway error, expired reservation, promo rejection | screenshots + notes |
| responsive | viewport sweep incl. social webview | screenshots at 3 widths |
| keyboard | keyboard-only checkout | notes |

---

## UF-03 — Track an order (guest-safe)

**Actor:** P1 · **Goal:** know where the order stands without contacting anyone ·
**Trigger:** header/footer track-order link, confirmation page, email link ·
**Preconditions:** order code (+ phone for on-site lookup) ·
**Success:** current status shown on a timeline ·
**Related requirements:** `FR-ORD-1`, `UX-003`, `DEC-021`

### Steps (happy path)

| # | User action | System response | Screen / state | Notes |
|---|---|---|---|---|
| 1 | opens track-order entry point | compact lookup form (code + phone) | track / default | reachable site-wide (`UX-AC-003.1`) |
| 2 | enters order code + phone from confirmation/SMS-free memory | status timeline Paid → Shipped → Delivered | track / success | forward-only (`BR-2`) |
| — | (or) opens the emailed link | same timeline, pre-filled lookup | track / success | only when email was provided (`DEC-017`) |

### Alternative paths

| Branch | Condition | Divergence | Returns to step |
|---|---|---|---|
| A1 | logged-in account holder | "my orders" list replaces manual lookup | — |

### Failure paths

| Failure | Detection | User sees | Recovery | Logged |
|---|---|---|---|---|
| unknown code, or wrong phone | lookup fails | single Farsi not-found message (no data leak, identical for both cases) | re-enter / contact link | yes (rate-limited) |

### States around the flow

| State | Where | What the user sees |
|---|---|---|
| loading | lookup in flight | brief progress |
| empty | no match | not-found state (`UX-AC-003.3`) |
| error | service failure | message + retry |
| success | match | status timeline + order summary |
| permission-denied | — | n/a (code+phone *is* the permission) |

### Data touched

| Data | Read | Written | Sensitivity | Validation |
|---|---|---|---|---|
| order status (by code+phone) | yes | no | personal data — **anti-enumeration care** (`DEC-021`) | code format; phone match |

### Responsive behaviour

| Breakpoint | Behaviour |
|---|---|
| all | compact form; timeline renders vertically on mobile, horizontally on desktop |

### Accessibility notes

- Keyboard path: two fields + submit, natural order.
- Focus order and focus return: error returns focus to the failed field.
- Announcements: status result announced politely; errors via `role="alert"`.
- Bidi: Latin/digit order code inside RTL text renders unambiguously (`UX-G-009`).

### Acceptance criteria

- [ ] UF-03-AC1 — site-wide entry point → lookup form in ≤ 1 click (`UX-AC-003.1`)
- [ ] UF-03-AC2 — status lookup works with no email at all (`DEC-021`)
- [ ] UF-03-AC3 — wrong phone + valid code is indistinguishable from unknown code
- [ ] UF-03-AC4 — timeline states are forward-only and match the order record

### Verification

| Check | How | Evidence |
|---|---|---|
| happy path | browser walkthrough with seeded order | screenshots |
| failure paths | unknown code, wrong phone | screenshots + notes |
| responsive | viewport sweep | screenshots at 3 widths |
| keyboard | keyboard-only walkthrough | notes |

---

## UF-04 — Owner daily operations

**Actor:** P2 · **Goal:** run the day: rate in, orders forward ·
**Trigger:** opening `/admin` · **Preconditions:** owner login ·
**Success:** today's rate entered; new Paid orders seen; statuses advanced ·
**Related requirements:** `FR-RATE-1`, `FR-ADM-2`, `FR-ORD-1`, `UX-007`

### Steps (happy path)

| # | User action | System response | Screen / state | Notes |
|---|---|---|---|---|
| 1 | logs into `/admin` | dashboard: today's-rate state, new orders count, sales overview | admin / default | banner if rate missing (`UX-AC-007.3`) |
| 2 | enters today's silver rate | rate saved with date; staleness banner clears; history updated | admin rate / success | auditable (`FR-RATE-1`); same-day edits allowed, latest wins |
| 3 | opens new Paid orders | order detail: buyer contact, items, totals | admin order detail / default | full buyer info (`AC-FR-ADM-2.1`) |
| 4 | advances status Paid → Shipped (→ Delivered later) | status saved; buyer email queued (if provided); timeline updates | admin order detail / success | forward-only, no backward moves (`BR-2`) |

### Alternative paths

| Branch | Condition | Divergence | Returns to step |
|---|---|---|---|
| A1 | needs to fix stock/price inputs for an item | jumps to admin catalog (separate flow, W2) | — |
| A2 | no rate entered yet today | rate banner deep-links to the rate screen | 2 |

### Failure paths

| Failure | Detection | User sees | Recovery | Logged |
|---|---|---|---|---|
| invalid rate (≤ 0, malformed) | validation | Farsi field error, previous value kept (`AC-FR-RATE-1.3` note) | correct and resubmit | no |
| email send failure on status change | notification queue | non-blocking; visible in admin/log (NFR-OBS-1) | order stands; retry automatic | yes |
| duplicate status click | server idempotence | second click is a no-op, no error | — | no |

### States around the flow

| State | Where | What the user sees |
|---|---|---|
| loading | dashboard/order lists | skeletons |
| empty | no orders yet | explanation + what will appear here |
| error | save fails | message + retry, form intact |
| success | after each save | explicit saved-state confirmation |
| permission-denied | not logged in | admin login screen |

### Data touched

| Data | Read | Written | Sensitivity | Validation |
|---|---|---|---|---|
| daily rate | read + write | history retained | business data, auditable (`BR-4`) | > 0, numeric |
| orders + status | read + advance | status history | personal data | forward-only |

### Responsive behaviour

| Breakpoint | Behaviour |
|---|---|
| ≥ 1280 px | sidebar + content, tables |
| 768–1279 px | collapsible sidebar, reduced-column tables |
| < 768 px | deferred unless P2 asks (`ux_requirements.md` §7) |

### Accessibility notes

- Keyboard path: sidebar → tables → detail forms fully operable.
- Focus order and focus return: dialogs (confirmations) trap and return focus.
- Announcements: status change success announced politely.
- Target sizes: ≥ 24 px (desktop); tables keep readable row heights.

### Acceptance criteria

- [ ] UF-04-AC1 — the daily rate takes < 30 s from login to saved (task walkthrough)
- [ ] UF-04-AC2 — a missing rate is visible from every admin page until resolved (`UX-AC-007.3`)
- [ ] UF-04-AC3 — status can only move forward; UI offers no backward action (`AC-FR-ORD-1.2`)
- [ ] UF-04-AC4 — email failure never blocks the status change (NFR-OBS-1)

### Verification

| Check | How | Evidence |
|---|---|---|
| happy path | task walkthrough with the owner (NFR-MAINT-1) | notes + timings |
| failure paths | invalid rate, email outage simulation | screenshots + notes |
| responsive | two widths (desktop, tablet) | screenshots |
| keyboard | keyboard-only walkthrough | notes |
