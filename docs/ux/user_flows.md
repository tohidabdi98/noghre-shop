# User flows

> Owned by the Frontend/UX Agent. A flow is the end-to-end path a user takes to accomplish one
> goal: happy path **plus** the states and failures around it. Implementation agents receive only
> the flows their module touches (via `ux_refs` in the module contract).

## Flow index

| ID | Flow | Persona | Entry points | Screens | Modules | Priority |
|---|---|---|---|---|---|---|
| UF-01 | Example: sign up and start first project | P1 | marketing page, invite link | `signup`, `onboarding`, `dashboard` | `AUTH-001`, `USER-001` | must |

## Flow format

Each flow answers, in order: who, why, from where, what happens step by step, what can go wrong,
where the user can leave and come back, and how we know it worked.

```text
UF-<n> — <flow name>                                   [flow id]
  Actor:      <persona>
  Goal:       <what "done" means for the user>
  Trigger:    <what starts the flow>
  Preconditions: <state required before step 1>
  Success:    <observable end state>
  Abandonment: <where users realistically drop out and what we do about it>
```

## UF-01 — <flow name>

**Actor:** P1 · **Goal:** · **Trigger:** · **Preconditions:** ·
**Success:** · **Related requirements:** `FR-###`, `UX-###`

### Steps (happy path)

| # | User action | System response | Screen / state | Notes |
|---|---|---|---|---|
| 1 | | | | |

### Alternative paths

| Branch | Condition | Divergence | Returns to step |
|---|---|---|---|
| A1 | | | 2 |

### Failure paths

| Failure | Detection | User sees | Recovery | Logged |
|---|---|---|---|---|
| invalid input | client + server validation | inline field error + summary | correct and resubmit | yes |
| service unavailable | timeout | "we could not reach X; retry" | retry button, data preserved | yes |

### States around the flow

| State | Where | What the user sees |
|---|---|---|
| loading | | skeleton / spinner with label |
| empty | | explanation + primary action |
| error | | actionable message, retry, preserved input |
| success | | confirmation + next step |
| permission-denied | | explanation + how to get access |

### Data touched

| Data | Read | Written | Sensitivity | Validation |
|---|---|---|---|---|

### Responsive behaviour

| Breakpoint | Behaviour |
|---|---|
| ≥ 1280 px | |
| 768–1279 px | |
| < 768 px | |

### Accessibility notes

- Keyboard path:
- Focus order and focus return:
- Announcements:
- Target sizes:

### Acceptance criteria

- [ ] UF-01-AC1 — the flow completes in ≤ N steps from `<entry>`
- [ ] UF-01-AC2 — every failure path preserves user input
- [ ] UF-01-AC3 — abandonable and resumable at steps …

### Verification

| Check | How | Evidence |
|---|---|---|
| happy path | browser walkthrough | screenshots |
| failure paths | forced error (network offline, 500) | screenshots + notes |
| responsive | viewport sweep | screenshots at 3 widths |
| keyboard | keyboard-only walkthrough | notes |

<!-- Copy this section per flow. Keep the flow index at the top current. -->
