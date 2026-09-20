# Assumptions — Example SaaS

| ID | Assumption | Why we believe it | Impact if wrong | Confirmation plan | Status | Owner |
|---|---|---|---|---|---|---|
| ASM-01 | users have a modern evergreen browser | target audience is knowledge workers | legacy support + polyfills needed for `UX-G-005` | analytics at M1 end | open | ux-001 |
| ASM-02 | email delivery within ~60 s is acceptable for resets | no realtime requirement in the specification | reset UX needs a "check spam / resend" path; `RISK-002` grows | measure delivery p95 in staging | confirming | impl-notify-001 |
| ASM-03 | 200 projects per user is the realistic upper bound | interviews with two pilot users | dashboard pagination becomes necessary (`OQ-03`) | telemetry of project counts | open | arch-001 |

## Detail

### ASM-02 — email delivery latency
- **Statement:** a reset email arriving within about a minute is acceptable; users are not blocked.
- **Basis:** no realtime requirement in `FR-AUTH-1`; the reset link has a 30-minute validity window.
- **Affects:** `FR-AUTH-1` (UX copy), `FR-NOTIF-1`, `RISK-002`
- **Verification:** measure provider latency p95 in staging during M1 (`reports/`).
- **Decision if falsified:** surface a visible "resend" affordance and consider a secondary channel —
  requires a change request.
- **Status:** confirming.
