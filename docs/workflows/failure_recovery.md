# Failure recovery

Agents crash, run out of context, misread a contract, or produce work that cannot be salvaged. What
matters is that **project state survives every failure** and the next agent can continue without
the previous conversation.

The principle: *the repository is the memory; a failed agent is a replaced worker, not lost work.*

## 0. Universal first steps

1. **Stop and record.** Move the module to `blocked` or `failed` with a reason
   (`python scripts/tp.py status` must show the truth). Never leave a silent failure.
2. **Preserve the branch.** Do not delete it and do not force-push over it — it is evidence.
3. **Write a failure report** (`docs/agents/templates/failure_report.md`) before fixing anything.
4. **Classify the failure** to pick the procedure below.
5. **Re-validate the claims** of the failed agent — a failed agent's "tests pass" is not trustworthy.

## 1. Failure modes and procedures

### Agent crash / session lost
- Inspect the branch: commits are safe, uncommitted work is gone.
- Commit or stash whatever is in the working tree (with a clear message noting it is salvaged).
- State: keep `in_progress` if commits show real progress, else `assigned`.
- Recovery: same agent id, new session, with `tp.py context` refreshed. If it crashes repeatedly
  (> 2), treat as *scope exhaustion* below.

### Agent abandonment (silent, no commits, no report)
- Verify the branch state and whether the module is partially implemented.
- `failed` + a handoff record; assign a new agent id (`impl-auth-002`).
- Check whether the module is simply too large (`parallelism.md` §scope) — if yes, decompose further
  rather than assigning another agent to the same wall.

### Bad implementation (works but violates the contract/architecture)
- Do **not** patch on top. Attribute per `integration_workflow.md` §4.
- If the approach is wrong: revert to the last good commit, keep the branch for reference,
  re-assign with an explicit note of the rejected approach in the handoff ("do not repeat X").
- If only details are wrong: `changes_requested`, fix within the same branch.

### Incorrect assumptions
- Find the falsifying evidence, then update `assumptions.md` (`status: falsified`).
- Impact analysis: which requirements, UX, architecture, modules assumed it? Run the change
  management pipeline for anything material.
- Fix the documents **first**, then re-implement against the corrected truth.
- If an agent acted on an `open` assumption without escalating, that is a process failure: record
  it and add the assumption to `AGENTS.md` visibility (the escalation list) if it was consequential.

### Failed tests
- Reproduce locally first; distinguish *defect* (code wrong) from *stale test* (requirement changed).
- Stale test ⇒ verify the requirement change is recorded (change request / decision), then update
  the test in the module that owns it.
- Real defect ⇒ debugging agent, smallest fix, regression test
  (proof it fails before the fix).
- Never delete or weaken a test to get green without a recorded decision.

### Failed CI / red pipeline for unrelated reasons
- Classify: infrastructure (runner, cache, network), tooling version drift, or a real failure.
- Pin versions and caches; do not let a flaky pipeline become background noise.
- If it blocks a module, move that module to `blocked` and record the blocker rather than disabling
  the check. Disabling a required check requires explicit human approval recorded in the PR.

### Merge conflicts
- Rebase onto the default branch; resolve inside your ownership.
- Conflict in a shared zone or another module ⇒ ownership violation: stop, escalate, and let the
  owner make the change.
- After resolving: re-run full validation (resolutions change behaviour).

### Broken module contract (implementation contradicted the contract)
- Treat the contract as the source of truth until the human/architect changes it.
- Correct path: contract test failure → review finding → either the module is fixed, or a change
  request amends the contract and the *other* side is updated too.
- Never leave `modules/<ID>.md` describing behaviour that does not exist. Mark it
  `status: needs-revision` immediately.

### Architectural change after implementation started
- Run the full change pipeline (`change_management.md`).
- Expect to re-open modules: record which modules were `validated` and are now invalidated
  (honest state beats convenient state).
- Re-freeze interfaces before restarting parallel work; never let two agents build against different
  versions of the same interface.

### Requirement change
Same as above; the Discovery Agent (or the human) updates requirements first, then UX, architecture,
contracts, then implementation.

### Stale agent context
- Symptom: agent implements old behaviour, ignores recent decisions, references deleted files.
- Fix: `python scripts/tp.py context --module <ID> --agent <ID>` regenerated after a rebase, and tell
  the agent to re-read the contract + `docs/project/decisions.md` tail.
- Prevention: context packs are generated per session, never reused across a change request.

### Incorrect decomposition
- Symptom: two modules cannot be developed without touching each other's files; the same invariant
  is implemented twice; interfaces keep changing.
- Recovery: stop the wave, re-run the Decomposition Agent for the affected subgraph, keep existing
  code as the starting point for the new contracts (assignments migrate, code does not move twice).
- Record the reason in `docs/project/decisions.md` so the next decomposition avoids it.

### Partially completed work
- State must reflect partial completion: `in_progress` with the handoff listing what is done,
  incomplete, untouched, and the remaining acceptance criteria.
- Never mark `awaiting_review` on partial work "to get a review going".

## 2. Replacing an agent (lossless)

```bash
python scripts/tp.py handoff \
  --module AUTH-001 \
  --from impl-auth-001 --to impl-auth-002 \
  --reason "context exhausted mid-module"
```

This writes `handoffs/<date>-impl-auth-001-to-impl-auth-002-AUTH-001.md` from real state (status,
branch, PR, validation), marks the old instance `replaced` and the new one `active` with
`parent_agent` set. The new agent then:

1. reads the module contract and the handoff,
2. inspects the branch (`git log`, `git diff` against the default branch),
3. **re-runs** the validation the handoff claims,
4. continues or restarts deliberately — and records which, in the report.

## 3. Recovery table (quick reference)

| Failure | First action | State | New agent? | Document to update |
|---|---|---|---|---|
| crash | preserve branch, salvage commits | in_progress | same id | failure report |
| abandonment | inspect branch, handoff | failed | yes | handoff + report |
| bad implementation | attribute, revert if wrong approach | changes_requested / failed | maybe | failure report |
| wrong assumption | falsify + impact analysis | blocked → ready | as needed | assumptions + change pipeline |
| failed test | reproduce, classify defect vs stale | in_progress | debugging | failure report |
| red CI (infra) | classify, record blocker | blocked | no | failure report |
| merge conflict | rebase within ownership | in_progress | no | handoff note if escalated |
| contract break | mark needs-revision, decide contract vs code | changes_requested | no | contract + failure report |
| architecture change | change pipeline first | blocked | maybe | ADR + CR |
| requirement change | change pipeline first | blocked | maybe | requirements + CR |
| stale context | regenerate context pack | in_progress | no | handoff note |
| bad decomposition | re-decompose subgraph | blocked | decomposition role | decisions + contracts |
| partial work | handoff with remaining criteria | in_progress | maybe | handoff |

## 4. What must never happen

- Deleting a branch to make a problem disappear.
- Marking work complete to close a milestone.
- Fixing symptoms in several modules at once.
- Leaving a failed module with no recorded reason.
- Rewriting the failed agent's history (force-push) so the next agent sees a clean story.
