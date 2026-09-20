# Git workflow

Git is not bookkeeping here — it is **part of the coordination system**. Branches encode ownership,
commit trailers encode identity, PRs encode evidence, and history encodes what actually happened.

## 1. Branches

| Purpose | Pattern | Example | Created by |
|---|---|---|---|
| Agent work on a module | `agent/<agent-id>/<MODULE-ID>` | `agent/impl-auth-001/AUTH-001` | `python scripts/tp.py start …` |
| Human work | `human/<name>/<topic>` | `human/tohid/nav-rework` | human |
| Integration of a milestone | `integration/<milestone>` | `integration/M1-core` | integration agent / human |
| Release | `release/<version>` | `release/0.2.0` | human |
| Hotfix | `hotfix/<MODULE-ID>-<slug>` | `hotfix/AUTH-001-token-expiry` | human |

Rules

- **Never commit directly to the default branch.** It is protected: PR + passing checks + review.
- **One module per agent branch.** A branch that touches two modules' ownership sets is a
  decomposition problem — split it or escalate.
- **Replacing an agent** means a new branch from the default branch (or from the failed branch if it
  carries useful commits) — see `failure_recovery.md`.
- **Long-lived branches are a smell.** Rebase on the default branch daily; a module should live for
  a day or two, not a week.

## 2. Commits

```
<type>(<scope>): <subject>          ≤ 72 chars, imperative, no trailing period

<body: what changed and why, wrapped at 72>

Agent: impl-auth-001
Agent-Role: implementation
Module: AUTH-001
Refs: #42
Validated-With: python scripts/verify.py (exit 0), 14 passed
```

| Element | Rule |
|---|---|
| type | `feat` `fix` `refactor` `perf` `docs` `test` `build` `ci` `chore` `revert` `spec` `ux` `contract` |
| scope | a `MODULE-ID`, or `repo` for repository-wide changes (docs, CI, tooling) |
| trailers | `Agent`, `Agent-Role`, `Module` **required** on `agent/*` branches; `Refs` and `Validated-With` expected |
| granularity | one coherent change; never mix a refactor with a behaviour change |

Enable the template: `git config commit.template .gitmessage`.
Enforced in CI by `python scripts/tp.py pr-check`.

## 3. Pull requests

**Title:** `[<MODULE-ID>] <type>: <summary> — agent <agent-id>`
**Body:** the repository template, filled completely:
`.github/pull_request_template.md` (Module, Agent, Summary, Implementation details, Acceptance
criteria, Tests executed, Validation results, Known limitations, Risks, Dependencies, Screenshots).

PR rules

1. One module per PR. Cross-module changes need the orchestrator's agreement and a contract
   permission, and are labelled `cross-module`.
2. Self-review before opening: re-read your own diff and remove unrelated changes.
3. Evidence in the body: exact commands and outcomes, not adjectives.
4. Do not merge your own PR. Agents never merge; the human merges (or delegates explicitly).
5. Keep the PR description current if the PR changes during review.
6. A `Blocking` finding must be resolved or explicitly downgraded by the human before merge.

Labels (typical): `module:<ID>` `agent` `state:review` `cross-module` `ux` `security` `needs-human`.

## 4. Merge policy

| Situation | Merge style |
|---|---|
| Module PR | squash merge into the default branch (or the integration branch during a milestone) |
| Multi-commit narrative worth keeping | rebase merge, commits already conventional |
| Never | merge commit from an agent branch into the protected branch by an agent |

After merge: the module moves to `complete`; the branch may be deleted; `state/modules.yaml` is
updated by the orchestrator (`tp.py status` should reflect reality).

## 5. Merge conflicts

1. Rebase your branch on the default branch (`git fetch && git rebase origin/main`).
2. Resolve conflicts **inside your ownership**. A conflict in a shared zone or another module's file
   means ownership was violated: stop, escalate (`failure_recovery.md` §merge conflicts).
3. Re-run validation after resolving; conflicts change behaviour more often than people expect.
4. Never resolve a conflict by discarding the other side "because it was not your change".

## 6. Protected branch settings (required, one-time)

| Setting | Value |
|---|---|
| Protect `main` | no direct pushes, no force-push, no deletion |
| Required checks | `ci`, `agent-pr-check` |
| Required reviews | 1 (human or review agent acting for the human) |
| Dismiss stale reviews on new commits | on |
| Require linear history | recommended (squash/rebase only) |
| Require conversation resolution | on (forces blocking findings to be addressed) |
| CODEOWNERS review | required for `state/**`, `docs/project/**`, `modules/**` |

GitHub: Settings → Branches. GitLab equivalents: *Protected branches* + *Merge request approvals*
+ *Status checks* (`.gitlab-ci.yml` jobs with the same names). Bitbucket: branch restrictions + merge
checks. The conventions above are provider-independent.

## 7. Anti-patterns (seen in agent-driven repositories)

| Anti-pattern | Why it hurts | Instead |
|---|---|---|
| One giant branch accumulating every module | reviews collapse, conflicts multiply | one branch per module, short-lived |
| `--force` after review | invalidates the evidence the reviewer relied on | new commits, or a re-reviewed force-push with notice |
| Commit message `wip` / `fix stuff` | destroys the audit trail | conventional message + trailers, always |
| Merging with failing checks "temporarily" | silently invalidates the validation model | fix, or record an explicit human waiver in the PR |
| Agent edits another module to unblock itself | breaks ownership, hides integration problems | consume the interface, request the change, or escalate |
