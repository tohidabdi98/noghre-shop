# State — machine-readable project truth

Four small YAML files describe **where the project is right now**. They contain status, identity and
edges — never explanations (`docs/README.md` rule 2). Prose lives in `docs/`.

| File | Contains | Written by | Validated by |
|---|---|---|---|
| `project.yaml` | project identity, profile, stage, milestone, spec status, **gates**, shared zones, `initialised` | human + orchestrator (`tp.py bootstrap`) | `tp.py validate` |
| `modules.yaml` | per-module status, assigned agent, branch, PR, validation result | `tp.py start/handoff`, orchestrator, agents at clear transitions | `tp.py validate` |
| `agents.yaml` | agent instances: role, module, branch, status, authority, history | `tp.py start/handoff`, orchestrator | `tp.py validate` |
| `dependencies.yaml` | dependency edges: `from` **depends on** `to`, type, interface, freeze status | decomposition; re-frozen by architecture/integration | `tp.py validate` |

## Editing rules

1. **Use the tools first.** `python scripts/tp.py …` keeps files consistent; hand-editing is allowed
   but you must run `python scripts/tp.py validate` afterwards.
2. **One line per change.** These files are diffed constantly; keep edits surgical.
3. **No duplication of meaning.** Ownership/acceptance criteria live in `modules/<ID>.md`; only
   *status* lives here.
4. **Never fake state.** A module is `validated` only with evidence; a blocked module stays `blocked`
   until the blocker is cleared. False state corrupts every planning decision.
5. **Dates** are `YYYY-MM-DD`. **IDs** are permanent.
6. Nothing in `state/.cache/` is committed (generated context packs).
7. `initialised: false` means "this repository is still the template": `tp.py bootstrap` sets it to
   `true`, and only then do the `{{PLACEHOLDER}}` tokens in this directory become validation errors.

## Source of truth for a single module

```
class:            modules/<MODULE-ID>.md      (what it must do, who owns what, criteria)
status/agent/PR:   state/modules.yaml          (where it is now)
who is working:    state/agents.yaml           (which instance, which branch)
who depends on whom: state/dependencies.yaml   (edges + freeze status)
```

## Quick commands

```bash
python scripts/tp.py validate      # schema, references, cycles, placeholders, doc links, prompt sync
python scripts/tp.py status        # human-readable board + next actions
python scripts/tp.py ready         # ready set, waves, overlap/shared-zone warnings
python scripts/tp.py start --module AUTH-001 --agent impl-auth-001
python scripts/tp.py handoff --module AUTH-001 --from impl-auth-001 --to impl-auth-002 --reason "..."
```
