# Handoff — <MODULE-ID> from <from-agent-id> to <to-agent-id>

> Generate with `python scripts/tp.py handoff --module <MODULE-ID> --from <a> --to <b> --reason "<why>"`,
> then fill in the narrative sections. Store in `handoffs/` and commit it. The receiving agent must
> be able to continue **without reading the previous conversation**.

## 1. Identity

| Field | Value |
|---|---|
| Project | `<project_id>` |
| Module | `<MODULE-ID>` — contract `modules/<MODULE-ID>.md` |
| From agent | `<from-agent-id>` (`<role>`) — status now `<failed|replaced|done>` |
| To agent | `<to-agent-id>` (`<role>`) |
| Reason | `<agent crash | stale context | scope exhaustion | model change | deliberate rotation | other>` |
| Date | YYYY-MM-DD |
| Branch | `agent/<from-agent-id>/<MODULE-ID>` → continue on `agent/<to-agent-id>/<MODULE-ID>` |
| PR | #`<number>` (or none) |
| Module state | `assigned | in_progress | awaiting_review | changes_requested | blocked | failed` |

## 2. Current state of the work

- What exists and **works** (with commit SHAs):
- What exists and is **incomplete or known broken**:
- What was **not started**:
- Last validation run and its result (paste the command and the outcome):

## 3. Relevant files and artifacts

| Path | What it is | State |
|---|---|---|
| | | |

## 4. Decisions made by the outgoing agent

| ID / reference | Decision | Rationale | Reversible? |
|---|---|---|---|
| | | | |

## 5. Assumptions and open questions

| Item | Type | Status | Impact on the remaining work |
|---|---|---|---|
| | `[ASSUMPTION]` / `[OPEN]` | | |

## 6. Known issues and risks

| Issue | Severity | Where | Suggested next step |
|---|---|---|---|

## 7. Validation performed so far

| Command | Result | Trustworthy now? |
|---|---|---|
| | | |

## 8. Warnings for the receiving agent

<!-- Traps, dead ends already explored, approaches that failed, files that look relevant but are
     not, environment quirks, flaky tests. This section saves the most time — and it is the one
     agents most often skip. -->

## 9. Next recommended action

1. <!-- the single most important next step -->
2. <!-- following steps -->

## 10. Acceptance criteria remaining

| Criterion | Status | Evidence needed |
|---|---|---|
| AC-1 | met | — |
| AC-2 | not met | test + screenshot |

## 11. Acknowledgement (filled by the receiving agent)

- I have read the module contract, this handoff, and the current branch state.
- I have re-run the validation above to confirm the reported state *(recommended, not optional for
  a failed outgoing agent)*:
- My first action will be:
