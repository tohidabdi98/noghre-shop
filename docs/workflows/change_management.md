# Change management

Requirements change. Architecture changes. The human has a better idea mid-milestone. The framework
must absorb change **without accumulating contradictory documentation** — that is the whole purpose
of this procedure.

## 1. What needs a change request

| Change | Needs a CR? |
|---|---|
| New or changed product behaviour, scope, priority | yes |
| UX change to a primary flow, navigation, or an approved screen | yes |
| Interface change consumed by other modules | yes |
| New runtime dependency, new external service, anything billable | yes (`ADR` + CR) |
| Module boundary change (split, merge, ownership move) | yes |
| Non-functional target change (performance, security level, retention) | yes |
| Data model change with migration or data loss potential | yes |
| Documentation typo, code refactor inside one module, test-only change | no — normal PR |
| Defect fix that restores specified behaviour | no — `failure_recovery.md` (unless the spec was wrong) |

## 2. Pipeline

```
1  Change request raised        docs/project/change_requests/CR-###-slug.md (from the template)
2  Impact analysis              which requirements, UX, architecture, data, modules, agents, PRs, tests
3  Decision                     human approves / rejects / defers  (recorded as [DECISION])
4  Document updates             requirements → ux → architecture/ADRs → contracts → state
5  Contract & state re-freeze   state/dependencies.yaml edges, modules.yaml statuses reset
6  Work re-plan                 orchestrator: close/rebase/re-assign affected PRs
7  Implementation               per module, normal branch/PR flow
8  Validation                   testing + integration + review on the new truth
9  Verification & closure       CR marked implemented → verified; docs contain one consistent story
```

**Order matters.** Documents are updated *before* code, because agents implement documents. Code
written against the old spec while the new spec lands is exactly how contradictions appear.

## 3. Impact analysis checklist

| Area | Questions |
|---|---|
| Requirements | which `FR-###`/`NFR-###` change? what becomes out of scope? |
| UX | which `UX-###`, `UF-##`, screens, patterns, tokens? |
| Architecture | components, interfaces, data model, auth, deployment, observability? |
| Data | schema change? migration? data loss? retention/privacy implications? rollback? |
| Modules | which contracts change? which modules must be re-opened? any new module? |
| Ownership | do `owns`/`allowed_to_modify` sets change? shared zones? |
| Dependencies | which edges need re-freezing? who consumes the changed interface? |
| In-flight work | which branches/PRs are invalidated? rebase, continue, or close? |
| Agents | which agents keep working, which get new context, which are retired? |
| Tests | which tests now assert obsolete behaviour? |
| CI/infrastructure | new checks, new environments, new secrets? |
| Docs | everything in `docs/README.md` that touches the change |
| Cost/schedule | milestone impact, deferred items |

## 4. Handling in-flight work

| Situation | Action |
|---|---|
| Module not started | update its contract; no rework cost |
| Module `in_progress`, change affects it | stop, refresh context, handoff note with what changed; keep the branch if commits remain valid |
| Module `awaiting_review` and affected | review against the new contract, not the old one; re-open if needed |
| Module `validated`/`complete` and affected | reopen to `ready` with a note; the human decides whether the milestone slips |
| Interface changes | everyone building against it stops until it is re-frozen — never let two agents build against different versions |
| PR almost merged and unaffected | proceed; the change lands in a follow-up |

## 5. Communication of a change

Every change produces exactly one authoritative statement of the new truth:

- `docs/project/decisions.md` → the `DEC-###`/`ADR-###` entry (the *why*).
- the affected source documents → the new *what* (edited in place; no legacy copies).
- `docs/project/project_state.md` → the current status + next actions.
- the CR file → the full analysis trail (the *history*).

Stale text is deleted, not annotated as "(old)". If someone needs history, Git has it.

## 6. Preventing contradictions (documentation hygiene)

1. One source of truth per fact (`docs/README.md`) — enforced by review, not just convention.
2. Supersede explicitly: `ADR-012 supersedes ADR-004`.
3. After any change, run `python scripts/tp.py validate` (links + contracts + prompt sync) — broken
   links and orphaned references are the early symptoms of drift.
4. Reviewers check the *documents* as part of the review; a PR that changes behaviour without
   updating the requirement is a blocking finding.

## 7. Fast path for small changes

For a genuinely small change (one module, no interface, no data impact), the CR can be a
two-paragraph entry in `docs/project/decisions.md` plus a `requirements.md` edit in the same PR —
but the tag `[CHANGE-REQUEST]` and a `CR-###`-style note must still exist so the trail is visible.
"Small" is judged by impact, not by diff size.
