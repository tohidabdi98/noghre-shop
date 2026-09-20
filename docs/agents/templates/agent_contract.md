# Agent contract template

> Copy the YAML below into `roles:` in `docs/agents/agent_registry.yaml`, then create
> `agents/<role>/STARTER_PROMPT.md`. `python scripts/tp.py validate` enforces the correspondence
> between the registry and the prompt files.

```yaml
  - role: <role-slug>                     # lowercase, matches the agents/<role>/ directory
    name: <Human Readable Name>
    category: conversational | analytical | coordination | implementation | validation
    agent_id_pattern: "<prefix>-<slug>-<seq>"     # e.g. "rev-dash-001"
    prompt: agents/<role-slug>/STARTER_PROMPT.md
    mission: "One sentence: what this role is for."
    inputs:                               # files this role reads
      - AGENTS.md
      - <path>
    outputs:                              # files this role writes (or artifacts it produces)
      - <path>
    tools: [read_repo, write_owned_docs, run_local_commands]
    authority: [read_repo, write_owned_docs]
    allowed_actions:
      - <action that is inside the role's remit>
    forbidden_actions:
      - <action that would break the framework's guarantees>
    scope:                                # path globs this role may write
      - <path or glob>
    escalation_conditions:
      - <condition that must go to the human>
    completion_criteria:
      - <observable condition that ends the role's work>
    handoff_to: [<role>, ...]
    may_combine_with: [<role>, ...]        # one instance may hold both scopes
    must_stay_separate_from: [<role>, ...] # combining would break independence
```

## Design rules for a new contract

1. **One mission, one sentence.** If it needs "and", it is probably two roles.
2. **Explicit scope.** A role without `scope` will wander; `pr-check` enforces the paths it is given.
3. **Write the forbidden list first.** The most valuable part of a contract is what the role must
   *not* do.
4. **Escalation must be concrete.** "Escalate uncertainty" is useless; list the decisions.
5. **Completion criteria are observable**, and end with evidence, not activity.
6. **Never give a validator the author's role** (`must_stay_separate_from`).
7. **Keep the prompt and contract aligned.** The prompt explains *how*, the contract defines *what*.
