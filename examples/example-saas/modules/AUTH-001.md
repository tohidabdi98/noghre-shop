# AUTH-001 — Authentication

```yaml
module_id: AUTH-001
name: Authentication
status: complete
priority: must
kind: library
purpose: "Authenticate users: signup, sign in, session lifecycle and password reset, exposing a session port that other modules consume."

requirement_refs: ["FR-AUTH-1", "NFR-SEC-1"]
ux_refs: ["UX-001", "UX-002"]
architecture_refs:
  - "docs/project/architecture.md#7-authentication-and-authorization"
  - "ADR-002"

owns:
  - src/auth/**
  - tests/auth/**
allowed_to_modify:
  - src/auth/**
  - tests/auth/**
  - modules/AUTH-001.md
forbidden_to_modify:
  - src/billing/**
  - src/projects/**
  - state/project.yaml
  - docs/project/architecture.md

depends_on: []
blocks: ["USER-001", "DASH-001"]

interfaces:
  provides:
    - name: IF-AUTH-SESSION
      kind: library
      contract: docs/project/architecture.md#6-interfaces
      version: v1
      consumers: ["DASH-001", "PROJECT-001"]
      test: "tests/auth/session.contract.test.ts"
  requires:
    - name: IF-USER-PORT
      from: USER-001
      contract: modules/USER-001.md
      frozen: true

data:
  owns_entities: ["Session", "ResetToken"]
  reads: ["User"]
  migrations: ["db/migrations/0002_sessions_and_reset_tokens.sql"]
  retention: "sessions expire after 30 days idle; reset tokens 30 minutes, single use"

security:
  - "passwords hashed with argon2id; no plaintext ever stored or logged"
  - "reset tokens stored hashed, single use, 30 minute expiry (AC-FR-AUTH-1.2)"
  - "session ids are opaque and stored hashed; cookie is httpOnly + SameSite=Lax (NFR-SEC-1)"
  - "no user enumeration on sign in, sign up or reset"
performance:
  - "sign in p95 < 250 ms server time at 100 rps"
testing:
  - "unit tests per acceptance criterion, including token expiry and reuse"
  - "contract test for IF-AUTH-SESSION"
  - "authz test: a session cannot read another user's profile"
validation:
  - command: python scripts/verify.py
    expects: exit 0
  - command: python scripts/tp.py validate
    expects: exit 0

acceptance_criteria:
  - id: AC-1
    criterion: "invalid credentials are rejected with a non-enumerating error (AC-FR-AUTH-1.1)"
    evidence: "tests/auth/signin.test.ts::rejects_invalid_credentials_without_enumeration"
  - id: AC-2
    criterion: "a reset link works exactly once and expires after 30 minutes (AC-FR-AUTH-1.2)"
    evidence: "tests/auth/reset.test.ts::token_is_single_use_and_expires"
  - id: AC-3
    criterion: "sessions survive reload and expire after 30 days idle (AC-FR-AUTH-1.3)"
    evidence: "tests/auth/session.test.ts::expires_after_idle_window"
  - id: AC-4
    criterion: "screens implement all applicable states per screens.md#screen-01 (UX-AC-001.1/2)"
    evidence: "reports/ux-validation-AUTH-001-2026-03-08.md + screenshots"

definition_of_done:
  - all acceptance criteria evidenced by tests or validation reports
  - IF-AUTH-SESSION contract test passes
  - NFR-SEC-1 verified by review checklist (no plaintext secret, no token in JS)
  - auth screens visually validated and signed off by frontend-ux
  - docs and state updated in the same PR

open_questions: []
known_risks: ["RISK-001"]
shared_zones_touched: []
owner_agent: impl-auth-001
```

## Purpose

Give the product a trustworthy identity layer: a user can create an account, sign in, stay signed in
across reloads, and recover access with a single-use reset link — without leaking whether an account
exists.

## Responsibilities

- account creation, credential verification, password hashing (argon2id)
- session issuance, validation, revocation and idle expiry
- password reset token issuance, verification and single-use enforcement
- exposing `requireSession` to other modules through `IF-AUTH-SESSION`

## Non-responsibilities

- user profile data and collaborator roles → `USER-001`
- authorization of project actions → `PROJECT-001` (uses the session context)
- notification delivery for reset emails → `NOTIFY-001` (called through a port)
- UI composition of the dashboard → `DASH-001`

## Interfaces

### Provides

`IF-AUTH-SESSION` — `requireSession(request): Promise<SessionContext | null>`; returns `null` for an
absent/expired session and throws only on infrastructure failure. Consumers must not read session
tables directly. Version v1, additive changes only. Conformance test:
`tests/auth/session.contract.test.ts`.

### Requires

`IF-USER-PORT` from `USER-001` (`getUser`, `getUserByEmail`), frozen before implementation. A `null`
result means "no such user" and must never be treated as an error.

## Data

Owns `Session` and `ResetToken`; reads `User` through the port. Invariants: a session is invalid when
expired or revoked; a reset token is invalid when used or expired. Retention per the contract YAML.

## Security

Per the YAML: argon2id hashes, hashed single-use reset tokens, opaque hashed session ids in an
httpOnly cookie, no enumeration, and no secrets in logs. Authorization of everything beyond identity
lives in the owning modules.

## Performance

Sign in p95 < 250 ms server time; hashing cost tuned to the platform (documented in the PR). Reset
requests are rate-limited to 5 per hour per email.

## Testing

One test per acceptance criterion plus edge cases (reused token, expired token, concurrent sign-ins,
unicode email, 1000-character password). Contract test for `IF-AUTH-SESSION`. No network in unit tests.

## Acceptance criteria

| ID | Criterion | Evidence |
|---|---|---|
| AC-1 | invalid credentials rejected without enumeration | `tests/auth/signin.test.ts` |
| AC-2 | reset link single-use, 30 min expiry | `tests/auth/reset.test.ts` |
| AC-3 | session survives reload, expires after 30 days idle | `tests/auth/session.test.ts` |
| AC-4 | all applicable screen states implemented | `reports/ux-validation-AUTH-001-2026-03-08.md` |

## Definition of done

Per the YAML list, plus: no plaintext secret in any log or fixture, and the review checklist for
`NFR-SEC-1` signed by the review agent.

## Example usage

```ts
// PROJECT-001 route guard
const session = await requireSession(request);
if (!session) return unauthorized("session_required");
if (!(await requireProjectAccess(session.userId, projectId, "edit"))) return forbidden("not_a_member");
```

## Open questions

| ID | Question | Blocks | Owner |
|---|---|---|---|
| — | none | — | — |

## Known risks

| ID | Risk | Mitigation |
|---|---|---|
| RISK-001 | clock skew between app instances weakens expiry checks | all expiry comparisons use the database clock |

## Change log

| Date | Change | By | Reference |
|---|---|---|---|
| 2026-03-05 | contract created | decomposition | — |
| 2026-03-07 | `IF-AUTH-SESSION` frozen after architecture review | architecture | ADR-002 |
| 2026-03-09 | implemented, validated, merged | impl-auth-001 | PR #12 |
