# UX requirements — NoghreShop

> **Status:** draft v2 — full spec written, awaiting human review (`screens.md` 25 screens, `design_system.md`, `interaction_patterns.md`) · **Owner:** Frontend/UX Agent ·
> **Approved by:** — (gate `gates.ux_approved`, set only after human review of the full spec)
>
> Personas, user goals and numbered UX requirements. Requirements here are **behavioural and
> measurable**; visual detail lives in `design_system.md`, flows in `user_flows.md`.

## 1. Personas

| Persona | Role | Context of use | Devices | Frequency | Skill / accessibility needs |
|---|---|---|---|---|---|
| P1 | domestic retail buyer | discovers the shop via social media on a phone; buys from the bus, the couch, the queue | mid-range Android or iPhone, sometimes weak connection | first-time buyer, then occasional | mixed ages; expects Persian UI; some low-vision users; touch-dominant |
| P2 | owner (store admin) | runs the shop alone alongside the physical business | desktop, daily | daily (rates, orders) / weekly (catalog) | **non-technical** — must never need developer help (NFR-MAINT-1) |

### P1 — Domestic retail buyer
- **Job to be done:** find a silver piece she trusts, understand its price, pay safely online, receive it, and be able to check her order without calling anyone.
- **Pain today:** no way to buy from this business online at all (round 1: "not selling yet"); distrust of unfamiliar online shops is the default posture in the market.
- **Definition of success for them:** from product page to paid order in minutes, with a price she understands (weight × today's rate + craft fee, `BR-4`) and a confirmation she can keep.
- **Where they work from:** phone-first, mobile connections, social-app webviews (`DEC-025`: mobile-heavy traffic).
- **Accessibility considerations:** Farsi screen-reader users (VoiceOver/NVDA), zoom users, one-handed use; colour never the only signal.

### P2 — Owner (store admin)
- **Job to be done:** enter today's silver rate, list products with photos, advance orders Paid → Shipped → Delivered, manage promo codes and policy pages — without technical help.
- **Pain today:** runs everything offline; every manual step is his time.
- **Definition of success for them:** each daily task takes seconds, forms never lose input, and anything wrong (expired rate, failed email, gateway issue) is *visible* in admin (NFR-OBS-1).
- **Where they work from:** desktop, private device, good connection (`DEC-037`); occasional phone use for order status was left undecided (`UX-OPEN`, see §7).
- **Accessibility considerations:** readable numerals for money/rates, ≥ 24 px targets, no hover-only affordances, plain Farsi copy.

## 2. UX principles

| ID | Principle | Means | Test in review |
|---|---|---|---|
| PRIN-1 | **The price is never ambiguous.** Every price shows its computation basis and rate date; the final total is re-displayed at the payment step (`DEC-020`) | price line = amount + "وزن × نقره‌ی روز + اجرت" + rate date; payment step repeats the total | every price on every screen carries a rate date; no total changes without a visible reason |
| PRIN-2 | **No account is ever required to buy** (`DEC-005`) | guest checkout is the default path; register/login is offered after value, never before it | a first-time visitor completes checkout with zero account interactions |
| PRIN-3 | **Quiet chrome, loud product** (modern minimal, `DEC-035`) | whitespace, restrained palette, photos and prices carry the page; no decorative clutter | every screen passes the "nothing decorative competes with the product" review |
| PRIN-4 | **Persian-native RTL, not mirrored LTR** (`DEC-004`) | logical layout properties, Persian numerals and dates, RTL-aware icons/carousels, bidi-safe order codes | no screen shows a mirrored-by-accents LTR layout; mixed-direction text renders correctly |
| PRIN-5 | **The UI never lies about state.** Stock, reservations, rate staleness and failures are shown truthfully and immediately | out-of-stock is visible, reserved stock explains itself, stale rate warns (RISK-002 fallback, `FR-RATE-1`) | forced-failure sweep shows no silent states |
| PRIN-6 | **The owner is not technical.** Admin copy, flows and errors are plain Farsi; destructive actions are confirmable and recoverable | single-column forms, explicit confirmations, no jargon, no dead ends | a non-technical user completes every admin task from the contract unaided (NFR-MAINT-1) |

## 3. UX requirements

> `UX-###` IDs are referenced by module contracts (`ux_refs`). Never renumber.

### UX-001 — Rate-dated price display everywhere `[DECISION]`
- **Persona:** P1
- **Statement:** every product price on every screen shows the computed price **and the date of the silver rate** it is based on; when no rate exists for today, the last-known rate and its date are shown with an unobtrusive staleness note (storefront side; the hard warning lives in admin, `FR-RATE-1`).
- **Trigger / entry point:** any product price render (listing, product page, cart, checkout, payment).
- **States:** default (rate current) · fallback (rate stale → date shown, note shown) · error (no rate ever entered → product not buyable, message explains, `FR-RATE-1`).
- **Responsive behaviour:** full line on all widths; the explanation collapses under the amount on mobile.
- **Accessibility:** the rate date is real text (not watermark); contrast ≥ 4.5:1; announced with the price by screen readers.
- **Acceptance criteria:**
  - [ ] UX-AC-001.1 — every rendered price is visually accompanied by a rate date, on all of: listing, product page, cart, checkout, payment step
  - [ ] UX-AC-001.2 — with a stale rate, the fallback (last-known rate + date + note) renders and the "add to cart" stays available unless `FR-RATE-1` forbids it
  - [ ] UX-AC-001.3 — a screen reader announces price + date as one coherent statement
- **Related requirement:** `FR-PROD-1`, `FR-RATE-1`, `BR-4`, RISK-002
- **Screens:** all commerce screens (`screens.md`)
- **Flows:** UF-01, UF-02 (`user_flows.md`)
- **Status:** proposed · **Wave:** W1

### UX-002 — Guest-first purchase path `[DECISION]`
- **Persona:** P1
- **Statement:** a first-time visitor can go from product page to paid order without creating an account; account entry points (login, register) never interrupt checkout and are offered at natural moments (header, post-order success).
- **Trigger / entry point:** any product page → cart → checkout.
- **States:** default · loading · error · success (order confirmation with code); permission-denied does not exist for guests by design.
- **Responsive behaviour:** identical guest path at all widths.
- **Accessibility:** checkout form fully keyboard operable; progress perceivable without colour.
- **Acceptance criteria:**
  - [ ] UX-AC-002.1 — zero account interactions are needed between landing and payment
  - [ ] UX-AC-002.2 — register/login offers are dismissible and never overlay the checkout form
- **Related requirement:** `FR-CHK-1`, `FR-ACC-1`, `DEC-005`
- **Screens:** checkout, confirmation
- **Flows:** UF-02
- **Status:** proposed · **Wave:** W1

### UX-003 — Guest order transparency `[DECISION]`
- **Persona:** P1
- **Statement:** the buyer can check order status on-site at any time: order code + phone lookup reachable from a persistent site-wide entry point, and via the emailed link when an email exists (`DEC-021`); the confirmation screen states this explicitly ("save your order code").
- **Trigger / entry point:** header/footer "track order" (پیگیری سفارش), confirmation page, email link.
- **States:** default · loading · empty (unknown code/phone → not-found message, no data leak `FR-ORD-1`) · error · success (status timeline).
- **Responsive behaviour:** lookup is a compact form at all widths.
- **Accessibility:** mixed-direction order code (Latin/digits inside RTL text) renders unambiguously (see `UX-G-009`); errors announced via `role="alert"`.
- **Acceptance criteria:**
  - [ ] UX-AC-003.1 — a site-wide track-order entry point is reachable from every storefront page in ≤ 1 click
  - [ ] UX-AC-003.2 — the confirmation screen shows the order code prominently with an explicit "how to check status later" line
  - [ ] UX-AC-003.3 — wrong phone + valid code yields the not-found state, identical to unknown code
- **Related requirement:** `FR-ORD-1`, `DEC-021`
- **Screens:** order tracking, confirmation
- **Flows:** UF-03
- **Status:** proposed · **Wave:** W1

### UX-004 — Trust scaffolding `[DECISION]`
- **Persona:** P1
- **Statement:** shipping, returns/refund and contact pages are reachable from every page (footer), payment security is stated near the pay button, and every irreversible step is preceded by a confirmation the buyer actually reads (payment step).
- **Trigger / entry point:** footer (global), payment step.
- **States:** n/a (cross-cutting).
- **Responsive behaviour:** footer collapses to an accordion on mobile; links remain reachable.
- **Accessibility:** footer landmarks labelled; links descriptive in Persian.
- **Acceptance criteria:**
  - [ ] UX-AC-004.1 — all three policy pages reachable from every storefront page in ≤ 1 click
  - [ ] UX-AC-004.2 — the payment step states security/redirect behaviour before the buyer leaves for the gateway
- **Related requirement:** `FR-PAGE-1`, `FR-PAY-1`, `DEC-026`
- **Screens:** policy pages, payment step
- **Flows:** UF-02
- **Status:** proposed · **Wave:** W1

### UX-005 — RTL-first layout quality `[DECISION]`
- **Persona:** P1, P2
- **Statement:** all layouts are authored RTL-first with logical CSS properties; icons with direction (arrows, chevrons, progress) mirror correctly; carousels and galleries advance in reading direction (right → left).
- **Trigger / entry point:** all screens.
- **States:** n/a (cross-cutting).
- **Responsive behaviour:** identical rule at all widths.
- **Accessibility:** focus order follows visual RTL reading order.
- **Acceptance criteria:**
  - [ ] UX-AC-005.1 — zero hard-coded left/right positioning in shipped components (code-review check)
  - [ ] UX-AC-005.2 — gallery/carousel/progress indicators advance in RTL reading direction
  - [ ] UX-AC-005.3 — keyboard focus order matches visual order on 3 sampled screens per wave
- **Related requirement:** `DEC-004`, NFR-A11Y-1
- **Screens:** all
- **Flows:** —
- **Status:** proposed · **Wave:** W1 (continues through all waves)

### UX-006 — Mobile-first performance posture `[DECISION]`
- **Persona:** P1
- **Statement:** the storefront is designed mobile-first and stays interactive under 3 s on a mid-range phone/connection (NFR-PERF-1): skeleton loading that matches final layout, progressive gallery images, no blocking third-party scripts on commerce screens.
- **Trigger / entry point:** all storefront screens.
- **States:** loading (skeleton), error (retry), empty.
- **Responsive behaviour:** this requirement *is* the responsive rule for storefronts.
- **Accessibility:** skeletons announce busy state; content has stable layout (no shift on image load, `UX-G-007`).
- **Acceptance criteria:**
  - [ ] UX-AC-006.1 — home, category, product, cart, checkout each render a layout-matching skeleton within 300 ms on throttled connection
  - [ ] UX-AC-006.2 — gallery images load progressively without layout shift (CLS ≈ 0 on product page)
- **Related requirement:** NFR-PERF-1, NFR-SCALE-1, `DEC-025`
- **Screens:** all storefront screens
- **Flows:** all P1 flows
- **Status:** proposed · **Wave:** W1

### UX-007 — Desktop-first admin ergonomics `[DECISION]`
- **Persona:** P2
- **Statement:** admin is designed desktop-first: stable sidebar navigation, single-column forms, explicit save states, confirmations on destructive actions, and a persistent staleness banner on the daily-rate surface when today's rate is missing (`FR-RATE-1`).
- **Trigger / entry point:** `/admin` shell.
- **States:** default · loading · empty (no data yet — e.g., fresh catalog) · error · success (saved) · permission-denied (login).
- **Responsive behaviour:** desktop-first; usable-but-reduced on tablet; phone behaviour deferred unless P2 asks (`UX-OPEN`).
- **Accessibility:** form labels always visible (no placeholder-as-label), errors associated with fields, numbers right-punctuated in Persian formatting.
- **Acceptance criteria:**
  - [ ] UX-AC-007.1 — every admin form keeps entered data on validation error and states what to fix in Farsi
  - [ ] UX-AC-007.2 — destructive admin actions (retire product, delete promo code) require explicit confirmation and state the consequence
  - [ ] UX-AC-007.3 — the admin shows a visible banner on every admin page while today's rate is missing
- **Related requirement:** `FR-ADM-1`, `FR-ADM-2`, `FR-RATE-1`, NFR-MAINT-1
- **Screens:** admin shell + admin screens
- **Flows:** UF-04
- **Status:** proposed · **Wave:** W2

### UX-008 — Stock and reservation honesty `[DECISION]`
- **Persona:** P1
- **Statement:** the UI states stock truthfully at every step: out-of-stock items are viewable but not addable (`FR-PROD-1`); an item reserved by someone else's checkout shows out-of-stock (`BR-1`); an item that went out of stock inside a cart is flagged and blocks checkout (`FR-CART-1`); an expired reservation explains what happened and offers re-checkout (`FR-CHK-1`).
- **Trigger / entry point:** listing, product page, cart, checkout.
- **States:** in stock · out of stock (owner-set or reserved) · flagged-in-cart · reservation-expired.
- **Responsive behaviour:** same states at all widths.
- **Accessibility:** stock state is text, not colour-only (`UX-G-006`).
- **Acceptance criteria:**
  - [ ] UX-AC-008.1 — adding an unavailable product is blocked with a Farsi reason, from every entry point
  - [ ] UX-AC-008.2 — a cart containing a now-unavailable item blocks checkout and names the item
  - [ ] UX-AC-008.3 — after reservation expiry mid-checkout, the buyer sees what happened and a working re-checkout path
- **Related requirement:** `FR-CART-1`, `FR-CHK-1`, `BR-1`, `DEC-013`
- **Screens:** listing, product, cart, checkout
- **Flows:** UF-02 (failure paths)
- **Status:** proposed · **Wave:** W1

### UX-009 — Payment-step clarity `[DECISION]`
- **Persona:** P1
- **Statement:** the step that leaves for the gateway re-displays the final total (rate at payment per `DEC-020`, minus promo), states that the browser is leaving the store, and on failure returns the buyer to an intact checkout (`DEC-014`) with the cart and details preserved and a clear retry affordance.
- **Trigger / entry point:** checkout → payment.
- **States:** default (final total) · loading (redirect) · error (gateway unreachable/failed → intact return + retry) · success (confirmation) · cancelled (back to checkout, cart intact).
- **Responsive behaviour:** identical at all widths.
- **Accessibility:** total change between checkout start and payment is announced (not silent); retry is keyboard reachable.
- **Acceptance criteria:**
  - [ ] UX-AC-009.1 — the payment step shows the final total incl. promo and its basis before redirect
  - [ ] UX-AC-009.2 — after a failed payment, checkout re-renders with cart and entered details intact and a visible retry
  - [ ] UX-AC-009.3 — user-initiated cancel at the gateway returns to checkout with nothing lost
- **Related requirement:** `FR-PAY-1`, `DEC-014`, `DEC-020`, `FR-PROMO-1`
- **Screens:** checkout, payment step
- **Flows:** UF-02 (failure paths)
- **Status:** proposed · **Wave:** W1 (payment UI itself blocked by `OQ-001`)

### UX-010 — Homepage merchandising `[DECISION]`
- **Persona:** P1
- **Statement:** the homepage presents, in order: hero → category tiles (starter taxonomy incl. شمش, `DEC-038`) → new/bestselling products → سنگ ماه album (دوازده ماه) → trust row → craft story; a **small** silver-rate display (rate + date) and a «سنگ این ماه» chip sit on the homepage (`DEC-039`, `DEC-050`); a featured "design of the month" slot shows the owner's pick and **stays hidden when unset** (`DEC-043`). The homepage also carries a **سنگ ماه album** — all twelve **Gregorian** months' stones in one compact block, the current month's tile marked (`DEC-052`, `DEC-053`, `UX-012`); the shop's ماه‌سنگ speciality is reached through the stone filter and the product attribute (`DEC-051` clause b), not through a homepage CTA.
- **Trigger / entry point:** `/` (landing, social traffic `DEC-025`).
- **States:** default · loading (skeletons) · error (sections degrade independently — a failed section never blanks the page) · empty (no featured pick → slot hidden; empty category tiles link to taxonomy anyway).
- **Responsive behaviour:** blocks reflow to single column < 768 px; hero image swaps to a mobile crop.
- **Accessibility:** rate chip is real text; featured slot is a labelled section; hero headline is an h1, blocks are h2 sections.
- **Acceptance criteria:**
  - [ ] UX-AC-010.1 — all six fixed blocks render in the accepted order at 3 widths (hero, tiles, product row, سنگ ماه album, trust row, story)
  - [ ] UX-AC-010.2 — the rate chip shows rate + date (or hides when no rate ever entered) and never duplicates the per-product date rule (`UX-001`)
  - [ ] UX-AC-010.3 — with no featured pick, no empty slot renders (`DEC-043`)
  - [ ] UX-AC-010.4 — each block fails independently (one broken section never blanks the homepage)
  - [ ] UX-AC-010.5 — the سنگ ماه album renders in its accepted position (after the product row, before the trust row) at all three widths, needs no maintenance, and never hides a commerce block (`DEC-052`)
- **Related requirement:** `FR-CAT-1`, `FR-RATE-1`, `DEC-025`, `DEC-038`, `DEC-039`, `DEC-043`, `DEC-050`, `DEC-051`
- **Screens:** home
- **Flows:** UF-01
- **Status:** proposed · **Wave:** W1

### UX-011 — Featured design of the month (admin + storefront) `[DECISION]`
- **Persona:** P2 (setup) · P1 (consumption)
- **Statement:** the owner selects one active product as the featured design and may add a short Farsi note; the storefront homepage slot presents it with a prominent path to the product page; selection and clearing take effect immediately without a deploy.
- **Trigger / entry point:** `/admin/featured` → homepage slot.
- **States:** admin: default (current pick) · empty (none — storefront hides slot) · error · success (saved); storefront: present / hidden.
- **Responsive behaviour:** slot spans full width on mobile, framed feature on desktop.
- **Accessibility:** slot announced as a section; pick is keyboard operable in admin.
- **Acceptance criteria:**
  - [ ] UX-AC-011.1 — the owner selects/clears a featured product in ≤ 3 interactions; change is live without deploy
  - [ ] UX-AC-011.2 — clearing the pick hides the storefront slot immediately
  - [ ] UX-AC-011.3 — featuring a retired product is prevented (or falls back to hidden) rather than showing a dead link
- **Related requirement:** `FR-ADM-1`, `DEC-043`, `DEC-042`
- **Screens:** home, admin featured
- **Flows:** UF-01, UF-04
- **Status:** proposed · **Wave:** W1 (slot) / W2 (admin screen)

### UX-012 — Stone-of-the-month theme and the سنگ ماه album `[DECISION]`
- **Persona:** P1
- **Statement:** the storefront accent is the current month's stone (سنگ ماه تولد, **Gregorian** calendar — `DEC-053`) — twelve contrast-checked accent sets (`design_system.md` §2.1, `DEC-050`) — so the shop's own speciality, ماه‌سنگ, is the accent every ژوئن. The theme never carries meaning on its own and never changes layout. The homepage additionally carries a **سنگ ماه album** that makes the cycle legible: all twelve Gregorian months with their stone (Farsi + Latin) from `design_system.md` §2.2 and the same Gregorian month name the chip prints, the current month's tile marked with the text «این ماه». The album is intentionally compact (month and stone only — no care or appearance copy), static and non-interactive, and privileges no stone (`DEC-052`).
- **Trigger / entry point:** any storefront render (Gregorian month resolved server-side, Asia/Tehran) · month rollover on the 1st · reading the سنگ ماه album.
- **States:** default (month resolved → that stone's accent) · fallback (month unresolvable → ژانویه/گارنت set, still ≥ 4.5:1) · empty (empty catalogue → the album still renders; it depends on nothing) · error (n/a for the album — static content, and the `:root` set is the accent fallback) · success (n/a) · permission-denied (n/a, public).
- **Responsive behaviour:** identical accent at all widths; album tiles 4-up ≥ 1280, 3-up 768–1279, 2-up < 768 with no truncated stone names; the chip sits inline with the rate chip and wraps under the hero on mobile.
- **Accessibility:** white text on every monthly accent ≥ 4.5:1 (minimum 5.8:1) and `accent.subtle` ≥ 15:1 with primary text; the chip and the album are real text, the album is a labelled `<section>` with an `<h2>`, the current month is marked by the word «این ماه» (not by the swatch), and decorative stone swatches are `aria-hidden`; the accent is never the only signal (`UX-G-006`).
- **Acceptance criteria:**
  - [ ] UX-AC-012.1 — a token check computes contrast for all twelve months and fails the build if any pair drops below 4.5:1 (`DEC-050`)
  - [ ] UX-AC-012.2 — rollover to a new month changes colour only: no layout shift, no altered text, no moved control (CLS ≈ 0)
  - [ ] UX-AC-012.3 — the سنگ ماه album names all twelve **Gregorian** months (Farsi + Latin) and their stones from `design_system.md` §2.2, marks the current month with the text «این ماه», and gives no stone extra weight (`DEC-052`)
  - [ ] UX-AC-012.4 — with a grayscale filter on, every state on the homepage (stock, rate freshness, status) is still readable
  - [ ] UX-AC-012.5 — «سنگ این ماه» names the **Gregorian** month in Farsi and Latin («سپتامبر · September») and that month's stone, so an accent that changes mid-Jalali-month is still explained (`DEC-053`)
  - [ ] UX-AC-012.6 — the album and the chip are static and self-contained: no data call, no new route, no control, every tile legible with colour and images disabled, and the stone names can never drift from the reference table, the chip or the filter labels (`DEC-052`)
- **Related requirement:** `FR-CAT-1`, `FR-CAT-2`, `FR-PROD-1`, `DEC-050`, `DEC-051`, `DEC-052`, PRIN-3
- **Screens:** home, category, search (filter value)
- **Flows:** UF-01
- **Status:** proposed · **Wave:** W1

## 4. Global UX requirements

| ID | Requirement | Applies to | Verification |
|---|---|---|---|
| UX-G-001 | Every interactive element is keyboard reachable in a logical order | all screens | keyboard walkthrough |
| UX-G-002 | Every destructive action is confirmable and recoverable where feasible | all destructive controls | interaction review |
| UX-G-003 | User-visible errors state what happened and what to do next, in plain Farsi, without technical jargon | all error states | error-state sweep |
| UX-G-004 | Loading beyond ~300 ms shows progress; beyond ~10 s offers cancel/retry | all async actions | throttle test |
| UX-G-005 | Layout survives 320 px width and 200 % zoom without loss of function | all screens | viewport sweep |
| UX-G-006 | Colour is never the only carrier of meaning | all status indicators | contrast/vision check |
| UX-G-007 | No layout shift on font/image load | all screens | performance trace |
| UX-G-008 | RTL via logical properties only; no hard-coded left/right | all components | code review (`UX-AC-005.1`) |
| UX-G-009 | Bidi safety: order codes, prices, dates and mixed Latin tokens render unambiguously inside RTL text | all text surfaces | bidi test with real order code |
| UX-G-010 | Touch targets ≥ 44×44 CSS px on the storefront; ≥ 24×24 in admin (desktop mouse) | all controls | audit |
| UX-G-011 | Every informative image has Persian alt text; decorative images are hidden from assistive tech | all images | a11y scan |

## 5. Accessibility targets

| Concern | Target | Verified by |
|---|---|---|
| Standard | WCAG 2.1 AA as the floor ("AA-minded basics" per approved NFR-A11Y-1); 2.2 criteria adopted where they cost nothing | automated + manual sweep |
| Keyboard | every action reachable and operable | `visual_validation.md` §keyboard |
| Focus | visible focus indicator; focus moves predictably on navigation and dialogs | manual |
| Screen reader | names, roles, values; live-region announcements on async change; **tested with RTL content** (VoiceOver/NVDA on Persian) | manual + axe |
| Motion | `prefers-reduced-motion` respected | automated |
| Zoom/text | usable at 200 % zoom; no clipped Persian text (diacritics and descenders never clipped by line-height shortcuts) | manual |
| Forms | labels, error association, error summary — all in Farsi | manual |
| Contrast | ≥ 4.5:1 text, ≥ 3:1 large text/UI parts; jewellery photography may be light — text never sits on uncontrolled imagery without a scrim | automated per token |

## 6. UX constraints

| Constraint | Source | Consequence |
|---|---|---|
| Responsive web only — no native app in v1 | scope (`DEC-003`) | `UX-G-005` matters more; social-webview testing required |
| Farsi-only, RTL | `DEC-004` | PRIN-4, `UX-G-008/009`; no i18n machinery |
| No existing brand — identity is created in this phase | `DEC-035` | logo, palette, type ramp are UX deliverables (design_system.md) |
| Catalog includes silver bars (شمش), not only jewelry | `DEC-038` | bar items emphasise weight/purity; stone filters don't apply; photo setup differs (OQ-014) |
| The shop's speciality is moonstone (ماه‌سنگ)-set silver | `DEC-051` | homepage carries an evergreen ماه‌سنگ band; the stone filter gains a «ماه‌سنگ» value; photos must show the stone's blue sheen (photo guide §5.1) |
| Accent colour changes with the calendar month | `DEC-050` | tokens stay one-accent-at-a-time; visual baselines pin a month; no layout token may depend on the month |
| Visual direction: modern minimal | `DEC-035` | PRIN-3; tokens stay few; no ornamental noise |
| Reference patterns adapted from James Avery | `DEC-036` | storefront IA/merchandising patterns; everything re-derived for RTL + rate pricing |
| Storefront mobile-first; admin desktop-first | `DEC-037` | `UX-006` vs `UX-007`; admin phone support deferred (`§7`) |
| No product photos exist yet | OQ-014 | gallery/empty states must be designed; photo style guide goes to the owner before launch (SC-2) |
| Fonts not yet chosen — owner will test candidates | OQ-013 | design tokens carry a placeholder font stack; Vazirmatn is the working `[REC]` |
| Minimal costs posture | `DEC-030` | free/open fonts preferred; no paid stock assets in v1 |

## 7. Open UX questions

Tracked in `docs/project/open_questions.md` with type `ux` (or `product` where business-side).

| ID | Question | Blocks |
|---|---|---|
| OQ-013 | Which Persian web font(s) after the owner's test round? | design tokens, final typography (not flows/IA) |
| OQ-014 | Product photography: production plan, style, and schedule (none exist today) | SC-2, gallery realism, product-card art direction |
| OQ-015 | Accent month: calendar month (default) or the visitor's own birth month; owner pin? | design tokens §2.1, homepage stone chip, month resolver |
| OQ-016 | ماه‌سنگ scope: one stone value + filter option, a `/moonstone` landing page, or a full stone taxonomy | catalog attributes/filters, admin product form, IA/screens |
| UX-OPEN (unnumbered, minor) | Does P2 need admin on a phone (e.g., advancing orders on the go)? | admin responsive scope only |

## 8. Change log

| Date | Change | By | Reason |
|---|---|---|---|
| 2026-09-20 | initial draft — round 1 recorded: personas, principles PRIN-1…6, UX-001…009, globals, a11y, constraints | frontend-ux | visual direction, reference and platform split decided (`DEC-035`–`037`) |
| 2026-09-20 | round 2 recorded: UX-010 homepage merchandising, UX-011 featured design; scope clarification silver bars (`DEC-038`) | frontend-ux | homepage composition, rate chip, design-of-month adopted (`DEC-039`–`043`) |
| 2026-09-20 | round 3 defaults recorded (`DEC-044`–`049`); full spec completed: `screens.md` (25 screens), `design_system.md`, `interaction_patterns.md` | frontend-ux | human delegated all remaining round-3 choices; spec now in review before the `ux_approved` gate |
| 2026-09-21 | round 4 (owner-initiated): accent replaced by the **stone of the month** (`DEC-050`) and the ماه‌سنگ specialization specified — UX-012 added, UX-010 band position, OQ-015/016 opened | frontend-ux | owner asked for the birthstone accent and a homepage section for exploring moonstones |
| 2026-09-21 | round 5 (owner-initiated): **calendar switched to Gregorian** (`DEC-053`) — accent, chip and album keyed by the Gregorian month, Gregorian month named in Farsi + Latin, fallback ژانویه/گارنت, `UX-AC-012.3`/`UX-AC-012.5` reworded | frontend-ux | owner asked to show the stones on the Gregorian calendar |
| 2026-09-21 | round 5 (owner-initiated): the homepage stone section becomes the compact **سنگ ماه album** of all twelve months (`DEC-052`, superseding `DEC-051` clause a — band, copy and CTA removed) — UX-010/UX-012 wording, `UX-AC-010.5`, `UX-AC-012.3`, `UX-AC-012.6`; reference content added as `design_system.md` §2.2 | frontend-ux | owner asked for just the twelve month stones (current month highlighted, the rest selectable, nothing long) |
