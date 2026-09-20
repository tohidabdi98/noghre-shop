# Modules — contracts, ownership and state

> A **module** is the unit of parallel work: the smallest piece of the system that one agent can
> own, implement, test and validate end to end without touching another agent's files.
>
> `docs/modules/` explains the format (this file + `template.md`).
> `modules/` holds the real contracts, one file per module: `modules/AUTH-001.md`.

## 1. What makes a good module

| Property | Test |
|---|---|
| Cohesive | one purpose fits in the `purpose` sentence without "and" |
| Loosely coupled | it can be tested with the other modules replaced by their contracts |
| Independently testable | its tests pass with no other module's internals involved |
| Clearly owned | exactly one `owns` path set, no overlap with another module |
| Agent-sized | implementable, testable and reviewable in one agent session (roughly ≤ 1 day of work) |
| Minimally overlapping | few files shared with others; shared zones are explicit, single-owner |
| Validatable | acceptance criteria are observable, not "works well" |

**Split when:** two purposes evolve independently · the file set is too large to review · two
different stacks/layers are mixed · tests need most of the system to run.
**Do not split when:** the parts share deep invariants (a split invites duplicated rules) ·
the split would create chatty interfaces · the domain concept is genuinely atomic (e.g. a
serialization format), or the result would be a "utils" grab-bag.

**Forbidden module types:** `utils`, `common`, `misc`, `helpers`. A module with no domain meaning
either belongs to an owning module or is a shared zone with a named owner.

## 2. Contract anatomy

Every `modules/<MODULE-ID>.md` starts with a machine-readable YAML block, then human prose:

````markdown
# AUTH-001 — Authentication

```yaml
module_id: AUTH-001
name: Authentication
...
```

## Purpose
...
````

- **YAML block** = identity, ownership, interfaces, dependencies, criteria. Scripts read it
  (`tp.py context`, `tp.py validate`, `tp.py pr-check`) — keep it accurate.
- **Prose** = reasoning, detail, examples. Humans and agents read it; the required headings are
  enforced by `tp.py validate`.
- The full field reference is `docs/modules/template.md`. Copy it with
  `python scripts/tp.py new-module --id X-001 --name "..."` rather than by hand.

## 3. Ownership model (binding)

| Field | Meaning | Enforced by |
|---|---|---|
| `owns` | paths this module is conceptually responsible for | review + `pr-check` (must be a subset of `allowed_to_modify`) |
| `allowed_to_modify` | the exhaustive list of paths its agent may write | `tp.py pr-check` fails on anything outside |
| `forbidden_to_modify` | explicit denials, including other modules' areas | `pr-check` fails; **forbidden always beats allowed** |
| `shared_zones` (`state/project.yaml`) | files many modules need (routes, tokens, manifests, migrations) | single named owner; the owner writes it (declare it in `shared_zones_touched`), everyone else requests a change |

Path syntax: repository-relative globs (`src/auth/**`, `tests/auth/**`, `modules/AUTH-001.md`).
Use `**` for recursion; `*` never crosses `/`.

Three prefixes are **framework-managed** and therefore writable by every module's agent, because the
framework itself records state and evidence there: `state/**` (transitions, agent instances),
`handoffs/**` and `reports/**`. `forbidden_to_modify` still overrides this allowance — a module that
must not touch `state/project.yaml` can say so and the check will honour it.

Shared zones work the other way round: if `state/project.yaml` names your module as the owner of a
zone, you may write that path (list it in `shared_zones_touched` so the intent is visible in review),
and `pr-check` will not flag it. If another module owns it, the check fails and you request the change.
Declare the zone before you touch it: `tp.py validate` warns about a `shared_zones_touched` entry that
`state/project.yaml` does not list.

Cross-module needs have exactly three legitimate routes:

1. **Consume the frozen interface** of the other module (no edits there).
2. **Ask the owning agent/orchestrator** to make the change (a small follow-up PR by the owner).
3. **Escalate** to the human when the change affects a contract, the architecture, or a shared zone.

Editing another module's files "just to make it work" is a process violation, not a shortcut.

## 4. Module state machine

Canonical states live in `state/modules.yaml` (`status`), and are validated by `tp.py`.

```
planned ──► ready ──► assigned ──► in_progress ──► awaiting_review ──► validated ──► complete
                            ▲                              │
                            │                              ▼
                            └──────────── changes_requested ┘
   blocked ──► ready        failed ──► ready (new agent)      cancelled (terminal)
```

| State | Meaning | Set by |
|---|---|---|
| `planned` | in the dependency graph, not yet startable | decomposition |
| `ready` | all dependencies `validated`/`complete`, interfaces frozen, no blocking question | orchestrator / `tp.py ready` |
| `assigned` | an agent owns it | orchestrator / `tp.py start` |
| `in_progress` | agent is working on a branch | agent / `tp.py start` |
| `awaiting_review` | PR open, evidence attached | implementation agent |
| `changes_requested` | review found blocking issues | review agent |
| `validated` | criteria verified with evidence | review + testing agents |
| `complete` | merged to the default branch (or integration branch) | orchestrator |
| `blocked` | an external dependency, question or failure prevents progress | any role, with a recorded reason |
| `failed` | the attempt is abandoned (agent crash, wrong approach) | orchestrator / human |
| `cancelled` | deliberately dropped | human only |

Rules: transitions are one-way except back into `in_progress`; **only the human** may cancel, force
`validated`, or reopen `complete`; every transition records who and why (`tp.py` writes
`updated_at`, and `state/modules.yaml` keeps a `history` entry for non-trivial transitions).

## 5. Module lifecycle

```
decomposition → contract written → validate → dependencies resolved (frozen interfaces)
   → tp.py ready → tp.py start (branch, state) → implementation → PR → review → testing
   → integration → validated → complete → docs/state updated
```

## 6. Parallelism rules

- Two modules may run in parallel when their `owns`/`allowed_to_modify` sets do not intersect and
  neither depends on an unfrozen interface of the other.
- `tp.py ready` lists ready modules and warns about shared-zone and overlap conflicts.
- Dependency edges live in `state/dependencies.yaml`: `from` **depends on** `to` (so `to` is
  upstream and must be `validated`/`complete` first).
- Cap parallelism by review capacity, not by ambition (`docs/workflows/parallelism.md`).

## 7. Validation checklist for a contract

- [ ] `python scripts/tp.py validate` passes for this module
- [ ] every acceptance criterion is observable and has an evidence expectation
- [ ] `owns` ⊆ `allowed_to_modify`; no overlap with another module's sets
- [ ] every `depends_on` edge exists in `state/dependencies.yaml` with a type and owner
- [ ] every provided interface has a contract test requirement
- [ ] `requirement_refs` and `ux_refs` resolve to existing IDs
- [ ] open questions that block it are recorded in `docs/project/open_questions.md`
