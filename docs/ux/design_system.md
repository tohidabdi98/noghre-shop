# Design system

> Owned by the Frontend/UX Agent. Design-system decisions are **specified here first** and then
> implemented in the module that owns the design-system files. Implementation agents use these
> tokens and components; they do not invent colours, spacings or one-off components.
>
> Rule of thumb: if a value or a component appears twice, it belongs here; if it appears once, it
> belongs in the screen specification.

## 1. Principles

| # | Principle | Consequence for implementation |
|---|---|---|
| 1 | Consistency beats local cleverness | never style a control locally if a component exists |
| 2 | Hierarchy through spacing and weight before colour | fewer colour tokens, clearer layout (`PRIN-3`) |
| 3 | Colour is never the only signal | pair with icon/text/pattern (`UX-G-006`) |
| 4 | Motion explains, never entertains | short, interruptible, reducible |
| 5 | Accessible by default | AA contrast and keyboard support are part of each component's definition |
| 6 | Persian-native typography | generous line-height, Persian numerals for display, no Latin-font rendering of Farsi (`PRIN-4`) |

## 2. Tokens

> Tokens are the only sanctioned way to express these values. Implementation happens in the
> module owning the token file (declare it as a **shared zone** in `state/project.yaml`).

### Colour — silver base + stone-of-the-month accent (`DEC-045` base · accent `DEC-050` · calendar `DEC-053`)

| Token | Purpose | Light value | Contrast pair |
|---|---|---|---|
| `color.bg.canvas` | page background | `#FFFFFF` | with `color.text.primary` |
| `color.bg.subtle` | alternating sections, admin canvas | `#F6F6F7` | with `color.text.primary` |
| `color.bg.surface` | cards, drawers, menus, sheets | `#FFFFFF` | bordered or raised, never shadow-only |
| `color.text.primary` | body text | `#17171A` | ≥ 4.5:1 on canvas |
| `color.text.muted` | secondary text, rate dates, captions | `#6E6E76` | ≈ 5.1:1 on canvas |
| `color.border.default` | separators, card outlines | `#E5E5E8` | ≥ 3:1 against adjacent colours not required (decorative separator) |
| `color.border.strong` | field borders on hover, silver accents | `#C9C9CF` | ≥ 3:1 where it delimits a control |
| `color.on-accent` | text and icons on an accent fill | `#FFFFFF` | ≥ 5.8:1 on every monthly accent (§2.1) |
| `color.accent.default` | primary actions, links in body copy, active states | **current month's stone** (§2.1); fallback `#7E2A2E` (ژانویه · گارنت) | ≥ 5.8:1 on white for every month |
| `color.accent.hover` | hover / pressed | current month's stone (§2.1); fallback `#672226` | darker than `accent.default` by ≥ 15 % |
| `color.accent.subtle` | selected/active backgrounds, chips, badges | current month's stone (§2.1); fallback `#F2EAEA` | ≥ 15:1 with `color.text.primary` |
| `color.state.success` | positive confirmation | `#0F6B4B` (fixed — **never** the accent) | ≈ 6.5:1 on white; always with icon + text |
| `color.state.warning` | stale rate, stock warnings | `#A15C00` | ≈ 5.2:1 on white |
| `color.state.danger` | errors, destructive actions | `#B3261E` | ≈ 6.5:1 on white |
| `color.focus.ring` | focus indicator | `color.accent.default`, 2 px ring, 2 px offset | ≥ 3:1 against adjacent |

Photography is uncontrolled light content: text never sits directly on it — use a scrim or place text outside the image.

### 2.1 Accent = the stone of the month (`DEC-050`, calendar `DEC-053`)

The single accent is still **one accent at a time** (PRIN-3) — but which accent is no longer fixed:
it is the **stone of the month (سنگ ماه تولد)**, resolved at render time from the **Gregorian
calendar** (`DEC-053` — the calendar the birthstone convention itself is defined in): ژانویه = گارنت،
فوریه = آمیتیست، مارس = آکوامارین، آوریل = الماس، مه = زمرد، ژوئن = مروارید و ماه‌سنگ، ژوئیه = یاقوت
سرخ، اوت = زبرجد، سپتامبر = یاقوت کبود، اکتبر = اوپال، نوامبر = توپاز، دسامبر = فیروزه. Twelve accent
sets follow and are selected by `data-month="1…12"` on `<html>`, where `1` is ژانویه and `12` is
دسامبر. Raw stone colour is **decorative only**; the tokens are the accessible versions of those hues.

| Token | Purpose | Value |
|---|---|---|
| `theme.month` | the resolved month, `1`…`12` (Gregorian: `1` = ژانویه · January … `12` = دسامبر · December) | set as `data-month` on `<html>` |
| `color.accent.default` | primary fills, body links, active underline | month row → `accent` |
| `color.accent.hover` | hover / pressed | month row → `hover` |
| `color.accent.subtle` | selected/active backgrounds, chips, badges | month row → `subtle` |
| `color.accent.stone` | decorative only: stone swatch, album tile, month strip | month row → `swatch` |

| # | Gregorian month | Stone | `accent` | `hover` | `subtle` | on white | swatch (decorative) |
|---|---|---|---|---|---|---|---|
| 1 | ژانویه · January | گارنت · garnet | `#7E2A2E` | `#672226` | `#F2EAEA` | 9.3:1 | `#8E3038` |
| 2 | فوریه · February | آمیتیست · amethyst | `#5B3E9E` | `#4B3382` | `#EFECF5` | 8.0:1 | `#9C7FD8` |
| 3 | مارس · March | آکوامارین · aquamarine | `#16688C` | `#125573` | `#E8F0F4` | 6.2:1 | `#83C8DE` |
| 4 | آوریل · April | الماس · diamond | `#33475B` | `#2A3A4B` | `#EBEDEF` | 9.6:1 | `#E9EEF3` |
| 5 | مه · May | زمرد · emerald | `#0D6B4F` | `#0B5841` | `#E7F0ED` | 6.5:1 | `#2E9E76` |
| 6 | ژوئن · June | مروارید و ماه‌سنگ · pearl & moonstone | `#2F5D86` | `#274C6E` | `#EAEFF3` | 6.9:1 | `#DDE8F1` |
| 7 | ژوئیه · July | یاقوت سرخ · ruby | `#9B1C31` | `#7F1728` | `#F5E8EA` | 8.1:1 | `#C32F45` |
| 8 | اوت · August | زبرجد · peridot | `#5E6B12` | `#4D580F` | `#EFF0E7` | 5.9:1 | `#A8B63C` |
| 9 | سپتامبر · September | یاقوت کبود · sapphire | `#1B4A8A` | `#163D71` | `#E8EDF3` | 8.8:1 | `#2C5FB3` |
| 10 | اکتبر · October | اوپال · opal | `#7A3E82` | `#64336B` | `#F2ECF3` | 7.4:1 | `#C9A6CE` |
| 11 | نوامبر · November | توپاز · topaz | `#7A4E00` | `#644000` | `#F2EDE6` | 7.2:1 | `#DFA83C` |
| 12 | دسامبر · December | فیروزه · turquoise | `#0E6874` | `#0B555F` | `#E7F0F1` | 6.5:1 | `#45B6C2` |

Rules — binding for every storefront module:

1. **Resolution.** The month comes from the shop's date (`Asia/Tehran`) on the **Gregorian**
   calendar (`DEC-053`) as the page is rendered; `data-month="1…12"` on `<html>` selects the token
   block. Admin stays neutral (it never re-themes) — the accent is a storefront signal.
2. **Fallback.** The `:root` values *are* the ژانویه/گارنت set (month `1`), so markup rendered
   without a month is still valid and still ≥ 4.5:1. A failed month resolution is invisible to the
   user.
3. **No layout shift at rollover.** Only colour changes: no size, weight, radius or motion token may
   depend on the month (`UX-G-007`).
4. **Accessibility floor.** White text on `accent` is ≥ 4.5:1 in all twelve sets (minimum 5.85:1 —
   اوت · peridot; `subtle` carries `color.text.primary` at ≥ 15:1. Any new month entry must be
   contrast-computed before it is added to this table.
5. **States never follow the accent.** `success`, `warning` and `danger` are fixed. In مه (accent
   green ≈ success green), نوامبر (topaz ≈ warning amber) and ژانویه/ژوئیه/اکتبر (accent red and
   red-violet family ≈ danger red) the accent and the state colours are close in hue — the difference
   is carried by position, wording and icon, never by hue alone (`UX-G-006`).
6. **One accent.** No second decorative colour enters a screen; the raw `swatch` value may appear
   only as decoration (album tile, month strip) and never as text or control colour.
7. **Vocabulary.** «ماه‌سنگ» is the gemstone the shop sells; «سنگ ماه تولد» is this monthly cycle.
   Never call the gemstone «سنگ ماه» (ambiguous in Farsi).
8. **Preview override.** `theme.monthPreview` (owner/admin-only) forces a month for previews and
   screenshot tests, so visual baselines are never month-dependent by accident.
9. **Name the month, in Gregorian.** Anywhere the theme explains itself (chip, album tile, tooltip,
   admin preview) the month is written in Farsi + Latin Gregorian — «سپتامبر · September». A Jalali
   equivalent («≈ شهریور») may appear as secondary reference text beside it, never instead of it and
   never as the source of the theme (`DEC-053`).
10. **[PROTOTYPE — `OQ-015`, not part of the shipped theme.]** If `OQ-015` is answered option 2, a
   visitor may override the calendar accent with their own birth month: the preference is client-side
   only (`localStorage`, no cookie, never sent anywhere), read **before the first paint** by a small
   inline script in `<head>` that sets the same colour-only custom properties, with priority
   `?month=` pin → visitor month → calendar month and the resolution source recorded on `<html>` as
   `data-month-source`. The server still renders the calendar month, so the page is correct without
   JS, with storage blocked and from cache; the album's «این ماه» marker never follows the
   preference, and the chip says whose month is showing. Working prototype:
   `docs/ux/style_tile.html` (§3 picker).

### 2.2 The twelve stones — reference content (`DEC-052`, calendar `DEC-053`)

§2.1 decides *which colour* a month wears; this table is the **content** behind it — what the
month's stone is, why it belongs to that month, and how it behaves when it is set in silver. It is
the single source for the homepage stone album's tile labels (`SCR-001`), the «سنگ این ماه» chip
copy, the stone-filter labels (`SCR-002`, `SCR-003`) and the admin stone field (`SCR-021`).

**How much of a row is rendered where.** The homepage album shows only the short half — month,
its ≈ Gregorian month, and the stone in Farsi and Latin. The correlation, «در نقره» and care columns
are reference content: they may be rendered on a product page or a future per-stone surface, never as
a paragraph on the homepage (`DEC-052`).

**One month, one stone.** Since `DEC-053` the theme runs on the **Gregorian** calendar, so the
month *is* the stone's month: ژانویه = گارنت، فوریه = آمیتیست، مارس = آکوامارین، آوریل = الماس،
مه = زمرد، ژوئن = مروارید و ماه‌سنگ، ژوئیه = یاقوت سرخ، اوت = زبرجد، سپتامبر = یاقوت کبود،
اکتبر = اوپال، نوامبر = توپاز، دسامبر = فیروزه. Nothing is derived any more — the visitor's
birthday month and the theme's month are the same month (`DEC-050`, `DEC-053`). The Jalali
equivalent (e.g. ژوئن ≈ خرداد) is reference only, never a key.

| # | ماه میلادی (Gregorian) | سنگ | در نقره | سختی (موس) | نگهداری |
|---|---|---|---|---|---|
| 1 | ژانویه · January | گارنت · garnet | سرخِ تیره؛ روی نقره به نور یا قاب باز نیاز دارد تا خودش را نشان دهد | ۶٫۵–۷٫۵ | مناسبِ هر روز؛ فقط از ضربهٔ شدید دور شود |
| 2 | فوریه · February | آمیتیست · amethyst | بنفش؛ جفت کلاسیک نقره از قدیم | ۷ | در آفتابِ طولانی کم‌رنگ می‌شود؛ در جعبه نگه داشته شود |
| 3 | مارس · March | آکوامارین · aquamarine | آبیِ دریا؛ برای دیده‌شدن رنگش نگین بزرگ‌تر بهتر جواب می‌دهد | ۷٫۵–۸ | مقاوم؛ در آفتابِ طولانی کم‌رنگ می‌شود |
| 4 | آوریل · April | الماس · diamond | درخشش سفید و بی‌رنگ؛ با جلاهای نقره یکدست می‌شود و در قطعات نقره معمولاً نگین ریز است | ۱۰ | مقاوم؛ سالی یک‌بار نشستن گیره‌ها بررسی شود |
| 5 | مه · May | زمرد · emerald | سبزِ عمیق روی نقرهٔ سفید پرکنتراست و گرم‌تر دیده می‌شود | ۷٫۵–۸ | شکننده؛ اولتراسونیک و مواد شیمیایی ممنوع، فقط دستمال نرم |
| 6 | ژوئن · June | مروارید و ماه‌سنگ · pearl & moonstone | درخشش آبی و پولکیِ ماه‌سنگ روی نقرهٔ صیقلی بیش از هر فلزی جلوه می‌کند؛ مروارید جفت کلاسیک نقره است | ۶–۶٫۵ (مروارید ۲٫۵–۴٫۵) | دور از مواد شیمیایی، عطر و ضربه؛ شست‌وشو با دستمال نرم و آب پاک |
| 7 | ژوئیه · July | یاقوت سرخ · ruby | سرخِ عمیق روی نقرهٔ سفید بیشترین کنتراست را می‌سازد | ۹ | مقاوم؛ با مسواک نرم و آب گرم و صابون ملایم تمیز شود |
| 8 | اوت · August | زبرجد · peridot | سبز-زردِ روشن؛ درخشش دوگانه‌اش با سفیدی سرد نقره جفت می‌شود | ۶٫۵–۷ | به تغییر دمای ناگهانی و ضربه حساس است؛ اولتراسونیک ممنوع |
| 9 | سپتامبر · September | یاقوت کبود · sapphire | آبیِ درخشان روی نقرهٔ سفید؛ جفت کلاسیک و همیشگی | ۹ | مقاوم؛ آب گرم و صابون ملایم کافی است |
| 10 | اکتبر · October | اوپال · opal | بازیِ رنگ اوپال روی پس‌زمینهٔ روشنِ نقره بیشتر دیده می‌شود | ۵٫۵–۶٫۵ | رطوبت‌دوست؛ از خشکی، حرارت و مواد شیمیایی دور بماند |
| 11 | نوامبر · November | توپاز · topaz | طلایی-کهربایی؛ تضاد گرم و سرد با نقره می‌سازد | ۸ | به ضربهٔ کناری و تغییر دمای ناگهانی حساس است |
| 12 | دسامبر · December | فیروزه · turquoise | فیروزهٔ نیشابور؛ سنگِ مادرِ ایران که در نقره یک جفت تاریخی است | ۵–۶ | متخلخل و جاذب؛ با آب، عرق و چربی رنگ می‌گیرد — خشک و دور از شوینده |

Rules — binding wherever these twelve entries are rendered:

1. **One copy.** The names, the correlation line, the «در نقره» line and the care line live only in
   this table. The album, the chip, the filter labels and the admin field read from it — never
   from a second hard-coded list (`DEC-052`).
2. **Always name the month.** Every rendering names the Gregorian month in Farsi and Latin
   («سپتامبر · September») — a bare stone name, or a Jalali month presented as the stone's month, is
   not allowed (`DEC-053`).
3. **Text first.** Every entry carries its Farsi name *and* its Latin name as text; the stone swatch
   is `aria-hidden` decoration from §2.1 and never the only carrier of identity (`UX-G-006`).
4. **No mysticism.** The content is gem knowledge and care, in warm-polite Farsi (`DEC-046`) — no
   طالع‌بینی, no fortune, luck or health claims, and no gemological jargon (say «درخشش پولکی», not
   «ادولِسانس»).
5. **No stone is privileged.** All twelve entries carry the same weight and the same detail (the album
   tiles are identical in shape). ژوئن is the month whose stone is ماه‌سنگ — that is enough for the
   shop's speciality to be visible; a «تخصص فروشگاه» marker, badge or accent on that entry is not
   allowed (`DEC-052`).
6. **Care lines are jewellery fact, not a product promise.** They never claim a specific listed item
   is water- or shock-proof.

### Typography

Font stack (working `[REC]`, final choice = `OQ-013`): `"Vazirmatn", "IRANSansX", "Estedad", "Tahoma", system-ui, sans-serif` — swapping families is a one-line token change, sizes stay.

| Token | Size / line-height | Weight | Use |
|---|---|---|---|
| `text.display` | 36 px (28 mobile) / 1.35 | 700 | hero headline, rare |
| `text.title` | 24 / 1.4 | 600 | page titles (h1) |
| `text.section` | 20 / 1.5 | 600 | section headings (h2/h3) |
| `text.body` | 16 / 1.8 | 400 | default text — Persian needs the generous line-height |
| `text.body-strong` | 16 / 1.8 | 600 | emphasis, price basis lines |
| `text.label` | 14 / 1.6 | 500 | control labels, navigation |
| `text.caption` | 12 / 1.6 | 400 | helper text, rate dates, badges |
| `text.price` | 18 / 1.5 | 600 | amounts (Persian digits, see §5) |

No text below 12 px; no weight below 400 for Farsi (thin weights break at small sizes).

### Space, radius, elevation, motion

| Scale | Values |
|---|---|
| `space` | 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 px (multiples of 4 only) |
| page gutters | 16 px mobile · 24 px tablet · 32 px desktop; max content width 1200 px; reading measure ≈ 70ch |
| `radius` | `sm` 6 (inputs, chips) · `md` 10 (buttons, cards) · `lg` 16 (panels, sheets) · `pill` 999 |
| `elevation` | `flat` (borders only — default) · `raised` 0 1 3 rgb(23 23 26 / 8%) (dropdowns, toasts) · `overlay` 0 12 32 rgb(23 23 26 / 16%) (drawer, modal) — never for decoration |
| `motion.duration` | fast 120 ms · base 200 ms · slow 320 ms |
| `motion.easing` | standard ease-out; entrance decelerate; exit accelerate; `prefers-reduced-motion` ⇒ no transform/parallax, opacity only |

## 3. Brand mark (`DEC-044`)

| Concern | Specification |
|---|---|
| Wordmark | «نقره‌شاپ» set in the design-system font at weight 700 (`text.section` scale and up); never re-typed in another font, never outlined |
| Geometric motif | ingot outline + ring, 24 px grid, 2 px stroke, geometric (no calligraphy imitation) — used alone as favicon/app icon |
| Lockup | horizontal: motif inline-start + wordmark; monochrome `color.text.primary`, accent allowed for the motif only |
| Minimums | wordmark cap-height ≥ 20 px; mark ≥ 24 px; clearspace = motif height on all sides |
| Backgrounds | works on canvas and subtle backgrounds; no gradients, shadows or effects |
| Favicon | motif alone, 32 px, same stroke weight scaled optically |

## 4. Components

| Component | Purpose | Variants | States to implement | Owner module | A11y notes |
|---|---|---|---|---|---|
| Button | trigger an action | primary / secondary / ghost / danger | default, hover, focus, active, loading, disabled | TBD | keyboard; ≥ 44 px storefront / ≥ 24 px admin target; loading keeps width |
| IconButton | compact action (cart, close, copy) | plain / bordered | as Button | TBD | always `aria-label` in Farsi |
| Input / Textarea | text entry | text / tel / email / search / textarea | default, focus, filled, invalid, disabled, readonly | TBD | label always visible; error text linked; `dir=ltr` for phone/code |
| Select | choose one of many | native (v1 — cheapest, accessible) | as Input + open | TBD | native keyboard model |
| Checkbox | binary choice (filters, «سنگ دارد») | — | default, checked, indeterminate, invalid | TBD | label is the click target |
| FilterChip | active filter | removable / static | default, selected, focus | TBD | removal announced |
| Badge | status text (موجود / ناموجود / order status) | neutral / success / warning / danger | static | TBD | text-first, never colour-only |
| PriceLine | **the** price display: amount + basis «وزن × نرخ روز + اجرت» + rate date | full / compact (cards) / summary (totals) | fresh · stale (+ note) · no-rate (disabled + message) | TBD | amount + date announced as one statement (`UX-AC-001.3`) |
| RateChip | homepage silver-rate line | default / stale | hidden when no rate ever | TBD | real text, ≥ 4.5:1, `text.caption` |
| ProductCard | grid item | default / unavailable | default, hover, focus, unavailable | TBD | single focusable link; stock as text |
| Gallery | multi-photo product view | storefront / admin preview | default, zoom open, broken-image placeholder | TBD | thumbs roving tabindex; zoom dialog traps focus; swipe respects RTL (`UX-AC-005.2`) |
| Drawer | cart / mobile menu | inline-end (cart, RTL left) / start (menu) | open, closing, focus-trapped | TBD | `Esc` closes, focus returns to trigger |
| BottomSheet | mobile filters | — | open, closing | TBD | focus trap + restore |
| Dialog / ConfirmDialog | focused decision, destructive confirm | info / destructive | open, loading, error, closing | TBD | names object + consequence; typed confirm only if no undo |
| Toast | transient confirmation + undo | neutral / success / error | enter, pause on hover/focus, dismiss | TBD | polite live region; 5 s auto-dismiss |
| Banner | persistent state (missing rate, degraded mode) | info / warning / danger | static, dismissible where appropriate | TBD | never dismissible when it hides a required action (rate banner) |
| Timeline | order status (3 states, forward-only) | storefront / admin | current, past, future | TBD | ordered list semantics; text + shape |
| Table | admin collections | full / reduced-column | default, loading, empty, error, row-focus | TBD | scoped headers; row acts as link with visible focus |
| Pagination | «نمایش بیشتر» (storefront) / page controls (admin) | — | default, loading, exhausted | TBD | button announces appended count |
| Tabs | admin page editor sections | underline | default, active, disabled | TBD | roving tabindex |
| Uploader | product/policy images (multi, ordered) | drop zone / list | empty, uploading, error, reorder | TBD | reorder has keyboard controls, not drag-only |
| Skeleton | layout-matching loading | per-block | static | TBD | `aria-busy`, no fake data |
| EmptyState | explain absence | inline / full-page | — | TBD | heading + one action (`interaction_patterns.md` §10) |

**Component definition of done:** variants and states implemented · keyboard operable · focus visible · labelled for assistive tech · contrast verified · documented in the component catalogue · used (not re-implemented) elsewhere.

## 5. Icons and imagery

| Concern | Decision |
|---|---|
| Icon set | stroke-based 24 px grid, 1.5–2 px stroke; Lucide (ISC) as the base set `[REC]`, vendored as inline SVG components — no icon-font dependency (DEC-030). Custom additions only when a concept is missing |
| Sizing | 16 / 20 / 24 px optical sizes; icon-only controls get ≥ 44 px (storefront) / ≥ 24 px (admin) hit areas |
| RTL mirroring | directional glyphs (chevrons, arrows, back, progress) mirror; identity marks (logo motif) never mirror (`UX-AC-005.2`) |
| Decorative vs meaningful | decorative icons `aria-hidden`; meaningful icons always carry a Persian text label or `aria-label` |
| Contrast | icons convey status only together with text (`UX-G-006`) |

### 5.1 Product photography guide (`OQ-014`)

| Concern | Rule |
|---|---|
| Aspect & framing | **1:1** product photos everywhere (grid, gallery, admin). Hero: 16:9 desktop, 4:5 mobile crop. Item occupies ≈ 80 % of frame |
| Background & light | seamless light neutral (`#F2F3F5` or white), soft even lighting, no props that compete (`PRIN-3`); shadows soft and short |
| Per product | 3–5 photos recommended; **≥ 1 required** to activate a product. First photo = cover (straight-on front). Sequence: front → angle → detail (hallmark/clasp) → scale/context (optional) |
| Silver bars (`DEC-038`) | straight-on front; at least one photo where the hallmark and purity stamp are legible; weight/purity details live in the description; no stone/wear shots |
| Source quality | ≥ 1600 × 1600 px, JPG/PNG/WebP; no watermarks, no text overlays; naming `{slug}-{n}.webp` |
| Web delivery | responsive sizes served per breakpoint; below-the-fold lazy loading; fixed aspect box prevents layout shift (`UX-G-007`) |
| Owner hand-off | this table *is* the SC-2 photography checklist — usable by a phone camera and a rented lightbox |

## 6. Content and tone (`DEC-046`)

| Concern | Rule |
|---|---|
| Voice (storefront) | warm-polite Persian: always «شما», short plain sentences, no stiff bureaucratic register, no over-familiarity |
| Voice (admin) | plain functional Farsi, no jargon (`PRIN-6`) |
| Action labels | verb + object, sentence case: «افزودن به سبد خرید»، «ثبت نرخ امروز» — never bare «ثبت» / «باشه» |
| Error copy formula | what happened → what to do → how to recover, second person, no blame, no codes (`UX-G-003`) |
| Numbers | Persian digits (۰–۹) for every customer-facing number; amounts use the «٬» thousands separator + «تومان»; rate unit always «تومان/گرم»; phone inputs accept both digit sets, display canonically Persian |
| Dates | Jalali calendar, e.g. «۲۰ شهریور» (add year when space allows); admin logs may use relative recency («۲ دقیقه پیش») with the absolute value on hover/focus |
| Order codes | Latin letters + digits; rendered inside `<bdi>` (LTR isolate) everywhere they appear in RTL text (`UX-G-009`) |
| Localisation readiness | no concatenated strings; text never baked into images; one word per concept: **سبد خرید** · **سفارش** · **نرخ** (never synonyms) |

## 7. Theming and platform

| Concern | Decision |
|---|---|
| Accent theming (`DEC-050`, calendar `DEC-053`) | the accent is the current **Gregorian** month's stone, applied as CSS custom properties from `<html data-month>` (`1` = ژانویه … `12` = دسامبر); all other tokens are month-independent |
| Month source / override | `theme.monthSource` = `gregorian` (default, `DEC-053`) · `jalali` (kept only for an owner preview/override experiment — it is not the shipped theme); `theme.monthPreview` forces a month for owner previews and screenshot tests (never linked publicly) |
| Visitor birth month (**prototype only**, `OQ-015`) | `theme.birthMonth` — a client-side override read from `localStorage` before first paint (priority: pin → visitor → calendar, source on `<html data-month-source>`). **Not a shipped token**: do not bind it to a module until `OQ-015` is answered (§2.1 rule 10) |
| Month rollover & caching | the attribute is set server-side so the first paint is already correct; if HTML is cached, key the cache by month **or** set the attribute with a tiny pre-paint inline script — colour-only, so no layout shift either way |
| Dark mode | **not now** — v1 ships light only; all colour tokens are semantic, so a dark theme is an additive change later |
| Density | comfortable by default; admin tables may gain a compact toggle later (change request) |
| Platform differences | responsive web only (no native app, `DEC-003`); storefront touch-first, admin mouse/keyboard-first (`DEC-037`); social webviews are first-class test targets (Instagram/Telegram) |
| Design-tool source of truth | **this file** — there is no Figma file; the token tables and component definitions are the contract |

## 8. Governance

- **Changing a token or component** is a UX decision: the Frontend/UX Agent records it, updates this file and its change log, and lists affected modules. Interface changes consumed by others go through `docs/workflows/change_management.md`.
- **Adding a component** requires: a use case, a screen reference, its states table, and a11y notes.
- **Design-system version** tracks in `state/project.yaml` and follows the release version; breaking token renames become `ADR-###` when they force module changes.
- **Refactor rule:** when a second screen needs a one-off style, it becomes a component here *before* the second implementation — not after.

## 9. Change log

| Date | Change | By | Affected modules |
|---|---|---|---|
| 2026-09-20 | initial system — palette (`DEC-045`), type ramp with Persian line-heights, spacing/radius/elevation/motion, brand mark spec (`DEC-044`), 24 components, photo guide (`OQ-014` input), content rules (`DEC-046`) | frontend-ux | — (bind at decomposition) |
| 2026-09-20 | review artifact added: `docs/ux/style_tile.html` (renders this system's palette, type, brand mark, PriceLine and component samples for owner review) | frontend-ux | — |
| 2026-09-21 | **accent replaced**: deep green → **stone of the month** — twelve Jalali-month accent sets, all ≥ 5.9:1 with white text, plus month-resolution, fallback, caching and accent-vs-state rules (`DEC-050`); `color.state.success` decoupled from the accent; `color.on-accent` added | frontend-ux | all storefront modules (token file, shared zone) |
| 2026-09-21 | homepage «کاوش ماه‌سنگ» band, «سنگ این ماه» chip and the ماه‌سنگ filter/product value specified (`DEC-051`) — screens `SCR-001`, `SCR-002`, `SCR-003`, `SCR-021`; vocabulary rule added (§2.1 rule 7) | frontend-ux | home/catalog/admin modules (TBD) |
| 2026-09-21 | **§2.2 added**: the twelve stones as reference content (appearance in silver, Mohs, care) plus six binding rules, and the note on how much of a row each surface renders — the homepage album shows month + stone names only (`DEC-052`, and see §2.1 rule 7 for vocabulary) | frontend-ux | home/catalog/admin modules (TBD) |
| 2026-09-21 | prototype (not a decision): visitor birth-month accent in `style_tile.html` — pre-paint `<head>` resolver, `localStorage` preference, priority pin → visitor → calendar, `data-month-source`, calendar-only album marker (§2.1 rule 10, §7 row, `OQ-015`) | frontend-ux | owner asked to prototype `OQ-015` option 2 |
| 2026-09-21 | **calendar switched to Gregorian** (`DEC-053`): the accent and the homepage album are keyed by the Gregorian month (`data-month` `1` = ژانویه … `12` = دسامبر), stone↔month is direct (no derived dominant-month mapping — §2.2's «جفتشدگی» column is gone), the `:root` fallback is ژانویه/گارنت, rule 9 requires the Gregorian month to be named in Farsi + Latin, and §7 defaults `theme.monthSource` to `gregorian` — accent values unchanged, contrast re-verified (min 5.85:1 with white) | frontend-ux | all storefront modules (token file, shared zone) |
