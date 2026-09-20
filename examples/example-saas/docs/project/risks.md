# Risks — Example SaaS

| ID | Risk | Category | L | I | Score | Mitigation | Trigger | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|
| RISK-001 | clock skew between app instances weakens session/reset expiry checks | technical | 3 | 3 | 9 | all expiry comparisons use the database clock | auth test failing intermittently | impl-auth-001 | closed |
| RISK-002 | email provider latency or outage delays reset and assignment emails | delivery | 3 | 2 | 6 | queue + retry with backoff; the primary action never depends on delivery | delivery p95 > 60 s | impl-notify-001 | open |
| RISK-003 | timezone handling around due dates produces off-by-one overdue items | technical | 3 | 3 | 9 | store UTC, render in the user's timezone, inject the clock in tests | user report of a wrong overdue item | impl-project-001 | mitigating |
| RISK-004 | the dashboard becomes a coupling magnet ("just fetch it here") | technical | 2 | 3 | 6 | every read model goes through `PROJECT-001`'s interfaces; `DASH-001` owns no domain rules | a PR adding direct table access to `src/dashboard/**` | rev-dash-001 | open |
| RISK-005 | agent context exhaustion on UI modules with many states | delivery | 3 | 2 | 6 | `tp.py context` packs; handoff procedure when a session dies | a second handoff on the same module | orch-001 | open |

## Detail

### RISK-003 — timezone handling around due dates
- **Cause:** users in different timezones; a naive "today" comparison makes items overdue a day early.
- **Impact:** the dashboard loses trust — the one thing it must not do.
- **Mitigation:** UTC storage, timezone rendering, clock injection in tests (`DEC-DASH-1` family).
- **Contingency:** show due dates without an "overdue" label until fixed.
- **Review date:** end of M1.
