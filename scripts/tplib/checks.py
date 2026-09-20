"""checks — integrity checks for the whole template.

`validate` answers: is the written truth internally consistent and are all references real? It
covers state schema, contract completeness, dependency consistency, doc links, placeholder tokens,
the agent registry ↔ prompt correspondence, and notebook prompt sync.
"""

from __future__ import annotations

import fnmatch
import json
import os
import re

from . import repoutil
from . import state as state_mod

CONFIG_RELATIVE = "scripts/validate.config.yaml"

DEFAULT_CONFIG = {
    "allow_missing_paths": [],
    "placeholder_check_exclude": ["HOW_TO_USE.ipynb", "scripts/README.md"],
    "link_check_prefixes": [
        "docs/",
        "agents/",
        "modules/",
        "state/",
        "scripts/",
        "handoffs/",
        "reports/",
        "examples/",
        ".github/",
    ],
    "link_check_extra_files": ["README.md", "AGENTS.md", "HOW_TO_USE.ipynb"],
}

PROMPT_MARKER = "<!-- PROMPT-SYNC:"
PROMPT_RE = re.compile(r"<!--\s*PROMPT-SYNC:\s*([^\s]+)\s*-->")


def load_config(root: str):
    """Project config, merged over the framework defaults (nearest config wins)."""
    config = dict(DEFAULT_CONFIG)
    layers = []
    for candidate_root in reversed(repoutil.search_roots(root)):
        path = os.path.join(candidate_root, CONFIG_RELATIVE)
        if os.path.isfile(path):
            layers.append(repoutil.load_yaml_file(path) or {})
    for data in layers:
        for key, value in data.items():
            if key in config or key == "notes":
                config[key] = value
    return config


def issue(level: str, code: str, message: str, path: str = ""):
    return {"level": level, "code": code, "message": message, "path": path}


def errors(issues):
    return [item for item in issues if item["level"] == "error"]


def warnings(issues):
    return [item for item in issues if item["level"] == "warning"]


# --------------------------------------------------------------------------------------
# State checks
# --------------------------------------------------------------------------------------
def check_project(root, state, issues):
    project = state["project"]
    required = (
        "project_id",
        "name",
        "profile",
        "stage",
        "spec_status",
        "default_branch",
        "gates",
        "docs",
    )
    for key in required:
        if project.get(key) in (None, "", [], {}):
            issues.append(issue("error", "project.missing_key", "state/project.yaml: missing `%s`" % key, "state/project.yaml"))
    if project.get("profile") not in state_mod.PROFILES:
        issues.append(issue("error", "project.profile", "profile must be one of %s" % (", ".join(state_mod.PROFILES)), "state/project.yaml"))
    if project.get("stage") not in state_mod.STAGES:
        issues.append(issue("error", "project.stage", "stage must be one of %s" % (", ".join(state_mod.STAGES)), "state/project.yaml"))
    if project.get("spec_status") not in state_mod.SPEC_STATUSES:
        issues.append(issue("error", "project.spec_status", "spec_status must be one of %s" % (", ".join(state_mod.SPEC_STATUSES)), "state/project.yaml"))
    gates = project.get("gates") or {}
    for gate in ("requirements_approved", "ux_approved", "architecture_approved", "decomposition_approved", "release_approved"):
        if gate not in gates:
            issues.append(issue("error", "project.gate_missing", "missing gate `%s`" % gate, "state/project.yaml"))
    for key, relative in (project.get("docs") or {}).items():
        if not os.path.isfile(os.path.join(root, relative)):
            issues.append(issue("error", "project.doc_missing", "docs.%s → %s does not exist" % (key, relative), "state/project.yaml"))
    # gate coherence: a stage implies the earlier gates are closed
    order = ["requirements_approved", "ux_approved", "architecture_approved", "decomposition_approved"]
    stage_index = state_mod.STAGES.index(project.get("stage", "discovery")) if project.get("stage") in state_mod.STAGES else 0
    if project.get("profile") != "backend" and stage_index >= 4:
        for gate in order[: stage_index]:
            if not gates.get(gate) and not (gate == "ux_approved" and project.get("profile") == "backend"):
                issues.append(
                    issue(
                        "warning",
                        "project.gate_behind_stage",
                        "stage is `%s` but gate `%s` is not approved" % (project.get("stage"), gate),
                        "state/project.yaml",
                    )
                )


def check_modules(root, state, issues, strict=False):
    seen = set()
    contracts = {}
    for module in state["modules"]:
        module_id = module.get("module_id")
        if not module_id:
            issues.append(issue("error", "module.id_missing", "a module entry has no module_id", "state/modules.yaml"))
            continue
        if not state_mod.MODULE_ID_RE.match(module_id):
            issues.append(issue("error", "module.id_format", "module_id `%s` must look like AUTH-001" % module_id, "state/modules.yaml"))
        if module_id in seen:
            issues.append(issue("error", "module.duplicate", "duplicate module_id %s" % module_id, "state/modules.yaml"))
        seen.add(module_id)
        if module.get("status") not in state_mod.MODULE_STATUSES:
            issues.append(issue("error", "module.status", "%s has invalid status `%s`" % (module_id, module.get("status")), "state/modules.yaml"))
        if module.get("validation") not in state_mod.VALIDATION_RESULTS:
            issues.append(issue("error", "module.validation", "%s has invalid validation `%s`" % (module_id, module.get("validation")), "state/modules.yaml"))
        contract = state_mod.load_contract(root, module)
        contracts[module_id] = contract
        relative_contract = repoutil.relative(root, contract["path"])
        if not contract["exists"]:
            issues.append(issue("error", "module.contract_missing", "%s: contract %s not found" % (module_id, relative_contract), "state/modules.yaml"))
            continue
        check_contract(root, state, module, contract, issues, strict=strict)
        data = contract["data"] or {}
        if data.get("status") != module.get("status"):
            issues.append(
                issue(
                    "error",
                    "module.status_drift",
                    "%s: contract status `%s` != registry status `%s` (they must match; use tp.py start/handoff)"
                    % (module_id, data.get("status"), module.get("status")),
                    relative_contract,
                )
            )
        # dependency consistency: contract depends_on <-> edges
        declared = set(data.get("depends_on") or [])
        from_edges = set(edge.get("to") for edge in state["edges"] if edge.get("from") == module_id)
        for missing in sorted(declared - from_edges):
            issues.append(
                issue("error", "module.dep_missing_edge", "%s declares depends_on %s but has no edge in state/dependencies.yaml" % (module_id, missing), relative_contract)
            )
        for missing in sorted(from_edges - declared):
            issues.append(
                issue("error", "module.dep_missing_contract", "%s has an edge to %s but does not declare it in `depends_on`" % (module_id, missing), relative_contract)
            )
        if module.get("status") in ("assigned", "in_progress", "awaiting_review"):
            if not module.get("assigned_agent"):
                issues.append(issue("warning", "module.no_agent", "%s is `%s` without an assigned_agent" % (module_id, module.get("status")), "state/modules.yaml"))
            if not module.get("branch"):
                issues.append(issue("warning", "module.no_branch", "%s is `%s` without a branch" % (module_id, module.get("status")), "state/modules.yaml"))
        if module.get("status") == "validated" and module.get("validation") != "passed":
            issues.append(issue("error", "module.validated_without_evidence", "%s is `validated` but validation is `%s`" % (module_id, module.get("validation")), "state/modules.yaml"))
        if module.get("status") == "blocked" and not module.get("blocked_reason"):
            issues.append(issue("error", "module.blocked_no_reason", "%s is `blocked` without a blocked_reason" % module_id, "state/modules.yaml"))
    # ownership overlap between all modules (not just parallel ones)
    ids = sorted(contracts)
    for index, left in enumerate(ids):
        for right in ids[index + 1 :]:
            shared = state_mod.overlaps(contracts[left]["data"].get("owns"), contracts[right]["data"].get("owns"))
            if shared:
                issues.append(
                    issue(
                        "error",
                        "module.ownership_overlap",
                        "%s and %s claim the same paths: %s" % (left, right, ", ".join("%s ~ %s" % pair for pair in shared)),
                        "modules/",
                    )
                )
    if not state["modules"]:
        issues.append(issue("info", "module.none", "no modules registered yet (expected before the decomposition stage)", "state/modules.yaml"))


def check_contract(root, state, module, contract, issues, strict=False):
    module_id = module.get("module_id")
    relative = repoutil.relative(root, contract["path"])
    data = contract["data"]
    if not data:
        issues.append(issue("error", "contract.no_yaml_block", "%s: no machine-readable ```yaml contract block found" % relative, relative))
        return
    for key in state_mod.REQUIRED_CONTRACT_KEYS:
        if key not in data:
            issues.append(issue("error", "contract.missing_key", "%s: contract key `%s` is missing" % (relative, key), relative))
    if data.get("module_id") != module_id:
        issues.append(issue("error", "contract.id_mismatch", "%s: module_id `%s` != registry `%s`" % (relative, data.get("module_id"), module_id), relative))
    if not list(data.get("acceptance_criteria") or []):
        issues.append(issue("error", "contract.no_criteria", "%s: acceptance_criteria is empty — the module cannot be verified" % relative, relative))
    if not list(data.get("validation") or []):
        issues.append(issue("error", "contract.no_validation", "%s: validation is empty — no commands prove completion" % relative, relative))
    if strict and not list(data.get("definition_of_done") or []):
        issues.append(issue("error", "contract.no_dod", "%s: definition_of_done is empty" % relative, relative))
    owns = list(data.get("owns") or [])
    allowed = list(data.get("allowed_to_modify") or [])
    forbidden = list(data.get("forbidden_to_modify") or [])
    for path in owns:
        if not any(state_mod._paths_overlap(path, candidate) for candidate in allowed):
            issues.append(
                issue("error", "contract.owns_not_allowed", "%s: owns path `%s` is not covered by allowed_to_modify" % (relative, path), relative)
            )
    for path in allowed:
        if any(state_mod._paths_overlap(path, candidate) for candidate in forbidden):
            issues.append(
                issue("warning", "contract.allow_and_forbid", "%s: `%s` is in both allowed_to_modify and forbidden_to_modify (forbidden wins)" % (relative, path), relative)
            )
    if not owns and not allowed:
        issues.append(issue("error", "contract.no_paths", "%s: neither owns nor allowed_to_modify is set" % relative, relative))
    # traceability: cited IDs must exist as headings in the referenced documents
    requirements = repoutil.read_text(os.path.join(root, "docs/project/requirements.md")) if os.path.isfile(os.path.join(root, "docs/project/requirements.md")) else ""
    for ref in data.get("requirement_refs") or []:
        if not state_mod.REQ_ID_RE.match(str(ref)):
            issues.append(issue("warning", "contract.req_id_format", "%s: requirement_ref `%s` is not FR-### / NFR-### shaped" % (relative, ref), relative))
        if requirements and ref not in requirements:
            issues.append(issue("error", "contract.req_unknown", "%s: requirement `%s` does not appear in docs/project/requirements.md" % (relative, ref), relative))
    ux_refs = list(data.get("ux_refs") or [])
    if ux_refs:
        ux_directory = os.path.join(root, "docs", "ux")
        ux_text = "".join(
            repoutil.read_text(os.path.join(ux_directory, relative_ux))
            for relative_ux in repoutil.iter_files(ux_directory, suffixes=(".md",))
        )
        for ref in ux_refs:
            if not state_mod.UX_ID_RE.match(str(ref)):
                issues.append(issue("warning", "contract.ux_id_format", "%s: ux_ref `%s` is not UX-### shaped" % (relative, ref), relative))
            if ref not in ux_text:
                issues.append(issue("error", "contract.ux_unknown", "%s: UX requirement `%s` is not in docs/ux/" % (relative, ref), relative))
    declared_zones = {str(zone.get("path")) for zone in (state.get("shared_zones") or []) if zone.get("path")}
    for zone in data.get("shared_zones_touched") or []:
        if str(zone) not in declared_zones:
            issues.append(
                issue(
                    "warning",
                    "contract.zone_undeclared",
                    "%s: shared zone `%s` is not declared in state/project.yaml → shared_zones" % (relative, zone),
                    relative,
                )
            )
    headings = [heading.lower() for heading in contract["headings"]]
    for required in state_mod.REQUIRED_CONTRACT_HEADINGS:
        if not any(required in heading for heading in headings):
            issues.append(issue("error", "contract.missing_section", "%s: required section `%s` is missing" % (relative, required), relative))
    provides = ((data.get("interfaces") or {}).get("provides")) or []
    for item in provides:
        if isinstance(item, dict) and item.get("name") and not item.get("test"):
            issues.append(issue("warning", "contract.interface_untested", "%s: interface `%s` has no conformance test declared" % (relative, item.get("name")), relative))


def check_agents(root, state, issues):
    roles = registry_roles(root, issues)
    seen = set()
    for agent in state["agents"]:
        agent_id = agent.get("agent_id")
        if not agent_id:
            issues.append(issue("error", "agent.id_missing", "an agent entry has no agent_id", "state/agents.yaml"))
            continue
        if agent_id in seen:
            issues.append(issue("error", "agent.duplicate", "duplicate agent_id %s" % agent_id, "state/agents.yaml"))
        seen.add(agent_id)
        role = agent.get("role")
        if roles and role not in roles:
            issues.append(issue("error", "agent.unknown_role", "%s has role `%s` which is not in docs/agents/agent_registry.yaml" % (agent_id, role), "state/agents.yaml"))
        if agent.get("status") not in state_mod.AGENT_STATUSES:
            issues.append(issue("error", "agent.status", "%s has invalid status `%s`" % (agent_id, agent.get("status")), "state/agents.yaml"))
        module_id = agent.get("module_id")
        if module_id and state_mod.module_by_id(state, module_id) is None:
            issues.append(issue("error", "agent.unknown_module", "%s references module %s which is not registered" % (agent_id, module_id), "state/agents.yaml"))
        branch = agent.get("branch") or ""
        if branch:
            match = state_mod.AGENT_BRANCH_RE.match(branch)
            if not match:
                issues.append(issue("error", "agent.branch_format", "%s branch `%s` must match agent/<agent-id>/<MODULE-ID>" % (agent_id, branch), "state/agents.yaml"))
            elif match.group(1) != agent_id:
                issues.append(issue("error", "agent.branch_agent_mismatch", "%s branch names agent `%s`" % (agent_id, match.group(1)), "state/agents.yaml"))
            elif module_id and match.group(2) != module_id:
                issues.append(issue("error", "agent.branch_module_mismatch", "%s branch names module `%s` but agent.module_id is `%s`" % (agent_id, match.group(2), module_id), "state/agents.yaml"))
        if agent.get("status") in ("active", "blocked", "replacing") and not agent.get("current_task"):
            issues.append(issue("warning", "agent.no_task", "%s is `%s` without a current_task" % (agent_id, agent.get("status")), "state/agents.yaml"))
    # modules assigned to an agent must agree with the agent's module
    for module in state["modules"]:
        assigned = module.get("assigned_agent")
        if not assigned:
            continue
        agent = next((item for item in state["agents"] if item.get("agent_id") == assigned), None)
        if agent is None:
            issues.append(issue("warning", "module.agent_unknown", "%s is assigned to `%s` which is not in state/agents.yaml" % (module.get("module_id"), assigned), "state/modules.yaml"))
        elif agent.get("module_id") not in (None, module.get("module_id")):
            issues.append(issue("error", "module.agent_module_mismatch", "%s assigned to `%s` whose module_id is `%s`" % (module.get("module_id"), assigned, agent.get("module_id")), "state/modules.yaml"))


def check_edges(root, state, issues):
    module_ids = set(state_mod.module_ids(state))
    seen = set()
    graph = {}
    for edge in state["edges"]:
        left, right = edge.get("from"), edge.get("to")
        if (left, right) in seen:
            issues.append(issue("error", "edge.duplicate", "duplicate dependency edge %s → %s" % (left, right), "state/dependencies.yaml"))
        seen.add((left, right))
        if left == right:
            issues.append(issue("error", "edge.self", "edge %s depends on itself" % left, "state/dependencies.yaml"))
        for side, value in (("from", left), ("to", right)):
            if value not in module_ids:
                issues.append(issue("error", "edge.unknown_module", "edge %s `%s` is not a registered module" % (side, value), "state/dependencies.yaml"))
        if edge.get("type") not in state_mod.DEPENDENCY_TYPES:
            issues.append(issue("error", "edge.type", "edge %s → %s has invalid type `%s`" % (left, right, edge.get("type")), "state/dependencies.yaml"))
        if edge.get("status") not in state_mod.DEPENDENCY_STATUSES:
            issues.append(issue("error", "edge.status", "edge %s → %s has invalid status `%s`" % (left, right, edge.get("status")), "state/dependencies.yaml"))
        graph.setdefault(left, []).append(right)
        if edge.get("status") != "frozen" and state_mod.module_by_id(state, left) and state_mod.module_by_id(state, left).get("status") in ("in_progress", "assigned"):
            issues.append(
                issue("warning", "edge.not_frozen", "%s is already working while its edge to %s is `%s` (freeze before parallel work)" % (left, right, edge.get("status")), "state/dependencies.yaml")
            )
    try:
        for module_id in graph:
            state_mod.dependency_depth(state, module_id)
    except Exception as exc:  # YamlError on a cycle
        issues.append(issue("error", "edge.cycle", str(exc), "state/dependencies.yaml"))
    # every edge should exist in the contracts too (mirror of check_modules)
    for edge in state["edges"]:
        entry = state_mod.module_by_id(state, edge.get("from"))
        if entry is None:
            continue
        contract = state_mod.load_contract(root, entry)
        declared = list((contract["data"] or {}).get("depends_on") or [])
        if edge.get("to") not in declared:
            issues.append(
                issue("error", "edge.not_in_contract", "%s → %s edge exists but %s does not declare it in depends_on" % (edge.get("from"), edge.get("to"), edge.get("from")), "state/dependencies.yaml")
            )


# --------------------------------------------------------------------------------------
# Documentation, registry and prompt checks
# --------------------------------------------------------------------------------------
def _doc_files(root, config):
    files = list(repoutil.markdown_files(root))
    files = [path for path in files if not path.startswith("examples/")]
    for extra in config.get("link_check_extra_files") or []:
        if os.path.isfile(os.path.join(root, extra)) and extra not in files:
            files.append(extra)
    return sorted(set(files))


def check_links(root, config, issues):
    prefixes = tuple(config.get("link_check_prefixes") or ())
    allow = list(config.get("allow_missing_paths") or [])
    roots = repoutil.search_roots(root)
    pattern = re.compile(r"((?:%s)[A-Za-z0-9_\-./]*)" % "|".join(re.escape(prefix) for prefix in prefixes))
    for relative in _doc_files(root, config):
        full = os.path.join(root, relative)
        text = repoutil.read_text(full)
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in pattern.finditer(line):
                token = match.group(1).rstrip(".,;:)`'\"")
                if not token or token.endswith(("_", "-")):
                    continue
                if any(fnmatch.fnmatch(token, pattern_item) for pattern_item in allow):
                    continue
                candidate = token.split("#", 1)[0]
                if not candidate:
                    continue
                if candidate.endswith("/"):
                    directory = candidate.rstrip("/")
                    if directory and not any(os.path.isdir(os.path.join(base, directory)) for base in roots):
                        issues.append(issue("error", "link.directory_missing", "%s:%d: `%s` does not exist" % (relative, line_number, candidate), relative))
                    continue
                last = candidate.rsplit("/", 1)[-1]
                looks_like_file = "." in last
                if not looks_like_file and not any(os.path.isdir(os.path.join(base, candidate)) for base in roots):
                    continue
                if not any(os.path.exists(os.path.join(base, candidate)) for base in roots):
                    issues.append(issue("error", "link.missing", "%s:%d: `%s` does not exist" % (relative, line_number, candidate), relative))


def registry_path(root):
    """The agent registry: project copy first, then the framework copy (nested sample projects)."""
    for base in repoutil.search_roots(root):
        candidate = os.path.join(base, "docs", "agents", "agent_registry.yaml")
        if os.path.isfile(candidate):
            return candidate
    return os.path.join(root, "docs", "agents", "agent_registry.yaml")


def registry_roles(root, issues=None):
    path = registry_path(root)
    if not os.path.isfile(path):
        if issues is not None:
            issues.append(issue("error", "registry.missing", "docs/agents/agent_registry.yaml not found", "docs/agents/agent_registry.yaml"))
        return {}
    data = repoutil.load_yaml_file(path) or {}
    roles = {}
    for entry in data.get("roles") or []:
        role = entry.get("role")
        if not role:
            continue
        roles[role] = entry
    return roles


def check_registry(root, issues):
    roles = registry_roles(root, issues)
    taxonomy = {}
    path = registry_path(root)
    if os.path.isfile(path):
        taxonomy = (repoutil.load_yaml_file(path) or {}).get("taxonomy") or {}
    categories = taxonomy.get("categories") or []
    roots = repoutil.search_roots(root)
    for role, entry in roles.items():
        if not entry.get("prompt") or not any(
            os.path.isfile(os.path.join(base, entry["prompt"])) for base in roots
        ):
            issues.append(issue("error", "registry.prompt_missing", "role `%s` prompt `%s` does not exist" % (role, entry.get("prompt")), "docs/agents/agent_registry.yaml"))
        if categories and entry.get("category") not in categories:
            issues.append(issue("error", "registry.category", "role `%s` has unknown category `%s`" % (role, entry.get("category")), "docs/agents/agent_registry.yaml"))
        for key in ("mission", "inputs", "outputs", "allowed_actions", "forbidden_actions", "scope", "escalation_conditions", "completion_criteria"):
            if not entry.get(key):
                issues.append(issue("error", "registry.incomplete", "role `%s` is missing `%s`" % (role, key), "docs/agents/agent_registry.yaml"))
        if entry.get("scope"):
            for scope in entry["scope"]:
                # A scope may legitimately be a delegation (module-scoped roles write paths granted by
                # their contract), so prose scopes are informational rather than wrong.
                if scope and not any(character in scope for character in (".", "/", "*")):
                    issues.append(issue("info", "registry.scope_delegated", "role `%s` scope `%s` is prose (paths come from the module contract)" % (role, scope), "docs/agents/agent_registry.yaml"))
        for other in entry.get("must_stay_separate_from") or []:
            if other not in roles:
                issues.append(issue("warning", "registry.unknown_role_ref", "role `%s` references unknown role `%s` in must_stay_separate_from" % (role, other), "docs/agents/agent_registry.yaml"))
    prompt_dirs = {}
    for base in roots:
        agents_dir = os.path.join(base, "agents")
        if not os.path.isdir(agents_dir):
            continue
        for name in sorted(os.listdir(agents_dir)):
            prompt = os.path.join(agents_dir, name, "STARTER_PROMPT.md")
            if os.path.isfile(prompt) and name not in prompt_dirs:
                prompt_dirs[name] = repoutil.relative(base, prompt)
    for role, relative in prompt_dirs.items():
        if role not in roles:
            issues.append(issue("error", "registry.prompt_orphan", "%s has no matching role in docs/agents/agent_registry.yaml" % relative, relative))
    for role in roles:
        if role not in prompt_dirs:
            issues.append(issue("error", "registry.role_without_prompt", "role `%s` has no agents/%s/STARTER_PROMPT.md" % (role, role), "docs/agents/agent_registry.yaml"))
    # notebook prompt sync
    notebook = os.path.join(root, "HOW_TO_USE.ipynb")
    if os.path.isfile(notebook):
        try:
            payload = json.loads(repoutil.read_text(notebook))
        except ValueError as exc:
            issues.append(issue("error", "notebook.json", "HOW_TO_USE.ipynb is not valid JSON: %s" % exc, "HOW_TO_USE.ipynb"))
            return
        if payload.get("nbformat") != 4:
            issues.append(issue("error", "notebook.nbformat", "HOW_TO_USE.ipynb must be nbformat 4", "HOW_TO_USE.ipynb"))
        synced = 0
        for cell in payload.get("cells", []):
            source = "".join(cell.get("source") or [])
            match = PROMPT_RE.search(source)
            if not match:
                continue
            relative = match.group(1)
            expected = repoutil.read_text(os.path.join(root, relative)) if os.path.isfile(os.path.join(root, relative)) else None
            if expected is None:
                issues.append(issue("error", "notebook.prompt_missing", "notebook references missing prompt %s" % relative, "HOW_TO_USE.ipynb"))
                continue
            embedded = _embedded_prompt(source)
            if embedded is None:
                issues.append(issue("error", "notebook.prompt_block", "no fenced block after marker for %s" % relative, "HOW_TO_USE.ipynb"))
                continue
            synced += 1
            if _normalise(embedded) != _normalise(expected):
                issues.append(
                    issue(
                        "error",
                        "notebook.prompt_drift",
                        "notebook prompt for %s differs from the file — run `python scripts/tp.py sync-notebook`" % relative,
                        "HOW_TO_USE.ipynb",
                    )
                )
        if synced == 0:
            issues.append(issue("warning", "notebook.no_prompts", "HOW_TO_USE.ipynb contains no PROMPT-SYNC markers", "HOW_TO_USE.ipynb"))


def _fence_length(line: str):
    """Return the backtick-run length of a fence line, or 0 when it is not a fence.

    Prompts contain their own ``` blocks, so notebook cells wrap them in a longer fence; the closing
    fence must be at least as long as the opening one.
    """
    stripped = line.strip()
    if not stripped.startswith("```"):
        return 0
    return len(stripped) - len(stripped.lstrip("`"))


def _embedded_prompt(source: str):
    lines = source.splitlines()
    start = None
    for index, line in enumerate(lines):
        if PROMPT_RE.search(line):
            start = index + 1
            break
    if start is None:
        return None
    body = []
    opening = 0
    for line in lines[start:]:
        length = _fence_length(line)
        if not opening:
            if length:
                opening = length
            continue
        if length >= opening:
            return "\n".join(body)
        body.append(line)
    return None


def _normalise(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").split("\n")).strip()


def check_placeholders(root, config, issues, project=None):
    """Unreplaced `{{TOKEN}}` values are errors — except while the repo is still the pristine template.

    `initialised: false` (and `profile: template`) means nobody has run `bootstrap` yet, so the tokens
    are expected. They collapse into one informational line instead of a wall of errors; an initialised
    project treats them as blocking, because an unreplaced token there means somebody shipped a
    placeholder into a real repository.
    """
    exclude = set(config.get("placeholder_check_exclude") or [])
    found = repoutil.find_placeholders(root, exclude_paths=exclude)
    if not found:
        return
    project = project or {}
    template_profile = project.get("profile") == "template" or project.get("initialised") is False
    if template_profile:
        files = sorted({relative for relative, _, _ in found})
        issues.append(
            issue(
                "info",
                "template.uninitialised",
                "%d placeholder(s) in %d file(s) — this repository is still the template; "
                "run `python scripts/tp.py bootstrap <dir> --name … --project-id …` to initialise a project "
                "(%s)" % (len(found), len(files), ", ".join(files[:4]) + (", …" if len(files) > 4 else "")),
                "state/project.yaml",
            )
        )
        return
    for relative, line_number, token in found:
        issues.append(
            issue(
                "error",
                "placeholder.unreplaced",
                "%s:%d: unreplaced placeholder %s — run `python scripts/tp.py bootstrap …`" % (relative, line_number, token),
                relative,
            )
        )


def validate(root: str, state, strict: bool = False):
    """Run every check. Returns a list of issues."""
    config = load_config(root)
    issues = []
    check_project(root, state, issues)
    check_modules(root, state, issues, strict=strict)
    check_agents(root, state, issues)
    check_edges(root, state, issues)
    check_registry(root, issues)
    check_placeholders(root, config, issues, project=state.get("project"))
    check_links(root, config, issues)
    return issues
