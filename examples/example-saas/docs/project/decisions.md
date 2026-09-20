# Decisions — Example SaaS

> Append-only. Supersede, never rewrite.

| ID | Title | Type | Status | Decider | Date |
|---|---|---|---|---|---|
| DEC-001 | Instantiate from TemplateProject | process | accepted | human | 2026-03-01 |
| DEC-002 | Email/password auth in v1 (no SSO) | product | accepted | human | 2026-03-02 |
| ADR-001 | Modular monolith with interface ports | architecture | accepted | arch-001 | 2026-03-05 |
| ADR-002 | Opaque session cookies and hashed reset tokens | architecture | accepted | arch-001 | 2026-03-05 |
| DEC-003 | Defer invite codes to after M1 | product | accepted | human | 2026-03-03 |

---

## ADR-001 — Modular monolith with interface ports
- **Status:** accepted · **Date:** 2026-03-05 · **Decider:** arch-001
- **Supersedes:** —

**Context.** Five functional areas, one team of agents, low traffic, one deployable is enough. The
decisive constraint is that independent agents must be able to implement modules without stepping on
each other, and that integration failures must be attributable.

**Options considered**

| Option | Pros | Cons | Cost to change later |
|---|---|---|---|
| A. Modular monolith with interface ports | cheap ops, fast tests, clean ownership, easy attribution | a little indirection; discipline required | low — boundaries already mirror services |
| B. Separate services per area | independent deploys and scaling | ops overhead, network failure modes, distributed debugging for a small product | high |
| C. Single-layer application | fastest to start | any change touches shared files; agents collide constantly | very high (rewrite) |

**Decision.** One deployable, with `AUTH-001`, `USER-001`, `PROJECT-001`, `DASH-001`, `NOTIFY-001` as
internal modules separated by the ports in architecture §6; modules never import each other's
internals; `APP-001`/`DB-001` own the shared zones.

**Rationale.** Interface ports make each module testable in isolation, keep ownership disjoint, and
convert integration failures into contract failures — exactly the properties this framework depends
on.

**Consequences.**
- Easy: parallel module work, module-level tests, replacing the email provider.
- Hard: cross-module refactors need a change request.
- Revisit if: a module needs independent scaling or a separate release cadence.

**Reversibility.** Moderate — the ports make a later service split mechanical, not architectural.

**Verification.** `NFR-MAINT-1` (no cross-module imports) is checked in CI; integration failures are
attributed by contract tests, tracked in `reports/`.

## ADR-002 — Opaque session cookies and hashed reset tokens
- **Status:** accepted · **Date:** 2026-03-05 · **Decider:** arch-001

**Context.** `NFR-SEC-1` requires no token in `localStorage` and no plaintext secrets at rest.

**Options considered**
| Option | Pros | Cons |
|---|---|---|
| A. Opaque session id in httpOnly cookie | revocable, no client-side token handling, simple expiry | server-side session store required |
| B. Signed JWT in cookie | stateless | revocation is hard; key rotation overhead |
| C. JWT in localStorage | simplest | XSS-exposed; explicitly forbidden by `NFR-SEC-1` |

**Decision.** Option A. Sessions are opaque ids stored hashed server-side; reset tokens are 32 random
bytes stored hashed with a 30-minute single-use expiry.

**Consequences.** Easy: revocation and session listing. Hard: a session store must be maintained.
**Reversibility.** Moderate (a token format change is contained inside `AUTH-001`).
**Verification.** Authorization and expiry tests in `tests/auth/**`; review checklist for `NFR-SEC-1`.
