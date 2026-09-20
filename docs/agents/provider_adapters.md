# Provider adapters — running these roles in your coding-agent tool

> The framework's contracts (role, scope, branches, commits, PRs, state) are vendor-neutral. This
> file isolates the provider-specific details so they can be changed without touching the framework.
>
> **Assumption made by this template:** an agent is a *session in a coding tool* operated by you.
> The template supplies prompts, context packs, state, contracts and gates — it does not launch
> agents. If you later add automation (a driver that shells out to a CLI), treat it as an adapter
> listed here, not as a change to the workflow.

## 1. Instruction files by provider

| Provider / tool | Reads automatically | How to wire this framework |
|---|---|---|
| Any (generic) | — | paste `agents/<role>/STARTER_PROMPT.md` as the first message, then paste the context pack |
| OpenAI Codex CLI / Codex-style agents | `AGENTS.md` | works out of the box — `AGENTS.md` is the entry point |
| Claude Code | `CLAUDE.md` (and `AGENTS.md` if referenced) | create `CLAUDE.md` containing `See AGENTS.md — read it first, then the assigned role prompt.` Optionally add sub-agent definitions under `.claude/agents/` per role |
| Cursor | `.cursor/rules/*.mdc`, `.cursorrules` | add a rule that says: read `AGENTS.md`, then `agents/<role>/STARTER_PROMPT.md`, then the context pack for the assigned module |
| GitHub Copilot (chat / coding agent) | `.github/copilot-instructions.md` | point it at `AGENTS.md` and state the hard rules (scope, evidence, escalation) |
| Cline / Roo / Continue / Aider and similar | project rules / `CONVENTIONS.md` | same pattern: point at `AGENTS.md` + role prompt; keep the per-role scope in the prompt |
| Autonomous repo agents (issue-to-PR services) | repository instructions + issue text | open issues from `.github/ISSUE_TEMPLATE/module_proposal.md`; include the context pack in the issue body; require the PR template to be filled |

Whichever you use: **the role prompt + context pack is the unit of delegation.** Do not paste the
whole repository.

## 2. Recommended directory of adapters

```
CLAUDE.md                          (symlink/copy of a 3-line pointer to AGENTS.md)
.cursor/rules/00-project.mdc       (pointer + hard rules)
.github/copilot-instructions.md    (pointer + hard rules)
```

These files are intentionally **not** shipped by the template: they are provider-specific and
would create noise for users of other tools. Create only the one you need, keep it short, and never
let it duplicate the rules in `AGENTS.md` (link instead — `docs/README.md` rule 3).

## 3. Agent identity options

The template's default identity mechanism is **commit trailers + PR text**, which works everywhere:

```
Agent: impl-auth-001
Agent-Role: implementation
Module: AUTH-001
Validated-With: python scripts/verify.py (exit 0)
```

Stronger identities, in increasing order of setup cost:

| Option | How | Pros | Cons |
|---|---|---|---|
| Trailers only (default) | the human's Git identity pushes; the agent names itself in the message | zero setup, auditable in history | author is the human, tooling sees one author |
| Per-agent Git identity | set `user.name`/`user.email` per worktree or per clone: `git -c user.name="impl-auth-001" commit …` or `GIT_AUTHOR_NAME`/`GIT_AUTHOR_EMAIL` env vars | attribution is real in Git | must be configured per session/worktree; do not change global config |
| Per-agent bot account | one Git account per role/agent with fine-grained, least-privilege access | clean attribution, separate permissions, reviewable as an actor | account sprawl; PAT management |
| GitHub App / installation tokens | app installed on the repo, token minted per run with scoped permissions | best least-privilege story, short-lived tokens, bot identity in UI | most setup; needed only for real automation |

Document whichever you choose in `docs/project/conventions.md`. **Never** put tokens in the repo
(`docs/workflows/security.md`).

## 4. Branch and PR permissions per role

| Role | Branch write | PR create | PR review/comment | Merge |
|---|---|---|---|---|
| discovery, frontend-ux, architecture, decomposition | no (docs on their own branch if they prefer PR flow) | optional | comment | no |
| orchestration | state/handoff branches | optional | comment | no |
| implementation, debugging | own branch only | yes | comment | **never** |
| testing, review, integration | test/report branches when assigned | optional | yes | **never** |
| human | all | yes | yes | yes |

Enforce with branch protection + CODEOWNERS (`.github/CODEOWNERS`) rather than trust.

## 5. Tool surfaces an agent may need

| Need | Typical mechanism | Notes |
|---|---|---|
| Read/write files | the tool's file tools | scope enforced by `allowed_to_modify` and `pr-check` |
| Run commands | the tool's terminal | run `python scripts/verify.py`, `tp.py validate`, tests |
| Git | the tool's Git integration or CLI | never force-push, never commit to default branch |
| Browser / screenshots | the tool's browser automation (Playwright MCP, computer-use, or the human's browser) | required for UX validation when the provider supports it; otherwise the human captures screenshots (`docs/ux/visual_validation.md` §5) |
| External docs | web fetch/search | restrict to documentation needs; never fetch secrets |
| Production / databases | **not granted to agents** | see `docs/workflows/security.md` |

## 6. If your provider has no long context

Small-context or single-shot providers still work:

1. Generate a context pack: `python scripts/tp.py context --module AUTH-001 --format md`.
2. Paste the pack + the role prompt as the whole session input.
3. Ask for a single coherent deliverable (one file or one commit) rather than a whole module.
4. Repeat per file/commit; the state files and contracts carry continuity between sessions.

This is slower but preserves every guarantee of the framework — the state lives in the repository,
not in the model's context.
