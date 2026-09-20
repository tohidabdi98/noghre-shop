# example-saas — a filled-in reference project

This is a **worked example** of the framework mid-flight: the same five-module SaaS project walked
through in `HOW_TO_USE.ipynb` section F. It exists so you can see what "good" looks like before your
own project produces it.

TypeScript/Node source paths (`src/auth/**`, `tests/auth/**`) appear in the contracts but **no source
code is included** — this directory is documentation and state only.

## What it demonstrates

| Artifact | Shows |
|---|---|
| `docs/project/requirements.md` | requirement IDs (`FR-*`, `NFR-*`) with observable acceptance criteria |
| `docs/project/architecture.md` | interfaces, shared zones, and the module-boundary intent |
| `docs/project/decisions.md` | an ADR with options, reversibility and consequences |
| `docs/ux/*` | UX requirements, flows, IA and screens with all six states |
| `modules/*.md` | five complete contracts: ownership, interfaces, criteria, validation commands |
| `state/*.yaml` | a real board: complete, validated, changes_requested, ready — plus an agent replacement |
| `handoffs/*.md` | a lossless handoff after an agent failed mid-module |

## How to use it

```bash
# validate the example as if it were a real project
python scripts/tp.py validate --root examples/example-saas --strict

# see the board, the ready set and the parallelism warnings
python scripts/tp.py status --root examples/example-saas
python scripts/tp.py ready  --root examples/example-saas

# generate the context pack an implementation agent would receive for AUTH-001
python scripts/tp.py context --module AUTH-001 --agent impl-auth-001 --root examples/example-saas
```

## Delete it when you know the shape

This directory is not part of your project. After your first decomposition you can remove it:

```bash
git rm -r examples/example-saas
```

The framework's own tests use it as a fixture, so keep it in the template itself.
