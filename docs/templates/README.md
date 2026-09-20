# Artifact templates

Copy these when you need the artifact. **Never edit a template in place** — each one is the
canonical shape that agents and `python scripts/tp.py validate` expect.

| Template | Used for | Written to |
|---|---|---|
| `requirements.md` | the product specification | `docs/project/requirements.md` (already present — this copy is for reference/parallel drafts) |
| `adr.md` | architecture decision record | appended to `docs/project/decisions.md` |
| `change_request.md` | a significant change after approval | `docs/project/change_requests/CR-###-slug.md` |
| `user_flow.md` | one user flow | appended to `docs/ux/user_flows.md` |
| `screen_spec.md` | one screen specification | appended to `docs/ux/screens.md` |
| `review_report.md` | a review or validation report | `reports/<MODULE-ID>/review-<date>.md` |

Agent-specific artifacts (handoff, validation report, failure report, agent instance, agent
contract) live in `docs/agents/templates/`.

Conventions that apply to every artifact:

- **Tag claims**: `[DECISION]`, `[REC]`, `[ASSUMPTION] ASM-###`, `[OPEN] OQ-###`, `[RISK] RISK-###`.
- **IDs are permanent**: `FR-###`, `NFR-###`, `UX-###`, `UF-##`, `ADR-###`, `DEC-###`, `CR-###`.
- **One source of truth per fact** (`docs/README.md`); link instead of copying.
- **Name the author**: a human name or an `agent-id`, always.
