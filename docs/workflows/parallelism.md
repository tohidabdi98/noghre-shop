# Parallelism — running agents safely

> The goal is **maximum useful parallelism without compromising correctness or maintainability** —
> not the maximum number of agents. Parallel work that creates merge conflicts, duplicated domain
> logic, or review overload *reduces* throughput.

## 1. When two modules may run in parallel

All of these must hold:

| Condition | Check |
|---|---|
| No dependency edge requiring the other's *implementation* | `state/dependencies.yaml` |
| Consumed interfaces are `frozen` | edge `status` |
| Ownership sets do not intersect | contract `owns` / `allowed_to_modify` |
| Neither touches the same shared zone | `state/project.yaml → shared_zones` |
| Data model changes do not collide (migrations ordered) | contracts' `data.migrations` |
| A reviewer is available for each PR | review capacity |
| The human's attention is not the bottleneck for both | escalation load |

`python scripts/tp.py ready` computes the ready set and warns about shared-zone/overlap conflicts.

## 2. Waves

```
Wave 0  foundation     contracts, schemas, design tokens, CI, interfaces (usually 1–2 modules, serial)
Wave 1  core domain    independent modules that others depend on
Wave 2  dependents     modules consuming wave-1 interfaces
Wave 3  composition    screens/flows that join modules
Wave 4  hardening      performance, accessibility, security, polish (often serial review-heavy)
```

Rules

- **Freeze interfaces at the end of each wave.** Never start a wave against an unfrozen interface.
- Keep waves small: a wave of 2–4 concurrent agents is usually optimal; > 5 requires a dedicated
  orchestrator session and a real review pipeline.
- The foundation wave is often serial on purpose. Speed there costs more later than it saves now.

## 3. Conflict risk model

| Risk factor | Low | High | Mitigation |
|---|---|---|---|
| Shared files | none | 2+ modules want the same file | make it a shared zone with one owner |
| Interface churn | frozen | changing daily | freeze first, then parallelise |
| Repository size of change | isolated dirs | many cross-cutting edits | sequence them |
| Migrations | none / independent | multiple ordered migrations | serialize the migration author |
| Generated files | none | codegen/output committed by all | single owner regenerates |
| Formatting | enforced by tooling | humans/agents hand-format | formatter in CI |
| Test fixtures | module-local | shared factory files | assign a fixture owner |
| Knowledge overlap | disjoint domains | one agent must understand the other's domain | pair the work sequentially |

Rule of thumb: **coordination cost grows roughly quadratically with the number of agents touching
the same surface.** Split by surface, not by task count.

## 4. Serialized zones (never parallelise)

| Zone | Why | Rule |
|---|---|---|
| Dependency manifests / lockfiles | every module wants to add a dependency | one owner; changes batched per wave |
| Database migrations | ordering and data integrity | one author per wave, reviewed by architecture |
| Routing tables / navigation registry | every UI module adds entries | single owner implements additions |
| Design tokens / theme files | global visual consistency | Frontend/UX decides, one owner writes |
| CI configuration | global effects | owner = human or architecture agent |
| Shared type/schema definitions | breaks everyone at once | freeze; changes via change request |
| i18n catalogues | merge conflicts by nature | single owner, generated updates |
| Package markers / barrel files (`src/__init__.py`, `index.ts`) | one file every module's tests or imports need | name an owner in `shared_zones` before the second module needs it |
| Default branch | protected | never written directly |

Declare these in `state/project.yaml → shared_zones` with a named owner and a change mechanism. The
named owner may write the zone (say so in the module contract's `shared_zones_touched`); every other
module requests the change, and `tp.py pr-check` enforces exactly that split.

## 5. Caps and review capacity

| Constraint | Practical cap |
|---|---|
| Concurrent implementation agents | 3–5 (beyond this, review and integration become the bottleneck) |
| Open PRs awaiting review | 5 (a PR waiting for review is stalled work) |
| Modules in `awaiting_review` at once | 3 |
| Simultaneous human escalations | 1–2 (batch questions; a queue of decisions stalls everything) |

When the cap is reached, the orchestrator does not start new work — it unblocks review, fixes
blockers, or improves the specification.

## 6. Overlap smells (treat as decomposition bugs)

- two modules with `owns` globs that intersect
- a module whose `allowed_to_modify` contains another module's source
- an interface that changes more than once per wave
- the same invariant (e.g. "a project must have an owner") implemented in two modules
- a shared zone without an owner
- frequent `cross-module` PRs on the same pair of modules

## 7. Measuring parallelism (optional but useful)

| Metric | Healthy direction |
|---|---|
| PRs merged per wave | steady, not spiky |
| Rework PRs (`cross-module`, `changes_requested` repeats) | down |
| Modules reopened after `validated` | down |
| Blocked time per module | down |
| Review latency | bounded (a wave should not stall on one review) |
| Integration failures attributed to contracts | down over time (a decomposition-quality signal) |
