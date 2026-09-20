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
| RISK-001 | Example: agent edits a shared file owned by another module | delivery | 3 | 3 | 9 | shared zones with single owners + `tp.py pr-check` | CI rejects the PR | orchestrator | open |

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

### RISK-001 — <risk title>
- **Description:**
- **Cause:**
- **Impact:** <!-- on product, users, schedule, cost, security -->
- **Likelihood / impact:** 3 / 3
- **Mitigation:**
- **Contingency:** <!-- what we do if it happens -->
- **Owner:** · **Status:** open · **Review date:** —
