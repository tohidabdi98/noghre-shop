#!/usr/bin/env python3
"""tp.py — the TemplateProject command line.

    bootstrap      create a project from the template (copy + placeholders + identity + git init)
    new-module     scaffold a module contract and register it in state
    validate       state + contracts + doc links + prompt sync (the integrity gate)
    sync-notebook  keep HOW_TO_USE.ipynb prompt cells in sync with agents/*/STARTER_PROMPT.md
    status         the board: states, blockers, open questions, next actions
    ready          ready set, dependency waves, overlap/shared-zone warnings
    context        layered context pack for one module (+ agent)
    start          create the agent branch and move the module to in_progress
    handoff        replace an agent losslessly (records the handoff)
    pr-check       CI gate: branch/commit conventions, ownership, PR completeness

Standard library only. Run `python scripts/tp.py <command> --help` for options.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tplib import checks, context as context_mod, repoutil  # noqa: E402
from tplib import state as state_mod  # noqa: E402
from tplib.yamlmini import YamlError  # noqa: E402

PASS = 0
FAIL = 1
USAGE = 2

# Human-readable output uses arrows, dashes and box characters. Legacy Windows consoles default to a
# code page that cannot encode them, which would turn every run into a UnicodeEncodeError; replace
# rather than crash (the files themselves stay UTF-8).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):  # pragma: no cover - non-standard streams
        pass


# --------------------------------------------------------------------------------------
# shared helpers
# --------------------------------------------------------------------------------------
def resolve_root(args):
    if getattr(args, "root", None):
        return repoutil.find_root(args.root)
    return repoutil.find_root(os.getcwd())


def load(root):
    return state_mod.load_state(root)


def fail(message, code=FAIL):
    print("x %s" % message, file=sys.stderr)
    return code


def ok(message):
    print("ok %s" % message)
    return PASS


def save_modules(root, state):
    payload = {"schema_version": 1, "updated_at": repoutil.today(), "modules": state["modules"]}
    repoutil.write_text(
        state_mod.state_path(root, "modules"), repoutil.dump_yaml(state_mod.HEADERS["modules"], payload)
    )


def save_agents(root, state):
    payload = {"schema_version": 1, "updated_at": repoutil.today(), "agents": state["agents"]}
    repoutil.write_text(
        state_mod.state_path(root, "agents"), repoutil.dump_yaml(state_mod.HEADERS["agents"], payload)
    )


def save_edges(root, state):
    payload = {"schema_version": 1, "updated_at": repoutil.today(), "edges": state["edges"]}
    repoutil.write_text(
        state_mod.state_path(root, "dependencies"),
        repoutil.dump_yaml(state_mod.HEADERS["dependencies"], payload),
    )


# --------------------------------------------------------------------------------------
# bootstrap
# --------------------------------------------------------------------------------------
def _clean(value, fallback=""):
    """Treat an unreplaced placeholder as "not supplied" instead of copying it forward."""
    if value is None:
        return fallback
    text = str(value)
    return fallback if "{{" in text else text


def cmd_bootstrap(args):
    destination = getattr(args, "destination", None)
    if destination and getattr(args, "root", None):
        return fail("give either a destination path or --root, not both")
    if destination:
        destination = os.path.abspath(destination)
        source = os.path.abspath(resolve_root(args))
        inside = os.path.normcase(destination).startswith(os.path.normcase(source) + os.sep)
        if os.path.isfile(destination):
            return fail("destination %s is a file" % destination)
        if inside:
            return fail("destination must be outside the template (%s)" % source)
        if os.path.isfile(os.path.join(destination, "state", "project.yaml")):
            print("bootstrap: %s already holds a project — filling it in place" % destination)
        else:
            _copy_template(source, destination)
            print("bootstrap: copied the template from %s to %s" % (source, destination))
        root = repoutil.find_root(destination)
    else:
        root = resolve_root(args)
    state = load(root)
    project = state["project"]
    project_id = args.id or _slugify(_clean(args.name) or _clean(project.get("name")) or "project")
    name = _clean(args.name) or _clean(project.get("name")) or project_id
    mapping = {
        "{{PROJECT_ID}}": project_id,
        "{{PROJECT_NAME}}": name,
        "{{PROJECT_DESCRIPTION}}": _clean(args.description),
        "{{OWNER}}": _clean(args.owner),
        "{{REPO_URL}}": _clean(args.repo_url),
        "{{DEFAULT_BRANCH}}": _clean(args.branch, "main"),
    }
    project.update(
        {
            "project_id": project_id,
            "name": name,
            "description": _clean(args.description) or _clean(project.get("description")) or "",
            "owner": _clean(args.owner) or _clean(project.get("owner")) or "",
            "repo_url": _clean(args.repo_url) or _clean(project.get("repo_url")) or "",
            "default_branch": _clean(args.branch, "main") or _clean(project.get("default_branch")) or "main",
            "profile": args.profile or project.get("profile") or "fullstack",
            "initialised": True,
            "created_at": repoutil.today(),
            "updated_at": repoutil.today(),
        }
    )
    repoutil.write_text(
        state_mod.state_path(root, "project"),
        repoutil.dump_yaml(state_mod.HEADERS["project"], project),
    )
    changed = repoutil.replace_placeholders(
        root, mapping, exclude_paths=("HOW_TO_USE.ipynb",), skip_prefixes=("examples/", "scripts/")
    )
    touched = {relative for relative, _ in changed}
    if _prepend_readme_banner(root, project):
        touched.add("README.md")
    if _stamp_env_example(root, name):
        touched.add(".env.example")
    if getattr(args, "adopt_env", False):
        if _adopt_env(root):
            touched.add(".env")
    print("bootstrap: %d file(s) updated" % len(touched))
    for relative, count in changed[:20]:
        print("  - %s (%d substitution%s)" % (relative, count, "" if count == 1 else "s"))
    if len(changed) > 20:
        print("  - … and %d more" % (len(changed) - 20))

    remaining = repoutil.find_placeholders(
        root, exclude_paths=checks.load_config(root).get("placeholder_check_exclude") or ()
    )
    if remaining:
        print("\nstill-unreplaced placeholders (fix by hand):")
        for relative, line, token in remaining[:10]:
            print("  - %s:%d %s" % (relative, line, token))

    if args.init_git:
        code, _, _ = repoutil.git(["rev-parse", "--is-inside-work-tree"], root)
        if code == 0:
            print("\ngit: repository already initialised — skipping --init-git")
        else:
            repoutil.git(["init", "-b", project["default_branch"]], root)
            repoutil.git(["add", "."], root)
            repoutil.git(
                [
                    "-c",
                    "user.name=%s" % (project.get("owner") or "bootstrap"),
                    "-c",
                    "user.email=bootstrap@example.invalid",
                    "commit",
                    "-m",
                    "chore(repo): import TemplateProject template",
                ],
                root,
            )
            print("\ngit: repository initialised and first commit created")

    print(
        "\nnext steps\n"
        "  1. review state/project.yaml (profile, gates, shared_zones)\n"
        "  2. python scripts/tp.py validate            # must be clean before you start\n"
        "  3. create the remote repository, protect the default branch (docs/workflows/git_workflow.md §6)\n"
        "  4. open HOW_TO_USE.ipynb section B and paste agents/discovery/STARTER_PROMPT.md\n"
    )
    return PASS


def _copy_template(source, destination):
    """Copy the framework tree into a new project directory.

    VCS metadata, caches, scratch directories and any local `.env` stay behind: a new project starts
    with a clean history and without somebody else's secrets.
    """
    ignored = {
        ".git",
        ".tmp",
        ".freebuff",
        "__pycache__",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "node_modules",
        ".venv",
        "venv",
        ".env",
    }

    def ignore(directory, names):
        skip = {name for name in names if name in ignored or name.endswith(".pyc")}
        if os.path.basename(directory) == "state":
            skip |= {name for name in names if name == ".cache"}
        return skip

    os.makedirs(destination, exist_ok=True)
    shutil.copytree(source, destination, ignore=ignore, dirs_exist_ok=True)
    return destination


def _adopt_env(root):
    """Copy `.env.example` to a local, gitignored `.env` (never overwrites an existing one)."""
    example = os.path.join(root, ".env.example")
    target = os.path.join(root, ".env")
    if not os.path.isfile(example):
        print("adopt-env: no .env.example to copy")
        return False
    if os.path.isfile(target):
        print("adopt-env: .env already exists — left untouched")
        return False
    repoutil.write_text(target, repoutil.read_text(example))
    print("adopt-env: created .env from .env.example (gitignored — put real values there, never in Git)")
    return True


def _prepend_readme_banner(root, project):
    path = os.path.join(root, "README.md")
    if not os.path.isfile(path):
        return False
    text = repoutil.read_text(path)
    if text.lstrip().startswith("<!-- PROJECT-BANNER -->"):
        return False
    banner = (
        "<!-- PROJECT-BANNER -->\n"
        "# %s\n\n"
        "- **Project ID:** `%s`\n"
        "- **Owner:** %s\n"
        "- **Profile:** `%s`\n"
        "- **Stage:** `%s` · gates and state in `state/project.yaml`\n\n"
        "> How this project is developed: [`HOW_TO_USE.ipynb`](HOW_TO_USE.ipynb).\n"
        "> The template documentation below describes the framework this project is built on — keep it,\n"
        "> it is the operating manual for every agent that works here.\n\n"
        "---\n\n"
        "# Template documentation (framework reference)\n\n"
        % (project.get("name") or "Project", project.get("project_id"), project.get("owner") or "—", project.get("profile"), project.get("stage"))
    )
    body = text.replace(
        "# TemplateProject — an AI-native software project template", "", 1
    )
    repoutil.write_text(path, banner + body.lstrip("\n"))
    return True


def _stamp_env_example(root, name):
    path = os.path.join(root, ".env.example")
    if not os.path.isfile(path):
        return False
    text = repoutil.read_text(path)
    updated = text.replace("{{PROJECT_NAME}}", name)
    if updated != text:
        repoutil.write_text(path, updated)
        return True
    return False


def _slugify(text):
    cleaned = "".join(character if character.isalnum() else "-" for character in (text or "").lower())
    return "-".join(part for part in cleaned.split("-") if part) or "project"


# --------------------------------------------------------------------------------------
# new-module
# --------------------------------------------------------------------------------------
def cmd_new_module(args):
    root = resolve_root(args)
    state = load(root)
    module_id = args.id.upper()
    if not state_mod.MODULE_ID_RE.match(module_id):
        return fail("module id `%s` must look like AUTH-001" % module_id)
    if state_mod.module_by_id(state, module_id):
        return fail("module %s is already registered in state/modules.yaml" % module_id)
    template_path = os.path.join(root, "docs", "modules", "template.md")
    if not os.path.isfile(template_path):
        return fail("docs/modules/template.md not found — cannot scaffold a contract")
    slug = args.slug or _slugify(module_id.split("-")[0] if args.slug is None else args.slug)
    text = repoutil.read_text(template_path)
    for token, value in (
        ("MODULE-001", module_id),
        ("MODULE-ID", module_id),
        ("Module Name", args.name),
        ("module_slug", slug),
    ):
        text = text.replace(token, value)
    contract_relative = "modules/%s.md" % module_id
    repoutil.write_text(os.path.join(root, contract_relative), text)

    depends_on = list(args.dep or [])
    state["modules"].append(
        {
            "module_id": module_id,
            "name": args.name,
            "contract": contract_relative,
            "priority": args.priority,
            "status": "planned",
            "assigned_agent": None,
            "branch": None,
            "pr": None,
            "validation": "pending",
            "blocked_reason": None,
            "updated_at": repoutil.today(),
            "history": [
                {"at": repoutil.today(), "from": None, "to": "planned", "by": args.actor, "reason": "contract scaffolded"}
            ],
        }
    )
    for upstream in depends_on:
        if state_mod.module_by_id(state, upstream) is None:
            print("  ! %s is not registered yet — the edge will fail validation until it is" % upstream)
        state["edges"].append(
            {
                "from": module_id,
                "to": upstream,
                "type": args.edge_type,
                "interface": "",
                "status": "pending",
                "notes": "created by tp.py new-module — describe the interface and freeze it",
            }
        )
    repoutil.write_text(
        os.path.join(root, "state", "modules.yaml"),
        repoutil.dump_yaml(
            state_mod.HEADERS["modules"], {"schema_version": 1, "updated_at": repoutil.today(), "modules": state["modules"]}
        ),
    )
    repoutil.write_text(
        os.path.join(root, "state", "dependencies.yaml"),
        repoutil.dump_yaml(
            state_mod.HEADERS["dependencies"], {"schema_version": 1, "updated_at": repoutil.today(), "edges": state["edges"]}
        ),
    )
    print("created %s and registered %s" % (contract_relative, module_id))
    print(
        "next:\n"
        "  - fill acceptance_criteria, validation commands, interfaces and ownership in %s\n"
        "  - run `python scripts/tp.py validate`\n"
        "  - run `python scripts/tp.py ready` then `python scripts/tp.py start --module %s --agent impl-%s-001`\n"
        % (contract_relative, module_id, slug)
    )
    return PASS


# --------------------------------------------------------------------------------------
# validate / sync-notebook
# --------------------------------------------------------------------------------------
def cmd_validate(args):
    root = resolve_root(args)
    try:
        state = load(root)
    except (YamlError, FileNotFoundError) as exc:
        return fail("could not load state: %s" % exc)
    issues = checks.validate(root, state, strict=args.strict)
    errors_found = checks.errors(issues)
    warnings_found = checks.warnings(issues)
    infos = [item for item in issues if item["level"] == "info"]
    for item in errors_found:
        print("x [%s] %s" % (item["code"], item["message"]))
    for item in warnings_found:
        print("! [%s] %s" % (item["code"], item["message"]))
    # `template.*` notices always print: a pristine template must say so rather than look broken.
    for item in infos:
        if args.verbose or item["code"].startswith("template."):
            print("· [%s] %s" % (item["code"], item["message"]))
    print(
        "\n%d error(s), %d warning(s), %d module(s) · yaml backend: %s"
        % (len(errors_found), len(warnings_found), len(state["modules"]), repoutil.yaml_backend())
    )
    if errors_found:
        return FAIL
    if args.strict and warnings_found:
        print("strict mode: warnings are errors")
        return FAIL
    return PASS


def cmd_sync_notebook(args):
    root = resolve_root(args)
    path = os.path.join(root, "HOW_TO_USE.ipynb")
    if not os.path.isfile(path):
        return fail("HOW_TO_USE.ipynb not found")
    payload = json.loads(repoutil.read_text(path))
    updated = 0
    for cell in payload.get("cells", []):
        source = "".join(cell.get("source") or [])
        match = checks.PROMPT_RE.search(source)
        if not match:
            continue
        relative = match.group(1)
        file_path = os.path.join(root, relative)
        if not os.path.isfile(file_path):
            print("! %s is referenced but missing — skipped" % relative)
            continue
        prompt = repoutil.read_text(file_path).rstrip("\n")
        new_source = _replace_prompt_block(source, prompt)
        if new_source != source:
            cell["source"] = new_source.splitlines(keepends=True)
            updated += 1
    if updated:
        repoutil.write_text(path, json.dumps(payload, indent=1, ensure_ascii=False) + "\n")
    print("sync-notebook: %d prompt cell(s) updated" % updated)
    return PASS


def _replace_prompt_block(source, prompt):
    """Rewrite the fenced prompt block that follows the PROMPT-SYNC marker.

    The fence is one backtick longer than the longest fence inside the prompt, because prompts
    contain their own ``` blocks.
    """
    longest = 0
    for line in prompt.split("\n"):
        length = checks._fence_length(line)
        if length > longest:
            longest = length
    fence = "`" * max(4, longest + 1)
    lines = source.split("\n")
    out = []
    skipping = False
    written = False
    opening = 0
    for line in lines:
        if not skipping and checks.PROMPT_RE.search(line):
            out.append(line)
            out.append(fence + "text")
            out.extend(prompt.split("\n"))
            out.append(fence)
            written = True
            skipping = True
            opening = 0
            continue
        if skipping:
            length = checks._fence_length(line)
            if not opening:
                if length:
                    opening = length
                continue
            if length >= opening:
                skipping = False
            continue
        out.append(line)
    if not written:
        out.extend([fence + "text", prompt, fence])
    return "\n".join(out)


# --------------------------------------------------------------------------------------
# status / ready
# --------------------------------------------------------------------------------------
def cmd_status(args):
    root = resolve_root(args)
    state = load(root)
    board = state_mod.compute_board(root, state)
    project = state["project"]
    uninitialised = project.get("initialised") is False or project.get("profile") == "template"
    payload = {
        "project": {
            "initialised": not uninitialised,
            "id": project.get("project_id"),
            "name": project.get("name"),
            "stage": project.get("stage"),
            "milestone": project.get("milestone"),
            "gates": project.get("gates"),
        },
        "board": board,
        "modules": state["modules"],
        "agents": state["agents"],
    }
    if args.json:
        print(json.dumps(payload, indent=2))
        return PASS
    if uninitialised:
        print("! uninitialised template — placeholders in state/project.yaml and docs/project/* are expected")
        print("  run: python scripts/tp.py bootstrap <dir> --name \"...\" --project-id <id> --profile <frontend|backend|fullstack>")
        print()
    print("%s (%s) · stage %s · milestone %s" % (project.get("name"), project.get("project_id"), project.get("stage"), project.get("milestone")))
    gates = project.get("gates") or {}
    print("gates: " + ", ".join("%s=%s" % (key, value) for key, value in sorted(gates.items())))
    print()
    by_status = {}
    for module in state["modules"]:
        by_status.setdefault(module.get("status") or "unknown", []).append(module)
    if not state["modules"]:
        print("no modules registered yet — decomposition has not happened (expected before stage 4)")
    for status in state_mod.MODULE_STATUSES:
        entries = by_status.get(status) or []
        if not entries:
            continue
        print("%-18s %s" % (status, ", ".join(_module_label(entry) for entry in entries)))
    if board["blocked"]:
        print("\nblocked:")
        for module in state["modules"]:
            if module.get("status") == "blocked":
                print("  - %s — %s" % (module["module_id"], module.get("blocked_reason") or "no reason recorded"))
    if state["agents"]:
        print("\nagents:")
        for agent in state["agents"]:
            print(
                "  - %-18s %-14s %-9s %s"
                % (agent.get("agent_id"), agent.get("role"), agent.get("status"), agent.get("current_task") or "—")
            )
    open_questions = _register_rows(root, "docs/project/open_questions.md")
    risks = _register_rows(root, "docs/project/risks.md")
    print("\nopen questions: %d · risks: %d · ready: %s" % (open_questions, risks, ", ".join(board["ready"]) or "none"))
    print("\nnext actions:")
    for line in _next_actions(state, board):
        print("  - %s" % line)
    return PASS


def _module_label(module):
    parts = [module.get("module_id")]
    if module.get("assigned_agent"):
        parts.append("→%s" % module["assigned_agent"])
    if module.get("pr"):
        parts.append("PR#%s" % module["pr"])
    if module.get("validation") and module["validation"] != "pending":
        parts.append("[%s]" % module["validation"])
    return " ".join(parts)


def _register_rows(root, relative):
    path = os.path.join(root, relative)
    if not os.path.isfile(path):
        return 0
    rows = 0
    for line in repoutil.read_text(path).splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and "|" in stripped[1:] and "--" not in stripped:
            first = stripped.strip("|").split("|")[0].strip()
            if first and first.upper() not in ("ID", "ITEM", "QUESTION") and not first.startswith("#"):
                rows += 1
    return rows


def _next_actions(state, board):
    actions = []
    project = state["project"]
    gates = project.get("gates") or {}
    if not gates.get("requirements_approved"):
        actions.append("start/continue the Discovery Agent (agents/discovery/STARTER_PROMPT.md)")
    if project.get("profile") != "backend" and gates.get("requirements_approved") and not gates.get("ux_approved"):
        actions.append("run the Frontend/UX Agent (agents/frontend-ux/STARTER_PROMPT.md)")
    if gates.get("ux_approved") and not gates.get("architecture_approved"):
        actions.append("run the Architecture Agent (agents/architecture/STARTER_PROMPT.md)")
    if gates.get("architecture_approved") and not gates.get("decomposition_approved"):
        actions.append("run the Module Decomposition Agent (agents/decomposition/STARTER_PROMPT.md)")
    if board["blocked"]:
        actions.append("resolve blockers: %s" % ", ".join(board["blocked"]))
    if board["awaiting_review"]:
        actions.append("review: %s (agents/review/STARTER_PROMPT.md)" % ", ".join(board["awaiting_review"]))
    if board["ready"]:
        actions.append("assign ready modules: %s (agents/orchestration/STARTER_PROMPT.md)" % ", ".join(board["ready"]))
    if board["warnings"]:
        actions.append("resolve parallelism warnings before starting the next wave")
    if not actions:
        actions.append("nothing pending — check docs/project/project_state.md for the next milestone")
    return actions


def cmd_ready(args):
    root = resolve_root(args)
    state = load(root)
    board = state_mod.compute_board(root, state)
    print("ready modules: %s" % (", ".join(board["ready"]) or "none"))
    for depth, modules in board["waves"].items():
        print("  wave %s (depth %d): %s" % (depth + 1, depth, ", ".join(modules)))
    for warning in board["warnings"]:
        print("! %s" % warning)
    for error in board["errors"]:
        print("x %s" % error)
    if board["blocked"]:
        print("blocked: %s" % ", ".join(board["blocked"]))
    if board["failed"]:
        print("failed: %s" % ", ".join(board["failed"]))
    for module_id in board["ready"]:
        module = state_mod.module_by_id(state, module_id)
        upstreams = state_mod.upstream_of(state, module_id)
        print(
            "  start with: python scripts/tp.py start --module %s --agent impl-%s-001   (deps: %s)"
            % (module_id, module_id.split("-")[0].lower(), ", ".join(upstreams) or "none")
        )
    return FAIL if board["errors"] else PASS


# --------------------------------------------------------------------------------------
# context
# --------------------------------------------------------------------------------------
def cmd_context(args):
    root = resolve_root(args)
    state = load(root)
    try:
        pack = context_mod.build_pack(root, state, args.module, args.agent)
    except KeyError as exc:
        return fail(str(exc))
    if args.format == "json":
        payload = json.dumps(pack["layers"], indent=2)
    else:
        payload = pack["markdown"]
    if args.out:
        repoutil.write_text(args.out if os.path.isabs(args.out) else os.path.join(root, args.out), payload)
        print("wrote %s (%d lines)" % (args.out, payload.count("\n") + 1))
    else:
        print(payload)
    return PASS


# --------------------------------------------------------------------------------------
# start
# --------------------------------------------------------------------------------------
def cmd_start(args):
    root = resolve_root(args)
    state = load(root)
    module = state_mod.module_by_id(state, args.module)
    if module is None:
        return fail("module %s is not registered — create it with `tp.py new-module` first" % args.module)
    if module.get("status") not in ("planned", "ready", "assigned", "blocked", "failed"):
        return fail(
            "module %s is `%s` — start is only valid from planned/ready/assigned/blocked/failed"
            % (args.module, module.get("status"))
        )
    unmet = [
        upstream
        for upstream in state_mod.upstream_of(state, args.module)
        if (state_mod.module_by_id(state, upstream) or {}).get("status") not in state_mod.TERMINAL_STATUSES
    ]
    if unmet and not args.force:
        return fail(
            "module %s depends on %s which are not validated/complete — finish them first "
            "(override only with an explicit reason via --force)" % (args.module, ", ".join(unmet))
        )
    if args.force:
        print("! overriding dependency readiness — record the reason in the module history")

    branch = "agent/%s/%s" % (args.agent, args.module)
    role = args.role or "implementation"
    agent_entry = next((item for item in state["agents"] if item.get("agent_id") == args.agent), None)
    if agent_entry is None:
        agent_entry = {
            "agent_id": args.agent,
            "name": "%s %s" % (args.module, role.title()),
            "role": role,
            "category": "implementation" if role in ("implementation", "debugging") else role,
            "module_id": args.module,
            "project_id": state["project"].get("project_id"),
            "branch": branch,
            "status": "active",
            "current_task": args.task or "implement %s to its contract" % args.module,
            "parent_agent": None,
            "replaced_by": None,
            "created_at": repoutil.today(),
            "updated_at": repoutil.today(),
            "tools": ["read_repo", "write_code", "run_local_commands", "create_branch", "create_commit", "create_pull_request"],
            "authority": ["modify assigned module", "create tests", "create commits", "create pull request"],
            "validation": [],
            "notes": "",
        }
        state["agents"].append(agent_entry)
    else:
        agent_entry.update({"status": "active", "branch": branch, "module_id": args.module, "updated_at": repoutil.today()})

    module["assigned_agent"] = args.agent
    module["branch"] = branch
    if module.get("status") in ("blocked", "failed"):
        state_mod.apply_transition(state, args.module, "ready", args.agent, args.force_reason or "unblocked")
    if module.get("status") == "planned":
        state_mod.apply_transition(state, args.module, "ready", args.agent, "readiness confirmed")
    if module.get("status") == "ready":
        state_mod.apply_transition(state, args.module, "assigned", args.agent, "assigned by %s" % args.actor)
    state_mod.apply_transition(state, args.module, "in_progress", args.agent, args.task or "work started")

    save_modules(root, state)
    save_agents(root, state)
    state_mod.update_contract_status(root, module, "in_progress")

    git_note = "not a git repository — create the branch yourself: git checkout -b %s" % branch
    if repoutil.git_available(root):
        code, out, err = repoutil.git(["rev-parse", "--verify", branch], root)
        if code == 0:
            repoutil.git(["checkout", branch], root, check=True)
            git_note = "checked out existing branch %s" % branch
        else:
            repoutil.git(["checkout", "-b", branch], root, check=True)
            git_note = "created and checked out %s" % branch
    print("module %s → in_progress · agent %s" % (args.module, args.agent))
    print("git: %s" % git_note)
    print(
        "\nnow:\n"
        "  1. python scripts/tp.py context --module %s --agent %s   # paste the contract + layers into your agent\n"
        "  2. implement, test, then run python scripts/verify.py\n"
        "  3. commit with trailers:\n"
        "       feat(%s): <subject>\n\n       Agent: %s\n       Agent-Role: %s\n       Module: %s\n"
        "  4. push, open the PR with .github/pull_request_template.md, then set:\n"
        "       python scripts/tp.py validate   # integrity\n"
        % (args.module, args.agent, args.module, args.agent, role, args.module)
    )
    return PASS


# --------------------------------------------------------------------------------------
# handoff
# --------------------------------------------------------------------------------------
def cmd_handoff(args):
    root = resolve_root(args)
    state = load(root)
    module = state_mod.module_by_id(state, args.module)
    if module is None:
        return fail("module %s is not registered" % args.module)
    previous = next((item for item in state["agents"] if item.get("agent_id") == args.frm), None)
    if previous is None:
        return fail("agent %s is not in state/agents.yaml" % args.frm)
    branch = "agent/%s/%s" % (args.to, args.module)
    contract = state_mod.load_contract(root, module)
    data = contract["data"] or {}
    remaining = [
        item for item in (data.get("acceptance_criteria") or []) if isinstance(item, dict)
    ]
    relative = "handoffs/%s-%s-to-%s-%s.md" % (repoutil.today(), args.frm, args.to, args.module)
    body = _handoff_document(state, module, previous, args, branch, remaining)
    repoutil.write_text(os.path.join(root, relative), body)

    previous.update({"status": "replaced", "replaced_by": args.to, "updated_at": repoutil.today()})
    new_agent = {
        "agent_id": args.to,
        "name": "%s %s" % (args.module, (args.role or previous.get("role") or "implementation").title()),
        "role": args.role or previous.get("role") or "implementation",
        "category": previous.get("category") or "implementation",
        "module_id": args.module,
        "project_id": state["project"].get("project_id"),
        "branch": branch,
        "status": "active",
        "current_task": "continue %s from handoff: %s" % (args.module, args.reason),
        "parent_agent": args.frm,
        "replaced_by": None,
        "created_at": repoutil.today(),
        "updated_at": repoutil.today(),
        "tools": previous.get("tools") or [],
        "authority": previous.get("authority") or [],
        "validation": [],
        "notes": "handoff: %s" % relative,
    }
    state["agents"].append(new_agent)
    module["assigned_agent"] = args.to
    module["branch"] = branch
    if module.get("status") in ("failed", "blocked"):
        state_mod.apply_transition(state, args.module, "ready", args.to, "agent replaced: %s" % args.reason)
        state_mod.apply_transition(state, args.module, "in_progress", args.to, "handoff from %s" % args.frm)
    save_modules(root, state)
    save_agents(root, state)
    print("handoff written: %s" % relative)
    print("agent %s → replaced by %s (module %s stays %s)" % (args.frm, args.to, args.module, module.get("status")))
    print("\nnext: give %s the prompt + `python scripts/tp.py context --module %s --agent %s`" % (args.to, args.module, args.to))
    return PASS


def _handoff_document(state, module, previous, args, branch, remaining):
    module_id = module.get("module_id")
    lines = [
        "# Handoff — %s from %s to %s" % (module_id, args.frm, args.to),
        "",
        "| Field | Value |",
        "|---|---|",
        "| Project | `%s` |" % state["project"].get("project_id"),
        "| Module | `%s` (`%s` status)" % (module_id, module.get("status")),
        "| From agent | `%s` (`%s`) → status now `replaced` |" % (args.frm, previous.get("role")),
        "| To agent | `%s` |" % args.to,
        "| Reason | %s |" % args.reason,
        "| Date | %s |" % repoutil.today(),
        "| Branch | `%s` → continue on `%s` |" % (module.get("branch") or "—", branch),
        "| PR | %s |" % ("#%s" % module.get("pr") if module.get("pr") else "none"),
        "| Validation | %s |" % module.get("validation"),
        "",
        "## 1. State of the work (complete this section before the new agent starts)",
        "",
        "- What exists and works (with commit SHAs):",
        "- What is incomplete or known broken:",
        "- What was never started:",
        "- Last validation command and result:",
        "",
        "## 2. Relevant files",
        "",
        "| Path | What it is | State |",
        "|---|---|---|",
        "| | | |",
        "",
        "## 3. Decisions made by the outgoing agent",
        "",
        "| Reference | Decision | Rationale | Reversible? |",
        "|---|---|---|---|",
        "| | | | |",
        "",
        "## 4. Assumptions and open questions",
        "",
        "| Item | Type | Status | Impact |",
        "|---|---|---|---|",
        "| | | | |",
        "",
        "## 5. Known issues and risks",
        "",
        "| Issue | Severity | Where | Suggested next step |",
        "|---|---|---|---|",
        "| | | | |",
        "",
        "## 6. Warnings for the receiving agent (do not skip)",
        "",
        "- Dead ends already explored:",
        "- Approaches that failed:",
        "- Environment quirks / flaky tests:",
        "",
        "## 7. Remaining acceptance criteria",
        "",
        "| Criterion | Status | Evidence needed |",
        "|---|---|---|",
    ]
    if remaining:
        for item in remaining:
            lines.append("| %s | not verified | %s |" % (item.get("criterion"), item.get("evidence") or "—"))
    else:
        lines.append("| (no structured criteria in the contract) | | |")
    lines += [
        "",
        "## 8. Next recommended action",
        "",
        "1. Read `modules/%s.md`, this handoff, and `git log` on the branch." % module_id,
        "2. **Re-run** the validation claimed above before trusting it.",
        "3. Continue or restart deliberately, and record which — plus why — in your report.",
        "",
        "## 9. Receiving agent acknowledgement",
        "",
        "- [ ] contract read",
        "- [ ] handoff read",
        "- [ ] branch state inspected",
        "- [ ] claimed validation re-run",
        "",
        "Generated by `python scripts/tp.py handoff`. Fill in sections 1–6 before handing over.",
    ]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------------------
# pr-check
# --------------------------------------------------------------------------------------
REQUIRED_PR_HEADINGS = (
    "Summary",
    "Acceptance criteria",
    "Tests executed",
    "Validation results",
    "Known limitations",
)
COMMIT_TYPES = (
    "feat",
    "fix",
    "refactor",
    "perf",
    "docs",
    "test",
    "build",
    "ci",
    "chore",
    "revert",
    "spec",
    "ux",
    "contract",
)


def _branch_name(ref):
    """`agent/x/Y`, `refs/heads/agent/x/Y`, `origin/agent/x/Y` and `refs/remotes/origin/...` all mean
    the same branch. CI hands over a remote-tracking ref, so the naming rules must ignore the prefix.
    """
    text = (ref or "").strip()
    if text.startswith("refs/heads/"):
        return text[len("refs/heads/") :]
    match = re.match(r"^refs/remotes/[^/]+/(.+)$", text)
    if match:
        return match.group(1)
    head, _, tail = text.partition("/")
    if tail and head in ("origin", "upstream", "refs/heads"):
        return tail
    return text


def cmd_pr_check(args):
    root = resolve_root(args)
    state = load(root)
    problems = []
    notes = []
    if not repoutil.git_available(root):
        return fail("pr-check needs a git repository (run it in CI or after `git init`)")
    revision = args.branch or repoutil.current_branch(root)
    branch = _branch_name(revision)
    base = args.base or (state["project"].get("default_branch") or "main")
    if branch == base:
        notes.append("running on the default branch — ownership checks are skipped")
    match = state_mod.AGENT_BRANCH_RE.match(branch or "")
    module = None
    if match:
        agent_id, module_id = match.group(1), match.group(2)
        entry = state_mod.module_by_id(state, module_id)
        if entry is None:
            problems.append("branch names module %s which is not registered in state/modules.yaml" % module_id)
        else:
            module = entry
            contract = state_mod.load_contract(root, entry)
            if not contract["exists"]:
                problems.append("contract for %s is missing" % module_id)
            else:
                _check_ownership(root, state, module_id, contract["data"] or {}, base, revision, problems, notes)
            assigned = entry.get("assigned_agent")
            if assigned and assigned != agent_id:
                notes.append("module %s is assigned to %s, not %s (stale state?)" % (module_id, assigned, agent_id))
        _check_commits(root, base, revision, module_id, agent_id, problems)
    elif branch and branch.startswith("human/"):
        notes.append("human branch — agent conventions are not enforced")
    else:
        problems.append(
            "branch `%s` does not match agent/<agent-id>/<MODULE-ID> or human/<name>/<topic> (see docs/workflows/git_workflow.md)"
            % (branch or "?")
        )
    body = args.body or os.environ.get("PR_BODY") or ""
    if args.body_file and os.path.isfile(args.body_file):
        body = repoutil.read_text(args.body_file)
    if body:
        for heading in REQUIRED_PR_HEADINGS:
            if heading.lower() not in body.lower():
                problems.append("pull request body is missing the `%s` section" % heading)
        if "agent" not in body.lower():
            problems.append("pull request body must identify the agent (see .github/pull_request_template.md)")
    else:
        notes.append("no PR body supplied (--body/--body-file/PR_BODY) — completeness checks skipped")

    for note in notes:
        print("· %s" % note)
    for problem in problems:
        print("x %s" % problem)
    if problems:
        print("\npr-check FAILED: %d problem(s)" % len(problems))
        return FAIL
    print("ok pr-check passed (branch %s vs %s)" % (branch, base))
    return PASS


# Paths every module's agent legitimately writes: state transitions and agent instances (written by the
# tooling), handoff records, and validation/review evidence. They are not module source, so requiring a
# module to grant them would be noise — but `forbidden_to_modify` still wins over this allowance.
FRAMEWORK_MANAGED_PREFIXES = ("state/", "handoffs/", "reports/")


def _check_ownership(root, state, module_id, data, base, branch, problems, notes):
    allowed = list(data.get("allowed_to_modify") or [])
    forbidden = list(data.get("forbidden_to_modify") or [])
    try:
        changed = repoutil.changed_paths(root, base, branch)
    except RuntimeError as exc:
        problems.append(str(exc))
        return
    if not changed:
        notes.append("no changed paths detected between %s and %s" % (base, branch))
    # A shared zone is a file many modules need but only one may write. The owner is allowed to write
    # it (that is the point of naming an owner); everyone else must request the change instead.
    zones_owned = [
        zone.get("path")
        for zone in (state.get("shared_zones") or [])
        if zone.get("path") and zone.get("owner") == module_id
    ]
    zones_touched = [
        zone
        for zone in (data.get("shared_zones_touched") or [])
        if any(state_mod._paths_overlap(zone, owned) for owned in zones_owned)
    ]
    framework_paths = sorted({path for path in changed if path.startswith(FRAMEWORK_MANAGED_PREFIXES)})
    if framework_paths:
        notes.append(
            "framework-managed paths in this diff (allowed for every module): %s" % ", ".join(framework_paths[:6])
        )
    if zones_touched:
        notes.append("shared zone(s) this module owns: %s" % ", ".join(zones_touched[:4]))
    for path in changed:
        if any(state_mod._paths_overlap(path, pattern) for pattern in forbidden):
            problems.append("%s is in forbidden_to_modify for %s — ownership breach" % (path, module_id))
            continue
        if path.startswith(FRAMEWORK_MANAGED_PREFIXES):
            continue
        if any(state_mod._paths_overlap(path, zone) for zone in zones_touched):
            continue
        if allowed and not any(state_mod._paths_overlap(path, pattern) for pattern in allowed):
            problems.append(
                "%s is outside allowed_to_modify for %s (allowed: %s)" % (path, module_id, ", ".join(allowed) or "none")
            )
    for other in state["modules"]:
        if other.get("module_id") == module_id:
            continue
        if other.get("status") not in ("in_progress", "assigned", "awaiting_review", "changes_requested"):
            continue
        contract = state_mod.load_contract(root, other)
        if state_mod.overlaps(changed, contract["data"].get("owns")):
            notes.append(
                "changed paths overlap %s's ownership — coordinate with %s before merging"
                % (other.get("module_id"), other.get("assigned_agent") or "its owner")
            )


def _check_commits(root, base, branch, module_id, agent_id, problems):
    try:
        commits = repoutil.commits_between(root, base, branch)
    except RuntimeError as exc:
        problems.append(str(exc))
        return
    if not commits:
        problems.append("no commits found between %s and %s" % (base, branch))
        return
    for sha, subject, body in commits:
        if not subject.startswith("Merge ") and not subject.startswith("Revert "):
            if not any(subject.startswith("%s(" % kind) or subject.startswith("%s:" % kind) for kind in COMMIT_TYPES):
                problems.append(
                    "%s: commit subject must start with a conventional type (%s): %r"
                    % (sha[:8], ", ".join(COMMIT_TYPES), subject)
                )
            scope = ""
            if "(" in subject.split(":")[0]:
                scope = subject.split("(")[1].split(")")[0]
            if scope and scope not in (module_id, "repo"):
                problems.append(
                    "%s: commit scope `%s` must be `%s` or `repo` on branch %s" % (sha[:8], scope, module_id, branch)
                )
            if not scope:
                problems.append("%s: commit subject should carry the module scope, e.g. feat(%s): …" % (sha[:8], module_id))
        text = subject + "\n" + body
        if "Agent:" not in text:
            problems.append("%s: missing `Agent:` trailer (see .gitmessage)" % sha[:8])
        if "Module:" not in text:
            problems.append("%s: missing `Module:` trailer" % sha[:8])
        elif module_id not in text:
            problems.append("%s: `Module:` trailer does not mention %s" % (sha[:8], module_id))
        if "Validated-With:" not in text:
            problems.append("%s: missing `Validated-With:` trailer — state the command you ran" % sha[:8])


# --------------------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------------------
def build_parser():
    parser = argparse.ArgumentParser(prog="tp.py", description="TemplateProject toolkit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add(name, help_text):
        sub = subparsers.add_parser(name, help=help_text)
        sub.add_argument("--root", default=None, help="repository root (defaults to auto-discovery)")
        return sub

    p = add("bootstrap", "fill in a copied template (or create a new project from it)")
    p.add_argument(
        "destination",
        nargs="?",
        help="new project directory: the template is copied there, then filled in (default: in place)",
    )
    p.add_argument("--name")
    p.add_argument("--id")
    p.add_argument("--description")
    p.add_argument("--owner")
    p.add_argument("--profile", choices=state_mod.PROFILES)
    p.add_argument("--branch", help="default branch name (default main)")
    p.add_argument("--repo-url")
    p.add_argument("--init-git", action="store_true", help="git init + first commit")
    p.add_argument("--adopt-env", action="store_true", help="create a gitignored .env from .env.example")
    p.set_defaults(func=cmd_bootstrap)

    p = add("new-module", "scaffold a module contract")
    p.add_argument("--id", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--slug", help="source directory slug (default from id)")
    p.add_argument("--priority", default="must", choices=("must", "should", "could"))
    p.add_argument("--dep", action="append", help="module this one depends on (repeatable)")
    p.add_argument("--edge-type", default="contract", choices=state_mod.DEPENDENCY_TYPES)
    p.add_argument("--actor", default="decomposition")
    p.set_defaults(func=cmd_new_module)

    p = add("validate", "state + contract + link + prompt integrity")
    p.add_argument("--strict", action="store_true", help="treat warnings as errors")
    p.add_argument("--verbose", action="store_true")
    p.set_defaults(func=cmd_validate)

    p = add("sync-notebook", "regenerate notebook prompt cells from the prompt files")
    p.set_defaults(func=cmd_sync_notebook)

    p = add("status", "the project board")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_status)

    p = add("ready", "ready modules, waves and parallelism warnings")
    p.set_defaults(func=cmd_ready)

    p = add("context", "build a layered context pack")
    p.add_argument("--module", required=True)
    p.add_argument("--agent")
    p.add_argument("--format", default="md", choices=("md", "json"))
    p.add_argument("--out", help="write to this path instead of stdout")
    p.set_defaults(func=cmd_context)

    p = add("start", "create the agent branch and start the module")
    p.add_argument("--module", required=True)
    p.add_argument("--agent", required=True)
    p.add_argument("--role", default="implementation")
    p.add_argument("--task")
    p.add_argument("--actor", default="orchestrator")
    p.add_argument("--force", action="store_true", help="start despite unmet dependencies")
    p.add_argument("--force-reason", help="reason recorded in the module history")
    p.set_defaults(func=cmd_start)

    p = add("handoff", "replace an agent losslessly")
    p.add_argument("--module", required=True)
    p.add_argument("--from", dest="frm", required=True)
    p.add_argument("--to", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--role")
    p.set_defaults(func=cmd_handoff)

    p = add("pr-check", "CI gate: conventions, ownership, PR completeness")
    p.add_argument("--base")
    p.add_argument("--branch")
    p.add_argument("--body")
    p.add_argument("--body-file")
    p.set_defaults(func=cmd_pr_check)

    return parser


def _configure_output():
    """Keep output readable on every terminal (Windows consoles are often cp1252)."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main(argv=None):
    _configure_output()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except YamlError as exc:
        return fail("YAML error: %s" % exc)
    except FileNotFoundError as exc:
        return fail(str(exc))
    except RuntimeError as exc:
        return fail(str(exc))


if __name__ == "__main__":
    sys.exit(main())
