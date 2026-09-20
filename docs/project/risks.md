# Risks

> What could go wrong, and what we are doing about it. Owned collectively; reviewed by the
> Orchestrator Agent at every milestone.
>
> Rules
> * One row per risk, `RISK-###`, never renumbered.
> * Score `likelihood` × `impact` (1–5 each). `score ≥ 12` must have a mitigation owner and a
>   trigger for escalation to the human.
> * Risks that are really unverified beliefs belong in `docs/project/assumptions.md`; link them.
> * Agents may raise risks at any time; they may not silently accept a high risk.
> * Update `status` when a risk is mitigated, accepted, or materialised (a materialised risk
>   becomes a failure — see `docs/workflows/failure_recovery.md`).

## Risk register

| ID | Risk | Category | Likelihood | Impact | Score | Mitigation | Trigger / early warning | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|
| RISK-001 | Domestic payment gateway cannot be obtained/approved in time (owner has not applied yet) | product | 3 | 5 | 15 | owner applies NOW (OQ-001/ASM-001); architecture keeps the payment provider behind one integration boundary | no application filed by end of discovery; no account decision before decomposition gate | human | open |
| RISK-002 | Daily silver rate unavailable or wrong (DEC-016 makes it a hard dependency of every price) | product | 2 | 4 | 8 | manual owner entry in admin as v1 default (OQ-007 `[REC]`); rate changes are auditable; staleness warning in admin | a trading day starts with no rate entered and prices cannot be displayed | human + discovery | open |

Category: `product` · `technical` · `delivery` · `security` · `compliance` · `cost` · `quality`.
Status: `open` · `mitigating` · `accepted` · `closed` · `materialised`.

## Standard risks for agent-driven projects

| Risk | Symptom | Mitigation built into this template |
|---|---|---|
| Agent invents requirements | code implements behaviour nobody agreed | Discovery gate + `AGENTS.md` rule 2 + `open_questions.md` |
| Context starvation | agent works from half the specification | `tp.py context` layered context packs |
| Context pollution | agent follows irrelevant modules' details | narrow extraction by requirement/module ID |
| Two agents edit the same file | merge conflicts, broken ownership | one-owner rule + shared zones + `pr-check` |
| False "done" | tests pass, feature does not work | evidence-based DoD, review + integration agents |
| UX drift | implementation diverges from design | UX spec + visual validation loop |
| Stale agent | agent works from an outdated spec after a change | change management + context refresh + `handoff` |
| Silent assumption | agent builds on an unconfirmed belief | `assumptions.md` + escalation list |

## Detail

### RISK-001 — Payment gateway not obtainable in time
- **Description:** DEC-003/DEC-015 make online payment the only purchase path, but the
  owner has not yet applied for any domestic payment gateway (OQ-001, ASM-001).
- **Cause:** administrative lead time for merchant onboarding is outside the project's
  control and has not started.
- **Impact:** launch blocked or delayed; worst case, v1 degrades to manual payment — a
  major scope change.
- **Likelihood / impact:** 3 / 5 → **score 15** (escalation rule applies).
- **Mitigation:** owner files the application immediately (before architecture is final);
  Architecture Agent isolates the payment provider behind a single integration boundary so
  a late gateway choice does not ripple.
- **Contingency:** if approval drags, human decides via change request between waiting,
  manual-payment launch, or a different provider.
- **Owner:** human · **Status:** open · **Review date:** at every discovery round.

### RISK-002 — Daily silver rate missing or wrong
- **Description:** DEC-016 computes every product price from a daily silver rate; a missing
  or wrong rate breaks pricing store-wide.
- **Cause:** manual daily entry can be forgotten; an automated feed (if chosen later) can
  fail or disagree with the market.
- **Impact:** catalog prices cannot be displayed or are wrong → checkout disputes, refunds.
- **Likelihood / impact:** 2 / 4 → score 8.
- **Mitigation:** `[REC]` manual admin entry in v1 (OQ-007); admin shows a staleness warning;
  rate history is auditable.
- **Contingency:** last-known rate with explicit "rate of DATE" display until corrected.
- **Owner:** human + discovery · **Status:** open · **Review date:** at decomposition.
