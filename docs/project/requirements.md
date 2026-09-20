# Requirements — NoghreShop

> **Status:** draft · **Approved by:** — · **Last updated:** —
>
> **How to use this file.** The Discovery Agent owns it. It is written *after* the discovery
> interview, never before: the agent interviews the human, then records what was actually
> agreed. It is the **source of truth for what the product must do**.
>
> Rules
> * Tag every statement: `[DECISION]`, `[REC]`, `[ASSUMPTION] ASM-###`, `[OPEN] OQ-###`, `[RISK] RISK-###`.
> * Number requirements: `FR-###` (functional), `NFR-###` (non-functional), `UX-###` (UX, owned
>   by `docs/ux/`). Never renumber; retire with `status: retired` in `requirements.yaml`.
> * Every heading for a requirement must contain its ID so `scripts/tp.py context` can extract
>   exactly the requirements a module needs (e.g. `### FR-AUTH-1 — Password reset`).
> * Anything not agreed here is **not** a requirement. Agents may not invent requirements.
> * The human approval gate is `state/project.yaml → gates.requirements_approved`.
>
> Approval checklist (human): scope is honest · out-of-scope is explicit · success criteria are
> measurable · no requirement contradicts another · every `[OPEN]` item is either resolved or
> knowingly accepted as a risk.

---

## 1. Product

### 1.1 Problem statement
<!-- What problem exists today, for whom, and why existing solutions are insufficient. -->

### 1.2 Vision (one paragraph)
<!-- The shortest honest description of what we are building. -->

### 1.3 Target users
<!-- Personas at product level. Persona *UX* detail lives in docs/ux/ux_requirements.md. -->
| Persona | Who they are | Primary goal | Notes |
|---|---|---|---|
| | | | |

### 1.4 Core use cases
| ID | Use case | Actor | Trigger | Outcome |
|---|---|---|---|---|
| UC-1 | | | | |

### 1.5 Success criteria
<!-- Measurable. If you cannot measure it, it is a hope, not a criterion. -->
| ID | Criterion | Measurement | Target |
|---|---|---|---|
| SC-1 | | | |

### 1.6 Scope (in)
- <!-- agreed capability -->

### 1.7 Out of scope (explicitly not built)
- <!-- capability we deliberately exclude; agents must not implement these -->
  `[DECISION]`

### 1.8 Business rules
| ID | Rule | Applies to | Notes |
|---|---|---|---|
| BR-1 | | | |

### 1.9 Constraints and assumptions
<!-- Constraints: fixed boundaries (legal, budget, platform, deadline).
     Assumptions: beliefs that must hold — mirror each into assumptions.md. -->

---

## 2. Functional requirements

> Detail per requirement: behaviour, inputs, outputs, state transitions, permissions, error
> behaviour, edge cases. Behaviour belongs here; visual/flow detail belongs in `docs/ux/`.

### FR-AUTH-1 — <name> `[DECISION]`
- **Status:** proposed · **Priority:** must / should / could
- **Actor:**
- **Description:** <!-- what happens, in behavioural terms -->
- **Acceptance criteria:**
  - [ ] AC-FR-AUTH-1.1 — measurable, testable statement
  - [ ] AC-FR-AUTH-1.2 —
- **Permissions / roles:**
- **State transitions:**
- **Edge cases:**
- **Error behaviour:**
- **Related UX:** `UX-###`

<!-- Copy the block above for each functional requirement. -->

---

## 3. Non-functional requirements

> Each NFR must state how it is verified, otherwise it will be ignored.

| ID | Category | Requirement | Target | Verification |
|---|---|---|---|---|
| NFR-PERF-1 | performance | | | |
| NFR-SEC-1 | security | | | |
| NFR-SCALE-1 | scalability | | | |
| NFR-A11Y-1 | accessibility | | | `docs/ux/visual_validation.md` |
| NFR-OBS-1 | observability | | | |
| NFR-MAINT-1 | maintainability | | | |
| NFR-PRIV-1 | privacy/compliance | | | |

---

## 4. Data

### 4.1 Entities and ownership
| Entity | Owning module | Sensitivity | Retention |
|---|---|---|---|
| | | | |

### 4.2 Data flows
<!-- Cross-system movement of data, including third parties. -->

### 4.3 Privacy and compliance
<!-- What personal data exists, where it lives, who may see it, what must be deletable. -->

---

## 5. Integrations and external services

| Service | Purpose | Auth model | Failure behaviour | Cost |
|---|---|---|---|---|
| | | | | |

---

## 6. Engineering requirements

| Area | Requirement |
|---|---|
| Testing | |
| CI/CD | |
| Coding conventions | see `docs/project/conventions.md` |
| Dependency policy | see `docs/project/conventions.md` |
| Documentation | |
| Definition of done | see `docs/project/definition_of_done.md` |

---

## 7. Open items

Unresolved items are tracked in `docs/project/open_questions.md`; do not bury them here.

| Type | ID | Summary |
|---|---|---|
| OPEN | OQ-001 | |
| ASSUMPTION | ASM-001 | |
| RISK | RISK-001 | |

---

## 8. Change log

| Date | Change | By | Reference |
|---|---|---|---|
| | initial draft | discovery | — |
