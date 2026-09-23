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
| OQ-013 | Which Persian web font(s) does v1 use? (Owner will test candidates.) | ux | design tokens + final typography (not flows/IA) | human + frontend-ux | 2026-09-20 | open | Testing shortlist: Vazirmatn [REC], IRANSansX (licensed, paid), Estedad/Peyda (free) |
| OQ-014 | Product photography: who shoots the 50–200 launch items, in what style, by when? | product | SC-2 (fully listed catalog), gallery spec realism, product-card art direction | human | 2026-09-20 | open | No photos exist yet; style guide to be provided by frontend-ux (design_system.md) |
| OQ-015 | Does the monthly accent follow the calendar month (Gregorian, default) or each visitor's own birth month — and may the owner pin one stone? | ux | design tokens §2.1 (accent sets), homepage «سنگ این ماه» chip, month resolver | human + frontend-ux | 2026-09-21 | open | `DEC-050` ships the calendar-month reading, on the Gregorian calendar since `DEC-053`; per-visitor personalisation needs a decision (storage, first-paint flash, no-JS behaviour) |
| OQ-016 | How far does the ماه‌سنگ specialization go — one stone value plus a filter option, or a dedicated landing page plus a real stone taxonomy (stone types, counts, sizes) on products? | product | catalog attributes/filters, admin product form, IA and screens, `DEC-051` clause (b) | human | 2026-09-21 | open | v1 default: one stone value «ماه‌سنگ» + filter option (the homepage band of `DEC-051` clause a was superseded by the `DEC-052` album, which is informational only); a wider taxonomy is a requirement change |
| OQ-017 | Container registry & CI deploy path to the Iranian VPS: is a registry reachable from Iran, or do images build on the server? Which CI runner deploys (GitHub-hosted cannot reach the box)? | architecture (ops) | `OPS` deploy pipeline, CI credentials, rollback procedure (`ADR-003`) | human + architecture | 2026-09-21 | open | Default assumption until answered: build on the server (`git pull` + `docker compose build`), CI runs tests only — works everywhere, loses image-based rollback; a reachable registry restores `pull && up -d` deploys |
| OQ-018 | Which domestic SMTP/email provider sends order/status email, and what are its limits? | architecture (`ADR-008`) | `NOTIFY` transport config, retry/backoff tuning, buyer-email copy tests | human | 2026-09-21 | open | `NOTIFY` is transport-agnostic SMTP; provider named at launch; SMS stays out of v1 (`OQ-019`) |
| OQ-020 | Off-box backup copy: which object storage (or documented manual download routine) holds the nightly `pg_dump`? | architecture (ops) | disaster recovery, release drill (`ADR-003`, DoD L4) | human | 2026-09-21 | open | Today: on-box dumps (14-day retention) + pre-deploy snapshots; an off-box copy is the missing piece for a dead-VPS scenario |
| OQ-021 | Domain, DNS and TLS provider (domestic; is Let's Encrypt reachable?) and the owner's TOTP device for admin | architecture (ops) | `OPS` Caddyfile config, launch readiness, admin login hardening (`ADR-005`) | human | 2026-09-21 | open | Caddy automation assumed; if LE is unreachable, fall back to a domestic CA/manual cert — one config change |

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

### OQ-013 — Persian web font selection
- **Asked by:** frontend-ux (UX round 1)
- **Context:** Farsi-native typography (PRIN-4) needs a font with excellent screen
  legibility, full Persian glyph coverage, and multiple weights. DEC-030 (minimal costs)
  biases toward free fonts; the owner wants to test candidates before committing.
- **Options:**
  1. Vazirmatn — free/open, variable weights, excellent UI legibility `[REC]`
  2. IRANSansX family — the market's de-facto commercial standard, licensed (paid)
  3. Estedad / Peyda — free/open alternatives worth a side-by-side
- **Recommendation:** `[REC]` test Vazirmatn vs IRANSansX vs Estedad on real product data;
  default to Vazirmatn unless the licensed option visibly wins.
- **Impact:** design tokens, headings/body ramp, price/numeral rendering; does **not** block
  flows, IA or screens.
- **Answer:** —

### OQ-014 — Product photography production plan
- **Asked by:** frontend-ux (UX round 1) — **owner confirmed no product photos exist**
- **Context:** SC-2 requires every launch item listed with photo(s) within 90 days of
  launch; FR-PROD-1/FR-ADM-1 need multi-photo galleries; product-card and gallery art
  direction depend on a consistent photo style (modern minimal, DEC-035).
- **Options:**
  1. Owner shoots everything on a simple consistent setup (light box/neutral background) —
     cheapest; frontend-ux provides a one-page style guide.
  2. Professional photographer for hero categories, owner shoots the rest — costs money
     (DEC-030 tension), best first impression.
- **Recommendation:** `[REC]` option 1 for v1 (consistent neutral background, ≥ 3 photos per
  product per FR-ADM-1); style guide delivered with the design system.
- **Impact:** SC-2, gallery empty states, admin upload UX, launch readiness.
- **Answer:** —

### OQ-015 — Whose month drives the accent?
- **Asked by:** frontend-ux (`DEC-050` implementation) — **owner asked for a stone-of-the-month accent**
- **Context:** `DEC-050` themes the storefront with the current **Gregorian** month's birthstone colour (`DEC-053`).
  The obvious extension is personalisation: show a visitor the stone of *their* birth month (a small
  «ماه تولد شما؟» selection, stored locally). That changes the resolver (visitor state instead of the
  calendar), the first paint (possible flash or a client-only accent) and the no-JS/SEO rendering,
  so it cannot be assumed.
- **Options:**
  1. Calendar month only, no personalisation `[REC]` — one accent per render, trivially cacheable,
     zero privacy surface.
  2. Calendar month by default **plus** an optional visitor picker that switches the accent and the
     homepage chip until the browser is cleared — warmer, but needs a pre-paint script and a
     "why did the colour change?" explainer.
  3. Owner-pinned stone (a single accent chosen in admin instead of a monthly cycle) — calmest, but
     loses the monthly narrative and the moonstone season.
- **Prototype (option 2, built for review — not a decision):** `docs/ux/style_tile.html` now carries a
  working picker («ماه تولد شما (اختیاری)» + «پاک‌کردن») and behaves like the shipped version would:
  * **priority** `?month=` (review/owner pin) → stored birth month → Gregorian calendar month, with
    the resolution source written to `data-month-source` on `<html>` and named in the UI, so a
    reviewer can always see *why* this colour is showing;
  * **no flash by construction** — the tokens and the resolver sit in an inline script in `<head>`
    that sets a colour-only inline style on `<html>` before the body exists; the body script only
    updates labels. Verified against the artifact (stored month → correct accent on first paint,
    no layout change);
  * **storage** is `localStorage` key `noghre.birthMonth` only — never a cookie, never sent to the
    server, wrapped in `try/catch` so private mode just falls back to the calendar month;
  * **no-JS / cleared storage / server render** all land on the calendar month, which is also the
    `:root` fallback (`ژانویه · گارنت` if nothing resolves at all);
  * **the «این ماه» marker in the album always follows the calendar**, never the preference — the
    season is still the calendar's even when the visitor wears their own stone.
- **Open sub-questions the prototype exposes (needed before this can be accepted):**
  1. Where does the control live — beside the album tiles, a header chip, or a first-visit prompt?
     (The prototype puts it in the accent section of the style tile, which is not a storefront
     screen.)
  2. Does HTML caching stay safe? The server renders the calendar month and the script overrides it,
     so a cached page is still correct for every visitor — confirm before shipping.
  3. Do we explain a *second* time when the visitor's month differs from the calendar's (two stones
     on screen: chip + album marker)? The prototype copies that burden onto the chip wording and the
     source line.
  4. Analytics/telemetry: none in the prototype; decide whether a bare, non-identifying counter of
     «picker used» is acceptable (PRIN-6 keeps it optional).
- **Impact:** design tokens §2.1/§7 (prototype-tagged), homepage chip and album, month resolver,
  caching, visual baselines, privacy note in the footer.
- **Answer:** —

### OQ-016 — Scope of the ماه‌سنگ specialization
- **Asked by:** frontend-ux (`DEC-051`)
- **Context:** the ماه‌سنگ pieces need real product paths. `DEC-051` clause (b) adds one product
  value («ماه‌سنگ») on top of the existing stone/no-stone attribute, and the homepage stone album
  (`DEC-052`) is informational only — no tile is clickable in the storefront — so the speciality's
  traffic has to come from the filter and product pages. A real gemstone taxonomy (stone type, stone
  count/size, per-stone collections, a `/moonstone` landing page) is a much larger catalog and admin
  change — and gemstone inventory depth is a supply question only the owner can answer.
- **Options:**
  1. v1 as specified `[REC]` — one «ماه‌سنگ» value plus the stone filter option (no homepage CTA
     after `DEC-052`); revisit after launch with real demand data.
  2. Add a `/moonstone` collection page now (hero, education, grid, FAQ) and link it from the stone
     filter and the ژوئن album tile — stronger storefront storytelling, one more screen and IA
     change, and the only way an album tile becomes actionable.
  3. Full stone taxonomy (multiple stone types + stone fields on products + per-stone collections) —
     best long-term catalog, largest v1 cost and the most admin burden on a non-technical owner
     (PRIN-6).
- **Impact:** catalog attributes, admin product form, filters, IA/sitemap, screens, SEO surface.
- **Answer:** —

### OQ-017 — CI → VPS deploy path (registry reachability from Iran)
- **Asked by:** architecture (`ADR-003`) — **owner decision (cost/ops implication)**
- **Context:** the approved hosting is one domestic VPS running Docker Compose. Image-based deploys
  (`docker compose pull && up -d`) need a container registry reachable **from Iran**; GitHub-hosted CI
  runners also cannot reach the box for a deploy job. The two defaults disagree, so the pipeline shape
  must be chosen before the `OPS` module is contracted.
- **Options:**
  1. Build on the server (`git pull` + `docker compose build`) `[REC]` — works with any host, zero extra
     services; costs build minutes on the box and weakens rollback to "previous git tag rebuild".
  2. Domestic container registry (if the host offers one) — restores pull-based deploys and clean
     rollback; adds a service account and a small cost.
  3. Self-hosted CI runner on the VPS (GitHub Actions runner) — pull-based deploys from existing CI;
     runs workloads on the production box (isolation must be reviewed).
- **Impact:** `OPS` contract, CI workflows (shared zone), secrets, rollback procedure, release drill.
- **Answer:** —

### OQ-018 — Domestic SMTP/email provider for order and status email
- **Asked by:** architecture (`ADR-008`)
- **Context:** `DEC-021` requires email notifications where the buyer gave an address. The transport is
  provider-agnostic SMTP behind the outbox, but the provider (and its sending limits/spam reputation)
  affects retry tuning and whether buyer email is reliable enough to promise.
- **Options:** owner names a domestic provider at launch; v1 ships with SMTP config + sandbox-safe
  behaviour either way.
- **Impact:** `NOTIFY` config, failure drill, admin failure panel expectations.
- **Answer:** —

### OQ-020 — Off-box backup copy for the nightly `pg_dump`
- **Asked by:** architecture (`ADR-003`)
- **Context:** backups currently live on the same VPS (14-day retention + pre-deploy snapshots). A dead
  VPS then loses both the data and the backups. An off-box copy (domestic object storage, or a
  documented manual download routine the owner actually performs) closes that hole but needs a decision
  and possibly a small cost.
- **Options:**
  1. Domestic object storage bucket, nightly upload from the worker `[REC]` — automated, small cost.
  2. Documented manual routine (owner downloads weekly, verified by a checklist) — free, depends on
     discipline (`NFR-MAINT-1` risk).
- **Impact:** release drill (DoD L4), disaster recovery story, worker job list.
- **Answer:** —

### OQ-021 — Domain, DNS/TLS provider and admin TOTP device
- **Asked by:** architecture (`ADR-003`, `ADR-005`)
- **Context:** Caddy automates Let's Encrypt certificates, but reachability of LE from the domestic host
  (and the DNS provider's compatibility) must be confirmed; the admin login recommends TOTP, which needs
  the owner to have/choose an authenticator app.
- **Options:** owner picks the registrar/DNS; fallback if LE is unreachable = manual certificate from a
  domestic CA (one Caddyfile change).
- **Impact:** launch readiness, `OPS` config, admin hardening.
- **Answer:** —
