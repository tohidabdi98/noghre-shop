# Screens

> Owned by the Frontend/UX Agent. The **screen inventory** plus a specification per screen. A
> screen is specified *before* it is implemented; the implementation agent gets the screens its
> module contract references (`ux_refs`) and nothing else.
>
> Every screen specification covers: default, loading, empty, error, success and
> permission-denied states, responsive behaviour, and the keyboard path.
>
> **Modules are `TBD` until M2 decomposition** — the Module column binds to real module IDs then.
> **Waves:** W1 = storefront core (launch-critical) · W2 = accounts + admin (owner tooling).

## 1. Screen inventory

| ID | Screen | Route | Module | Flows | Priority | Wave | Status | Visual validation |
|---|---|---|---|---|---|---|---|---|
| SCR-001 | Home (خانه) | `/` | TBD | UF-01 | must | W1 | specified | pending |
| SCR-002 | Category (دسته) | `/category/:slug` | TBD | UF-01 | must | W1 | specified | pending |
| SCR-003 | Search results (جست‌وجو) | `/search` | TBD | UF-01 | must | W1 | specified | pending |
| SCR-004 | Product (محصول) | `/product/:slug` | TBD | UF-01, UF-02 | must | W1 | specified | pending |
| SCR-005 | Cart (سبد خرید) | drawer + `/cart` | TBD | UF-02 | must | W1 | specified | pending |
| SCR-006 | Checkout (تکمیل خرید) | `/checkout` | TBD | UF-02 | must | W1 | specified | pending |
| SCR-007 | Payment step (پرداخت) | `/checkout/pay` | TBD | UF-02 | must | W1 | specified | pending |
| SCR-008 | Order confirmation | `/order/:code` | TBD | UF-02, UF-03 | must | W1 | specified | pending |
| SCR-009 | Track order (پیگیری سفارش) | `/track` | TBD | UF-03 | must | W1 | specified | pending |
| SCR-010 | Policy pages (برگه‌های اطلاعاتی) | `/pages/:slug` | TBD | UF-01, UF-02 | must | W1 | specified | pending |
| SCR-011 | Not found (۴۰۴) | catch-all | TBD | — | must | W1 | specified | pending |
| SCR-012 | Login (ورود) | `/login` | TBD | — | should | W2 | specified | pending |
| SCR-013 | Register (ساخت حساب) | `/register` | TBD | — | should | W2 | specified | pending |
| SCR-014 | Account home (حساب من) | `/account` | TBD | UF-03 A1 | should | W2 | specified | pending |
| SCR-015 | Order history (سفارش‌های من) | `/account/orders` | TBD | UF-03 A1 | should | W2 | specified | pending |
| SCR-016 | Admin login | `/admin/login` | TBD | UF-04 | must | W2 | specified | pending |
| SCR-017 | Admin overview (نمای کلی) | `/admin` | TBD | UF-04 | must | W2 | specified | pending |
| SCR-018 | Admin orders (سفارش‌ها) | `/admin/orders` | TBD | UF-04 | must | W2 | specified | pending |
| SCR-019 | Admin order detail | `/admin/orders/:id` | TBD | UF-04 | must | W2 | specified | pending |
| SCR-020 | Admin products (محصولات) | `/admin/products` | TBD | UF-04 A1 | must | W2 | specified | pending |
| SCR-021 | Admin product form | `/admin/products/new`, `/admin/products/:id` | TBD | UF-04 A1 | must | W2 | specified | pending |
| SCR-022 | Admin daily rate (نرخ روز) | `/admin/rate` | TBD | UF-04 | must | W2 | specified | pending |
| SCR-023 | Admin promos (کدهای تخفیف) | `/admin/promos` | TBD | — | must | W2 | specified | pending |
| SCR-024 | Admin pages + hero (برگه‌ها) | `/admin/pages` | TBD | — | must | W2 | specified | pending |
| SCR-025 | Admin featured design (طرح ماه) | `/admin/featured` | TBD | UF-04 | must | W2 | specified | pending |

Status: `placeholder` · `specified` · `implemented` · `validated` · `needs-revision`.
Visual validation results are recorded in the QA validation artifact during implementation waves (created at the validation stage).

## 2. Screen specification format

```text
SCR-<id> — <screen name>
  Route:            /<path>
  Module:          <MODULE-ID>          (sole owner, TBD until decomposition)
  Flows:           UF-##
  Requirements:    FR-###, UX-###
  Entry points:    how the user gets here
  Exit points:     where they go next
  Primary action:  exactly one
  Secondary actions:
```

Each spec then covers: layout regions · content and controls · states (default / loading /
empty / error / success / permission-denied) · responsive behaviour · keyboard and focus ·
accessibility · content copy · acceptance criteria.

### 2.1 Standard evidence (applies to every screen)

- [ ] screenshots at 3 widths (≥1280, 768–1279, <768) in the default state
- [ ] screenshots of loading / empty / error / success (+ permission-denied where applicable)
- [ ] keyboard-only walkthrough notes
- [ ] automated accessibility scan (axe or equivalent), zero critical findings
- [ ] Frontend/UX Agent sign-off recorded in the PR

Per-screen specs add only screen-specific acceptance criteria; the shared evidence set is not
repeated below.

## 3. Storefront screens — W1

### SCR-001 — Home / خانه

**Route** `/` · **Module** TBD · **Flows** UF-01 · **Reqs** `FR-CAT-1`, `UX-010`, `UX-011`, `UX-012`, `UX-001`, `DEC-039`, `DEC-047`, `DEC-049`, `DEC-050`, `DEC-052`
**Entry** direct/shared/social links · logo · footer links. **Exit** category tile · featured design · product card · search · track · policies.
**Primary action** open a category or product. **Secondary** search, rate chip (informational), featured design.

**Layout regions**

| Region | Content | At small widths |
|---|---|---|
| header | logo · categories ▾ · search · track · account · cart (count) | hamburger drawer + persistent cart icon (`DEC-040`) |
| main | hero → category tiles → rate chip + سنگ این ماه chip → featured design (when set) → product row → سنگ ماه album (دوازده ماه) → trust row → story | single column; hero mobile crop; tiles 2-up; album 4-up → 3-up → 2-up |
| footer | policy pages, track order, account | link list (accordion) |

**Content and controls**

| Element | Type | Data | Empty behaviour | Error behaviour |
|---|---|---|---|---|
| hero | image + one line + CTA «دیدن محصولات» | owner content (`DEC-047`); default when unset | default hero renders | text-only hero, no image |
| category tiles | 2-col/7-up grid of taxonomy tiles | categories (`DEC-023`, `DEC-038`) | tiles still link; category shows its own empty state | section → plain text links |
| rate chip | small text line | latest rate + date | hidden entirely when no rate was ever entered | hidden on fetch error |
| featured design | image + name + «مشاهده» | owner pick (`DEC-043`) | slot hidden | slot hidden |
| product row | 4/3/2-up product cards | newest items, then bestsellers once paid orders exist (`DEC-049`) | row hidden when catalog empty (note «اولین محصولات به‌زودی») | section retry |
| سنگ این ماه chip | small text chip next to the rate chip | current **Gregorian** month's stone (`DEC-050`, `DEC-053`) | month unresolvable → fallback stone name (ژانویه · گارنت) | renders the fallback name |
| سنگ ماه album | labelled section: h2 «سنگ ماه» + twelve compact tiles — decorative swatch (`aria-hidden`), «{ماه میلادی} · {Month}», stone name in Farsi + Latin; the current Gregorian month's tile carries the text «این ماه» | static content from `design_system.md` §2.2 (`DEC-052`) — no query, no catalogue dependency, no copy to edit | never empty (static); nothing to hide | part of the page frame — cannot fail |
| trust row | 3 icon+text lines | static defaults (`DEC-048`) | never empty | — |
| story block | heading + short text | default copy in v1 (editable is a change-request candidate) | never empty | — |

**States**

| State | Trigger | Appearance | Actions | A11y |
|---|---|---|---|---|
| default | data loaded | all blocks in the accepted order | navigate | h1 hero; h2 per block |
| loading | sections in flight | per-block skeletons matching layout | — | `aria-busy` per section |
| empty | zero products | hero/tiles/album/trust/story render; product row hidden | browse categories | announced |
| error | a section fails | only that section (products or featured) shows a retry line; page frame intact | retry section | `role="alert"` (polite) |
| success | — | n/a (browsing has no terminal success) | — | — |
| permission-denied | — | n/a (public) | — | — |

**Responsive** ≥1280: 4-up tiles/products, full hero, album 4-up · 768–1279: 3-up, album 3-up · <768: 2-up, mobile hero crop, rate chip + سنگ این ماه chip directly under hero, album 2-up (tiles shrink, text never truncates).

**Keyboard & focus** skip-link → header → hero CTA → tiles → featured → products → footer; cards are single focusable links (Enter opens); the album adds no control of its own, so tabbing past it costs nothing; no traps on this screen.

**A11y** landmarks header/main/footer; featured slot and the سنگ ماه album are labelled sections with headings; each album tile states month and stone (Farsi + Latin) as real text, the swatch is `aria-hidden`, and the current month is marked by the text «این ماه», so nothing depends on a colour (`UX-G-006`); rate chip and سنگ این ماه chip are real text ≥ 4.5:1; white text on the monthly accent stays ≥ 4.5:1 in all twelve sets (`DEC-050`); Persian alt text on all photos (`UX-G-011`); zero layout shift — a month rollover changes colour only (`UX-G-007`).

**Copy**

| Element | Copy |
|---|---|
| title | «نقره‌شاپ — نقرهٔ خالص» |
| hero default | «نقرهٔ خالص، ساده و ماندگار» · CTA «دیدن محصولات» |
| rate chip | «نرخ نقره: {مبلغ} تومان/گرم · {تاریخ}» · stale suffix «(آخرین نرخ ثبت‌شده)» |
| سنگ این ماه chip | «سنگ این ماه: {نام سنگ} — {ماه میلادی}» — مثال: «سنگ این ماه: یاقوت کبود — سپتامبر» |
| album heading | «سنگ ماه» |
| album legend | «سنگ ماه تولد هر ماه میلادی؛ سنگ ماه جاری برجسته است.» |
| album tile | «{ماه میلادی} · {Month}» + «{سنگ} · {stone}» — مثال: «ژوئن · June» + «مروارید و ماه‌سنگ · pearl & moonstone» |
| album current marker | «این ماه» (فقط روی کارت ماه جاری) |
| trust row | «ارسال به سراسر کشور» · «ضمانت بازگشت» · «پرداخت امن آنلاین» |
| section error | «این بخش بارگذاری نشد؛ دوباره تلاش کنید.» |

**Acceptance criteria**

- [ ] SCR-001-AC1 — the six fixed blocks render in the accepted order at 3 widths (hero, tiles, product row, سنگ ماه album, trust row, story); the featured slot sits between tiles and product row when set (`UX-AC-010.1`)
- [ ] SCR-001-AC2 — rate chip shows rate + date, or hides when no rate ever entered (`UX-AC-010.2`)
- [ ] SCR-001-AC3 — no empty featured slot renders when unset (`UX-AC-010.3`)
- [ ] SCR-001-AC4 — each block fails independently; one broken section never blanks the page (`UX-AC-010.4`)
- [ ] SCR-001-AC5 — any starter category reachable in 1 tap (`UF-01-AC1`)
- [ ] SCR-001-AC6 — the سنگ ماه album renders in its accepted position at all three widths with all twelve **Gregorian** months, each tile naming the month in Farsi + Latin and the stone in Farsi + Latin; the current month's tile carries the text «این ماه» and no stone is singled out (`UX-AC-010.5`, `UX-AC-012.6`, `DEC-052`)
- [ ] SCR-001-AC7 — the album is static: no data call, no new route, no control and no link of its own, and every tile stays readable with colour and images disabled (`DEC-052`)
- [ ] SCR-001-AC8 — the سنگ این ماه chip names the **Gregorian** month in Farsi (and Latin) and the month's stone, and the accent matches that stone's token set (`UX-AC-012.5`, `DEC-053`)
- [ ] SCR-001-AC9 — the homepage's twelve stone tiles and the chip agree with `design_system.md` §2.2 for the same month (one source, no drift) (`DEC-052`)

---

### SCR-002 — Category / دسته

**Route** `/category/:slug` · **Module** TBD · **Flows** UF-01 · **Reqs** `FR-CAT-1`, `FR-CAT-2`, `UX-001`, `UX-006`
**Entry** home tiles · header/drawer menu · search suggestions · shared links. **Exit** product · other categories · search.
**Primary action** open a product. **Secondary** filter, sort, clear filters, switch category.

**Layout regions**

| Region | Content | At small widths |
|---|---|---|
| header | global | drawer |
| main | breadcrumb (خانه / {دسته}), h1 = category label, result count, product grid | single column, filter button above grid |
| filters | price range (min/max), weight range, stone (همه/ماه‌سنگ/با سنگ/بدون سنگ), sort | bottom sheet, focus-trapped |

**Content and controls**

| Element | Type | Data | Empty behaviour | Error behaviour |
|---|---|---|---|---|
| product card | link: photo (1:1), name, price + rate date, stock badge | catalog | — | grid section retry |
| filter controls | min/max number inputs (قیمت، وزن), segmented stone («همه / ماه‌سنگ / با سنگ / بدون سنگ», `DEC-051`), sort select | `FR-CAT-2` | — | invalid range → inline error, filters not applied |
| active filter chips | removable chips, «پاک کردن فیلترها» | URL state | hidden when none | — |
| pagination | «نمایش بیشتر» button (24/page) | — | hidden when all shown | retry line |

**States**

| State | Trigger | Appearance | Actions | A11y |
|---|---|---|---|---|
| default | loaded | grid + filters; URL carries state | open product, filter | result count announced politely |
| loading | fetch | skeleton grid matching card size | — | `aria-busy` |
| empty (category) | zero products | «هنوز محصولی در این دسته نیست…» + other category links | browse | announced; focus to heading |
| empty (filters) | filters exclude all | «با این فیلترها محصولی پیدا نشد…» + clear action | clear filters | announced |
| error | fetch fails | section message + retry; URL preserved | retry | `role="alert"` |
| success | — | n/a | — | — |
| permission-denied | — | n/a (public) | — | — |

**Responsive** ≥1280: 4-up, filters in side rail · 768–1279: 3-up, collapsible rail · <768: 2-up, filters in bottom sheet (returns focus to trigger).

**Keyboard & focus** cards tabbable in visual order; sheet traps focus, `Esc` closes, focus returns to the filter button; filter changes announce new count.

**A11y** h1 = category; price + rate date readable as one statement (`UX-AC-001.3`); stock badge is text, not colour-only; targets ≥ 44 px mobile.

**Copy**

| Element | Copy |
|---|---|
| title | {نام دسته} |
| count | «{n} محصول» |
| empty (category) | «هنوز محصولی در این دسته نیست؛ دسته‌های دیگر را ببینید.» |
| empty (filters) | «با این فیلترها محصولی پیدا نشد؛ فیلترها را پاک کنید.» |
| stock badge | «موجود» / «ناموجود» |

**Acceptance criteria**

- [ ] SCR-002-AC1 — price + rate date visible on every card (`UX-AC-001.1`)
- [ ] SCR-002-AC2 — filters combine with the category and live in a shareable URL (`UF-01-AC3`)
- [ ] SCR-002-AC3 — both empty variants render with their recovery action
- [ ] SCR-002-AC4 — filter sheet, chips and sort fully keyboard-operable
- [ ] SCR-002-AC5 — the «ماه‌سنگ» stone option yields a shareable URL (`?stone=moonstone`) and lists only tagged items (`DEC-051`)

---

### SCR-003 — Search results / جست‌وجو

**Route** `/search?q=&price_min=&price_max=&weight=&stone=&sort=` · **Module** TBD · **Flows** UF-01 · **Reqs** `FR-CAT-2`, `UX-006`
**Entry** header search (dedicated results page, no typeahead `DEC-040`), shared links. **Exit** product · category · refined search.
**Primary action** open a product. **Secondary** refine query, browse suggested categories.

**Layout regions** header (search field prefilled) · main (h1 «نتایج جست‌وجو» + same grid/filters as SCR-002) · footer.

**Content and controls** search field (prefilled, editable, submits on Enter) · same product grid and filter controls as SCR-002, including the «ماه‌سنگ» stone value (`DEC-051`) · suggested category chips on empty.

**States**

| State | Trigger | Appearance | Actions | A11y |
|---|---|---|---|---|
| default | results | grid | as SCR-002 | count announced |
| loading | fetch | skeleton grid | — | `aria-busy` |
| empty | no match | message + suggested categories | edit query, open category | focus to heading |
| error | fetch fails | retry preserving `q` | retry | `role="alert"` |
| success | — | n/a | — | — |
| permission-denied | — | n/a (public) | — | — |

**Responsive / keyboard / a11y** as SCR-002; search field is first in main's tab order.

**Copy**

| Element | Copy |
|---|---|
| title | «نتایج جست‌وجو» |
| empty | «چیزی برای «{q}» پیدا نشد؛ عبارت دیگری را امتحان کنید یا دسته‌ها را ببینید.» |
| placeholder | «جست‌وجو در محصولات» |

**Acceptance criteria**

- [ ] SCR-003-AC1 — query and filters survive reload and are shareable (URL state)
- [ ] SCR-003-AC2 — empty state suggests categories and keeps the query editable

---

### SCR-004 — Product / محصول

**Route** `/product/:slug` · **Module** TBD · **Flows** UF-01 (A1 deep link), UF-02 · **Reqs** `FR-PROD-1`, `BR-4`, `UX-001`, `UX-008`
**Entry** cards · shared/social links (primary social path) · search. **Exit** cart drawer · category · policies (footer).
**Primary action** «افزودن به سبد خرید». **Secondary** gallery browse/zoom, category link, track order.

**Layout regions**

| Region | Content | At small widths |
|---|---|---|
| header | global | drawer |
| main | gallery (multi-photo `DEC-022`) | swipeable gallery, thumbs below |
| info panel | name, price block, weight, stone, description, availability, CTA | stacks under gallery |

**Content and controls**

| Element | Type | Data | Empty behaviour | Error behaviour |
|---|---|---|---|---|
| gallery | main image + thumbs, pinch/zoom dialog | product photos | single-photo products show no thumb strip | broken image → neutral placeholder |
| price block | amount + basis «وزن × نرخ روز + اجرت» + rate date | rate + weight + fee (`BR-4`) | no rate ever → not buyable + message | stale → last-known + note (`UX-001`) |
| attributes | weight (گرم), stone (دارد/ندارد), description | product | — | — |
| availability | text badge | stock (`BR-1`) | out of stock → «ناموجود» with disabled CTA | reserve-held → same + note |
| add-to-cart | primary button | — | disabled with reason | — |
| zoom dialog | fullscreen image viewer | — | — | — |

**States**

| State | Trigger | Appearance | Actions | A11y |
|---|---|---|---|---|
| default | loaded, buyable | gallery + info + active CTA | add to cart | price+date announced together |
| loading | fetch | gallery + text skeletons | — | `aria-busy` |
| empty | invalid slug | 404 screen (SCR-011) | — | — |
| error | fetch fails | message + retry, frame intact | retry | `role="alert"` |
| success | add to cart | drawer opens with the line | continue shopping / checkout | toast + drawer announced |
| permission-denied | — | n/a (public) | — | — |
| out-of-stock | owner-set or reserved by other checkout | «ناموجود» + reserved note when held | view only | text not colour |
| no-rate-ever | no rate entered (`FR-RATE-1`) | CTA disabled + explanation | — | message associated with CTA |
| stale-rate | rate date ≠ today | buyable; price + last-known date + note | add to cart | note read with price |

**Responsive** ≥1280: gallery and info side by side, sticky CTA · <768: stacked, sticky bottom add-to-cart bar (touch target ≥ 44 px).

**Keyboard & focus** thumbs roving tabindex; zoom dialog traps focus, `Esc` closes, returns to the zoom trigger; CTA reachable in order.

**A11y** images have Persian alt; price basis and rate date are real text; zoom dialog labelled; reduced motion respected.

**Copy**

| Element | Copy |
|---|---|
| CTA | «افزودن به سبد خرید» |
| out of stock | «ناموجود» |
| reserved note | «این قطعه همین حالا در حال خرید است؛ کمی بعد دوباره سر بزنید.» |
| no rate | «قیمت‌گذاری در انتظار ثبت نرخ روز است؛ به‌زودی می‌توانید این قطعه را بخرید.» |
| basis line | «وزن {وزن} گرم × نرخ روز + اجرت» |
| added | «به سبد خرید افزوده شد.» |

**Acceptance criteria**

- [ ] SCR-004-AC1 — gallery supports all photos with swipe and keyboard access, no layout shift (`UX-AC-006.2`)
- [ ] SCR-004-AC2 — price block always shows amount + basis + rate date (`UX-AC-001.1`)
- [ ] SCR-004-AC3 — out-of-stock and no-rate states block adding with a Farsi reason (`UX-AC-008.1`)
- [ ] SCR-004-AC4 — deep-linked social entry renders fully on mobile in < 3 s (`UX-006`)

---

### SCR-005 — Cart / سبد خرید

**Route** drawer (primary surface) + `/cart` (keyboard/shareable equivalent) · **Module** TBD · **Flows** UF-02 · **Reqs** `FR-CART-1`, `UX-008`, `UX-001`
**Entry** add-to-cart (auto-open) · header cart icon · `/cart` link · post-add toast. **Exit** checkout · continue shopping.
**Primary action** «تکمیل خرید». **Secondary** edit quantity, remove line, continue shopping.

**Layout regions**

| Region | Content | At small widths |
|---|---|---|
| drawer | slides in from inline-end (left in RTL), focus-trapped | full-width sheet |
| lines | photo, name, unit price + rate date, qty stepper, line total, remove | stacked line layout |
| summary | «جمع سبد (بر پایه نرخ {تاریخ})» + CTAs | summary above CTAs |

**Content and controls**

| Element | Type | Data | Empty behaviour | Error behaviour |
|---|---|---|---|---|
| line item | row with qty stepper (max = stock) | cart state (per browser) | — | stock changed → flagged state |
| flagged line | warning row | live stock (`BR-1`) | — | blocks checkout, names the item |
| remove | text button + undo toast (5 s) | — | — | — |
| totals | estimate at current rate + rate date | rate | — | price refresh failed → last-known + note |
| checkout CTA | primary | — | disabled while a line is flagged, with reason | — |

**States**

| State | Trigger | Appearance | Actions | A11y |
|---|---|---|---|---|
| default | items present | lines + totals + CTA | checkout, edit, remove | drawer announced on open |
| loading | price refresh | inline shimmer on totals only | — | polite |
| empty | no items | «سبد خرید شما خالی است.» + «دیدن محصولات» | browse | announced |
| error | price refresh fails | last-known totals + note; checkout allowed | retry, continue | `role="alert"` |
| success | removal | line gone + undo toast | undo (5 s) | toast polite, pausable |
| permission-denied | — | n/a (public) | — | — |

**Responsive** drawer at all widths (`DEC-041`); `/cart` page: 2 columns ≥1280, single column below.

**Keyboard & focus** drawer traps focus, `Esc` closes, returns focus to trigger; stepper operable by arrows; `/cart` page is the complete no-drawer path; totals announced after change.

**A11y** flagged state is text + icon (not colour-only); qty controls labelled «کاهش/افزایش تعداد»; CTA states why it is disabled.

**Copy**

| Element | Copy |
|---|---|
| title | «سبد خرید» |
| empty | «سبد خرید شما خالی است.» · «دیدن محصولات» |
| estimate | «جمع سبد (بر پایه نرخ {تاریخ})» |
| flagged | «این محصول دیگر موجود نیست؛ برای ادامه آن را از سبد بردارید.» |
| removed | «از سبد حذف شد» + «بازگرداندن» |
| CTA | «تکمیل خرید» · «ادامه خرید» |

**Acceptance criteria**

- [ ] SCR-005-AC1 — cart persists per browser; abandoning loses nothing (`UF-02-AC4`)
- [ ] SCR-005-AC2 — a now-unavailable line blocks checkout and names the item (`UX-AC-008.2`)
- [ ] SCR-005-AC3 — totals always carry the rate date they are based on (`UX-AC-001.1`)
- [ ] SCR-005-AC4 — drawer and page are equivalent in function and both fully keyboard-operable

### SCR-006 — Checkout / تکمیل خرید

**Route** `/checkout` · **Module** TBD · **Flows** UF-02 · **Reqs** `FR-CHK-1`, `FR-PROMO-1`, `BR-1`, `DEC-013`, `DEC-014`, `DEC-020`
**Entry** cart CTA. **Exit** payment step (SCR-007) · back to cart.
**Primary action** «ادامه و پرداخت». **Secondary** apply promo code, edit cart, return to cart.

**Layout regions**

| Region | Content | At small widths |
|---|---|---|
| header | global (reduced to logo + back to cart) | same |
| form | contact → address sections, single column | single column, always |
| summary | items, totals, promo, rate note | sticky-block above the pay button |

**Content and controls**

| Element | Type | Data | Empty behaviour | Error behaviour |
|---|---|---|---|---|
| name / phone / address | text, tel (dir=ltr, inputmode=numeric), textarea | buyer input | — | inline error; nothing lost |
| email (optional) | email field, labelled «اختیاری» | buyer input | — | inline error |
| promo | labelled collapsible: input + «اعمال»; applied state = chip + «حذف» | `FR-PROMO-1` | collapsed by default | rejected → inline reason, total unchanged |
| totals | «جمع اقلام» · «تخفیف» · «مبلغ نهایی» + rate note | rate (`BR-4`) | — | — |
| reservation note | informational line | `DEC-013` | — | expired → explicit state + re-checkout path |

**States**

| State | Trigger | Appearance | Actions | A11y |
|---|---|---|---|---|
| default | cart valid | form + summary; reservation active | fill, pay | errors summary focusable |
| loading | submit in flight | button loading, form stays editable-blocked | — | `aria-busy` |
| empty | cart empty/flagged | blocked page: explanation + «بازگشت به فروشگاه» | back, remove flagged item | announced |
| error | submit fails / validation | field errors + summary; inputs preserved | correct, resubmit | focus to summary |
| success | valid submit | proceeds to payment step | continue | announced |
| permission-denied | — | n/a (guests by design, `PRIN-2`) | — | — |
| reservation-expired | expiry mid-checkout | explanation that stock was released | re-checkout if available | `role="alert"` |

**Responsive** ≥1280: two columns (form start, summary sticky) · 768–1279: one column + sticky summary · <768: one column, summary directly above «ادامه و پرداخت».

**Keyboard & focus** natural field order; `Enter` submits (single-page form); errors move focus to summary; promo toggle is a labelled disclosure; pay CTA ≥ 44 px height.

**A11y** labels always visible (never placeholder-as-label); phone input accepts Persian/Latin digits, displayed canonically; total changes announced politely; rate note read with the total.

**Copy**

| Element | Copy |
|---|---|
| title | «تکمیل خرید» |
| labels | «نام و نام خانوادگی» · «شماره موبایل» · «آدرس تحویل» · «ایمیل (اختیاری)» |
| promo | «کد تخفیف دارید؟» · «اعمال» |
| promo rejected | «این کد معتبر نیست یا منقضی شده است.» |
| rate note | «مبلغ نهایی هنگام پرداخت بر اساس نرخ لحظه محاسبه می‌شود.» |
| CTA | «ادامه و پرداخت» |
| expired reservation | «زمان رزرو تمام شد؛ اقلام آزاد شدند. دوباره از سبد خرید ادامه دهید.» |

**Acceptance criteria**

- [ ] SCR-006-AC1 — first-time guest completes with zero account interactions (`UF-02-AC1`)
- [ ] SCR-006-AC2 — every failure returns to an intact checkout with preserved input (`UF-02-AC2`)
- [ ] SCR-006-AC3 — promo rejection leaves the total unchanged and explains why (`AC-FR-PROMO-1.2`)
- [ ] SCR-006-AC4 — reservation expiry is explained with a working re-checkout path (`UX-AC-008.3`)

---

### SCR-007 — Payment step / پرداخت

**Route** `/checkout/pay` · **Module** TBD · **Flows** UF-02 · **Reqs** `FR-PAY-1`, `UX-009`, `DEC-014`, `DEC-020` · **Blocked by** `OQ-001` for the gateway itself; the UI spec below is complete.
**Entry** checkout CTA. **Exit** gateway (external) → confirmation (SCR-008) or back to checkout.
**Primary action** «پرداخت». **Secondary** back to checkout (cancel), retry after failure.

**Layout regions** single focused card: final total + basis · promo line · security statement · CTA. No global nav distractions (header reduced).

**Content and controls**

| Element | Type | Data | Empty behaviour | Error behaviour |
|---|---|---|---|---|
| final total | large amount + basis line + «نرخ لحظه پرداخت {تاریخ}» | rate at payment (`DEC-020`) | — | — |
| changed-total notice | warning line when total differs from checkout start | rate delta | hidden when unchanged | — |
| security statement | text near CTA | `DEC-048` | — | — |
| pay CTA | primary, opens gateway | — | — | failure → intact return + reason |
| redirect state | full-page progress + «صفحه را نبندید» | — | — | timeout → return + retry |

**States**

| State | Trigger | Appearance | Actions | A11y |
|---|---|---|---|---|
| default | ready | final total + basis + security + CTA | pay, go back | total announced on change |
| loading | redirecting | progress + stay-on-page note | wait | polite announcement |
| empty | — | n/a (total always present) | — | — |
| error | gateway unreachable/failed | returned to intact checkout + reason + «تلاش دوباره برای پرداخت» | retry | `role="alert"` |
| success | payment completed | confirmation screen (SCR-008) | continue | announced |
| permission-denied | — | n/a | — | — |
| cancelled | buyer cancels at gateway | «پرداخت را لغو کردید…» + intact checkout | retry | announced |

**Responsive** single centred column at all widths.

**Keyboard & focus** CTA first in tab order; retry focusable; no traps.

**A11y** total change is announced, never silent (`UX-AC-009`); security statement read before CTA; no colour-only status.

**Copy**

| Element | Copy |
|---|---|
| title | «پرداخت سفارش» |
| total label | «مبلغ نهایی» |
| changed notice | «مبلغ نهایی بر اساس نرخ امروز به‌روز شده است؛ مبلغ جدید در زیر آمده است.» |
| security | «برای پرداخت به درگاه بانکی منتقل می‌شوید. مبلغ نهایی همان مبلغی است که کسر خواهد شد.» |
| failed | «پرداخت انجام نشد؛ سبد و اطلاعات شما محفوظ است. دوباره تلاش کنید.» |
| cancelled | «پرداخت را لغو کردید؛ می‌توانید دوباره تلاش کنید.» |

**Acceptance criteria**

- [ ] SCR-007-AC1 — final total incl. promo + basis shown before redirect (`UX-AC-009.1`)
- [ ] SCR-007-AC2 — failed payment returns to intact checkout with visible retry (`UX-AC-009.2`)
- [ ] SCR-007-AC3 — cancel returns to checkout with nothing lost (`UX-AC-009.3`)
- [ ] SCR-007-AC4 — a total change between start and payment is stated explicitly, never silent (`DEC-020`)

---

### SCR-008 — Order confirmation

**Route** `/order/:code` · **Module** TBD · **Flows** UF-02, UF-03 · **Reqs** `FR-ORD-1`, `UX-003`, `DEC-021`
**Entry** post-payment redirect · confirmation email link · account order list. **Exit** track order · home · account (soft offer).
**Primary action** «پیگیری سفارش». **Secondary** copy order code, continue shopping, create account (dismissible offer).

**Layout regions** success headline + order code · status timeline (first step active) · order summary (items, totals, buyer info) · track explainer · soft account offer.

**Content and controls**

| Element | Type | Data | Empty behaviour | Error behaviour |
|---|---|---|---|---|
| order code | large, LTR-isolated `<bdi>`, copy button | `FR-ORD-1` | — | — |
| timeline | 3 steps, forward-only | order status (`BR-2`) | — | — |
| summary | items + totals + rate basis | order | — | — |
| email note | line when email provided | `DEC-017` | hidden without email | send failure → note «در صف ارسال» |
| account offer | dismissible card after success | `UX-002` | hidden for logged-in buyers | — |

**States**

| State | Trigger | Appearance | Actions | A11y |
|---|---|---|---|---|
| default | paid order | confirmation layout | track, copy, shop | h1 announced |
| loading | fetch | skeleton | — | `aria-busy` |
| empty | unknown code | «سفارشی با این کد پیدا نشد» (identical to not-found; anti-enumeration `DEC-021`) | track form | announced |
| error | fetch fails | message + retry | retry | `role="alert"` |
| success | — | this screen *is* the success state | — | announced |
| permission-denied | — | n/a (the code is the capability) | — | — |

**Responsive** single column; desktop keeps summary beside timeline.

**Keyboard & focus** copy button reachable and announces «کد سفارش کپی شد»; account offer dismissible by keyboard.

**A11y** order code renders unambiguously inside RTL text (`UX-G-009`); timeline steps readable as a list.

**Copy**

| Element | Copy |
|---|---|
| headline | «سفارش شما ثبت شد» |
| code label | «کد سفارش» |
| explainer | «برای پیگیری، کد سفارش و شماره موبایل خود را نگه دارید.» |
| email | «جزئیات سفارش به {ایمیل} ایمیل شد.» |
| account offer | «می‌خواهید سفارش‌هایتان را یک‌جا ببینید؟ می‌توانید حساب بسازید.» + «بعداً» |

**Acceptance criteria**

- [ ] SCR-008-AC1 — order code shown prominently with an explicit how-to-track line (`UX-AC-003.2`)
- [ ] SCR-008-AC2 — timeline matches the order record, forward-only (`UF-03-AC4`)
- [ ] SCR-008-AC3 — the account offer never blocks checkout or confirmation content (`UX-AC-002.2`)

---

### SCR-009 — Track order / پیگیری سفارش

**Route** `/track` (email link prefills code) · **Module** TBD · **Flows** UF-03 · **Reqs** `FR-ORD-1`, `UX-003`, `DEC-021`, `BR-2`
**Entry** header/footer (site-wide, ≤ 1 click) · confirmation page · email link. **Exit** confirmation/order view.
**Primary action** «پیگیری». **Secondary** clear form, contact via policy page.

**Layout regions** lookup form (code + phone) · result area: timeline + minimal order summary (date, total, item count).

**Content and controls**

| Element | Type | Data | Empty behaviour | Error behaviour |
|---|---|---|---|---|
| order code | text input, dir=ltr, Latin/digits | `FR-ORD-1` | — | inline error |
| phone | tel input, `inputmode=numeric` | — | — | inline error |
| result | timeline + summary | status (`BR-2`) | not-found (identical for wrong phone vs unknown code) | rate-limited, generic message |

**States**

| State | Trigger | Appearance | Actions | A11y |
|---|---|---|---|---|
| default | entry | compact form | submit | labels + autocomplete |
| loading | lookup | brief inline progress | — | polite |
| empty | no match | single not-found message (`UX-AC-003.3`) | re-enter | `role="alert"` |
| error | service failure | message + retry | retry | `role="alert"` |
| success | match | timeline (current + past steps marked) + summary | — | result announced politely |
| permission-denied | — | n/a (code + phone *is* the permission, `DEC-021`) | — | — |

**Responsive** vertical timeline on mobile, horizontal on desktop; form compact at all widths.

**Keyboard & focus** two fields + submit in natural order; error returns focus to the failed field.

**A11y** bidi safety on the code (`UX-G-009`); status is text + shape, not colour-only.

**Copy**

| Element | Copy |
|---|---|
| title | «پیگیری سفارش» |
| labels | «کد سفارش» · «شماره موبایل» · «پیگیری» |
| not found | «سفارشی با این مشخصات پیدا نشد؛ کد و شماره را دوباره بررسی کنید.» |
| steps | «پرداخت‌شده» → «ارسال‌شده» → «تحویل‌شده» |

**Acceptance criteria**

- [ ] SCR-009-AC1 — site-wide entry point → form in ≤ 1 click (`UF-03-AC1`)
- [ ] SCR-009-AC2 — works with no email at all (`UF-03-AC2`)
- [ ] SCR-009-AC3 — wrong phone + valid code indistinguishable from unknown code (`UF-03-AC3`)

---

### SCR-010 — Policy pages / برگه‌های اطلاعاتی

**Route** `/pages/:slug` (seed slugs: shipping · returns · contact) · **Module** TBD · **Flows** — (trust scaffolding) · **Reqs** `FR-PAGE-1`, `UX-004`, `DEC-026`
**Entry** footer on every page (≤ 1 click), payment step, product page. **Exit** contact/track · shop.
**Primary action** read (no commerce action). **Secondary** track order, call/message (contact page), back to shop.

**Layout regions** header · main: h1 + owner-provided content (headings, paragraphs, lists, links) · related links block (track order, other policies).

**Content and controls** owner content per slug; contact page shows the shop's contact info as entered by the owner (no forms in v1 — no message inbox in requirements).

**States**

| State | Trigger | Appearance | Actions | A11y |
|---|---|---|---|---|
| default | published | article layout | navigate | readable measure (~70ch) |
| loading | fetch | text skeleton | — | `aria-busy` |
| empty | unpublished slug | hidden from footer; direct hit → 404 | — | — |
| error | fetch fails | message + retry | retry | `role="alert"` |
| success | — | n/a | — | — |
| permission-denied | — | n/a (public) | — | — |

**Responsive** single column; font size and measure preserved at 200 % zoom (`UX-G-005`).

**Keyboard & focus** linear reading order; links have descriptive Persian labels.

**A11y** article landmark; links distinguishable beyond colour.

**Copy**

| Element | Copy |
|---|---|
| titles | «ارسال و تحویل» · «بازگشت و بازپرداخت» · «تماس با ما» |
| related | «پیگیری سفارش» |

**Acceptance criteria**

- [ ] SCR-010-AC1 — all three pages reachable from every storefront page in ≤ 1 click (`UX-AC-004.1`)
- [ ] SCR-010-AC2 — rendering survives the owner's paste-realistic content (lists, links, long paragraphs) without layout breakage

---

### SCR-011 — Not found / ۴۰۴

**Route** catch-all · **Module** TBD · **Flows** — · **Reqs** `UX-G-003`
**Entry** unknown URL, removed product/category. **Exit** home · categories · search · track.
**Primary action** «بازگشت به خانه». **Secondary** category links, search, track order.

**States** one static state only — default: message + recovery links (HTTP 404 status preserved, implementation note); loading n/a · empty n/a · error n/a · success n/a · permission-denied n/a (a 404 is not a permission event and must not be rendered as one).

**Responsive** single column.
**Keyboard** trivial linear order; home link first, then category links.
**A11y** one `h1`; recovery links are real links with a visible focus ring; no auto-redirect and no timed countdown; message text ≥ 4.5:1 (`UX-G-003`).

**Copy**

| Element | Copy |
|---|---|
| title | «این صفحه پیدا نشد» |
| body | «ممکن است نشانی تغییر کرده باشد یا این محصول دیگر در فروشگاه نباشد.» |
| actions | «بازگشت به خانه» + دسته‌ها |

**Acceptance criteria**

- [ ] SCR-011-AC1 — every recovery link works; no dead end (`UF-01` failure path)
- [ ] SCR-011-AC2 — unknown product/category URLs land here, not on a broken screen

## 4. Account screens — W2 (optional accounts, never required, `DEC-005`)

### SCR-012 — Login / ورود

**Route** `/login` · **Module** TBD · **Flows** — (supports UF-03 A1) · **Reqs** `FR-ACC-1`, `PRIN-2`, `DEC-005`
**Entry** header account link · account redirect (permission-denied) · soft offer on confirmation. **Exit** referring page or `/account`. **Primary action** «ورود». **Secondary** go to register, continue as guest.
**Fields** «شماره موبایل» + «رمز عبور» — *mechanism note:* password vs OTP is an architecture decision; copy here describes a password flow and adjusts via one UX decision if OTP is chosen.

**States**

| State | Trigger | Appearance | Actions | A11y |
|---|---|---|---|---|
| default | entry | two fields + CTA + guest note | sign in | labels visible |
| loading | submit | button loading | — | `aria-busy` |
| empty | — | n/a | — | — |
| error | wrong credentials | generic «شماره موبایل یا رمز عبور درست نیست.» (no user enumeration) | retry | `role="alert"` |
| success | signed in | redirect to intended page (return URL preserved) | continue | announced |
| permission-denied | — | this screen *is* the permission entry | — | — |

**Responsive** single compact column. **Keyboard** natural order; Enter submits. **A11y** errors associated with fields; rate-limit message states wait time when applicable.

**Copy** title «ورود» · guest note «خرید مهمان نیازی به حساب ندارد.» · link «حساب ندارید؟ بسازید»

**ACs** SCR-012-AC1 — guest path is never blocked by this screen (`UX-AC-002.1`) · SCR-012-AC2 — return URL lands the buyer where they were headed

### SCR-013 — Register / ساخت حساب

**Route** `/register` · **Module** TBD · **Reqs** `FR-ACC-1`
**Entry** header · login link. **Exit** account home. **Primary action** «ساخت حساب». **Secondary** sign in, continue as guest.
**Fields** «نام و نام خانوادگی» · «شماره موبایل» · «رمز عبور» (minimum policy shown).

**States** default · loading · error (field errors + summary, input preserved) · success (account home, welcome line) · empty n/a · permission-denied n/a.
**Responsive/keyboard/a11y** as SCR-012.
**Copy** title «ساخت حساب» · note «حساب فقط برای دیدن سفارش‌ها و خرید سریع‌تر است؛ همیشه می‌توانید مهمان خرید کنید.»
**ACs** SCR-013-AC1 — registration never interrupts checkout; no interstitial appears during UF-02 (`UX-AC-002.2`)

### SCR-014 — Account home / حساب من

**Route** `/account` · **Module** TBD · **Reqs** `FR-ACC-1`
**Entry** header · post-login. **Exit** order history, logout, shop.
**Layout** two blocks: «سفارش‌های من» (last 5 + link به SCR-015) · «اطلاعات من» (read-only name + phone in v1; editing is a change-request candidate) · «خروج».

**States**

| State | Trigger | Appearance | Actions | A11y |
|---|---|---|---|---|
| default | signed in | blocks as above | navigate, logout | landmarks per block |
| loading | fetch | skeletons | — | `aria-busy` |
| empty | no orders | «هنوز سفارشی ثبت نکرده‌اید.» + shop link | shop | announced |
| error | fetch fails | block retry | retry | `role="alert"` |
| success | logout | redirect home, session cleared | — | announced |
| permission-denied | not signed in | redirect to SCR-012 with return URL | sign in | — |

**Responsive** single column on phone; «سفارش‌های من» and «اطلاعات من» side by side ≥1280; order rows become two lines (code + total, status chip wrapping under) below 768.
**Keyboard** order rows and the logout control are the only focusables; logout is last in tab order; Enter on a row opens SCR-015.
**A11y** each block is a labelled section with its own heading; the status chip carries text, never colour alone (`UX-G-006`); empty and logout states are announced politely; phone number renders LTR inside the RTL label (`UX-G-009`).
**Copy** title «حساب من» · logout «خروج»
**ACs** SCR-014-AC1 — account holder sees only their own data (server-enforced, IA §5)

### SCR-015 — Order history / سفارش‌های من

**Route** `/account/orders` · **Module** TBD · **Reqs** `FR-ACC-1`, `FR-ORD-1`
**Entry** account home. **Exit** order view (same timeline as SCR-008 without the success headline).
**List** rows: code · date · total · status chip; newest first; full rows are links.

**States** default · loading (skeleton rows) · empty («هنوز سفارشی ثبت نکرده‌اید.») · error (retry) · success n/a · permission-denied (redirect to login).
**Responsive** table ≥1280, card rows below.
**Keyboard** rows tabbable, Enter opens; the only focusable content is the rows.
**A11y** each row reads as code · date · total · status in that order; status is text, not colour alone (`UX-G-006`); order codes and dates render bidi-safely inside the RTL row (`UX-G-009`).
**Copy** title «سفارش‌های من»
**ACs** SCR-015-AC1 — status chips match the order record and use the forward-only vocabulary (`BR-2`)

## 5. Admin screens — W2 (desktop-first, Farsi, `DEC-037`, `DEC-042`)

**Shared admin patterns (apply to every admin screen below; specs list only deltas):**

- Shell: stable sidebar (نمای کلی · سفارش‌ها · محصولات · نرخ روز · کدهای تخفیف · برگه‌ها · طرح ماه) + top bar (پیوند فروشگاه، خروج). Desktop ≥1280 full; 768–1279 collapsible sidebar + reduced-column tables; phone deferred (`UX-OPEN`).
- Permission-denied: not signed in → redirect to SCR-016 (server-enforced; the UI is not a boundary, IA §5).
- Global banner while today's rate is missing, on **every** admin screen (`UX-AC-007.3`): «نرخ امروز ثبت نشده است» + action «ثبت نرخ امروز» → SCR-022.
- States: loading = skeleton matching final layout · error = section message + retry with form input preserved · success = inline saved-state + toast «ذخیره شد» · destructive actions require confirmation naming the object and consequence (`UX-AC-007.2`).
- Keyboard: sidebar → content; dialogs/sheets trap focus, `Esc` closes, focus returns to trigger; tables keep ≥24 px targets and visible row focus.
- Copy: plain functional Farsi (`PRIN-6`), no jargon, labels always visible (`UX-007`).

### SCR-016 — Admin login

**Route** `/admin/login` · **Reqs** `FR-ADM-1`, `UX-007`
**Entry** direct `/admin` while signed out · session expiry. **Exit** `/admin` overview. **Primary action** «ورود». **Secondary** none (no self-registration link — owner accounts are provisioned out-of-band; provisioning mechanism is an ops/architecture decision).
**Fields** «نام کاربری» + «رمز عبور».

**States** default · loading (button) · empty n/a · error: generic «نام کاربری یا رمز عبور درست نیست.» + rate-limit wait note · success (redirect, return URL preserved) · permission-denied is this screen.
**Responsive** centred card, desktop and tablet. **Keyboard** two fields, Enter submits. **A11y** errors associated with fields; no enumeration hints.
**ACs** SCR-016-AC1 — every /admin route redirects here when signed out; no admin data flashes before redirect

### SCR-017 — Admin overview / نمای کلی

**Route** `/admin` · **Flows** UF-04 (steps 1–2) · **Reqs** `FR-ADM-2`, `FR-RATE-1`
**Entry** post-login, sidebar. **Exit** rate entry, orders list, products. **Primary action** «ثبت نرخ امروز» (when missing) / open work queues. **Secondary** jump to sections.
**Cards** «نرخ امروز» (state: ثبت‌شده {مبلغ} / ثبت‌نشده + CTA) · «سفارش‌های در انتظار ارسال» (count → filtered orders) · «فروش ۷ روز اخیر» (total) · «محصولات فعال» (count).

**States** default · loading (card skeletons) · empty (fresh store: «هنوز داده‌ای نیست؛ با ثبت نرخ و افزودن محصول شروع کنید.») · error (per-card retry) · success n/a · permission-denied (shared pattern).
**Responsive** card grid 4-up/2-up/1-up. **Keyboard** cards are links, tabbable. **A11y** numbers as real text with Persian formatting; rate state not colour-only.
**Copy** title «نمای کلی»
**ACs** SCR-017-AC1 — missing rate visible within 1 screen from login (`UX-AC-007.3`) · SCR-017-AC2 — counts link to the exact filtered lists they summarise

### SCR-018 — Admin orders / سفارش‌ها

**Route** `/admin/orders` · **Flows** UF-04 (step 3) · **Reqs** `FR-ADM-2`, `BR-2`
**Entry** sidebar · overview card. **Exit** order detail. **Primary action** open an order. **Secondary** filter by status (همه / پرداخت‌شده / ارسال‌شده / تحویل‌شده).
**Columns** «کد سفارش» · «خریدار» · «مبلغ» · «وضعیت» · «تاریخ ثبت»; default sort newest first; page controls (tabular data per `interaction_patterns.md`).

**States** default · loading (row skeletons) · empty («هنوز سفارشی ثبت نشده است؛ سفارش‌های پرداخت‌شده اینجا می‌آیند.») · error (retry) · success n/a · permission-denied (shared).
**Responsive** full table ≥1280; reduced columns 768–1279. **Keyboard** rows focusable, Enter opens. **A11y** headers scoped; status chips text-first.
**Copy** title «سفارش‌ها»
**ACs** SCR-018-AC1 — a Paid order appears here without manual refresh beyond the list's own reload

### SCR-019 — Admin order detail

**Route** `/admin/orders/:id` · **Flows** UF-04 (steps 3–4) · **Reqs** `FR-ADM-2`, `FR-ORD-1`, `BR-2`, NFR-OBS-1
**Entry** orders list. **Exit** back to list. **Primary action** advance status («ثبت ارسال» → «ثبت تحویل»). **Secondary** copy buyer contact, open product, email-resend note.
**Blocks** «اطلاعات خریدار» (نام، موبایل، آدرس، ایمیل in full per `AC-FR-ADM-2.1`) · «اقلام» (with price basis: وزن، نرخ لحظه سفارش، اجرت) · «مبلغ‌ها» (جمع، تخفیف، پرداخت‌شده) · «وضعیت» timeline + next-step button.

**States**

| State | Trigger | Appearance | Actions | A11y |
|---|---|---|---|---|
| default | loaded | all blocks | advance status | sections labelled |
| loading | fetch | block skeletons | — | `aria-busy` |
| empty | invalid id | not-found block + back link | back | announced |
| error | fetch/save fails | message + retry; no partial save | retry | `role="alert"` |
| success | status advanced | timeline updates + saved confirmation; email queued note | continue | announced politely |
| permission-denied | shared pattern | — | — | — |

**Confirm dialog** on advance: «وضعیت این سفارش به «{وضعیت}» تغییر کند؟ ایمیل اطلاع‌رسانی برای خریدار (در صورت وجود) ارسال می‌شود.» Forward-only: no backward control exists (`UF-04-AC3`). Email failure surfaces as a non-blocking note (NFR-OBS-1, `UF-04-AC4`).
**Responsive** two columns ≥1280, stacked below. **Keyboard** confirm dialog traps + returns focus.
**Copy** title «جزئیات سفارش {کد}» · actions «ثبت ارسال» / «ثبت تحویل»
**ACs** SCR-019-AC1 — status changes only forward, idempotent on double-click · SCR-019-AC2 — every order displays its price basis and the rate date it was locked at (`DEC-020`)

### SCR-020 — Admin products / محصولات

**Route** `/admin/products` · **Flows** UF-04 A1 · **Reqs** `FR-ADM-1`, `BR-4`, `DEC-011`
**Entry** sidebar · overview card. **Exit** product form, back. **Primary action** «افزودن محصول». **Secondary** edit, activate/deactivate (retire), open storefront view.
**Columns** «تصویر» · «نام» · «دسته» · «وزن» · «اجرت» · «قیمت امروز» (computed + rate date) · «وضعیت» (فعال/غیرفعال؛ موجودی badge).

**States** default · loading (row skeletons) · empty («هنوز محصولی ثبت نشده؛ اولین محصول را اضافه کنید.» + add CTA) · error (retry) · success (retire → toast + row state) · permission-denied (shared).
**Deactivate (retire)** is destructive for the storefront: confirmation «این محصول از فروشگاه پنهان می‌شود؛ سفارش‌های قبلی تغییر نمی‌کنند.» (`UX-AC-007.2`).
**Responsive** table ≥1280; reduced columns 768–1279. **Keyboard** rows/actions tabbable. **A11y** price column shows rate date; status text-first.
**Copy** title «محصولات» · actions «افزودن محصول»
**ACs** SCR-020-AC1 — catalog status (photos missing, zero stock, inactive) is visible column-by-column without opening each product · SCR-020-AC2 — SC-2 checklist readiness is assessable from this list alone

### SCR-021 — Admin product form / افزودن و ویرایش محصول

**Route** `/admin/products/new`, `/admin/products/:id` · **Reqs** `FR-ADM-1`, `FR-PROD-1`, `BR-4`, `DEC-022`
**Entry** products list. **Exit** back to list (success toast). **Primary action** «ذخیره محصول». **Secondary** cancel (unsaved-changes confirm), deactivate, preview storefront link.
**Fields** «نام» · «دسته» (select, taxonomy `DEC-023`+`DEC-038`) · «توضیحات» (textarea; purity/hallmark details for bars live here in v1 — a structured purity field is a change-request candidate) · «وزن (گرم)» · «اجرت (تومان)» · «سنگ» (ندارد/دارد، و وقتی «دارد»: نوع سنگ — v1 value «ماه‌سنگ» per `DEC-051`, list owner-extendable per `OQ-016`; hidden relevance for bars but harmless) · «تعداد موجودی» (0 ⇒ ناموجود; if architecture settles on boolean availability, this field collapses to a toggle — one UX decision) · «تصاویر» (multi-upload, drag to order, first = cover; ≥1 required to activate, 3–5 recommended per `design_system.md` photo guide) · «وضعیت نمایش» (فعال/غیرفعال).

**Validation** name required · weight > 0 · fee ≥ 0 · stock ≥ 0 integer · at least 1 photo before activation · category required. Previous input always preserved on error.

**States** default (new = empty form; edit = filled) · loading (edit fetch skeleton) · empty n/a · error (field + summary Farsi, saved nothing) · success (toast «ذخیره شد» + price preview with today's rate) · permission-denied (shared). Deactivate = shared destructive confirm.
**Responsive** single-column form ≥1280 with sticky save bar; reduced at 768–1279. **Keyboard** logical order; upload reorder via keyboard (move buttons, not drag-only). **A11y** labels visible; error association; photo alt/order controls labelled.
**Copy** titles «افزودن محصول» / «ویرایش محصول» · save «ذخیره محصول» · price preview «قیمت امروز: {مبلغ} (بر پایه نرخ {تاریخ})»
**ACs** SCR-021-AC1 — a product can be created end-to-end (fields + photos + active) in one form without side trips (`DEC-029`) · SCR-021-AC2 — invalid save loses nothing and states every fix needed (`UX-AC-007.1`)

### SCR-022 — Admin daily rate / نرخ روز

**Route** `/admin/rate` · **Flows** UF-04 (step 2) · **Reqs** `FR-RATE-1`, `DEC-019`, `BR-4`
**Entry** sidebar · global rate banner · overview card. **Exit** back to overview. **Primary action** «ثبت نرخ». **Secondary** edit today's value (latest wins), view history.
**Content** current state (today's rate or missing); input «نرخ هر گرم (تومان)» (Persian-formatted, accepts both digit sets); entry date fixed to today (backfill = change-request candidate); «ثبت نرخ»; history table «تاریخ» · «نرخ (تومان/گرم)» · «زمان ثبت» (auditable `FR-RATE-1`).

**States**

| State | Trigger | Appearance | Actions | A11y |
|---|---|---|---|---|
| default | loaded | input + history + save | save | label visible |
| loading | fetch | skeletons | — | `aria-busy` |
| empty | no history | history block: «هنوز نرخی ثبت نشده است.» | save first rate | announced |
| error | save fails / invalid (≤0, malformed) | Farsi field error, previous value kept (`AC-FR-RATE-1.3`) | correct, resubmit | focus to field |
| success | saved | «نرخ امروز ثبت شد.» + banner clears storewide | continue | polite announcement |
| permission-denied | shared pattern | — | — | — |

**Responsive** single column; history table ≥1280, list below. **Keyboard** input → save; history rows readable.
**Copy** title «نرخ روز نقره» · missing state «نرخ امروز ثبت نشده است.»
**ACs** SCR-022-AC1 — login → saved rate in < 30 s (`UF-04-AC1`) · SCR-022-AC2 — recording today's rate clears the staleness banner everywhere immediately

### SCR-023 — Admin promos / کدهای تخفیف

**Route** `/admin/promos` · **Reqs** `FR-PROMO-1`, `DEC-018`, `DEC-024`
**Entry** sidebar. **Exit** back. **Primary action** «افزودن کد». **Secondary** edit, delete, activate/deactivate.
**Table** «کد» · «درصد تخفیف» · «تاریخ انقضا» · «استفاده» ({used}/{max}) · «وضعیت». **Form** code (unique, Latin/digits) · percent 1–100 · expiry date (Jalali picker) · max uses ≥ 1.

**States** default · loading · empty («هنوز کد تخفیفی ساخته نشده.» + add CTA) · error (field errors; duplicate code named) · success (toast; storefront applies within minutes — no deploy) · permission-denied (shared). Delete = destructive confirm «کد «{کد}» حذف شود؟ سفارش‌های قبلی دست نمی‌خورند.»
**Responsive/keyboard/a11y** as SCR-020 patterns; expiry picker keyboard-operable; usage counter announced.
**Copy** title «کدهای تخفیف»
**ACs** SCR-023-AC1 — a code created here applies at checkout without deploy (`DEC-024`) · SCR-023-AC2 — used/exhausted codes are unmistakable in the table

### SCR-024 — Admin pages + hero / برگه‌ها و هیرو

**Route** `/admin/pages` · **Reqs** `FR-PAGE-1`, `DEC-026`, `DEC-047`
**Entry** sidebar. **Exit** storefront preview (new tab). **Primary action** «ذخیره». **Secondary** preview, revert-unsaved (confirm).
**Tabs** «ارسال و تحویل» · «بازگشت و بازپرداخت» · «تماس با ما» (+ contact info fields) · «هیرو صفحه اصلی» (image upload + one-line text; fallback note). Story/trust texts are defaults in v1 — making them editable is a change-request candidate.

**States** default · loading · empty (unwritten page → storefront hides its footer link until published) · error (save fails, content preserved) · success (toast «ذخیره شد» + storefront reflects immediately) · permission-denied (shared).
**Responsive** editor single column; preview responsive. **Keyboard/a11y** tab pattern with roving tabindex; textarea labelled; image upload order controls labelled.
**Copy** title «برگه‌های اطلاعاتی» · hero fallback «اگر خالی بماند، متن و تصویر پیش‌فرض نمایش داده می‌شود.»
**ACs** SCR-024-AC1 — policy wording reaches the storefront with no developer involvement (`FR-PAGE-1`, `UX-AC-004.1`) · SCR-024-AC2 — clearing the hero image/text restores the default rendering (`DEC-047`)

### SCR-025 — Admin featured design / طرح ماه

**Route** `/admin/featured` · **Flows** UF-04 · **Reqs** `DEC-043`, `UX-011`
**Entry** sidebar. **Exit** storefront preview. **Primary action** «ذخیره». **Secondary** «برداشتن انتخاب», preview.
**Content** current pick preview (photo + name) · picker «انتخاب محصول» (searchable select over **active** products only — featuring a retired product is prevented per `UX-AC-011.3`) · «یادداشت کوتاه (اختیاری)» (≤ 120 characters) · save.

**States** default (current pick or none) · loading · empty (no pick → storefront slot hidden, `DEC-043`) · error (save fails, selection preserved) · success (toast; storefront live without deploy) · permission-denied (shared). Clearing pick = confirm «طرح ماه از صفحه اصلی برداشته شود؟»
**Responsive** single column. **Keyboard** picker is a labelled combobox, fully keyboard-operable. **A11y** note field has a counter announced; preview labelled.
**Copy** title «طرح ماه» · empty «هنوز طرحی برای ماه انتخاب نشده؛ تا انتخاب نکنید، این بخش در صفحه اصلی نمایش داده نمی‌شود.»
**ACs** SCR-025-AC1 — select/clear in ≤ 3 interactions, live without deploy (`UX-AC-011.1`) · SCR-025-AC2 — clearing hides the storefront slot immediately (`UX-AC-011.2`)

## 6. Change log

| Date | Change | By |
|---|---|---|
| 2026-09-20 | initial spec — 25 screens (W1 storefront 11, W2 account 4 + admin 10), six-state coverage, ACs, Persian copy | frontend-ux |
| 2026-09-21 | SCR-001 gains the «کاوش ماه‌سنگ» band and the سنگ این ماه chip (`DEC-050`, `DEC-051`); SCR-002/003 stone filter gains «ماه‌سنگ»; SCR-021 product form gains the stone type | frontend-ux |
| 2026-09-21 | SCR-001: the band now carries the «دوازده سنگ ماه» explorer — all twelve months with stone names, correlation, «در نقره» and care lines («این ماه»/«تخصص فروشگاه» markers), static and non-interactive; copy table + AC9/AC10 added (`DEC-052`, `UX-AC-012.6`) | frontend-ux |
| 2026-09-21 | SCR-001: **Gregorian calendar** — the chip and the album name the Gregorian month in Farsi + Latin («سپتامبر · September»), fallback ژانویه/گارنت, AC6/AC8 reworded (`DEC-053`) | frontend-ux |
| 2026-09-21 | SCR-001: **the ماه‌سنگ band is replaced by the compact سنگ ماه album** (twelve tiles: month + ≈ Gregorian + stone names, current month marked, no copy/photo/CTA, no control); band rows, copy and AC6/7/9/10 rewritten, Reqs drop `DEC-051` (`DEC-052`, supersedes `DEC-051` clause a) | frontend-ux |

<!-- Update the inventory table and status on every screen change; new screens require an IA change first. -->
