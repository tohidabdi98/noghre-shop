# Information architecture

> Owned by the Frontend/UX Agent. This is the product's map: hierarchy, navigation, naming, URLs
> and who can see what. It prevents the classic agent failure mode of inventing a new page or a
> new navigation entry for every new feature.

## 1. Navigation model

| Aspect | Decision | Rationale |
|---|---|---|
| Primary navigation (storefront) | persistent top header: logo · categories menu · search · track order · cart · account (RTL order, `DEC-037`/`DEC-040`) | matches JA-derived pattern, adapted RTL |
| Primary navigation (admin) | stable left sidebar: Overview · Orders · Catalog · Daily rate · Promotions · Pages · Featured design (`DEC-042`) | owner workspace, desktop-first |
| Max depth | 3 levels (home → category → product; admin → section → detail) | deeper levels lose users |
| Where global actions live | storefront header (search/cart/account/track); admin top bar (shop link, logout) | consistent globals |
| Where contextual actions live | page headers and cards/rows; admin row actions | context stays with content |
| Back behaviour | browser history respected; cart drawer closes without breaking history; no navigation traps | mobile users swipe/back constantly |
| Deep linking | every category, product, search state, order-lookup and admin view has a URL | shareability (social traffic, `DEC-025`) |
| Persistence | filters reflected in URL; cart persists per browser; admin table state (page/filters) in URL | nothing lost on refresh |

### Storefront header (RTL reading order)

```text
→ [سبد خرید] [حساب] [پیگیری سفارش] [جست‌وجو] [دسته‌ها ▾] [نقره‌شاپ]
```

Mobile: hamburger drawer (categories + track order + account), persistent cart icon with count;
**no bottom bar** (`DEC-040`).

## 2. Site map

```text
/                            home (hero, category tiles, new/bestselling, سنگ ماه album (دوازده ماه میلادی), trust row, story, rate chip, سنگ این ماه chip, featured design)
├── /category/:slug          product grid + filters        (rings, necklaces, earrings, bracelets, sets, silver-bars, other)
├── /product/:slug           product detail + gallery
├── /search?q=&filters       search results (same grid)
├── /cart                    full cart page (drawer is the primary surface; this is the shareable/keyboard path)
├── /checkout                single-page checkout (guest or logged-in)
│   └── /checkout/pay        payment step (final total → gateway redirect)
├── /order/:code             order confirmation (post-payment, code prominent)
├── /track                   order lookup (code + phone) → status timeline
├── /login  /register        optional accounts (never required, PRIN-2)
├── /account                 account home
│   └── /account/orders      order history
├── /pages/:slug             policy pages: shipping · returns · contact (FR-PAGE-1)
└── /admin                   owner shell (desktop-first, UX-007)
    ├── /admin               overview (counts/totals + rate-state banner)
    ├── /admin/login         owner sign-in (SCR-016)
    ├── /admin/orders        order list  → /admin/orders/:id  (status advancement)
    ├── /admin/products      catalog     → /admin/products/new, /admin/products/:id
    ├── /admin/rate          daily silver rate entry + history
    ├── /admin/promos        promo code CRUD (FR-PROMO-1)
    ├── /admin/pages         policy pages + homepage hero editing (FR-PAGE-1, DEC-047)
    └── /admin/featured      "design of the month" pick (DEC-043)
```

Category slugs: Latin `kebab-case` for URLs (`/category/silver-bars`), **labels always Farsi**
(`انگشتر`, `گردنبند`, `گوشواره`, `دستبند`, `ست`, `شمش نقره`, `سایر`). Seed list per `DEC-023`
**plus شمش نقره per `DEC-038`**; owner-editable afterwards.

## 3. Hierarchy and ownership

| Level | Contains | Example | Rule |
|---|---|---|---|
| Shell | global chrome (header/footer; admin sidebar) | storefront header, `/admin` sidebar | one module owns each shell |
| Section | a coherent domain area | Catalog, Checkout, Admin | one module per section (decomposition) |
| Screen | one task or view | product detail | one module |
| Panel/dialog | a focused subtask | cart drawer, filter sheet | belongs to its screen |

**New screens require an IA change first** — the Frontend/UX Agent reviews and records it here,
then the affected module contract is updated. Implementation agents must not add navigation
entries on their own.

## 4. Naming rules

| Concern | Rule | Examples |
|---|---|---|
| Navigation labels | Persian user vocabulary, ≤ 2 words | «پیگیری سفارش», not «سیستم رهگیری» |
| URLs | Latin `kebab-case` slugs, plural nouns for collections, no verbs for GET routes | `/category/rings`, `/admin/products` |
| Actions | verb + object, sentence-case Persian | «افزودن به سبد», «ثبت نرخ امروز» |
| Consistent synonyms | one word per concept everywhere: **سبد خرید** (cart), **سفارش** (order), **نرخ** (rate) — never «سبد خریــد»/«سبد» mixed, never «قیمت روز» for the rate | enforced in copy review |
| Stone vocabulary | «ماه‌سنگ» = the gemstone the shop sells (moonstone); «سنگ ماه تولد» = the monthly cycle that drives the accent (`DEC-050`) — never «سنگ ماه» for the gemstone, never «طالع»/«برج» for the cycle | «سنگ ماه» · «سنگ این ماه: یاقوت کبود — سپتامبر» — «ماه‌سنگ» is a stone, «سنگ ماه» is the monthly album, and months are named on the Gregorian calendar in Farsi + Latin (`DEC-053`) |
| Stone reference | the twelve stones' names and care lines exist once, in `design_system.md` §2.2 (`DEC-052`); the album, the chip, the filter labels and the admin stone field all read from it — a module never adds a thirteenth entry, renames a stone or reorders the Gregorian months | «ژوئن · June — مروارید و ماه‌سنگ · pearl & moonstone» |
| Empty/error copy | second person, no blame, states the next action | «هنوز محصولی در این دسته نیست؛ دسته‌های دیگر را ببینید.» |

## 5. Visibility and permissions

| Area | Visitor | Buyer (account) | Owner | Enforced in |
|---|---|---|---|---|
| storefront browse/home/policies | full | full | full | public |
| cart / checkout / payment | full (guest) | full (pre-filled) | full | public |
| order confirmation `/order/:code` | holder of the link/code | same | full | server (code = capability, anti-enumeration `DEC-021`) |
| `/track` | code + phone | code + phone | full | server |
| `/account/**` | redirect to login | own data only | full | server |
| `/admin/**` | admin login screen | denied | owner only | **server** (UI is not a boundary) |

Rule: navigation hides what a user cannot use **and** the server still enforces it — the UI is not
a security boundary.

## 6. Search, filtering and sorting

| Concern | Decision |
|---|---|
| Global search scope | products only (name + description, `FR-CAT-2`); no content/policy search in v1 |
| Search behaviour | dedicated results page `/search`; no typeahead dropdown in v1 (mobile-first simplicity, `UX-006`) — `[REC]` recorded `DEC-040` |
| Per-section filters | category pages: price range (computed, `BR-4`), weight, stone (همه / ماه‌سنگ / با سنگ / بدون سنگ — `DEC-051`); combinable AND |
| Sort defaults | newest first; options: price ascending/descending (computed price) |
| Empty search results | Farsi empty state + suggested categories (`UF-01` A2) |
| Result URL state | `?q=&price_min=&price_max=&weight=&stone=&sort=` — shareable, survives reload |

## 7. Responsive IA

| Area | Desktop ≥ 1280 | Tablet 768–1279 | Mobile < 768 |
|---|---|---|---|
| storefront nav | full header | full header | hamburger drawer + cart icon |
| storefront nav — secondary | — | — | track order + account inside drawer, footer keeps policies |
| category/product grids | 4-up | 3-up | 2-up |
| filters | side rail | collapsible rail | bottom sheet |
| checkout | 2 columns (form/summary) | 1 column + sticky summary | 1 column |
| admin nav | sidebar | collapsible sidebar | deferred (`ux_requirements.md` §7) |
| data-heavy views | tables | reduced-column tables | card list (if ever needed) |

## 8. IA change log

| Date | Change | Reason | Affected modules |
|---|---|---|---|
| 2026-09-20 | initial draft — storefront + admin maps, routes, naming, visibility | UX rounds 1–2 (`DEC-035`–`043`) | TBD (decomposition) |
| 2026-09-20 | screens specified — SCR-001…025 bound to these routes (`screens.md`); hero + admin login routes added | `screens.md`, `DEC-047` | TBD (decomposition) |
| 2026-09-21 | home gains the ماه‌سنگ band + سنگ این ماه chip; stone filter gains the «ماه‌سنگ» value; stone vocabulary rule added — **no new routes** (the band links to `/search?stone=moonstone`) | `DEC-050`, `DEC-051`, owner request | home / catalog / search modules (TBD) |
| 2026-09-21 | the ماه‌سنگ band gains the «دوازده سنگ ماه» explorer — twelve months rendered in place, static content, **still no new routes** and no catalog attribute beyond `DEC-051` | `DEC-052`, owner request | home module (TBD) |
| 2026-09-21 | the stone cycle runs on the **Gregorian** calendar (`DEC-053`): chip and album name the Gregorian month in Farsi + Latin; home's album tiles are the twelve Gregorian months | `DEC-053`, owner request | home / catalog / search modules (TBD) |
| 2026-09-21 | home's stone block is now the compact **سنگ ماه album** (twelve months, current one marked); the ماه‌سنگ band is removed from the homepage, the `?stone=moonstone` route stays valid as a filter on `/search` and `/category` | `DEC-052` (supersedes `DEC-051` clause a), owner request | home / catalog / search modules (TBD) |
