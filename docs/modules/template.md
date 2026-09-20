# MODULE-ID — Module Name

<!--
  Module contract template. Create with:
      python scripts/tp.py new-module --id AUTH-001 --name "Authentication"
  The YAML block below is machine-readable and validated by `python scripts/tp.py validate`.
  The prose sections below it are required (headings must match).
  Replace every placeholder; delete the guidance comments when done.
-->

```yaml
module_id: MODULE-001
name: Module Name
status: planned              # planned|ready|assigned|in_progress|awaiting_review|changes_requested|validated|blocked|failed|complete|cancelled
priority: must               # must|should|could
kind: library                # library|service|ui|job|config|docs|infra
purpose: "One sentence: what this module is for, for whom, and why it exists."

# --- Traceability -----------------------------------------------------------
requirement_refs: []         # ["FR-AUTH-1", "NFR-SEC-1"] — headings in requirements.md must contain these IDs
ux_refs: []                  # ["UX-004"] — required when kind: ui and the project has a UI
architecture_refs: []        # ["docs/project/architecture.md#6-interfaces", "ADR-003"]

# --- Ownership (binding: enforced by tp.py pr-check) ------------------------
owns:                        # conceptually responsible
  - src/module_slug/**
  - tests/module_slug/**
allowed_to_modify:           # exhaustive list of writable paths
  - src/module_slug/**
  - tests/module_slug/**
  - modules/MODULE-001.md
  - reports/**               # your validation/handoff evidence
# `state/**`, `handoffs/**` and `reports/**` are framework-managed: every module may write them, because
# the tooling records state transitions and evidence there. List `reports/**` anyway — it documents intent.
forbidden_to_modify: []      # explicit denials; forbidden beats allowed (and beats framework-managed)
  # - src/other_module/**
  # - state/project.yaml

# --- Dependencies ----------------------------------------------------------
depends_on: []               # ["USER-001"] modules that must be validated/complete first
blocks: []                   # ["DASH-001"] downstream modules (mirror into state/dependencies.yaml)

# --- Interfaces ------------------------------------------------------------
interfaces:
  provides:
    - name: ExampleService
      kind: library          # library|http|event|ui|cli|schema
      contract: docs/project/architecture.md#6-interfaces
      version: v1
      consumers: []          # ["DASH-001"]
      test: "tests/module_slug/example-service.contract.test.ts"   # how conformance is verified
  requires:
    - name: UserRepository
      from: USER-001
      contract: modules/USER-001.md
      frozen: false          # must be true before parallel implementation starts

# --- Data ------------------------------------------------------------------
data:
  owns_entities: []          # entities this module is the system of record for
  reads: []                  # entities it reads from others
  migrations: []             # migration files/order it introduces
  retention: ""              # retention or deletion duties, if any

# --- Quality requirements --------------------------------------------------
security: []
  # - "Authorization is enforced server-side for every route; see architecture §7"
performance: []
  # - "p95 < 200 ms for list endpoints at 1k records"
testing: []
  # - "contract test for ExampleService; unit tests per acceptance criterion"
validation: []               # commands that must pass
  # - command: python scripts/verify.py
  #   expects: exit 0
  # - command: python scripts/tp.py validate
  #   expects: exit 0

acceptance_criteria: []
  # - id: AC-1
  #   criterion: Observable statement.
  #   evidence: "test name | command + output | screenshot"

definition_of_done:
  - all acceptance criteria have evidence
  - contract tests pass for every provided interface
  - docs and state updated in the same PR
  - review findings resolved or accepted as non-blocking

# --- Risk / openness -------------------------------------------------------
open_questions: []           # ["OQ-003"]
known_risks: []              # ["RISK-004"]
shared_zones_touched: []     # ["src/app/routes.ts"] — requires the owner's agreement
owner_agent: null            # "impl-auth-001" once assigned
```

## Purpose

<!-- Why this module exists, in product terms. Link the story/flow it serves. -->

## Responsibilities

- <!-- what it does -->

## Non-responsibilities

- <!-- what it deliberately does not do, and which module does it instead — this list prevents
     scope creep more effectively than the responsibilities list -->

## Interfaces

### Provides

<!-- For each provided interface: shape, error semantics, versioning, consumers. -->

### Requires

<!-- For each consumed interface: the frozen contract, and what happens if it is unavailable. -->

## Data

<!-- Entities owned, fields that matter, invariants, sensitivity, retention, migration notes. -->

## Security

<!-- Authorization rules, validation duties, secrets handling, sensitive data touched. -->

## Performance

<!-- Targets and how they are measured. -->

## Testing

<!-- Required test levels, notable edge cases, fixtures/factories this module owns. -->

## Acceptance criteria

<!-- Mirror the YAML list with the detail a reviewer needs; each criterion must be observable. -->

## Definition of done

<!-- Module-specific additions to docs/project/definition_of_done.md. -->

## Example usage

```
// minimal, realistic example of a consumer using this module's public interface
```

## Open questions

| ID | Question | Blocks | Owner |
|---|---|---|---|
| | | | |

## Known risks

| ID | Risk | Mitigation |
|---|---|---|
| | | |

## Change log

| Date | Change | By | Reference |
|---|---|---|---|
| | contract created | decomposition | — |
