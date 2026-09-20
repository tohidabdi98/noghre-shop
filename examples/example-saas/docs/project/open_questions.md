# Open questions — Example SaaS

| ID | Question | Type | Blocks | Owner | Asked | Status | Answer / decision |
|---|---|---|---|---|---|---|---|
| OQ-01 | do we need invite codes for signup in v1? | product | nothing in M1 | human | 2026-03-02 | deferred | DEC-003 — deferred to after M1 |
| OQ-02 | should users be able to opt out of the email digest? | product | nothing (in-app covers the requirement) | human | 2026-03-11 | open | — |
| OQ-03 | do we need pagination on the project list for M1? | technical | `PROJECT-001` polish, not M1 | arch-001 | 2026-03-10 | open | — |

## Detail

### OQ-02 — email digest opt-out
- **Asked by:** `impl-notify-001` (pre-implementation)
- **Context:** `FR-NOTIF-1` requires in-app notifications and an email digest entry. An opt-out is not
  mentioned in the approved requirements.
- **Options:**
  1. No opt-out in v1 — simplest, matches the approved scope; the risk of annoyance is low at this
     volume.
  2. A per-user digest toggle — one extra field, one extra screen state, one more acceptance criterion.
- **Recommendation `[REC]`: option 1.** The requirement does not ask for it, and adding scope requires a
  change request.
- **Impact if deferred:** none for M1; revisit if users complain (then: `CR-###`).
- **Answer:** pending.
