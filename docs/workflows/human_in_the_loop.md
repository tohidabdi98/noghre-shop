# Human in the loop

Agents are autonomous for ordinary engineering work and **must** stop for consequential decisions.
This file defines exactly where the line is, so agents neither interrupt needlessly nor decide
things that are not theirs.

## 1. Decision rights

| Decision | Human | Agent | Notes |
|---|---|---|---|
| What the product should do | **decides** | recommends | discovery records it; never invented by an agent |
| Scope, priorities, milestones | **decides** | recommends | scope creep is the most common agent-driven failure |
| UX direction (primary flows, navigation, established behaviour) | **decides** | proposes alternatives | must be discussed before implementation |
| Architecture with material trade-offs | approves | decides + ADR | escalate when >1 defensible option or cost/compliance impact |
| Technology/dependency choices | approves new run-time deps | decides dev tooling | dependency policy in `conventions.md` |
| Security model, crypto, permissions, secrets | **decides** | proposes | non-negotiable escalation |
| Destructive data changes, migrations with data loss | **decides** | prepares + rollback plan | never executed without approval |
| Public/cross-module interface changes | approves | proposes | contracts are coordination |
| Module boundaries | approves at decomposition | proposes/adjusts | re-decomposition after implementation = change request |
| Internal code structure, names, tests, refactors in-scope | — | **decides** | document as `[DECISION]` when non-obvious |
| Test strategy inside policy | — | decides | must satisfy `definition_of_done.md` |
| Formatting, linting fixes, documentation typos | — | decides | no ceremony |
| Merging a PR | **yes** | never | agents open PRs; humans merge |
| Releasing / publishing / deploying | **decides** | prepares | `gates.release_approved` |
| Cancelling a module, force-validating, reopening complete work | **yes** | never | human-only state transitions |
| Spending money / new external service | **decides** | proposes | includes free tiers with obligations |
| Anything that cannot be undone | **decides** | proposes | reversibility is the default preference |

## 2. Mandatory escalation triggers

An agent **must stop and ask** when any of these is true:

1. A requirement is ambiguous, contradictory, or missing and the answer affects behaviour.
2. Two acceptance criteria cannot both be satisfied.
3. More than one defensible architecture/approach exists with material cost to change.
4. The work touches auth, crypto, secrets, permissions, or personal data.
5. The change is destructive or irreversible (data, infrastructure, external effects).
6. A public or cross-module interface would break.
7. Scope would grow (new module, new service, new milestone, paid resource).
8. The UX direction of a primary flow or established behaviour would change.
9. Files outside the assigned scope must be modified beyond a trivial documented fix.
10. Evidence cannot be produced for a criterion (e.g. no browser available to validate UI).
11. A prior decision must be reversed.
12. A defect's root cause is in the specification rather than the code.

## 3. How to escalate

1. **Write it down first** — in `docs/project/open_questions.md` (with an `OQ-###`), or as a
   `[DECISION]`/`[CHANGE-REQUEST]` if it is a change proposal.
2. **State it in one screen**: context (3 lines), options (2–4), each with consequences, cost and
   reversibility, plus a `[REC]` recommendation.
3. **Say what is blocked** by the answer (module IDs, criteria) and what you will do meanwhile.
4. **Set the module to `blocked`** if the answer is required to proceed — honest state, not a
   half-finished implementation built on a guess.
5. **Batch questions** where possible; a queue of five interrupt-style messages costs the human more
   than one structured list.
6. **Record the answer** where it belongs (decision log, requirement, UX spec) and close the
   question — then refresh context before continuing.

## 4. What "autonomous" means for everything else

Ordinary engineering work needs no permission: reading the repository, writing code inside your
scope, writing tests, running commands, refactoring your own module, fixing lint, naming things,
choosing internal structure, updating documentation you own, opening a PR, commenting.

For choices that are low-risk but non-obvious, prefer the **reversible** option, record it as a
`[DECISION]` (or a `[REC]` if a human should confirm eventually), and continue. Do not stall work to
ask about reversible details — that is the failure mode this framework exists to avoid.

## 5. Human response patterns (what the human is expected to do)

| Agent asks | Human answers with |
|---|---|
| an `OQ-###` | a decision, or "defer until <event>" |
| a `[REC]` | accept / reject / modify — one line is enough |
| a change request | approval with which parts and when, or rejection with a reason |
| a gate review | approve / approve-with-conditions / send back, plus any conditions |
| a validation gap (e.g. UI unverifiable in the agent's environment) | perform the manual check and report evidence, or accept the risk explicitly |

## 6. Escalation anti-patterns

| Anti-pattern | Consequence |
|---|---|
| Guessing a product decision to keep moving | ships the wrong product, confidently |
| Asking about reversible implementation details | wastes the human's attention; agents lose autonomy |
| Escalating without options or a recommendation | the human must do the analysis too |
| Escalating in chat only | the decision is lost when the session ends |
| Marking work complete while an escalation is unanswered | false state, corrupts planning |
| Bypassing a gate "because it seemed obvious" | gates exist precisely for the cases that seem obvious |
