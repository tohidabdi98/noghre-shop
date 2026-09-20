"""state — load and reason about project state, contracts and the dependency graph.

The four state files are the machine-readable truth (`state/README.md`). This module loads them,
parses module contracts, validates legal transitions, and computes which modules are ready to work
on (and how they group into waves).
"""

from __future__ import annotations

import os
import re

from . import repoutil
from .yamlmini import YamlError

MODULE_STATUSES = (
    "planned",
    "ready",
    "assigned",
    "in_progress",
    "awaiting_review",
    "changes_requested",
    "validated",
    "blocked",
    "failed",
    "complete",
    "cancelled",
)

TERMINAL_STATUSES = ("validated", "complete")
ACTIVE_STATUSES = ("assigned", "in_progress", "awaiting_review", "changes_requested")
VALIDATION_RESULTS = ("pending", "passed", "failed", "partial")

# Legal transitions: from -> allowed next states. `in_progress` may always be re-entered from
# changes_requested; `blocked` and `failed` may return to the board once the problem is resolved.
TRANSITIONS = {
    "planned": ("ready", "blocked", "cancelled"),
    "ready": ("assigned", "blocked", "cancelled"),
    "assigned": ("in_progress", "ready", "blocked", "failed", "cancelled"),
    "in_progress": ("awaiting_review", "blocked", "failed", "cancelled"),
    "awaiting_review": ("validated", "changes_requested", "blocked", "failed", "cancelled"),
    "changes_requested": ("in_progress", "failed", "cancelled"),
    "validated": ("complete", "changes_requested", "blocked", "cancelled"),
    "blocked": ("ready", "assigned", "in_progress", "failed", "cancelled"),
    "failed": ("ready", "assigned", "cancelled"),
    "complete": ("changes_requested",),  # reopening requires the human; other moves are invalid
    "cancelled": (),
}

AGENT_STATUSES = ("planned", "active", "waiting", "blocked", "replacing", "replaced", "done", "failed")
DEPENDENCY_TYPES = ("contract", "data", "runtime", "build", "ui")
DEPENDENCY_STATUSES = ("pending", "agreed", "frozen", "broken")
PROFILES = ("frontend", "backend", "fullstack")
STAGES = (
    "discovery",
    "ux",
    "architecture",
    "decomposition",
    "implementation",
    "integration",
    "release",
    "maintenance",
)
SPEC_STATUSES = ("draft", "in_review", "approved", "superseded")

REQUIRED_CONTRACT_KEYS = (
    "module_id",
    "name",
    "status",
    "purpose",
    "owns",
    "allowed_to_modify",
    "forbidden_to_modify",
    "depends_on",
    "interfaces",
    "acceptance_criteria",
    "definition_of_done",
)

REQUIRED_CONTRACT_HEADINGS = (
    "purpose",
    "responsibilities",
    "non-responsibilities",
    "interfaces",
    "data",
    "security",
    "performance",
    "testing",
    "acceptance criteria",
    "definition of done",
    "example usage",
    "open questions",
    "known risks",
    "change log",
)

HEADERS = {
    "project": (
        "# state/project.yaml — project identity, stage and gates\n"
        "# Written by `python scripts/tp.py bootstrap` and the orchestrator; human owns the gates.\n"
        "# Validate with `python scripts/tp.py validate`."
    ),
    "modules": (
        "# state/modules.yaml — module runtime state (the board)\n"
        "# STATUS ONLY lives here; ownership and criteria live in modules/<MODULE-ID>.md\n"
        "# status: planned|ready|assigned|in_progress|awaiting_review|changes_requested|\n"
        "#         validated|blocked|failed|complete|cancelled\n"
        "# Managed by `python scripts/tp.py start|handoff|status` and the orchestrator."
    ),
    "agents": (
        "# state/agents.yaml — agent instances (who is working on what)\n"
        "# One entry per instance, not per role. Managed by `tp.py start|handoff` and the orchestrator."
    ),
    "dependencies": (
        "# state/dependencies.yaml — inter-module dependency edges\n"
        "# DIRECTION: from -> to means 'from depends on to' (to must be validated|complete first).\n"
        "# type: contract|data|runtime|build|ui    status: pending|agreed|frozen|broken\n"
        "# An interface must be `frozen` before the dependent module starts in a parallel wave."
    ),
}

MODULE_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*-\d+$")
AGENT_BRANCH_RE = re.compile(r"^agent/([a-z0-9][a-z0-9-]*)/([A-Z][A-Z0-9]*-\d+)$")
REQ_ID_RE = re.compile(r"^(FR|NFR)-[A-Z0-9-]*\d+$")
UX_ID_RE = re.compile(r"^UX-[A-Z0-9]*-?\d+$")
EDGE_ID_RE = re.compile(r"^(FR|NFR|UX|ADR|DEC|ASM|OQ|RISK|CR|AC)[A-Z0-9._-]*$")


# --------------------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------------------
def state_path(root: str, name: str) -> str:
    return os.path.join(root, "state", "%s.yaml" % name)


def load_state(root: str):
    """Load all four state files into a single dict. Missing files raise a clear error."""
    loaded = {}
    for name in ("project", "modules", "agents", "dependencies"):
        path = state_path(root, name)
        if not os.path.isfile(path):
            raise YamlError("missing state file: %s" % repoutil.relative(root, path))
        loaded[name] = repoutil.load_yaml_file(path) or {}
    project = loaded["project"] or {}
    loaded["project"] = project
    loaded["modules"] = list(loaded["modules"].get("modules") or [])
    loaded["agents"] = list(loaded["agents"].get("agents") or [])
    loaded["edges"] = list(loaded["dependencies"].get("edges") or [])
    loaded["docs"] = dict(project.get("docs") or {})
    loaded["shared_zones"] = list(project.get("shared_zones") or [])
    return loaded


def module_by_id(state, module_id: str):
    for module in state["modules"]:
        if module.get("module_id") == module_id:
            return module
    return None


def module_ids(state):
    return [module.get("module_id") for module in state["modules"]]


def upstream_of(state, module_id: str):
    """Modules that must be finished before `module_id` (its `to` dependencies)."""
    return [edge.get("to") for edge in state["edges"] if edge.get("from") == module_id]


def downstream_of(state, module_id: str):
    return [edge.get("from") for edge in state["edges"] if edge.get("to") == module_id]


def contract_path(root: str, module_entry) -> str:
    contract = module_entry.get("contract") or ""
    if contract:
        return os.path.join(root, contract)
    return os.path.join(root, "modules", "%s.md" % module_entry.get("module_id"))


def load_contract(root: str, module_entry):
    """Parse a module contract: returns {'path','text','data','headings','exists'}."""
    path = contract_path(root, module_entry)
    exists = os.path.isfile(path)
    if not exists:
        return {"path": path, "text": "", "data": None, "headings": [], "exists": False}
    text = repoutil.read_text(path)
    data = repoutil.extract_fenced_yaml(text, repoutil.relative(root, path))
    return {
        "path": path,
        "text": text,
        "data": data or {},
        "headings": repoutil.headings(text, level=2),
        "exists": True,
    }


# --------------------------------------------------------------------------------------
# Transitions
# --------------------------------------------------------------------------------------
def can_transition(old: str, new: str) -> bool:
    return new in TRANSITIONS.get(old, ())


def apply_transition(state, module_id: str, new_status: str, actor: str, reason: str = "") -> None:
    """Mutate `state` in memory: module + contract status + history entry."""
    module = module_by_id(state, module_id)
    if module is None:
        raise KeyError("unknown module %s" % module_id)
    old_status = module.get("status")
    module["status"] = new_status
    module["updated_at"] = repoutil.today()
    history = list(module.get("history") or [])
    history.append(
        {"at": repoutil.today(), "from": old_status, "to": new_status, "by": actor, "reason": reason or ""}
    )
    module["history"] = history


def update_contract_status(root: str, module_entry, new_status: str) -> None:
    """Keep the contract YAML `status` in sync with the registry (they must never diverge)."""
    contract = load_contract(root, module_entry)
    if not contract["exists"] or not contract["data"]:
        return
    text = contract["text"]
    pattern = re.compile(r"^(status:\s*)(\S+)(.*)$", re.MULTILINE)
    updated, count = pattern.subn(lambda m: "%s%s%s" % (m.group(1), new_status, m.group(3)), text, count=1)
    if count:
        repoutil.write_text(contract["path"], updated)


# --------------------------------------------------------------------------------------
# Readiness and waves
# --------------------------------------------------------------------------------------
def dependency_depth(state, module_id: str, cache=None, visiting=None):
    """Longest dependency chain below a module (0 = no dependencies). Detects cycles via visiting."""
    cache = {} if cache is None else cache
    visiting = set() if visiting is None else visiting
    if module_id in cache:
        return cache[module_id]
    if module_id in visiting:
        raise YamlError("dependency cycle detected at %s" % module_id)
    visiting.add(module_id)
    upstreams = upstream_of(state, module_id)
    depth = 0 if not upstreams else 1 + max(dependency_depth(state, item, cache, visiting) for item in upstreams)
    visiting.discard(module_id)
    cache[module_id] = depth
    return depth


def overlaps(left, right):
    """Return the intersection of two ownership path lists (glob-prefix comparison)."""
    shared = []
    for one in left or []:
        for other in right or []:
            if _paths_overlap(one, other):
                shared.append((one, other))
    return shared


def _paths_overlap(left: str, right: str) -> bool:
    left_base = left.split("*")[0].rstrip("/")
    right_base = right.split("*")[0].rstrip("/")
    if not left_base or not right_base:
        return True
    return (
        left_base == right_base
        or left_base.startswith(right_base + "/")
        or right_base.startswith(left_base + "/")
    )


def compute_board(root: str, state):
    """Compute the planning board: ready set, waves, warnings, blocked/failed lists."""
    warnings = []
    errors = []
    ready = []
    for module in state["modules"]:
        status = module.get("status")
        if status not in ("planned", "ready"):
            continue
        upstreams = upstream_of(state, module["module_id"])
        unmet = []
        for upstream in upstreams:
            entry = module_by_id(state, upstream)
            if entry is None or entry.get("status") not in TERMINAL_STATUSES:
                unmet.append(upstream)
        if unmet:
            continue
        ready.append(module["module_id"])

    # overlap + shared-zone warnings between modules that could run in parallel
    active_ids = [
        module["module_id"]
        for module in state["modules"]
        if module.get("status") in ACTIVE_STATUSES
    ]
    candidate_ids = ready + active_ids
    for index, left_id in enumerate(candidate_ids):
        for right_id in candidate_ids[index + 1 :]:
            left = load_contract(root, module_by_id(state, left_id))
            right = load_contract(root, module_by_id(state, right_id))
            shared = overlaps(left["data"].get("owns"), right["data"].get("owns"))
            if shared:
                warnings.append(
                    "%s and %s claim overlapping ownership (%s) — fix the boundary before running both"
                    % (left_id, right_id, ", ".join("%s ~ %s" % pair for pair in shared))
                )

    zone_owners = {}
    for zone in state["shared_zones"]:
        path = zone.get("path")
        owner = zone.get("owner")
        if not path:
            continue
        if not owner:
            warnings.append("shared zone %s has no owner (state/project.yaml)" % path)
        zone_owners[path] = owner
    for module_id in ready:
        contract = load_contract(root, module_by_id(state, module_id))
        for zone in contract["data"].get("shared_zones_touched") or []:
            if zone in zone_owners and zone_owners[zone] not in (None, module_id):
                warnings.append(
                    "%s wants shared zone %s owned by %s — request the change instead of editing it"
                    % (module_id, zone, zone_owners[zone])
                )

    waves = {}
    for module_id in ready:
        try:
            depth = dependency_depth(state, module_id)
        except YamlError as exc:
            errors.append(str(exc))
            continue
        waves.setdefault(depth, []).append(module_id)

    return {
        "ready": sorted(ready),
        "waves": {depth: sorted(ids) for depth, ids in sorted(waves.items())},
        "warnings": warnings,
        "errors": errors,
        "blocked": [m["module_id"] for m in state["modules"] if m.get("status") == "blocked"],
        "failed": [m["module_id"] for m in state["modules"] if m.get("status") == "failed"],
        "active": active_ids,
        "awaiting_review": [
            m["module_id"] for m in state["modules"] if m.get("status") == "awaiting_review"
        ],
        "complete": [m["module_id"] for m in state["modules"] if m.get("status") == "complete"],
    }
