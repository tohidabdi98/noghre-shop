# scripts/ — the toolkit

Zero dependencies: **Python ≥ 3.9, standard library only.** No `pip install` step, no virtualenv
required. State files are read with a built-in YAML-subset parser; if PyYAML happens to be installed
it is used instead (the backend is printed by every command).

| File | What it is |
|---|---|
| `tp.py` | the CLI: bootstrap, new-module, validate, sync-notebook, status, ready, context, start, handoff, pr-check |
| `verify.py` | the project verification pipeline (typecheck / lint / format / test), stack auto-detecting |
| `verify.config.yaml` | **the project fills this in** — the commands of record |
| `validate.config.yaml` | knobs for the integrity checks (allowlists) |
| `tplib/` | the library: `yamlmini`, `state`, `context`, `repoutil`, `checks` |
| `tests/` | the toolkit's own tests (stdlib `unittest`) |

## Commands

```bash
python scripts/tp.py bootstrap [<new-dir>] --name "My Project" --id my-project --profile fullstack [--init-git] [--adopt-env]
python scripts/tp.py new-module --id AUTH-001 --name "Authentication" [--dep USER-001]
python scripts/tp.py validate [--strict] [--root examples/example-saas]
python scripts/tp.py sync-notebook
python scripts/tp.py status [--json]
python scripts/tp.py ready
python scripts/tp.py context --module AUTH-001 --agent impl-auth-001 [--format json] [--out state/.cache/ctx.md]
python scripts/tp.py start --module AUTH-001 --agent impl-auth-001 [--task "..."] [--force --force-reason "..."]
python scripts/tp.py handoff --module AUTH-001 --from impl-auth-001 --to impl-auth-002 --reason "..."
python scripts/tp.py pr-check --base main [--body-file pr.md]
python scripts/verify.py [--list] [--strict] [--only test]
python -m unittest discover -s scripts/tests -t .
```

## What `validate` checks

| Check | Fails when |
|---|---|
| state schema | required keys missing, invalid enums, unknown stage/profile |
| gate coherence | the stage is ahead of the approved gates (warning) |
| contracts | missing YAML block, missing required keys, missing required sections, empty criteria/validation, `owns` not covered by `allowed_to_modify` |
| status drift | contract `status` differs from `state/modules.yaml` |
| dependency graph | cycles, unknown modules, missing mirror between `depends_on` and `state/dependencies.yaml`, invalid type/status |
| ownership | two modules claim overlapping paths |
| traceability | a cited `FR-###`/`NFR-###`/`UX-###` does not exist in the documentation |
| agents | unknown role, invalid branch format, branch/agent/module mismatch, duplicate ids |
| registry | a role has no prompt, a prompt has no role, missing contract fields |
| documentation links | a referenced `docs/…`, `state/…`, `scripts/…` path does not exist |
| notebook sync | a `PROMPT-SYNC` cell differs from `agents/*/STARTER_PROMPT.md` |
| placeholders | an initialised project still contains template placeholder tokens |
| shared zones | a contract claims a zone `state/project.yaml → shared_zones` does not declare (warning) |

While `state/project.yaml` says `initialised: false` (a pristine template, or a copy nobody has
bootstrapped yet) the placeholder check reports one notice instead of an error, so a fresh clone is
green. `bootstrap` sets `initialised: true`, and from then on any leftover `{{TOKEN}}` fails the build.

Exit codes: `0` clean · `1` errors (or warnings with `--strict`) · `2` usage error.

`pr-check` (the CI gate) additionally enforces branch naming, commit conventions and trailers,
ownership of every changed path, and the required PR-body sections. It accepts a plain branch name or a
ref (`origin/<branch>`, `refs/heads/<branch>`) — CI hands over a remote-tracking ref. Three prefix
groups are writable by every module because the framework itself uses them: `state/**`,
`handoffs/**`, `reports/**`; a shared zone is writable only by the module `state/project.yaml` names as
its owner. `forbidden_to_modify` overrides all of it.

## Adding your own checks

`scripts/verify.config.yaml` is where project-specific commands belong (it feeds `verify.py`, and your
module contracts reference `python scripts/verify.py`). Put repository-integrity additions in
`validate.config.yaml` rather than editing `tplib/checks.py`, and only extend the Python when a check
genuinely needs new logic.

## Tests

```bash
python -m unittest discover -s scripts/tests -t .     # toolkit tests, no external dependencies
```

The tests exercise `yamlmini` round-trips, readiness/wave computation, transition legality, context
assembly, the CLI (including a fresh-copy bootstrap simulation in `.tmp/`), and `pr-check` against a
scratch git repository.
