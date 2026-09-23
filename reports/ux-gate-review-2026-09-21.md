# UX gate review — M1 UX specification (gate `gates.ux_approved`)

- **Report type:** review (gate readiness) — the frontend-ux role's own submission for the UX gate
- **Agent:** `frontend-ux` (Frontend/UX Agent) · **Date:** 2026-09-21
- **Artifact under review:** the whole UX specification — `docs/ux/*` (7 spec files + the rendered
  review build `style_tile.html`) — plus the decision records `DEC-050` … `DEC-053`
- **Baseline:** `main` @ `46692fd` (`chore(repo): point CODEOWNERS at the project owner`)
- **Working tree:** **uncommitted** — 8 modified files (`decisions.md`, `open_questions.md` and six `docs/ux/*` specs), plus 2 new: the review build `docs/ux/style_tile.html` and this report. Round 4–5 UX work; nothing staged, nothing else touched.
- **Verdict:** **PASS WITH NON-BLOCKING FINDINGS** — the specification is complete against the
  frontend-ux completion criteria; the gate decision is the human's (step 10)

---

## 1. Scope of this review

| Checked | Not checked (and why) |
|---|---|
| Completeness of the spec against the frontend-ux completion criteria (`docs/agents/agent_registry.yaml`) | Per-screen screenshots at 3 widths (`screens.md` §2.1 standard evidence) — no implementation exists yet; owed by the implementation module, see finding NB-3 |
| Internal consistency of the UX docs after rounds 4–5 (`DEC-050`–`053`) | Automated accessibility scan (axe) — nothing to scan until a module renders |
| The rendered review build (`docs/ux/style_tile.html`): tokens, twelve monthly accents, album, picker | Admin screens' rendered behaviour; admin is W2 and desktop-first (`DEC-037`) |
| Traceability UX → screens → flows | Module-contract `ux_refs` — no modules exist before decomposition (criterion is N/A today) |

## 2. Reference documents used

| Document | Section / IDs |
|---|---|
| `docs/ux/ux_requirements.md` | `UX-001`…`UX-012`, `UX-G-001`…`UX-G-011`, `UX-AC-*` |
| `docs/ux/screens.md` | `SCR-001`…`SCR-025`, §2 specification format, §2.1 standard evidence |
| `docs/ux/user_flows.md` | `UF-01`…`UF-05` + flow ACs |
| `docs/ux/information_architecture.md` | §2 site map, §4 naming rules, §5 visibility |
| `docs/ux/design_system.md` | §2.1 accent sets + rules 1–10, §2.2 twelve-stone reference, §7 theming |
| `docs/ux/interaction_patterns.md`, `docs/ux/visual_validation.md` | patterns, validation procedure |
| `docs/project/decisions.md` | `DEC-034` (requirements gate), `DEC-050`, `DEC-051`, `DEC-052`, `DEC-053` |
| `docs/project/open_questions.md` | `OQ-013` … `OQ-016` |
| `docs/agents/agent_registry.yaml` | frontend-ux `completion_criteria` |

## 3. Executed commands and their results

| Command | Result |
|---|---|
| `python scripts/tp.py validate` | `0 error(s), 0 warning(s), 0 module(s)` — exit 0 |
| `python scripts/tp.py status` | `stage discovery · milestone M0-bootstrap`; gates `requirements_approved=True`, `ux_approved=False`, `architecture_approved=False`, `decomposition_approved=False`; `open questions: 16 · risks: 11 · ready: none`; next action = “run the Frontend/UX Agent” |
| `python scripts/verify.py` | `Nothing is configured to run yet` — expected: `scripts/verify.config.yaml` is owned by the Architecture Agent (architecture phase) |
| Spec-completeness audit (script in Appendix A) | 25/25 screens carry Route + `Reqs` + states + responsive + keyboard + a11y + ACs; all 12 `UX-###` carry `UX-AC-*` (38 AC lines). Three screens had genuine gaps (`SCR-011` accessibility line, `SCR-013`/`SCR-015` state and a11y wording) — **fixed in this round**, re-run: `25 screens · gaps: none` |
| Rendered check of `style_tile.html` (document assertions in the preview) | 12 month tiles + 12-month strip render; `data-month-source` = `calendar` on a clean load; clicking آوریل applies `#33475B` + its swatch; chip reads «سنگ این ماه: یاقوت کبود — سپتامبر» (today = سپتامبر); picker stores `noghre.birthMonth`, a reload resolves **before paint** with `data-month-source="birth"`; `?month=3` outranks the stored month; storage blocked → warning + still-correct accent; console empty |

Audit criteria (per screen): Route · Reqs · all six states (`default`/`loading`/`empty`/`error`/`success`/`permission-denied`) · responsive · keyboard/focus · accessibility · acceptance criteria; per UX requirement: an ID plus at least one measurable `UX-AC-*`.

## 4. Gate criteria verification (frontend-ux completion criteria)

| Criterion | Verdict | Evidence |
|---|---|---|
| Every screen has all six states specified | PASS | audit above: 25/25 (screens with genuinely n/a states, e.g. the 404, say so explicitly) |
| Every UX requirement has measurable acceptance criteria and an ID | PASS | 12 `UX-###` sections, each with `UX-AC-*`; 11 global rows `UX-G-001…011`; 38 AC lines total |
| Responsive and keyboard/accessibility behaviour specified for each screen | PASS | audit: all 25 after this round's fixes; W2 screens reference shared admin patterns (`screens.md` §5) |
| Affected module contracts list the UX refs they must implement | N/A yet | no modules exist (`state/modules.yaml` empty; decomposition follows this gate) |
| Human approves the UX direction (`gates.ux_approved`) | **PENDING — this report** | §9 review script, §10 how to set the flag |

## 5. What is in the specification now

| Area | Count | Where |
|---|---|---|
| Screens specified | 25 (11 `must` W1 storefront incl. 404, 10 `must` W2 admin, 4 `should` W2 account) | `screens.md` |
| UX requirements | 12 detailed + 11 global | `ux_requirements.md` |
| User flows | 5 (`UF-01`…`UF-05`) with alternative and failure paths | `user_flows.md` |
| Design tokens / components | 30 token rows, 22 component specs, 12 accent sets, 12-stone reference table | `design_system.md` |
| Decision records | 53 (`DEC-053` latest) | `decisions.md` |

## 6. What changed in rounds 4–5 (owner-driven, since the spec was first written)

| Change | Record | Touches |
|---|---|---|
| Deep-green accent replaced by **the stone of the month** | `DEC-050` | tokens §2.1, chip, screens |
| Moonstone specialization: homepage band + product value + filter option | `DEC-051` | `SCR-001`, `SCR-002/003`, `SCR-021` |
| Homepage stone section became the **compact twelve-stone album** (band removed; clause (b) of `DEC-051` stands) | `DEC-052` (supersedes `DEC-051` a) | `SCR-001`, `UX-010`, `UX-012`, IA, `UF-01` |
| Stone cycle moved to the **Gregorian calendar**; months named in Farsi + Latin | `DEC-053` (supersedes `DEC-050` calendar clause) | tokens §2.1/§2.2/§7, chip, album, all copy examples |
| **Prototype** (not a decision): visitor birth month, pre-paint, `localStorage` | `OQ-015` + tokens rule 10 | `style_tile.html` §3 |

Reviewed together: no stale references remain to the removed band, to the Jalali mapping, or to the
old fallback colour (grep for `کاوش ماهسنگ`, `ماهسنگ band`, `فروردین`, `Jalali` returns only
historical change-log rows and the intentional “Jalali dates elsewhere” note).

## 7. Findings

| # | Severity | Area | Finding | Expected | Suggested fix | Owner |
|---|---|---|---|---|---|---|
| NB-1 | Non-blocking | `screens.md` | W2 screens (account + admin) are specified in compressed form — one-line states, cross-references like “as SCR-002”, ACs on a single line | Full detail is required per §2 before *their* implementation wave | Expand each W2 screen to the full format when its wave starts (not before — the format is uniform, only the density differs) | frontend-ux |
| NB-2 | Non-blocking | `screens.md` | Four screens under-specified the same concerns the gate criterion names: `SCR-011` (no accessibility line, states implied not named), `SCR-013`/`SCR-015` (state `n/a`s phrased loosely, `SCR-015` had no a11y line), `SCR-014` (no responsive/keyboard/a11y lines at all) | Every screen names states, responsive, keyboard and accessibility behaviour | **Fixed in this round** — all four now carry the missing lines in the file's wording | frontend-ux |
| NB-3 | Non-blocking | `visual_validation.md` §2.1 | No per-screen visual evidence exists (no app yet); the review build proves tokens and the accent cycle only | Screenshots at 320/768/1280 + 200 % zoom, axe scan, keyboard walkthrough per screen | Owed by the first implementation module; `visual_validation.md` is the procedure, unchanged | implementation |
| NB-4 | Non-blocking | `docs/project/project_state.md` | Stale: “Open questions 3” (index says 4 open), milestone/history tables do not mention rounds 4–5, `stage` still `discovery` | State narrative matches the spec at the milestone boundary | Orchestrator refreshes it when it records this gate (this report is the input) | orchestrator |
| NB-5 | Non-blocking | `design_system.md` §2.1/§7 | The birth-month override exists in the review build and in a prototype-tagged rule | It must not be bound to a token or a module before `OQ-015` is answered | Keep the `[PROTOTYPE]` tag; treat as unowned until the answer arrives | frontend-ux |
| Q-1 | Question | `OQ-016` | Does v1 ship one «ماهسنگ» stone value + filter option, or a `/moonstone` page / wider taxonomy? | An answer before decomposition | Recommended: option 1 (`[REC]` in the OQ); a bigger scope changes module sizing | human |
| Q-2 | Question | `OQ-013` | Font: Vazirmatn is what the review build renders — accept it as the working choice? | An answer so the token file has one family | Recommended: accept Vazirmatn for v1, revisit at launch | human |

## 8. Open questions — do they block the gate?

| OQ | Blocks the UX gate? | Blocks what instead |
|---|---|---|
| `OQ-013` font candidate | No — Vazirmatn is reviewed as the working choice | the token file's final family, any real typography |
| `OQ-014` product photography | No | launch content quality (`FR-ADM-1` photos) |
| `OQ-015` birth month vs calendar month | No — the calendar reading ships; the prototype documents option 2 | the accent module's behaviour (and its tests: cache, first paint, no-JS) |
| `OQ-016` ماهسنگ scope | No, but **answer it with the gate** — it changes v1 catalog scope and therefore module sizing | catalog attributes, filters, admin product form, IA/sitemap |

## 9. Owner review script (~5 minutes)

1. Open the review build: `docs/ux/style_tile.html` (Preview tab, or any browser).
2. §3 — click through several months: the accent, focus rings, buttons and chip follow the stone;
   the «سنگ این ماه» chip and the source line always say *why* this colour.
3. §3 — pick «ماه تولد شما», then reload: the colour must be right on the first paint (no flash),
   and «پاککردن» must return to the calendar month.
4. §6 — the twelve-stone album: every month named in Farsi + Latin with its stone; «این ماه» only on
   the current calendar month; nothing else interactive.
5. §2/§4 — base palette and type at your usual reading size; §7 — buttons, badges, the
   «ماهسنگ» filter chips.
6. Resize to a phone width (≈360 px) once — no horizontal scroll, nothing clipped.
7. Answer: (a) v1 ماهسنگ scope (`OQ-016`), (b) Vazirmatn as the working font (`OQ-013`), (c) whether
   the birth-month idea is worth pursuing (`OQ-015`), (d) **approve the UX direction or request
   changes**.

## 10. Verdict and next step

**Verdict: PASS WITH NON-BLOCKING FINDINGS (NB-1…NB-5, Q-1, Q-2).** Nothing blocks the UX gate; two
findings were fixed while writing this report and the rest are either wave-ordered or owned by other
roles.

**Human action:** set `state/project.yaml → gates: ux_approved: true` (the gate is human-owned; there
is no `tp.py gate` command — edit the flag and let the Orchestrator record it in
`docs/project/project_state.md`).

**Then:** the Architecture Agent (`agents/architecture/STARTER_PROMPT.md`) turns this spec plus the
approved requirements into `docs/project/architecture.md`, publishes the stack/hosting/payment
boundary ADRs, fills `scripts/verify.config.yaml` (today it is empty by design) and declares shared
zones — after which decomposition writes module contracts whose `ux_refs` point at the `UX-###` IDs
listed above. The first implementation module is also what owes the §2.1 visual evidence (NB-3).

---

## Appendix A — spec-completeness audit (reproduce with `python - <<'PY' … PY`)

```python
import re, pathlib
s = pathlib.Path('docs/ux/screens.md').read_text(encoding='utf-8')
blocks = [b for b in re.split(r'\n(?=### SCR-\d+)', s) if b.startswith('### SCR-')]
STATES = ['default','loading','empty','error','success','permission-denied']
gaps = []
for b in blocks:
    sid = b.split('\n')[0].split(' ')[1]
    low = b.lower()
    states = b.split('**States**')[1].split('**')[0].lower() if '**States**' in b else low
    ms = [x for x in STATES if x not in states]
    missing = [n for n, v in (
        ('reqs', '**reqs**' in low),
        ('responsive', 'responsive' in low),
        ('keyboard', 'keyboard' in low),
        ('a11y', 'a11y' in low or 'accessibility' in low),
        ('AC', bool(re.search(r'- \[ \] SCR-\d+-AC', b)) or '**acs**' in low),
    ) if not v]
    if ms: missing.append('states:' + ','.join(ms))
    if missing: gaps.append((sid, missing))
print(len(blocks), 'screens | gaps:', gaps or 'none')

# UX requirements: an ID plus at least one measurable acceptance criterion each
ux = pathlib.Path('docs/ux/ux_requirements.md').read_text(encoding='utf-8')
reqs = [r for r in re.split(r'\n(?=### UX-\d+)', ux) if r.startswith('### UX-')]
print('UX-###:', len(reqs), '| without ACs:', [r.split('\n')[0] for r in reqs if '- [ ] UX-AC-' not in r] or 'none')
```

Last run (2026-09-21, working tree above): `25 screens | gaps: none` and
`UX-###: 12 | without ACs: none`.
