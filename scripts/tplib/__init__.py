"""tplib — the TemplateProject toolkit library (Python standard library only).

Modules
    yamlmini  — reader/writer for the YAML subset used by the state files (no PyYAML required)
    state     — load/validate project state, module contracts, dependency graph, readiness
    context   — assemble layered context packs for agents
    repoutil  — repository helpers: root discovery, placeholders, git, file walking
    checks    — integrity checks: contracts, doc links, prompt sync, agent registry

Design rule: no third-party imports. If PyYAML happens to be installed, `state` uses it for
reading (more forgiving), otherwise `yamlmini` handles the documented subset.
"""

__all__ = ["yamlmini", "state", "context", "repoutil", "checks"]

__version__ = "1.0.0"
