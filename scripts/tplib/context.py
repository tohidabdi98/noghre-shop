"""context — assemble layered context packs so agents receive enough and no more.

Layers (see docs/workflows/context_engineering.md):
    1 project identity   2 relevant requirements   3 relevant architecture   4 module contract
    5 neighbour interface contracts   6 conventions   7 current task & state   8 validation
    + UX slice (only when the contract lists ux_refs)   + discovery index
"""

from __future__ import annotations

import os

from . import repoutil

DISCOVERY_INDEX = """\
## Discovery index — when you need more context

| Need | Read |
|---|---|
| exact behaviour required | `docs/project/requirements.md` (the IDs cited above) |
| visual/flow detail | `docs/ux/*` (the `UX-###` cited above) |
| why it is built this way | `docs/project/decisions.md` (tail) and the cited `ADR-###` |
| what a neighbour promised | `modules/<OTHER-ID>.md` → `interfaces:` |
| what you may write | this contract's `allowed_to_modify` / `forbidden_to_modify` |
| commit/PR rules | `docs/workflows/git_workflow.md` |
| when work is done | the acceptance criteria above + `docs/project/definition_of_done.md` |
| known problems | `docs/project/open_questions.md`, `docs/project/risks.md`, `reports/` |
| previous attempts | `handoffs/`, `git log -- <path>` |

Do **not** read other modules' source code unless this contract lists their interface as a
dependency. If something you need is missing from this pack, ask instead of guessing.
"""


def _read(root: str, relative: str, required: bool = False):
    """Read a file from the project root, falling back to the framework root when nested."""
    for base in repoutil.search_roots(root):
        path = os.path.join(base, relative)
        if os.path.isfile(path):
            return repoutil.read_text(path)
    if required:
        return "_missing file: %s_" % relative
    return None


def _project_identity(state):
    project = state["project"]
    lines = [
        "project_id: %s" % project.get("project_id"),
        "name: %s" % project.get("name"),
        "profile: %s" % project.get("profile"),
        "stage: %s" % project.get("stage"),
        "milestone: %s" % project.get("milestone"),
        "default_branch: %s" % project.get("default_branch"),
        "spec_status: %s" % project.get("spec_status"),
    ]
    gates = project.get("gates") or {}
    lines.append(
        "gates: " + ", ".join("%s=%s" % (key, value) for key, value in sorted(gates.items()))
    )
    return "\n".join(lines)


def _ux_slice(root: str, ux_refs):
    """Extract only the UX sections that mention the cited UX ids."""
    if not ux_refs:
        return None
    ux_dir = os.path.join(root, "docs", "ux")
    if not os.path.isdir(ux_dir):
        return None
    chunks = []
    for relative in sorted(repoutil.iter_files(ux_dir, suffixes=(".md",))):
        full = os.path.join(ux_dir, relative)
        text = repoutil.read_text(full)
        found = repoutil.extract_sections(text, ux_refs, levels=(2, 3, 4))
        for token in ux_refs:
            if token in found:
                chunks.append("### %s (from %s)\n\n%s" % (token, relative, found[token]))
    if not chunks:
        return None
    chunks.append(
        "_Related UX detail you may need: `docs/ux/screens.md`, `docs/ux/interaction_patterns.md`, "
        "`docs/ux/design_system.md` — read only the sections your screens reference._"
    )
    return "\n\n".join(chunks)


def _neighbour_digest(root: str, state, module_id: str):
    """Interface-level summary of the modules this one depends on or blocks."""
    from . import state as state_mod

    neighbours = []
    for neighbour_id in sorted(set(state_mod.upstream_of(state, module_id)) | set(state_mod.downstream_of(state, module_id))):
        entry = state_mod.module_by_id(state, neighbour_id)
        if entry is None:
            continue
        contract = state_mod.load_contract(root, entry)
        data = contract["data"] or {}
        relation = "depends on" if neighbour_id in state_mod.upstream_of(state, module_id) else "is consumed by"
        block = [
            "### %s — %s (%s this module)" % (neighbour_id, data.get("name") or entry.get("name"), relation),
            "",
            "- status: %s · validation: %s" % (entry.get("status"), entry.get("validation")),
            "- contract: `%s`" % repoutil.relative(root, contract["path"]),
            "- purpose: %s" % (data.get("purpose") or "—"),
        ]
        interfaces = data.get("interfaces") or {}
        provides = interfaces.get("provides") or []
        requires = interfaces.get("requires") or []
        if provides:
            block.append("- provides: " + "; ".join(_interface_line(item) for item in provides))
        if requires:
            block.append("- requires: " + "; ".join(_interface_line(item) for item in requires))
        edges = [
            edge
            for edge in state["edges"]
            if {edge.get("from"), edge.get("to")} == {module_id, neighbour_id}
        ]
        for edge in edges:
            block.append(
                "- edge: %s → %s · type %s · status %s · interface %s"
                % (edge.get("from"), edge.get("to"), edge.get("type"), edge.get("status"), edge.get("interface") or "—")
            )
        neighbours.append("\n".join(block))
    return "\n\n".join(neighbours) if neighbours else None


def _interface_line(item):
    if isinstance(item, dict):
        name = item.get("name") or "?"
        kind = item.get("kind") or "?"
        contract = item.get("contract") or ""
        frozen = item.get("frozen")
        extra = "" if frozen is None else (" · frozen" if frozen else " · NOT FROZEN")
        return "%s (%s)%s%s" % (name, kind, extra, (" → %s" % contract) if contract else "")
    return str(item)


def _open_items(state, module_id: str, headings=("Open question register", "Risk register", "Assumption register")):
    """Pull register rows that mention the module id (keeps layer 7 narrow)."""
    return headings


def build_pack(root: str, state, module_id: str, agent_id=None):
    """Return {'markdown': str, 'layers': {name: str}} for one module + agent."""
    from . import state as state_mod

    entry = state_mod.module_by_id(state, module_id)
    if entry is None:
        raise KeyError("module %s is not registered in state/modules.yaml" % module_id)
    contract = state_mod.load_contract(root, entry)
    data = contract["data"] or {}
    layers = {}

    # 1 — project identity + hard rules
    hard_rules = ""
    agents_md = _read(root, "AGENTS.md")
    if agents_md:
        section = repoutil.extract_sections(agents_md, ["Hard rules"], levels=(2,))
        hard_rules = section.get("Hard rules", "")
    layers["1_project_identity"] = "\n".join(
        [
            "```yaml",
            _project_identity(state),
            "```",
            "",
            hard_rules or "_Read `AGENTS.md` in full before acting._",
        ]
    )

    # 2 — relevant requirements only
    requirement_refs = list(data.get("requirement_refs") or [])
    requirements_md = _read(root, state["docs"].get("requirements", "docs/project/requirements.md"))
    requirement_text = None
    if requirements_md and requirement_refs:
        found = repoutil.extract_sections(requirements_md, requirement_refs, levels=(2, 3))
        chunks = []
        for token in requirement_refs:
            if token in found:
                chunks.append(found[token])
            else:
                chunks.append(
                    "_%s: no section found in requirements.md whose heading contains this ID — "
                    "if it should exist, that is a documentation bug (fix the heading)._"
                    % token
                )
        requirement_text = "\n\n".join(chunks)
    layers["2_requirements"] = requirement_text or (
        "_This contract cites no requirement IDs._ If it should, fix `requirement_refs` in the contract."
    )

    # 3 — relevant architecture + ADRs
    arch_refs = list(data.get("architecture_refs") or [])
    architecture_md = _read(root, state["docs"].get("architecture", "docs/project/architecture.md")) or ""
    decisions_md = _read(root, state["docs"].get("decisions", "docs/project/decisions.md")) or ""
    arch_chunks = []
    tokens = []
    for ref in arch_refs:
        if "#" in ref:
            _, anchor = ref.split("#", 1)
            tokens.append(anchor.replace("-", " ").strip())
    if tokens:
        found = repoutil.extract_sections(architecture_md, tokens, levels=(2, 3))
        for token in tokens:
            if token in found:
                arch_chunks.append(found[token])
    plain_refs = [ref for ref in arch_refs if "#" not in ref]
    for ref in plain_refs:
        relative_path = ref.split()[0] if ref.split() else ref
        text = _read(root, relative_path)
        if text:
            arch_chunks.append("### %s\n\n%s" % (relative_path, text))
    adr_ids = sorted({ref for ref in arch_refs if ref.startswith("ADR-")})
    if adr_ids and decisions_md:
        found = repoutil.extract_sections(decisions_md, adr_ids, levels=(2, 3))
        for token in adr_ids:
            if token in found:
                arch_chunks.append(found[token])
    layers["3_architecture"] = "\n\n".join(arch_chunks) or (
        "_No architecture sections cited._ Read `docs/project/architecture.md` §6 (interfaces) if you "
        "consume or provide one."
    )

    # 4 — the module contract
    layers["4_module_contract"] = contract["text"] or "_MISSING CONTRACT: %s_" % repoutil.relative(
        root, contract["path"]
    )

    # 5 — neighbour interface contracts
    layers["5_neighbour_interfaces"] = _neighbour_digest(root, state, module_id) or (
        "_This module has no registered dependencies or consumers._"
    )

    # 6 — conventions
    conventions = _read(root, state["docs"].get("conventions", "docs/project/conventions.md")) or ""
    dod = _read(root, state["docs"].get("definition_of_done", "docs/project/definition_of_done.md")) or ""
    git_rules = _read(root, "docs/workflows/git_workflow.md") or ""
    git_sections = repoutil.extract_sections(git_rules, ["Branches", "Commits", "Pull requests"], levels=(2,))
    layers["6_conventions"] = "\n\n".join(
        part
        for part in [
            conventions,
            "\n\n".join(git_sections.get(key, "") for key in ("Branches", "Commits", "Pull requests")),
            dod,
        ]
        if part.strip()
    )

    # 7 — current task and state
    agent_entry = None
    for candidate in state["agents"]:
        if agent_id and candidate.get("agent_id") == agent_id:
            agent_entry = candidate
            break
    board_lines = [
        "- module: %s (%s)" % (module_id, data.get("name") or entry.get("name")),
        "- status: %s · validation: %s" % (entry.get("status"), entry.get("validation")),
        "- branch: %s" % (entry.get("branch") or "—"),
        "- pull request: %s" % (entry.get("pr") or "—"),
        "- blocked reason: %s" % (entry.get("blocked_reason") or "—"),
    ]
    if agent_entry:
        board_lines.append(
            "- you: %s (%s) · status %s · task: %s"
            % (agent_entry.get("agent_id"), agent_entry.get("role"), agent_entry.get("status"), agent_entry.get("current_task"))
        )
    elif agent_id:
        board_lines.append("- you: %s (not registered in state/agents.yaml yet)" % agent_id)
    registers = []
    for relative, heading in (
        ("docs/project/open_questions.md", "Open question register"),
        ("docs/project/risks.md", "Risk register"),
    ):
        text = _read(root, relative)
        if not text:
            continue
        rows = [line for line in text.splitlines() if module_id in line and line.strip().startswith("|")]
        if rows:
            registers.append("**%s** (rows mentioning %s)\n\n%s" % (heading, module_id, "\n".join(rows)))
    layers["7_task_and_state"] = "\n".join(board_lines) + ("\n\n" + "\n\n".join(registers) if registers else "")

    # 8 — validation requirements
    criteria = data.get("acceptance_criteria") or []
    validation = data.get("validation") or []
    verify_config = _read(root, "scripts/verify.config.yaml") or ""
    criteria_lines = []
    for item in criteria:
        if isinstance(item, dict):
            criteria_lines.append(
                "- %s: %s _(evidence: %s)_" % (item.get("id"), item.get("criterion"), item.get("evidence"))
            )
        else:
            criteria_lines.append("- %s" % item)
    validation_lines = []
    for item in validation:
        if isinstance(item, dict):
            validation_lines.append("- `%s` → expects %s" % (item.get("command"), item.get("expects")))
        else:
            validation_lines.append("- `%s`" % item)
    layers["8_validation"] = "\n\n".join(
        [
            "**Acceptance criteria**\n" + ("\n".join(criteria_lines) or "_none defined — the contract is incomplete_"),
            "**Commands that must pass**\n" + ("\n".join(validation_lines) or "_none defined_"),
            "**Project verification configuration**\n```yaml\n%s\n```" % verify_config.strip(),
        ]
    )

    ux = _ux_slice(root, data.get("ux_refs") or [])
    if ux:
        layers["9_ux_slice"] = ux

    order = [
        ("1_project_identity", "Layer 1 — Project identity"),
        ("2_requirements", "Layer 2 — Relevant requirements"),
        ("3_architecture", "Layer 3 — Relevant architecture"),
        ("4_module_contract", "Layer 4 — Your module contract"),
        ("5_neighbour_interfaces", "Layer 5 — Neighbour interfaces"),
        ("6_conventions", "Layer 6 — Conventions"),
        ("7_task_and_state", "Layer 7 — Current task and state"),
        ("8_validation", "Layer 8 — Validation requirements"),
        ("9_ux_slice", "Layer 9 — UX slice (cited only)"),
    ]
    header = [
        "# Context pack — %s" % module_id,
        "",
        "Generated by `python scripts/tp.py context`. Do not edit; regenerate after any change.",
        "Agent: %s" % (agent_id or "(unassigned)"),
        "Module contract: `%s`" % repoutil.relative(root, contract["path"]),
        "",
        "---",
        "",
    ]
    body = []
    for key, title in order:
        if key not in layers:
            continue
        if key == "4_module_contract":
            body.append("## %s\n\n_(the full contract is the definition of your task)_\n\n%s" % (title, layers[key]))
        else:
            body.append("## %s\n\n%s" % (title, layers[key]))
    body.append(DISCOVERY_INDEX)
    markdown = "\n".join(header) + "\n\n".join(body)
    return {"markdown": markdown, "layers": layers, "module_id": module_id, "agent_id": agent_id}
