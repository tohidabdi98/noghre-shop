# Interaction patterns

> Owned by the Frontend/UX Agent. Reusable answers to recurring interaction questions, so that
> implementation agents do not each invent their own. Each pattern states the **default** and when
> it is *not* appropriate. Deviating requires a UX decision recorded here.
>
> These patterns are binding across the storefront (W1) and admin (W2); screen specs reference
> them instead of restating them.

## 1. Feedback

| Situation | Pattern | Notes |
|---|---|---|
| action < 300 ms | no indicator | avoid flicker |
| action 300 ms – 10 s | inline progress on the triggering control | button size stays stable; skeleton for content |
| action > 10 s | labelled progress + cancel/retry | never an indefinite spinner (`UX-G-004`) |
| price/total refresh in flight | inline shimmer on the number only | never shift the layout under the finger |
| add to cart | drawer opens immediately + toast «به سبد خرید افزوده شد» | optimistic UI; failure surfaced inline |
| payment redirect | full-page progress + «صفحه را نبندید» | the one place a full-page state is correct (`UX-009`) |
| destructive success | confirmation naming the object + undo where feasible | never a bare «انجام شد» |
| background email send | non-blocking note in admin («در صف ارسال») + failure visible (NFR-OBS-1) | order status never waits on email (`UF-04-AC4`) |

## 2. Forms

| Concern | Default |
|---|---|
| Validation timing | on blur; re-validate on change once invalid; never on first focus |
| Error placement | inline beside the field; error summary at the top when submit fails or ≥ 3 errors |
| Error copy | what happened → what to fix → how to recover, in Farsi, no codes (`UX-G-003`) |
| Required fields | marked; only the four checkout fields (+ optional email) are required anywhere (`FR-CHK-1`) |
| Preservation | never clear input on failure — including payment failures (`DEC-014`) |
| Submit | disabled only while in flight; never disabled as validation theatre — press it and see the errors |
| Labels | always visible; placeholders are examples, never labels (`UX-007`) |
| Phone / order-code inputs | `dir="ltr"`, `inputmode="numeric"` / `"text"`; accept Persian and Latin digits; display canonically Persian (phones) / Latin (codes) |
| Promo code | labelled disclosure in checkout («کد تخفیف دارید؟»); rejection leaves the total unchanged and states the reason |
| Admin saves | inline saved-state + toast; button re-enables; no full-page reload |

## 3. Navigation and layout

| Concern | Default |
|---|---|
| Page transitions | skeletons matching final layout; chrome stays stable (`UX-006`) |
| Back/forward | browser history always works; cart drawer opens/closes **without** polluting history; closing a drawer never navigates |
| URL state | storefront filters/sort/search and admin table page+filters live in the URL — shareable and reload-safe (IA §6) |
| Unsaved changes | admin forms confirm before leaving: «ماندن / دور ریختن / ذخیره» |
| Scroll restoration | list → detail → back restores list position |
| Modals vs pages | dialog = one focused decision ≤ 3 fields; anything bigger gets a page (checkout is a page, `DEC-041`) |
| Mobile drawers | cart slides from inline-end (left in RTL); menu from start; focus trapped, `Esc`/backdrop closes, focus returns to trigger |
| RTL rails | nothing uses physical left/right; all layout via logical properties (`UX-G-008`) |

## 4. Destructive and irreversible actions

| Item | Default |
|---|---|
| Confirmation | required, naming the object and the consequence (`UX-AC-007.2`) |
| Confirmation strength | typed confirmation only for unrecoverable data loss — **does not occur in v1** |
| Undo window | 5 s toast-undo for cart line removal; admin actions confirm instead of undo |
| Admin destructive set | deactivate/retire product · delete promo code · clear featured design — each confirms and names what stays intact («سفارش‌های قبلی تغییر نمی‌کنند») |
| Not destructive, never confirmed | advancing order status (forward-only, `BR-2`); recording today's rate (latest wins, audited) |
| Irreversible reference point | leaving for the gateway is the single irreversible step; everything before it returns intact (`UX-009`) |
| Agent rule | destructive UX changes require human approval (`docs/workflows/human_in_the_loop.md`) |

## 5. Keyboard

| Pattern | Default |
|---|---|
| Overlays | `Esc` closes the top-most layer only (drawer, sheet, dialog, zoom); focus returns to the trigger |
| Storefront entry | skip-link → header → main content; visible focus ring on every interactive element (`UX-G-001`) |
| Forms | `Enter` submits single-page forms (checkout included); error summary receives focus on failed submit |
| Lists and grids | Tab moves card-to-card in visual RTL order; galleries use roving tabindex + arrow keys advancing right → left (`UX-AC-005.2`) |
| Quantity steppers | `↑`/`↓` (or `+`/`−`) change value, value change announced |
| Admin tables | row focus visible; `Enter` opens the row; page controls operable |
| Dialogs | trap + restore focus; destructive confirm's cancel button is the initial focus |
| Global shortcuts | **none in v1** — social webviews steal keys; every action has a visible control instead |
| Focus moves | never silent except: navigation, overlay open/close, error summary, and result-count announcements |

## 6. Notifications and messaging

| Kind | Placement (RTL) | Persistence | Use |
|---|---|---|---|
| inline | next to the trigger | transient | field errors, promo rejection, per-section retries |
| banner | top of the page | until resolved | admin missing-rate banner; degraded-mode notices |
| toast | bottom inline-start (left in RTL) | auto-dismiss 5 s, paused on hover/focus | add to cart, saved, removed + undo, copy code |
| live-region announcements | — | one polite announcement per event | totals changed, results count, status advanced, reservation expired |
| email | out of band | order events when email exists | never the only channel: on-site status always exists (`DEC-012`, `DEC-021`) |
| notification centre | — | **not in v1** (not in requirements) | revisit via change request |

## 7. Lists, search and filtering

| Concern | Default |
|---|---|
| Storefront grid paging | «نمایش بیشتر» button, 24 per page; count announced after append; no infinite scroll |
| Admin tables | explicit page controls; status filters in the URL |
| Search | dedicated `/search` page (no typeahead, `DEC-040`); results after `Enter`; query + filters shareable |
| Filters | combinable AND; active filters visible as removable chips; empty results state **which** filter excluded everything |
| Empty vs zero | distinguish «هنوز محصولی ثبت نشده» (never existed) from «با این فیلترها چیزی نیست» (filtered out) |
| Sorting | one documented default per list (newest first); storefront options: آن‌ترین/ارزان‌ترین/گران‌ترین; no silent per-session memory |
| Bulk actions | **none in v1** — not in requirements; admin list actions stay per-row |

## 8. Data display

| Concern | Default |
|---|---|
| Money | Persian digits + «٬» + «تومان»; rate as «تومان/گرم»; never a bare number without its unit |
| Order codes | Latin, LTR-isolated, never truncated or wrapped mid-code; one-tap copy with confirmation |
| Dates | Jalali («۲۰ شهریور»), absolute for precision; admin may add relative recency with absolute on hover/focus |
| Tables | numeric columns aligned to the reading edge (right in RTL); consistent units |
| Status | text + shape/icon; colour is never the only carrier (`UX-G-006`) |
| Charts | none in v1 — sales overview is counts and totals only (no fake graphs) |
| Long values | truncate with reveal (tooltip) except order codes and prices, which never truncate |

## 9. Errors and degraded states

| Kind | Presentation | Must include |
|---|---|---|
| field error | inline + summary | cause, correction, preserved input |
| section failure (storefront) | section-level retry line; the rest of the page lives (`UX-AC-010.4`) | retry, what was lost (usually nothing) |
| admin save failure | message + retry; form state intact, no partial writes | what failed, retry, safe fallback |
| permission | admin → SCR-016 redirect; account → login with return URL; non-judgemental copy | why, how to continue |
| offline / weak connection | global banner when detached; submit controls disabled with reason; cart persists locally (`UF-02-AC4`); no offline write queue in v1 | what is queued, what is not |
| payment failure | intact checkout + reason + retry (`DEC-014`) | retry, preserved data, cancellation path |
| rate staleness | storefront: last-known price + date + note; admin: persistent banner until resolved | the date of the rate in use |
| unexpected error | friendly Farsi message + copyable reference id | correlation id for support |

## 10. Price, rate and totals (project-specific)

| Concern | Default |
|---|---|
| Every price | rendered via the **PriceLine** component: amount + basis «وزن × نرخ روز + اجرت» + rate date (`UX-AC-001.1`) |
| Cart totals | labelled «جمع سبد (بر پایه نرخ {تاریخ})» — an estimate, never presented as final |
| Checkout totals | same structure + note that the final amount is computed at payment (`DEC-020`) |
| Payment step | final total + basis + rate-at-payment date; any change from checkout start is stated explicitly, never silent (`UX-AC-009.1`) |
| Stale rate | shopping continues; last-known rate + its date + unobtrusive note; tone calm, never alarming on the storefront |
| No rate ever | prices are not shown as amounts; buying is blocked with a Farsi explanation (`FR-RATE-1`) |
| Promo code | applies on top of the rate-computed total; rejection never mutates the displayed total |

## 11. RTL and bidi (project-specific)

| Concern | Default |
|---|---|
| Document | `dir="rtl"` + `lang="fa"`; all layout via logical properties (`UX-G-008`) |
| Mixed-direction text | order codes and phone numbers wrapped in `<bdi>`; Latin tokens never split lines mid-code (`UX-G-009`) |
| Directional icons | chevrons/arrows/back/progress mirror; identity marks never mirror |
| Carousels / galleries | advance in reading direction: swipe/arrow right → left (`UX-AC-005.2`) |
| Drawers | cart from inline-end (left), menu from start (right); focus order follows visual RTL order |
| Progress / steps | timelines read right → left (پرداخت‌شده begins at the inline-start edge) |
| Numerals | Persian digits for display; inputs accept both digit sets and normalise |

## 12. Onboarding and empty starts

| Concern | Default |
|---|---|
| Storefront first run | no onboarding, no tour; the homepage teaches by structure (`UX-010`) |
| Admin first run | empty states point to the first real action in order: ثبت نرخ → افزودن محصول → انتخاب طرح ماه (each is a link) |
| Sample content | **none** — the store is real; never insert placeholder products |
| Empty states | always teach the next action (`screens.md` per-screen copy); never a dead end |
| Returning user | nothing repeats; deep links land where intended (`DEC-021` email links) |

## 13. Change log

| Date | Pattern | Change | By |
|---|---|---|---|
| 2026-09-20 | initial | feedback, forms, navigation, destructive, keyboard, notifications, lists, data display, errors, price/rate, RTL/bidi, empty starts | frontend-ux |
