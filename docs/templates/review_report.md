# <Review|Validation> report — <MODULE-ID> <PR #>

- **Report type:** review | testing | integration | ux-validation
- **Module:** `MODULE-ID` — contract: `modules/MODULE-ID.md`
- **Agent:** `<agent-id>` (`<role>`)
- **Date:** YYYY-MM-DD
- **Artifact under review:** PR #, branch `agent/<agent-id>/<MODULE-ID>`, commits `<sha>..<sha>`
- **Baseline:** `main` @ `<sha>`
- **Verdict:** PASS | PASS WITH NON-BLOCKING FINDINGS | FAIL

## 1. Scope of this review

<!-- What was checked, and explicitly what was not. Never imply broader coverage than performed. -->

| Checked | Not checked (and why) |
|---|---|
| | |

## 2. Reference documents used

| Document | Section / IDs |
|---|---|
| `modules/MODULE-ID.md` | acceptance criteria AC-1… |
| `docs/project/requirements.md` | `FR-###` |
| `docs/project/architecture.md` | §6 interfaces |
| `docs/ux/*` | `UX-###` |
| `docs/project/conventions.md` | §2, §3 |

## 3. Acceptance criteria verification

| Criterion | Verdict | Evidence (command / test / screenshot) |
|---|---|---|
| AC-1 | PASS / FAIL / NOT VERIFIED | |

## 4. Findings

> Taxonomy: **Blocking** (must be fixed before merge) · **Non-blocking** (fix now or record a
> follow-up) · **Suggestion** · **Question**.

| # | Severity | Area | Finding | Expected | Suggested fix | Owner |
|---|---|---|---|---|---|---|
| 1 | Blocking | | | | | |

## 5. Validation performed

| Command | Result | Notes |
|---|---|---|
| `python scripts/verify.py` | exit 0 | |
| `python scripts/tp.py validate` | exit 0 | |
| | | |

## 6. Contract conformance

| Interface provided | Contract test | Result |
|---|---|---|
| | | |

| Interface consumed | Used as specified? | Notes |
|---|---|---|

## 7. Security / performance / accessibility

| Area | Check | Result |
|---|---|---|
| Security | authorization enforced, inputs validated, secrets untouched | |
| Performance | contract targets measured | |
| Accessibility | scan + keyboard walkthrough (UI changes) | |

## 8. Known limitations and risks accepted

| Item | Impact | Accepted by |
|---|---|---|

## 9. Conclusion

- **Mergeable:** yes / no / after fixes
- **Required follow-ups:** <issue links>
- **State recommendation:** `awaiting_review` → `validated` | `changes_requested`
