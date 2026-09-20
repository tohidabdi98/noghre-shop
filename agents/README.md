# Starter prompts

One file per role: `agents/<role>/STARTER_PROMPT.md`. Copy the **whole file** and paste it as the
first message of a coding-agent session. Then paste the context pack if the prompt asks for one.

```bash
# generate the context pack the prompt asks for, and copy the prompt to the clipboard
python scripts/tp.py context --module AUTH-001 --agent impl-auth-001
```

| Role | Prompt | Use it when |
|---|---|---|
| discovery | [`discovery/STARTER_PROMPT.md`](discovery/STARTER_PROMPT.md) | the project starts; you have an idea and want it specified |
| frontend-ux | [`frontend-ux/STARTER_PROMPT.md`](frontend-ux/STARTER_PROMPT.md) | requirements are approved; also whenever you want to rethink UX |
| architecture | [`architecture/STARTER_PROMPT.md`](architecture/STARTER_PROMPT.md) | requirements + UX are approved |
| decomposition | [`decomposition/STARTER_PROMPT.md`](decomposition/STARTER_PROMPT.md) | architecture is approved |
| orchestration | [`orchestration/STARTER_PROMPT.md`](orchestration/STARTER_PROMPT.md) | contracts exist; you want waves and assignments |
| implementation | [`implementation/STARTER_PROMPT.md`](implementation/STARTER_PROMPT.md) | one module is `ready` and assigned |
| testing | [`testing/STARTER_PROMPT.md`](testing/STARTER_PROMPT.md) | a PR or milestone needs verification |
| review | [`review/STARTER_PROMPT.md`](review/STARTER_PROMPT.md) | a module is `awaiting_review` |
| integration | [`integration/STARTER_PROMPT.md`](integration/STARTER_PROMPT.md) | ≥ 2 validated modules must work together |
| debugging | [`debugging/STARTER_PROMPT.md`](debugging/STARTER_PROMPT.md) | something is broken and needs a root cause |

Rules for using the prompts

1. **One role per session.** Mixing roles in one context is how scope discipline fails.
2. **Paste the prompt as-is.** It is written to be self-contained: it names every file the agent
   should read and every rule that binds it.
3. **Re-paste after any change request.** A session that started before a specification change is
   stale (`docs/workflows/failure_recovery.md` §stale agent context).
4. **The prompt is not the contract.** The binding contract is
   `docs/agents/agent_registry.yaml` — if a prompt and the registry disagree, the registry wins and
   the discrepancy is a bug to fix.
5. **Keep prompts and the notebook in sync:** after editing any prompt, run
   `python scripts/tp.py sync-notebook` (CI fails if they drift).

Everything the prompts reference lives in this repository, so nothing here depends on undocumented
knowledge or a specific coding-agent vendor.
